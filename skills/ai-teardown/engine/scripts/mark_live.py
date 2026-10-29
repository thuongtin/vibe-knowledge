#!/usr/bin/env python3
"""Sau khi một bài học lên sóng: ghi lại liên kết bản tương tác, làm mới "số bài đã lên sóng", tạo lại trang khóa học.
Cách dùng: python3 scripts/mark_live.py <thư mục series> <số bài> <liên kết bản tương tác>"""
import json, subprocess, sys
from pathlib import Path

sd, n, url = Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
p = sd / "series.json"
s = json.load(open(p))
next(l for l in s["lessons"] if l["n"] == n)["interactive"] = url
live = [l["n"] for l in s["lessons"] if l.get("video") and l["n"] >= 1]
total = len([l for l in s["lessons"] if l["n"] >= 1])
k = len(live)
span = (f"Bài 1–{max(live)}" if max(live) > 1 else "Bài 1") if live == list(range(1, max(live) + 1)) else f"{k} bài"
s["status_label"] = f"{span} đã lên sóng · {total - k} bài còn lại đang sản xuất" if k < total else f"Cả {total} bài đã lên sóng"
json.dump(s, open(p, "w"), ensure_ascii=False, indent=2)
print(s["status_label"])
subprocess.run([sys.executable, str(Path(__file__).parent / "course_page.py"), str(p), str(sd / "publish" / "course")], check=True)
