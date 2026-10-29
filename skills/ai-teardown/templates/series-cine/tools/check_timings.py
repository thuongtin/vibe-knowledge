#!/usr/bin/env python3
"""Sau khi lồng tiếng, kiểm tra thời gian từng chữ có bị "đứt" không: một chuỗi chữ dài dồn vào cùng một thời điểm = việc căn chỉnh đã thất bại từ chỗ đó (nguyên nhân thường gặp: tên tiếng Anh có dấu gạch nối, lời dẫn và cách đọc lệch nhau quá nhiều).
Cách dùng (chạy trong thư mục series): python3 tools/check_timings.py <số bài>"""
import json, sys
from pathlib import Path
L = sys.argv[1]
t = json.loads((Path(__file__).resolve().parent.parent / "lessons" / L / "build" / "timings.json").read_text(encoding="utf-8"))
bad = 0
for b, bt in t["beats"].items():
    ch, txt, run = bt["chars"], bt["text"], 0
    for i in range(1, len(ch)):
        run = run + 1 if abs(ch[i] - ch[i - 1]) < 1e-6 and txt[i].strip() else 0
        if run == 8:
            bad += 1
            print(f"{b}: căn chỉnh bị đứt bắt đầu từ '{txt[i - 8:i + 8]}' (kẹt ở {ch[i]:.2f}s, nhịp này kết thúc lúc {bt['end']:.2f}s)")
            break
    cues = bt.get("cues", {})
    late = [k for k, v in cues.items() if v >= bt["end"] - 0.02]
    if late:
        print(f"{b}: các cue này rơi vào cuối nhịp, nhiều khả năng căn chỉnh bị đứt: {late}")
print("Không phát hiện vấn đề" if not bad else f"{bad} nhịp có vấn đề: sau khi sửa cách viết lời dẫn, xoá build/audio/<nhịp>.* rồi lồng tiếng lại")
