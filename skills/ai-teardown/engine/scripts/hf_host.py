#!/usr/bin/env python3
"""Dựng thư mục render Hyperframes cho một bài: sao chép bundle, bản mix âm thanh, font, GSAP, các ảnh đã dùng, viết sẵn index.html (thời lượng lấy từ timings.json).

Cách dùng: python3 scripts/hf_host.py <bundle.js> <mix.wav> <timings.json> <thư mục đầu ra> --id id composition [--images thư mục ảnh] [--bg #FFF8F2]

Sau đó trong thư mục đầu ra:
    node <hyperframes>/dist/cli.js lint / inspect / validate / render --quality high --output renders/<id>.mp4
Sân khấu được điều khiển từng khung qua sự kiện hf-seek; dòng thời gian mà lint yêu cầu được đáp ứng bằng một timeline GSAP rỗng chỉ khai báo thời lượng (xem memory: hyperframes-integration).
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GSAP = ROOT / "examples/codex/film/hf/vendor/gsap.min.js"


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    bundle, mix, timings, out = map(Path, sys.argv[1:5])
    cid = arg("--id", "lesson")
    bg = arg("--bg", "#FFF8F2")
    total = json.loads(timings.read_text(encoding="utf-8"))["total"]
    for d in ("assets/fonts", "audio", "vendor", "img", "renders"):
        (out / d).mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "assets/fonts").glob("*.ttf"):
        shutil.copy(f, out / "assets/fonts" / f.name)
    shutil.copy(GSAP, out / "vendor/gsap.min.js")
    shutil.copy(bundle, out / "app.js")
    shutil.copy(mix, out / "audio/mix.wav")
    js = bundle.read_text(encoding="utf-8")
    n = 0
    if "--images" in sys.argv:
        for f in Path(arg("--images")).iterdir():
            if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg"} and f.name in js:
                shutil.copy(f, out / "img" / f.name)
                n += 1
    # Sticker video: HyperFrames chỉ nhận media được khai báo tĩnh trong trang, nên viết lần lượt <video class="clip" data-vclip> theo bảng đăng ký, khi chạy mới chuyển vào thẻ sticker
    vids, vtags = [], ""
    if "--videos" in sys.argv:
        vids = json.loads(Path(arg("--videos")).read_text(encoding="utf-8")).get("videos", [])
        vdir = Path(arg("--vdir", "."))
        (out / "video").mkdir(exist_ok=True)
        import subprocess
        for f in sorted({v["file"] for v in vids}):
            dst = out / "video" / f
            if not dst.exists():   # bỏ track âm thanh, chỉ giữ hình
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vdir / f), "-an", "-c:v", "copy", str(dst)], check=True)
        vtags = "".join(f'  <video data-vclip="{v["vid"]}" class="clip" data-start="{v["start"]}" data-duration="{v["dur"]}" data-track-index="{2 + i}" src="video/{v["file"]}" muted playsinline></video>\n'
                        for i, v in enumerate(vids))
    (out / "meta.json").write_text(json.dumps({"id": cid, "name": cid}), encoding="utf-8")
    (out / "index.html").write_text(f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<script>window.__hfTimelinesBuilding = true;</script>
<style>
@font-face{{font-family:"Noto Sans SC";src:url("assets/fonts/NotoSansSC-VF.ttf") format("truetype");font-weight:100 900}}
@font-face{{font-family:"Geist";src:url("assets/fonts/Geist-VF.ttf") format("truetype");font-weight:100 900}}
@font-face{{font-family:"Geist Mono";src:url("assets/fonts/GeistMono-VF.ttf") format("truetype");font-weight:100 900}}
@font-face{{font-family:"LXGW WenKai";src:url("assets/fonts/LXGWWenKai-Regular.ttf") format("truetype");font-weight:100 450}}
@font-face{{font-family:"LXGW WenKai";src:url("assets/fonts/LXGWWenKai-Medium.ttf") format("truetype");font-weight:451 900}}
html,body{{margin:0;background:{bg}}}
#stage{{position:relative;width:1920px;height:1080px;overflow:hidden}}
</style>
</head>
<body>
<div id="stage" data-composition-id="{cid}" data-start="0" data-duration="{total}" data-width="1920" data-height="1080" data-fps="30">
  <div id="scene" class="clip" data-start="0" data-duration="{total}" data-track-index="0"></div>
  <audio id="mix" class="clip" data-start="0" data-duration="{total}" data-track-index="1" src="audio/mix.wav"></audio>
{vtags}</div>
<script src="vendor/gsap.min.js"></script>
<script src="app.js"></script>
<script>
  // Chỉ dùng để khai báo thời lượng với Hyperframes; hình ảnh do hf-seek điều khiển
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{cid}"] = gsap.timeline({{ paused: true }}).to({{}}, {{ duration: {total} }});
</script>
<script>
  AT.start(document.getElementById("scene"), {{ imgBase: "img/" }}).then((stage) => {{
    window.__stage = stage;
    window.addEventListener("hf-seek", (e) => stage.seek(e.detail.time));
    window.__hfTimelinesBuilding = false;
    window.dispatchEvent(new Event("hf-timelines-built"));
  }});
</script>
</body>
</html>
""", encoding="utf-8")
    print(f"→ {out} (thời lượng {total}s, {n} ảnh, {len(vids)} đoạn sticker video)")


if __name__ == "__main__":
    main()
