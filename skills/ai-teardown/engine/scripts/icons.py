#!/usr/bin/env python3
"""Rút các icon mà phim dùng từ bộ icon ngoại tuyến, ghi thành một JSON nhỏ rồi đóng vào bundle.

Cách dùng: python3 scripts/icons.py <đầu ra.json> <file nguồn hoặc thư mục>...
Quét trong mã nguồn các tên có dạng "icon-park:robot" (IconPark nhiều màu), "icon-park-outline:robot", "tabler:robot"; bộ icon nằm ở assets/iconsets/.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"\b(tabler|lucide|iconoir|icon-park(?:-outline|-solid|-twotone)?):([a-z0-9]+(?:-[a-z0-9]+)*)\b")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out = Path(sys.argv[1])
    files = []
    for a in sys.argv[2:]:
        p = Path(a)
        files += [f for f in p.rglob("*") if f.suffix in {".js", ".json", ".mjs"}] if p.is_dir() else [p]
    want = sorted({m.group(0) for f in files for m in NAME.finditer(f.read_text(encoding="utf-8", errors="ignore"))})
    sets, res, miss = {}, {}, []
    for name in want:
        pre, ic = name.split(":")
        if pre not in sets:
            sets[pre] = json.loads((ROOT / "assets/iconsets" / f"{pre}.json").read_text(encoding="utf-8"))
        s = sets[pre]
        rec = s["icons"].get(ic)
        if rec is None and ic in s.get("aliases", {}):
            rec = s["icons"].get(s["aliases"][ic]["parent"])
        if rec is None:
            miss.append(name)
            continue
        res[name] = {"body": rec["body"], "w": rec.get("width", s.get("width", 24)), "h": rec.get("height", s.get("height", 24))}
    out.write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
    print(f"{len(res)} icon → {out}" + (f"; thiếu {miss}" if miss else ""))
    if miss:
        sys.exit(1)


if __name__ == "__main__":
    main()
