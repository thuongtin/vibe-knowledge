#!/usr/bin/env python3
"""Trang duyệt văn án: gom bản lời dẫn của từng bài trong series (script.md + narration.json + sổ cái kiểm chứng) thành một trang, để người dùng xác nhận từng bài.

Cách dùng: python3 scripts/review_page.py <thư mục series> <thư mục xuất> [--from 2] [--to 12]
Mỗi bài hiển thị: số chữ, số nhịp, thời lượng dự kiến (tính 4,3 chữ mỗi giây), số sự thật đã/chưa kiểm chứng, toàn văn script.md (lời dẫn từng nhịp, gợi ý hình ảnh, căn cứ),
cùng claims.md (kết luận kiểm chứng, thu gọn).
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown

E = html.escape
CUE = re.compile(r"\[\[[a-z0-9_-]+\]\]")

CSS = """
:root{--bg:#F0FAF6;--surface:#FFFFFF;--surface2:#E6F5EE;--line:#D3E9DF;--ink:#16332D;--ink2:#3F5E57;--ink3:#5E7B74;
  --acc:#137A66;--acct:#DDF6F0;--ok:#3C7F2E;--okt:#E6F7E2;--warn:#B83A55;--warnt:#FDE5EA}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#10211D;--surface:#172D28;--surface2:#1E3832;--line:#2B4A42;
  --ink:#EAF7F2;--ink2:#B5D3CA;--ink3:#8DB1A7;--acc:#8FE3CF;--acct:rgba(127,214,194,.16);--ok:#B5EDD0;--okt:rgba(134,217,176,.15);--warn:#FFD0B5;--warnt:rgba(255,180,138,.16)}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#10211D;--surface:#172D28;--surface2:#1E3832;--line:#2B4A42;
  --ink:#EAF7F2;--ink2:#B5D3CA;--ink3:#8DB1A7;--acc:#8FE3CF;--acct:rgba(127,214,194,.16);--ok:#B5EDD0;--okt:rgba(134,217,176,.15);--warn:#FFD0B5;--warnt:rgba(255,180,138,.16)}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:16px/1.75 "Noto Sans SC","PingFang SC",system-ui,sans-serif;padding-inline:20px;margin:0}
.wrap{max-width:1180px;margin:0 auto;padding-block:36px 90px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:32px}
nav{position:sticky;top:env(safe-area-inset-top,0px);align-self:start;padding-top:8px}
nav a{display:flex;gap:10px;padding:7px 10px;border-radius:10px;color:var(--ink2);text-decoration:none;font-size:15px}
nav a:hover{background:var(--surface2)} nav b{color:var(--acc);min-width:1.6em;font-variant-numeric:tabular-nums}
h1{font-size:40px;line-height:1.2;margin:0 0 8px;text-wrap:balance}
.lede{color:var(--ink2);margin:0 0 22px}
table{border-collapse:collapse;width:100%;font-size:14.5px;background:var(--surface);border-radius:16px;overflow:hidden}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;font-variant-numeric:tabular-nums}
th{color:var(--ink3);font-weight:600;background:var(--surface2)}
.tbl{overflow-x:auto;border-radius:16px;border:1.5px solid var(--line)}
section{margin-top:44px;padding-top:10px;border-top:2px dashed var(--line)}
section h2{font-size:28px;margin:6px 0 6px}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 16px}
.pill{font-size:13px;font-weight:700;padding:3px 10px;border-radius:999px;background:var(--acct);color:var(--acc)}
.pill.ok{background:var(--okt);color:var(--ok)} .pill.warn{background:var(--warnt);color:var(--warn)}
.md{background:var(--surface);border:1.5px solid var(--line);border-radius:18px;padding:6px 24px 18px}
.md h1,.md h2,.md h3{font-size:19px;margin:18px 0 6px} .md h1{font-size:22px}
.md table{font-size:14px} .md blockquote{margin:8px 0;padding:6px 14px;border-left:4px solid var(--acct);color:var(--ink2);background:var(--surface2);border-radius:0 10px 10px 0}
.md code{font-size:13px;background:var(--surface2);padding:1px 5px;border-radius:5px}
details{margin-top:12px;background:var(--surface);border:1.5px solid var(--line);border-radius:14px;padding:10px 18px}
details summary{cursor:pointer;font-weight:700;color:var(--ink2)}
.missing{color:var(--warn);font-weight:700}
@media (max-width:860px){.wrap{grid-template-columns:1fr}nav{position:static;display:flex;flex-wrap:wrap;gap:4px}}
"""


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sd, out = Path(sys.argv[1]), Path(sys.argv[2])
    lo, hi = int(arg("--from", 2)), int(arg("--to", 12))
    S = json.loads((sd / "series.json").read_text(encoding="utf-8"))
    rows, secs, nav = [], [], []
    for n in range(lo, hi + 1):
        L = sd / "lessons" / f"{n:02d}"
        title = S["lessons"][n - 1]["title"] if n - 1 < len(S.get("lessons", [])) else f"Bài {n}"
        nav.append(f'<a href="#l{n:02d}"><b>{n}</b>{E(title)}</a>')
        nj, sm = L / "narration.json", L / "script.md"
        if not nj.exists():
            rows.append(f'<tr><td>{n}</td><td>{E(title)}</td><td colspan="5" class="missing">Chưa viết xong</td></tr>')
            secs.append(f'<section id="l{n:02d}"><h2>Bài {n} · {E(title)}</h2><p class="missing">Văn án chưa viết xong.</p></section>')
            continue
        beats = json.loads(nj.read_text(encoding="utf-8"))["beats"]
        chars = sum(len(CUE.sub("", b["narration"])) for b in beats)
        est = chars / 4.3 + 0.8 * len(beats)
        fx = L / "research/facts.json"
        facts = json.loads(fx.read_text(encoding="utf-8"))["facts"] if fx.exists() else []
        ver = sum(1 for f in facts if f.get("status") == "verified")
        unv = len(facts) - ver
        rows.append(f"<tr><td>{n}</td><td><a href=\"#l{n:02d}\">{E(title)}</a></td><td>{chars}</td><td>{len(beats)}</td>"
                    f"<td>{int(est // 60)}:{int(est % 60):02d}</td><td>{ver}</td><td>{unv}</td></tr>")
        body = markdown.markdown(sm.read_text(encoding="utf-8"), extensions=["tables"]) if sm.exists() else \
            "<ol>" + "".join(f"<li>{E(CUE.sub('', b['narration']))}</li>" for b in beats) + "</ol>"
        claims = L / "research/claims.md"
        cl = f'<details><summary>Kết luận kiểm chứng (claims.md)</summary><div class="md">{markdown.markdown(claims.read_text(encoding="utf-8"), extensions=["tables"])}</div></details>' if claims.exists() else ""
        secs.append(f"""<section id="l{n:02d}"><h2>Bài {n} · {E(title)}</h2>
<div class="stats"><span class="pill">{chars} chữ · {len(beats)} nhịp</span><span class="pill">khoảng {int(est // 60)} phút {int(est % 60)} giây</span>
<span class="pill ok">Đã kiểm chứng {ver} mục</span>{f'<span class="pill warn">Chưa kiểm chứng {unv} mục (chưa đưa vào lời dẫn)</span>' if unv else ''}</div>
<div class="md">{body}</div>{cl}</section>""")
    page = f"""<title>Duyệt văn án Khoá nhập môn AI</title>
<style>{CSS}</style>
<div class="wrap"><nav>{''.join(nav)}</nav><main>
<h1>Khoá nhập môn AI · Văn án bài {lo}–{hi}</h1>
<p class="lede">Nguyên văn lời dẫn, gợi ý hình ảnh và căn cứ của mỗi bài đều ở bên dưới. Sau khi xác nhận sẽ thu âm và làm hình theo văn án này; muốn sửa câu nào, cứ báo số bài và số nhịp (như "Bài 5 B07").</p>
<div class="tbl"><table><thead><tr><th>Bài</th><th>Tiêu đề</th><th>Số chữ</th><th>Số nhịp</th><th>Thời lượng dự kiến</th><th>Đã kiểm chứng</th><th>Chưa kiểm chứng</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
{''.join(secs)}
</main></div>
"""
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"→ {out / 'index.html'} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
