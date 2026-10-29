#!/usr/bin/env python3
"""Video Renoise → chuỗi khung hình (cho vclip của know.js dùng).
Cách dùng: python3 clip2frames.py <in.mp4> <lessons/NN/assets/clips/v01> [--fps 30] [--w 1920] [--from 0] [--dur 0] [--nocrop]
- Tự động cắt viền đen: đầu ra của các mô hình như Wan thường có viền đen letterbox trên dưới (đo thực 2026-10-27: Wan 3.0 720p đỉnh có 66 pixel đen thuần).
  Lấy 3 khung đo độ sáng trung bình mỗi hàng, các hàng liên tiếp ≤2.5 tính là viền đen, lấy giá trị nhỏ nhất trong 3 khung, cắt thêm 2 pixel. --nocrop để tắt.
- Xuất 0001.jpg… và info.json {n, fps, w, h, crop, src}; in n. Track âm thanh của video gốc lưu riêng thành audio.wav (muốn dùng âm môi trường thì đặt vào mục music của film.js)."""
import json, subprocess, sys
from pathlib import Path

import numpy as np


def arg(n, d): return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def probe(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(src)], capture_output=True, text=True).stdout
    j = json.loads(out); s = j["streams"][0]
    return s["width"], s["height"], float(j["format"]["duration"])


def bars(src, w, h, dur):
    tops, bots = [], []
    for t in (dur * 0.15, dur * 0.5, dur * 0.85):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        if len(raw) < w * h:
            continue
        r = np.frombuffer(raw[: w * h], np.uint8).reshape(h, w).mean(1)
        top = next((i for i in range(h) if r[i] > 2.5), 0)
        bot = next((i for i in range(h) if r[h - 1 - i] > 2.5), 0)
        tops.append(top); bots.append(bot)
    if not tops:
        return 0, 0
    t, b = min(tops), min(bots)
    return (t + 2 if t > 4 else 0), (b + 2 if b > 4 else 0)


src, out = Path(sys.argv[1]), Path(sys.argv[2])
fps, W, t0, dur = arg("--fps", "30"), arg("--w", "1920"), arg("--from", "0"), float(arg("--dur", "0"))
out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*.jpg"): f.unlink()
w, h, d = probe(src)
top, bot = (0, 0) if "--nocrop" in sys.argv else bars(src, w, h, d)
ch = (h - top - bot) // 2 * 2
vf = (f"crop={w}:{ch}:0:{top}," if (top or bot) else "") + f"fps={fps},scale={W}:-2:flags=lanczos"
cut = ["-ss", t0] + (["-t", str(dur)] if dur else [])
subprocess.run(["ffmpeg", "-v", "error", "-y", *cut, "-i", str(src), "-vf", vf, "-q:v", "2", str(out / "%04d.jpg")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *cut, "-i", str(src), "-vn", "-ac", "2", "-ar", "48000", str(out / "audio.wav")], check=False, capture_output=True)  # không có track âm thanh thì không xuất audio.wav
n = len(list(out.glob("*.jpg")))
pw, ph = (int(x) for x in subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(out / "0001.jpg")], capture_output=True, text=True).stdout.strip().split(","))
(out / "info.json").write_text(json.dumps({"n": n, "fps": int(fps), "w": pw, "h": ph, "crop": {"top": top, "bottom": bot}, "src": str(src)}, ensure_ascii=False), encoding="utf-8")
if top or bot:
    print(f"Đã cắt viền đen: trên {top} dưới {bot} (nguồn {w}×{h})", file=sys.stderr)
print(n)
