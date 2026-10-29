#!/usr/bin/env python3
"""Tải biểu tượng 3D nhiều màu từ Microsoft Fluent Emoji (MIT), đặt vào assets/img/ của series và đăng ký vào images.json (nguồn tự động hiển thị).

Cách dùng: python3 scripts/emoji.py <thư mục series> [--color] "Robot" "Bar chart" "Man office worker" ...
- Mặc định tải bản 3D (PNG, id emoji-<tên>, dùng cho phong cách sổ tay); --color tải bản phẳng nhiều màu (SVG, id emojic-<tên>, dùng cho phong cách Notion tối giản).
- Tên chính là tên thư mục dưới assets/ trong kho fluentui-emoji (chép đúng hoa thường, ví dụ "Magnifying glass tilted left").
- Mục có biến thể màu da (người, cử chỉ) tự động lấy Default. id ảnh là emoji-<chữ thường nối gạch ngang>, ví dụ emoji-bar-chart.
"""
import json, subprocess, sys, urllib.parse
from pathlib import Path
from PIL import Image

RAW = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"


def fetch(url, out):
    r = subprocess.run(["curl", "-sfL", "--max-time", "60", "-o", str(out), url])
    return r.returncode == 0 and out.exists() and out.stat().st_size > 1000


def main():
    sd = Path(sys.argv[1]); names = [n for n in sys.argv[2:] if n != "--color"]
    color = "--color" in sys.argv
    img = sd / "assets/img"; img.mkdir(parents=True, exist_ok=True)
    led = img / "images.json"
    data = json.loads(led.read_text()) if led.exists() else {"images": []}
    have = {i["id"] for i in data["images"]}
    for n in names:
        slug = n.lower().replace(" ", "-").replace("’", "").replace("'", "")
        pre, ext, kind = ("emojic", "svg", "Color") if color else ("emoji", "png", "3D")
        iid, out = f"{pre}-{slug}", img / f"{pre}-{slug}.{ext}"
        snake = n.lower().replace(" ", "_").replace("-", "_")
        q = urllib.parse.quote(n)
        k = kind.lower()
        ok = out.exists() or any(fetch(RAW + p, out) for p in (f"{q}/{kind}/{snake}_{k}.{ext}", f"{q}/Default/{kind}/{snake}_{k}_default.{ext}"))
        if not ok:
            print(f"✗ {n}(hãy tra tên thư mục chính xác trong kho fluentui-emoji)"); out.unlink(missing_ok=True); continue
        w, h = (256, 256) if color else Image.open(out).size
        if iid not in have:
            data["images"].append({"id": iid, "file": out.name, "width": w, "height": h, "artist": "Microsoft",
                                   "license": "MIT", "source": "Fluent Emoji (github.com/microsoft/fluentui-emoji)", "credit": "Biểu tượng: Microsoft Fluent Emoji · MIT"})
            have.add(iid)
        print(f"✓ {iid}  {w}×{h}")
    led.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
