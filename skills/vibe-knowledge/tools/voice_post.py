#!/usr/bin/env python3
"""Hậu kỳ giọng người cho giọng nhân bản của người dùng (chuỗi xử lý đã chốt trong voice-clone-test/README.md), chạy sau khi lồng tiếng + đổi tốc độ.
Cách dùng: python3 voice_post.py <lessons/NN>      bản gốc giữ ở build/narration.pre.wav, chạy lặp lại sẽ tính từ bản gốc."""
import shutil, subprocess, sys
from pathlib import Path
b = Path(sys.argv[1]) / "build"
pre, cur = b / "narration.pre.wav", b / "narration.wav"
if not pre.exists() or cur.stat().st_mtime > pre.stat().st_mtime + 1: shutil.copy(cur, pre)
chain = "highpass=f=70,equalizer=f=140:t=o:w=1:g=3.5,equalizer=f=420:t=o:w=1:g=-2,equalizer=f=3200:t=o:w=1:g=3,acompressor=threshold=-22dB:ratio=3.5:attack=4:release=90:makeup=2"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(pre), "-af", chain, "-ar", "48000", str(cur)], check=True)
shutil.copystat(pre, cur); cur.touch()
print("✓ Hậu kỳ giọng người →", cur)
