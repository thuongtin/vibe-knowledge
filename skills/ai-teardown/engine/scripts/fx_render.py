#!/usr/bin/env python3
"""Render các hiệu ứng trong thư viện chuyển động thành đoạn dùng làm "sticker video": <series>/assets/fx/<id>.mp4 + <id>.jpg (ảnh bìa), đồng thời cập nhật danh sách fx.json.

Cách dùng: python3 scripts/fx_render.py <thư mục series> <id> [<id> …] [--force] [--lib ~/Desktop/motionlab-replica]

- Mẫu chính thức của HyperFrames (hf/<id>/ của phòng thí nghiệm chuyển động): sao chép vào dự án tạm, dùng HyperFrames CLI render chính thức (tất định, 30fps, 1920×1080).
- Bản gốc của phòng thí nghiệm chuyển động (những cái được ML.register trong demos/*.js): nạp kit.js + demos vào trình duyệt không đầu (chỉ đọc), seek từng khung chụp màn hình, truyền qua pipe cho ffmpeg.
- <series>/assets/fx/overrides.json có thể sửa văn án theo id: {"typewriter": {"variables": {...}, "replace": [["cũ", "mới"]], "vars": {...}, "duration": 6}}
  · variables: biến do mẫu HyperFrames khai báo (render --variables); replace: thay chuỗi trong HTML của mẫu trước khi render (đổi dòng chữ HyperFrames mặc định)
  · vars / duration: biến và thời lượng của cảnh văn án gốc
Thư mục thư viện chuyển động chỉ đọc, không ghi bất cứ thứ gì vào đó.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HF_CLI = Path.home() / ".npm/_npx/702923228c2ce1e6/node_modules/hyperframes/dist/cli.js"
EXE = Path.home() / "Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell"


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def probe(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-show_entries", "format=duration",
                          "-of", "json", str(mp4)], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    return float(d["format"]["duration"]), d["streams"][0]["width"], d["streams"][0]["height"]


def poster(mp4, t, jpg):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "3", str(jpg)], check=True)


def hf_catalog(lib):
    s = (lib / "hf-catalog.js").read_text(encoding="utf-8")
    return {x["id"]: x for x in json.loads(s[s.index("["):s.rindex("]") + 1])}


def render_hf(lib, item, out, ov):
    src = lib / "hf" / item["id"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for f in src.iterdir():
            (shutil.copytree if f.is_dir() else shutil.copy)(f, tmp / f.name)
        # block render thẳng bản thân; component là đoạn, dùng demo.html có sẵn của chính thức (bọc đoạn vào một composition)
        entry = tmp / "demo.html" if item.get("type") == "component" and (tmp / "demo.html").exists() else tmp / f"{item['id']}.html"
        html = entry.read_text(encoding="utf-8")
        for a, b in ov.get("replace", []):
            html = html.replace(a, b)
        (tmp / "index.html").write_text(html, encoding="utf-8")
        cmd = ["node", str(HF_CLI), "render", ".", "-o", str(out), "-q", "high"]
        if ov.get("variables"):
            cmd += ["--variables", json.dumps(ov["variables"], ensure_ascii=False)]
        r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
        if r.returncode or not out.exists():
            raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])


ML_PAGE = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{lib}/styles.css">
<style>html,body{{margin:0;background:#000;overflow:hidden}}#host{{position:relative;width:1920px;height:1080px}}</style>
<script src="{lib}/kit.js"></script>{demos}</head><body><div id="host"></div></body></html>"""


def render_ml(lib, id_, out, ov, fps=30):
    from playwright.sync_api import sync_playwright
    demos = "".join(f'<script src="{(lib / "demos" / f.name).as_uri()}"></script>' for f in sorted((lib / "demos").glob("*.js")))
    page = Path(tempfile.mkdtemp()) / "cap.html"
    page.write_text(ML_PAGE.format(lib=lib.as_uri(), demos=demos), encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(EXE) if EXE.exists() else None)
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(page.as_uri())
        meta = pg.evaluate("""([id, vars, dur]) => { const d = ML.byId.get(id); if (!d) return null;
          window.__inst = ML.mount(d, document.getElementById('host'), { vars, duration: dur });
          return { name: d.name, duration: window.__inst.duration, poster: d.poster, category: d.category, description: d.description }; }""",
                           [id_, ov.get("vars", {}), ov.get("duration")])
        if not meta:
            b.close()
            raise RuntimeError(f"Phòng thí nghiệm chuyển động không có: {id_}")
        pg.evaluate("document.fonts.ready")
        n = max(1, round(meta["duration"] * fps))
        enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), str(out)], stdin=subprocess.PIPE)
        for i in range(n):
            pg.evaluate("(t) => new Promise((r) => { window.__inst.seek(t); requestAnimationFrame(() => requestAnimationFrame(r)); })", i / fps)
            enc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        enc.stdin.close()
        enc.wait()
        b.close()
    if errs:
        print("   ⚠ Trang báo lỗi:", errs[:2])
    return meta


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    series = Path(sys.argv[1]).resolve()
    ids = [a for a in sys.argv[2:] if not a.startswith("--") and sys.argv[sys.argv.index(a) - 1] not in ("--lib",)]
    lib = Path(arg("--lib", str(Path.home() / "Desktop/motionlab-replica"))).expanduser()
    force = "--force" in sys.argv
    fxdir = series / "assets/fx"
    fxdir.mkdir(parents=True, exist_ok=True)
    man_p = fxdir / "fx.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    ovs = json.loads((fxdir / "overrides.json").read_text(encoding="utf-8")) if (fxdir / "overrides.json").exists() else {}
    HF = hf_catalog(lib)
    for id_ in ids:
        out, jpg = fxdir / f"{id_}.mp4", fxdir / f"{id_}.jpg"
        if out.exists() and not force and id_ in man:
            print(f"· {id_} đã có, bỏ qua (--force để render lại)")
            continue
        ov = ovs.get(id_, {})
        try:
            if id_ in HF:
                it = HF[id_]
                render_hf(lib, it, out, ov)
                dur, w, h = probe(out)
                poster(out, min(it.get("poster", dur * 0.6), dur - 0.05), jpg)
                man[id_] = {"name": it["name"], "source": "Mẫu HyperFrames", "license": "Apache-2.0", "category": it.get("category"),
                            "cmd": f"npx hyperframes add {id_}", "duration": round(dur, 3), "width": w, "height": h, "poster": jpg.name,
                            "description": it.get("description")}
            else:
                meta = render_ml(lib, id_, out, ov)
                dur, w, h = probe(out)
                poster(out, min(meta.get("poster") or dur * 0.6, dur - 0.05), jpg)
                man[id_] = {"name": meta["name"], "source": "Bản gốc của phòng thí nghiệm chuyển động", "license": "Tự sở hữu", "category": meta.get("category"),
                            "cmd": None, "duration": round(dur, 3), "width": w, "height": h, "poster": jpg.name, "description": meta.get("description")}
            print(f"✓ {id_}  {man[id_]['duration']}s  {man[id_]['width']}×{man[id_]['height']}  {man[id_]['source']}")
        except Exception as e:  # một cái thất bại không ảnh hưởng các cái còn lại
            print(f"✗ {id_}: {str(e)[-600:]}")
        man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
