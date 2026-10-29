#!/usr/bin/env python3
"""Điền các bài đã bàn giao vào series.json: video, ảnh bìa, thời lượng, đồng thời cập nhật trạng thái lên sóng; sau đó chạy course_page.py để ra trang khóa học.
Cách dùng (chạy trong thư mục series): python3 tools/update_series.py [--web publish/course] [--prefix p]
Số bài = tiền tố + hai chữ số (như p03 → publish/course/lessonp03.mp4); khi bàn giao deliver.sh đã đặt sẵn theo tên này."""
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
P, WEB, PRE = R / "series.json", R / arg("--web", "publish/course"), arg("--prefix", "")
S = json.loads(P.read_text(encoding="utf-8"))
done = 0
for les in S["lessons"]:
    n = f"{PRE}{les['n']:02d}"
    v = WEB / f"lesson{n}.mp4"
    if v.exists():
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)], capture_output=True, text=True).stdout)
        les.update(video=v.name, poster=f"lesson{n}.jpg", length=f"{int(d // 60)} phút {int(round(d % 60))} giây")
        done += 1
    else:
        for k in ("video", "poster", "length"):
            les.pop(k, None)
total = len(S["lessons"])
S["status_label"] = "Đã lên sóng đủ" if done == total else f"Đã lên sóng {done}/{total}"
P.write_text(json.dumps(S, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{done}/{total}  bài đã được điền")
