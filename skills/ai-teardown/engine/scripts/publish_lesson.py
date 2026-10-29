#!/usr/bin/env python3
"""Đóng gói bài giảng tương tác thành thư mục tự chứa có thể xuất bản: phông chữ được cắt theo các chữ đã dùng thành woff2 rồi nhúng trực tiếp, script và âm thanh là các file cùng thư mục.

Cách dùng: python3 scripts/publish_lesson.py <app.js> <audio.mp3> <out_dir> [--title tiêu-đề] [--subtitle phụ-đề] [--facts facts.js]
                                       [--light] [--images thư-mục-ảnh]
--light: trang và trình phát nền sáng (dùng cho loạt bài macaron).
--images: sao chép các ảnh dùng trong app.js (khớp theo tên file) vào <out_dir>/img/, sân khấu tải bằng imgBase "img/".
Đầu ra: <out_dir>/index.html (không có vỏ html/head/body, phù hợp với Artifact), app.js, audio.<phần-mở-rộng> (Artifact chỉ nhận mp3/wav/ogg/mp4/webm).
"""
import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = [("Noto Sans SC", "NotoSansSC-VF.ttf"), ("Geist", "Geist-VF.ttf"), ("Geist Mono", "GeistMono-VF.ttf")]


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    app, audio, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    title = arg("--title", "Bản mẫu bài giảng tương tác Codex")
    subtitle = arg("--subtitle", "Bản mẫu Spike · cùng một file nguồn với video · sau khi tạm dừng có thể bấm vào hình để xem nguồn")
    facts_js = Path(arg("--facts", "")) if "--facts" in sys.argv else None
    out.mkdir(parents=True, exist_ok=True)
    js = app.read_text(encoding="utf-8")
    # Chữ Trung Quốc trong JS có thể là dạng thoát \uXXXX, khôi phục trước rồi mới thu thập các chữ đã dùng
    decoded = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), js)
    extra = facts_js.read_text(encoding="utf-8") if facts_js else ""
    chars = set(decoded) | set(extra) | set(title + subtitle) | {chr(c) for c in range(0x20, 0x7F)} | set("‹›▶❚×·—…「」：，。？！")
    text = "".join(sorted(c for c in chars if c.isprintable()))
    faces = []
    with tempfile.TemporaryDirectory() as tmp:
        tf = Path(tmp) / "chars.txt"
        tf.write_text(text, encoding="utf-8")
        fonts = [(f, fn, "100 900") for f, fn in FONTS]
        if "LXGW WenKai" in decoded:   # Phong cách sổ tay dùng LXGW WenKai (OFL), hai mức độ đậm
            fonts += [("LXGW WenKai", "LXGWWenKai-Regular.ttf", "100 450"), ("LXGW WenKai", "LXGWWenKai-Medium.ttf", "451 900")]
        for family, fn, wr in fonts:
            dst = Path(tmp) / (Path(fn).stem + ".woff2")
            subprocess.run(["pyftsubset", str(ROOT / "assets/fonts" / fn), f"--text-file={tf}", "--flavor=woff2",
                            "--layout-features=*", f"--output-file={dst}"], check=True)
            b64 = base64.b64encode(dst.read_bytes()).decode()
            faces.append(f'@font-face{{font-family:"{family}";src:url(data:font/woff2;base64,{b64}) format("woff2");font-weight:{wr};font-display:block}}')
            print(f"{family}: {dst.stat().st_size / 1024:.0f} KB")
    shutil.copy(app, out / "app.js")
    light = "--light" in sys.argv
    start_opts = "{}"
    if "--images" in sys.argv:
        img_dir = Path(arg("--images", ""))
        (out / "img").mkdir(exist_ok=True)
        used = [f for f in img_dir.iterdir() if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg"} and f.name in decoded]
        for f in used:
            shutil.copy(f, out / "img" / f.name)
        print(f"Ảnh {len(used)} tấm → {out / 'img'}")
        start_opts = '{imgBase: "img/"}'
    # Sticker video: sao chép các đoạn theo bảng đăng ký videos của cues.json vào <out>/video/ (bỏ track âm thanh, nén xuống 720p để tiết kiệm dung lượng), sân khấu tải bằng vidBase "video/"
    if "--videos" in sys.argv:
        vids = json.loads(Path(arg("--videos", "")).read_text(encoding="utf-8")).get("videos", [])
        vdir = Path(arg("--vdir", "."))
        if vids:
            (out / "video").mkdir(exist_ok=True)
            for f in sorted({v["file"] for v in vids}):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vdir / f), "-an", "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "slow", "-crf", "26",
                                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out / "video" / f)], check=True)
                jpg = vdir / (Path(f).stem + ".jpg")  # Ảnh bìa (jpg cùng tên do fx_render tạo), hiển thị khi tạm dừng trước lúc bắt đầu
                if jpg.exists():
                    shutil.copy(jpg, out / "video" / jpg.name)
            print(f"Sticker video {len({v['file'] for v in vids})} đoạn → {out / 'video'}")
            start_opts = start_opts[:-1] + ', vidBase: "video/"}' if start_opts != "{}" else '{vidBase: "video/"}'
    bg, ink, ink2 = ("#FFF8F2", "#2F2A45", "#7A7390") if light else ("#070B18", "#EAF0FF", "#8A96BA")
    audio_name = f"audio{audio.suffix}"
    for old in out.glob("audio.*"):
        old.unlink()
    shutil.copy(audio, out / audio_name)
    html = f"""<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{subtitle}">
<style>
{chr(10).join(faces)}
:root{{color-scheme:{"light" if light else "dark"}}}
body{{margin:0;background:{bg};color:{ink}}}
main{{max-width:1400px;margin:0 auto;padding:28px 16px 60px}}
header{{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:16px;font-family:"Geist","Noto Sans SC",sans-serif}}
h1{{margin:0;font-size:26px;font-weight:700;letter-spacing:.01em}}
header p{{margin:0;color:{ink2};font-size:13px}}
#offstage{{position:absolute;left:-99999px;top:0}}
</style>
<main>
  <header><h1>{title}</h1><p>{subtitle}</p></header>
  <div id="player"></div>
</main>
<div id="offstage" aria-hidden="true"></div>
<audio id="audio" src="{audio_name}" preload="auto"></audio>
{"<script>" + extra + "</script>" if extra else ""}
<script src="app.js"></script>
<script>
  AT.start(document.getElementById("offstage"), {start_opts}).then((stage) => {{
    window.__stage = stage;
    window.__player = AT.mountPlayer(document.getElementById("player"), {{
      stage, audio: document.getElementById("audio"),
      chapters: stage.chapters, captions: stage.captions,
      facts: window.FACTS || {{}}, sources: window.SOURCES || {{}}, light: {"true" if light else "false"},
    }});
  }});
</script>
"""
    (out / "index.html").write_text(html, encoding="utf-8")
    size = sum(p.stat().st_size for p in out.iterdir())
    print(f"→ {out} (tổng {size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
