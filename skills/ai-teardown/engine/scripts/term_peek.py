#!/usr/bin/env python3
"""Xem toàn bộ chữ trên màn hình tại một thời điểm của bản quay màn hình (dùng khi viết bố cục hình ảnh, xác định số dòng cần làm nổi bật).
Cách dùng: python3 scripts/term_peek.py <x.frames.json> <giây hoặc mark:tên> [--nums]"""
import json, sys
d = json.load(open(sys.argv[1]))
t = sys.argv[2]
t = d["marks"][t[5:]] if t.startswith("mark:") else float(t)
rows = [""] * d["rows"]
for f in d["frames"]:
    if f["t"] > t:
        break
    for k, v in f["d"].items():
        rows[int(k)] = "".join(r[0] for r in v)
for i, r in enumerate(rows):
    print(f"{i:>2}│{r}" if "--nums" in sys.argv else r)
