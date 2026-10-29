#!/usr/bin/env python3
"""Đổi tốc độ lồng tiếng cả bài (cao độ không đổi): lời dẫn dùng ffmpeg atempo để tăng tốc, mọi thời điểm trong timings.json được chia cho hệ số tốc độ tương ứng.
Bản gốc giữ ở narration.orig.wav / timings.orig.json, lần nào cũng tính từ bản gốc nên chạy lặp lại kết quả vẫn như nhau; tốc độ 1 chính là khôi phục.
Cách dùng: python3 scripts/speed.py <lessonDir> 1.15"""
import json, shutil, subprocess, sys
from pathlib import Path

L, f = Path(sys.argv[1]), float(sys.argv[2])
b = L / "build"
ot, ow = b / "timings.orig.json", b / "narration.orig.wav"
fresh = "speed" not in json.loads((b / "timings.json").read_text(encoding="utf-8"))   # Vừa lồng tiếng xong: file hiện tại chính là bản gốc
if fresh or not ot.exists(): shutil.copy(b / "timings.json", ot)
if fresh or not ow.exists(): shutil.copy(b / "narration.wav", ow)
t = json.loads(ot.read_text(encoding="utf-8"))
cur = json.loads((b / "timings.json").read_text(encoding="utf-8"))
if cur.get("speed", 1) == f and (b / "narration.wav").stat().st_mtime >= ow.stat().st_mtime:
    print(f"Đã là tốc độ {f}x, bỏ qua"); sys.exit(0)

s = lambda v: round(v / f, 3)
B = t["beats"]
for bt in (B.values() if isinstance(B, dict) else B):
    for k in ("start", "end", "duration"):
        if k in bt: bt[k] = s(bt[k])
    for w in bt.get("words", []):
        w["start"], w["end"] = s(w["start"]), s(w["end"])
    if "chars" in bt: bt["chars"] = [s(v) for v in bt["chars"]]
    if "cues" in bt: bt["cues"] = {k: s(v) for k, v in bt["cues"].items()}
t["total"] = s(t["total"])
t["speed"] = f
(b / "timings.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
if f == 1: shutil.copy(ow, b / "narration.wav")
else: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ow), "-filter:a", f"atempo={f}", "-ar", "48000", "-ac", "1", str(b / "narration.wav")], check=True)
print(f"{L.name}: tốc độ {f}x, tổng độ dài {t['total']:.1f} giây")
