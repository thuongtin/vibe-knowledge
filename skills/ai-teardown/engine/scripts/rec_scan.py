#!/usr/bin/env python3
"""Quét qua các khung hình quay màn hình, tìm chữ riêng tư vẫn còn lộ trên hình: python3 scripts/rec_scan.py <frames.json>... [--pat regex]
Mỗi khung hình được khôi phục toàn màn hình theo sai khác, rồi toàn màn hình (ghép thành một chuỗi, xuyên dòng cũng tính) được so khớp với regex, báo cáo thời điểm xuất hiện đầu tiên và ngữ cảnh."""
import json, re, sys

pat = r"andyhu|feishu|/Users/(?!myname)|chatcut|cowart|pireel|node_repl|codex_app|codex_tui|cua_repl|computer-use|memmy|dashi|youware|@(?!example)[\w-]+\.(com|cn|io)"
args = sys.argv[1:]
if "--pat" in args:
    i = args.index("--pat"); pat = args[i + 1]; del args[i:i + 2]
P = re.compile(pat, re.I)
bad = 0
for f in args:
    d = json.load(open(f))
    rows, cols = d["rows"], d["cols"]
    state = [""] * rows
    seen = {}
    for fr in d["frames"]:
        for k, runs in fr["d"].items():
            state[int(k)] = "".join(r[0] for r in runs)
        txt = "".join(s.ljust(cols) for s in state)
        for m in P.finditer(txt):
            key = m.group(0).lower()
            if key not in seen:
                seen[key] = fr["t"]
                print(f"{f}  t={fr['t']:.1f}s  \"{txt[max(0, m.start()-30):m.end()+30].strip()}\"")
                bad += 1
print("sạch" if not bad else f"tổng {bad} chỗ")
