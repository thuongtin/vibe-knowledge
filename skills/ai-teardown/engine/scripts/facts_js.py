#!/usr/bin/env python3
"""Xuất sổ nghiên cứu (sources.json + facts.json) thành facts.js dùng cho bài giảng tương tác (window.FACTS / window.SOURCES).

Cách dùng: python3 scripts/facts_js.py <thư mục research> <out.js> [--images images.json]
--images: gộp cả sổ ảnh vào SOURCES (id dùng IMG:<id ảnh>), trong bài giảng nhấp vào thẻ nhân vật sẽ thấy tác giả và giấy phép của ảnh.
"""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    rd, out = Path(sys.argv[1]), Path(sys.argv[2])
    F = json.loads((rd / "facts.json").read_text(encoding="utf-8"))["facts"]
    S = json.loads((rd / "sources.json").read_text(encoding="utf-8"))["sources"]
    facts = {f["id"]: {"claim": f["claim"], "status": f.get("status", "verified"),
                       "evidence": [{"source": e["source"], "quote": e.get("quote", "")[:220]} for e in f.get("evidence", [])]} for f in F}
    sources = {s["id"]: {"publisher": s.get("publisher", ""), "title": s.get("title", ""), "locator": s.get("url", "")} for s in S}
    if "--images" in sys.argv:
        imgs = json.loads(Path(sys.argv[sys.argv.index("--images") + 1]).read_text(encoding="utf-8"))["images"]
        for i in imgs:
            sources[f"IMG:{i['id']}"] = {"publisher": i.get("artist", ""), "title": f"{i.get('title', '')} ({i.get('license', '')})", "locator": i.get("page", "")}
    out.write_text("window.FACTS = " + json.dumps(facts, ensure_ascii=False) + ";\nwindow.SOURCES = " + json.dumps(sources, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"{len(facts)} sự thật, {len(sources)} nguồn → {out}")


if __name__ == "__main__":
    main()
