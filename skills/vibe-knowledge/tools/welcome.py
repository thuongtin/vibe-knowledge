#!/usr/bin/env python3
"""Giới thiệu lần đầu sử dụng: tạo trang web cục bộ "Sổ tay phong cách" và đánh dấu đã giới thiệu.
Cách dùng: python3 welcome.py            # chỉ tạo và mở khi chưa giới thiệu (khi ~/.vibe-knowledge/welcomed chưa tồn tại)
      python3 welcome.py --force    # dù đã giới thiệu hay chưa đều tạo lại và mở (dùng sau khi thư viện phong cách được cập nhật)
      python3 welcome.py --no-open  # chỉ tạo, không mở
Đầu ra: ~/Desktop/vibe-knowledge/风格图鉴/index.html (ảnh phong cách, phim chớp nhoáng, phim mẫu được sao chép vào cùng thư mục, tham chiếu bằng đường dẫn tương đối, có thể gửi nguyên thư mục cho người khác)."""
import html, json, re, shutil, subprocess, sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
CAT = json.loads((SK / "styles/catalog.json").read_text(encoding="utf-8"))
MARK = Path.home() / ".vibe-knowledge/welcomed"
OUT = Path.home() / "Desktop/vibe-knowledge/风格图鉴"
VID = Path.home() / "Desktop/Vibe知识大赏_视频"
REEL = VID / "风格快闪_42s_八家族.mp4"          # phim chớp nhoáng phong cách (sau khi promo-video xuất phim thì đặt ở đây; bản cũ 风格快闪_30s.mp4 chỉ có 7 bộ)
POSTER_AT = {"风格快闪_42s_八家族.mp4": 20.4, "风格快闪_30s.mp4": 4.5, "styles_风格样片集.mp4": 14.5, "styles2_风格样片集_剪辑与纪实.mp4": 15.0, "styles3_风格样片集_补空白家族.mp4": 7.4, "styles4_风格样片集_增强档东方与印刷.mp4": 7.4, "styles5_风格样片集_第五批.mp4": 7.4, "styles6_风格样片集_第六批.mp4": 7.4, "styles7_风格样片集_第七批增强档.mp4": 7.4, "styles8_风格样片集_田园像素.mp4": 7.0, "styles9_风格样片集_第九批.mp4": 7.4, "styles10_风格样片集_手绘过程.mp4": 7.6, "01_商鞅立木.mp4": 58.0}
SAMPLES = {"styles": VID / "styles_风格样片集.mp4", "styles2": VID / "styles2_风格样片集_剪辑与纪实.mp4", "styles3": VID / "styles3_风格样片集_补空白家族.mp4", "styles4": VID / "styles4_风格样片集_增强档东方与印刷.mp4", "styles5": VID / "styles5_风格样片集_第五批.mp4", "styles6": VID / "styles6_风格样片集_第六批.mp4", "styles7": VID / "styles7_风格样片集_第七批增强档.mp4", "styles8": VID / "styles8_风格样片集_田园像素.mp4", "styles9": VID / "styles9_风格样片集_第九批.mp4", "styles10": VID / "styles10_风格样片集_手绘过程.mp4", "ep01": VID / "01_商鞅立木.mp4"}


def field(md, name):
    m = re.search(rf"\|\s*(?:{name})\s*\|\s*(.+?)\s*\|", md)
    return m.group(1) if m else ""


def main():
    if MARK.exists() and "--force" not in sys.argv:
        print(f"Đã giới thiệu rồi ({MARK}); muốn tạo lại hãy dùng --force"); return
    (OUT / "img").mkdir(parents=True, exist_ok=True); (OUT / "video").mkdir(exist_ok=True)
    cards, fams = {}, CAT.get("families") or sorted({x.get("fam", x["cat"]) for x in CAT["styles"]})
    for s in CAT["styles"]:
        md = (SK / "styles" / s["key"] / "STYLE.md").read_text(encoding="utf-8")
        shutil.copy(SK / "styles" / s["key"] / "still.jpg", OUT / "img" / f"{s['key']}.jpg")
        tpl = ", ".join(f"{t} {re.split(r'[（(]', CAT['templates'][t])[0]}" for t in s["templates"])
        tier = '<span class="tier">Bản nâng cao · cần tạo ảnh</span>' if s.get("tier") == "Nâng cao" else ""
        cards.setdefault(s.get("fam", s["cat"]), []).append(f"""<article class="card"><img src="img/{s['key']}.jpg" alt="{html.escape(s['name'])} ảnh phong cách" loading="lazy">
<div class="meta"><div class="no">{s['no']:02d} · {html.escape(s.get('fam', s['cat']))} {tier}</div><h3>{html.escape(s['name'])} <span>{html.escape(s['en'])}</span></h3>
<p class="one">{html.escape(s['one'])}</p><dl><dt>Phù hợp</dt><dd>{html.escape(s['fit'])}</dd><dt>Bản gốc kết hợp</dt><dd>{html.escape(tpl)}</dd>
<dt>Cảnh đặc trưng</dt><dd>{html.escape(field(md, "标志镜头|Cảnh đặc trưng"))}</dd><dt>Phim mẫu</dt><dd>{html.escape(s.get('sample', ''))}</dd></dl></div></article>""")
    vids = []
    for name, p in [("Phim chớp nhoáng phong cách 42 giây · 8 họ", REEL), ("5 bộ phim mẫu hệ thống thị giác", SAMPLES["styles"]), ("2 bộ phim mẫu dựng phim và tài liệu", SAMPLES["styles2"]), ("8 bộ phim mẫu họ bổ sung chỗ trống (0 điểm)", SAMPLES["styles3"]), ("4 bộ phim mẫu bản nâng cao phương Đông và in ấn", SAMPLES["styles4"]), ("8 bộ phim mẫu đợt 5 (0 điểm)", SAMPLES["styles5"]), ("8 bộ phim mẫu đợt 6 (0 điểm)", SAMPLES["styles6"]), ("Bản nâng cao cuộn dài · bảo tàng khắc đồng", SAMPLES["styles7"]), ("Pixel điền viên (kiểu Stardew Valley)", SAMPLES["styles8"]), ("5 bộ phim mẫu đợt 9 (0 điểm)", SAMPLES["styles9"]), ("Quá trình vẽ tay (vẽ cho bạn xem)", SAMPLES["styles10"]), ("Phim thành phẩm tập 01 \"Thương Ưởng dựng cây\"", SAMPLES["ep01"])]:
        if p.exists():
            shutil.copy(p, OUT / "video" / p.name)
            poster = OUT / "video" / (p.stem + ".jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(POSTER_AT.get(p.name, 3)), "-i", str(p), "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "3", str(poster)], check=False)
            vids.append(f'<figure><video src="video/{html.escape(p.name)}" poster="video/{html.escape(poster.name)}" controls preload="none"></video><figcaption>{html.escape(name)}</figcaption></figure>')
    tpls = "".join(f"<li><b>{k}</b> {html.escape(v)}</li>" for k, v in CAT["templates"].items())
    page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sổ tay phong cách · Vibe Knowledge</title><style>
:root{{--bg:#0d0c0b;--card:#17151a;--ink:#f2efe8;--dim:#a39d94;--line:rgba(255,255,255,.1);--acc:#e2b45a}}
@media (prefers-color-scheme: light){{:root:not([data-theme="dark"]){{--bg:#f6f3ee;--card:#fff;--ink:#1d1b18;--dim:#6f6a62;--line:rgba(0,0,0,.1);--acc:#b0802a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:48px 16px 80px}}h1{{font-size:clamp(32px,6vw,56px);margin:0 0 8px;letter-spacing:2px}}
.lead{{color:var(--dim);max-width:760px}}h2{{margin:56px 0 16px;font-size:26px}}
.vids{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:16px}}video{{width:100%;border-radius:12px;background:#000}}
figcaption{{color:var(--dim);font-size:14px;margin-top:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:18px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}}.card img{{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}}
.meta{{padding:16px 18px 20px}}.no{{color:var(--acc);font-size:13px;letter-spacing:2px}}h3{{margin:4px 0 6px;font-size:22px}}h3 span{{color:var(--dim);font-size:13px;letter-spacing:2px;font-weight:500}}
.one{{margin:0 0 10px}}dl{{display:grid;grid-template-columns:72px 1fr;gap:4px 10px;margin:0;font-size:14px}}dt{{color:var(--dim)}}dd{{margin:0}}
.how{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px}}.box{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}}
.box h4{{margin:0 0 8px;font-size:17px}}.tier{{display:inline-block;margin-left:6px;padding:0 8px;border-radius:10px;background:var(--acc);color:var(--bg);font-size:11px;letter-spacing:1px}}h2 small{{color:var(--dim);font-size:15px;font-weight:500;margin-left:8px}}code{{background:rgba(127,127,127,.15);padding:1px 6px;border-radius:5px}}ul{{padding-left:20px;margin:0}}
</style></head><body><main>
<h1>Sổ tay phong cách</h1><p class="lead">Một tập phim ngắn kiến thức = <b>bản gốc</b> (nói thế nào) × <b>phong cách</b> (trông thế nào) × <b>bậc</b> (hình ảnh bằng code 0 điểm, hoặc dùng Renoise nâng cao cảnh quay chân thực). {len(CAT['styles'])} phong cách dưới đây chia thành {len(fams)} họ, đều đã được render thực tế bằng cùng một đoạn mở đầu; chỉ cần nói một chủ đề, sẽ đề xuất 3 bộ trong số đó theo chủ đề.</p>
<h2>Xem phim trước</h2><div class="vids">{''.join(vids) or '<p class="lead">(phim mẫu chưa được tạo)</p>'}</div>
{''.join(f'<h2>{html.escape(f)}<small>{len(cards.get(f, []))} bộ</small></h2><div class="grid">' + ''.join(cards.get(f, [])) + '</div>' for f in fams if cards.get(f))}
<h2>Mở lời thế nào</h2><div class="how">
<div class="box"><h4>Chỉ đưa chủ đề</h4><p>"Làm một tập về Đình trưởng Ô Giang": đề xuất 3 phong cách (bộ được đề xuất nhất xếp đầu, kèm lý do và ảnh phong cách), bạn chọn một bộ.</p></div>
<div class="box"><h4>Chỉ định phong cách</h4><p>"Dùng thủy mặc trên giấy làm một tập về cải cách Vương An Thạch": bắt tay làm ngay theo phong cách này.</p></div>
<div class="box"><h4>Đổi thành phong cách của riêng bạn</h4><p>"Đổi phong cách cổ phong thành màu thương hiệu của tôi" hoặc "làm từ đầu một phong cách bảng đen phấn": mỗi vấn đề một câu hỏi để chốt phương án, ra ảnh phong cách đặt cạnh nhau và demo 15–30 giây, bạn gật đầu mới lưu thành "phong cách của tôi".</p></div>
</div>
<h2>Hai bậc</h2><div class="how">
<div class="box"><h4>Bản cơ bản · 0 điểm</h4><p>Mọi phong cách không gắn nhãn "bản nâng cao" đều làm được. Hình ảnh bằng code (Opus viết tay minh họa + hiệu ứng chuyển động), lồng tiếng Google Gemini TTS, nhạc nền từ thư viện, hiệu ứng âm thanh bằng code earshot.</p></div>
<div class="box"><h4>Bản nâng cao · chọn theo cảnh quay</h4><p>Chỉ giao cho Renoise các cảnh chân thực và 1–3 khoảnh khắc cần được nhớ nhất (ảnh minh họa / cảnh quay động / nhạc nền riêng / hiệu ứng âm thanh). Nhẹ ≈25–40, tiêu chuẩn ≈250–300, hàng đầu ≈600–700 điểm, mỗi lần báo giá trước, bạn xác nhận mới tạo.</p></div>
</div>
<h2>6 loại bản gốc</h2><div class="box"><ul>{tpls}</ul></div>
<h2>Quy trình mỗi tập</h2><div class="box"><p>① Chủ đề + bản gốc + phong cách + bậc → ② Danh sách sự kiện (mỗi mục đối chiếu nguyên văn) → ③ Lời dẫn + duyệt độc lập → ④ Phân cảnh / báo giá → ⑤ Nghe thử phần mở đầu để chốt giọng và tốc độ → ⑥ Lồng tiếng, hình ảnh, render → ⑦ Kiểm tra chất lượng (đọc lại chữ để đối chiếu sự kiện, độ lớn âm thanh) → ⑧ Gói đăng tải (tiêu đề, chủ đề, hai ảnh bìa).</p></div>
</main></body></html>"""
    (OUT / "index.html").write_text(page, encoding="utf-8")
    MARK.parent.mkdir(parents=True, exist_ok=True); MARK.write_text("1", encoding="utf-8")
    print(f"→ {OUT / 'index.html'} ({sum(len(v) for v in cards.values())} phong cách / {len(cards)} họ, {len(vids)} video)")
    if "--no-open" not in sys.argv:
        subprocess.run(["open", str(OUT / "index.html")], check=False)


if __name__ == "__main__":
    main()
