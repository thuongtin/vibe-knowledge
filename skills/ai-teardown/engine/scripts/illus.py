#!/usr/bin/env python3
"""Đưa các minh hoạ đã chọn trong thư viện minh hoạ vào thư mục illus/ của bài, trong cảnh viết "illus": "ip-5-48" là dùng được (vẽ viền nét + khối màu mờ vào).
Cách dùng: python3 scripts/illus.py <thư mục bài> ip-5-48 ip-2-12 ...
Thư viện minh hoạ: assets/illustrations/iconpark/ (catalog.json có tên và album; ảnh tổng quan _sheet.html).
"""
import json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
lib = ROOT / "assets/illustrations/iconpark"
cat = {i["id"]: i for i in json.loads((lib / "catalog.json").read_text())["items"]}
L = Path(sys.argv[1]); (L / "illus").mkdir(parents=True, exist_ok=True)
for iid in sys.argv[2:]:
    if iid not in cat: print(f"✗ Không có {iid}"); continue
    shutil.copy(lib / cat[iid]["file"], L / "illus" / f"{iid}.svg")
    print(f"✓ {iid} {cat[iid]['album']} · {cat[iid]['name']}")
