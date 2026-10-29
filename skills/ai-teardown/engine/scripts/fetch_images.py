#!/usr/bin/env python3
"""Lấy ảnh từ Wikimedia Commons, đồng thời ghi lại tác giả và giấy phép, ghi vào sổ cái ảnh.

Cách dùng:
    python3 scripts/fetch_images.py <spec.json> <thư mục đầu ra>

spec.json: {"images": [{"id": "turing", "title": "File:Alan Turing (1951).jpg", "width": 900, "note": "mô tả mục đích sử dụng"}]}
    title là tên tệp trên Commons; width là chiều rộng ảnh thu nhỏ cần lấy (PDF sẽ render trang đầu).

Đầu ra:
    <thư mục đầu ra>/<id>.<ext>        ảnh thu nhỏ
    <thư mục đầu ra>/images.json        sổ cái: trang nguồn, địa chỉ ảnh gốc, tác giả, giấy phép, chữ ghi công
Chỉ nhận ảnh có giấy phép cho phép tái sử dụng rõ ràng (phạm vi công cộng, CC0, CC BY, CC BY-SA); giấy phép khác thì bỏ qua và báo ra.
"""
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import date
from pathlib import Path

UA = "ai-teardown-course-builder/0.1 (local research script)"
API = "https://commons.wikimedia.org/w/api.php"
OK_LICENSE = re.compile(r"^(public domain|pd|cc0|cc by(-sa)? \d)", re.I)


def curl(url, out=None, tries=6):
    """Gọi API phải nhận được JSON mới tính là thành công (Wikimedia thỉnh thoảng trả về giới hạn tốc độ hoặc trang lỗi); tệp tải về phải không rỗng. Thất bại thì thử lại với độ lùi theo số lần."""
    for k in range(tries):
        cmd = ["curl", "-sL", "--max-time", "60", "-A", UA, url] + (["-o", str(out)] if out else [])
        r = subprocess.run(cmd, capture_output=True, text=out is None)
        if r.returncode == 0:
            if out is not None and out.exists() and out.stat().st_size > 0:
                return out
            if out is None and r.stdout.lstrip().startswith("{"):
                return r.stdout
        time.sleep(2 * (k + 1))
    raise RuntimeError(f"Tải xuống thất bại: {url}")


def plain(v):
    return html.unescape(re.sub(r"<.*?>", "", str(v) if v is not None else "")).strip()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    led_p = out / "images.json"
    ledger = json.loads(led_p.read_text(encoding="utf-8")) if led_p.exists() else {"images": []}
    have = {i["id"]: i for i in ledger["images"]}

    for it in spec["images"]:
        old = have.get(it["id"])
        if old and old.get("title") == it["title"] and (out / old["file"]).exists() and "--force" not in sys.argv:
            print(f"· {it['id']:12s} đã có, bỏ qua")
            continue
        q = urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo", "titles": it["title"],
                                    "iiprop": "url|size|mime|extmetadata", "iiurlwidth": it.get("width", 1200)})
        page = next(iter(json.loads(curl(f"{API}?{q}"))["query"]["pages"].values()))
        if "imageinfo" not in page:
            print(f"✗ {it['id']}: Commons không có {it['title']}")
            continue
        ii = page["imageinfo"][0]
        md = {k: plain(v.get("value")) for k, v in ii.get("extmetadata", {}).items()}
        lic = md.get("LicenseShortName", "")
        if not OK_LICENSE.match(lic):
            print(f"✗ {it['id']}: giấy phép «{lic}» không nằm trong danh sách cho phép, bỏ qua")
            continue
        src = ii.get("thumburl") or ii["url"]
        ext = Path(urllib.parse.urlparse(src).path).suffix.lower() or ".jpg"
        if ext == ".pdf":
            ext = ".jpg"
        f = out / f"{it['id']}{ext}"
        curl(src, f)
        artist = md.get("Artist", "") or "Khuyết danh"
        pd = lic.lower().startswith(("public domain", "pd", "cc0"))
        rec = {
            "id": it["id"], "file": f.name, "title": it["title"],
            "page": ii.get("descriptionurl"), "original": ii["url"], "thumb": src,
            "width": ii.get("thumbwidth") or ii.get("width"), "height": ii.get("thumbheight") or ii.get("height"),
            "license": lic, "license_url": md.get("LicenseUrl"), "artist": artist,
            "credit": f"{artist} · {lic} · Wikimedia Commons" if not pd else f"{artist} · {lic}(phạm vi công cộng)· Wikimedia Commons",
            "attribution_required": md.get("AttributionRequired", "true") != "false",
            "description": md.get("ImageDescription", "")[:300], "date": md.get("DateTimeOriginal", ""),
            "note": it.get("note", ""), "fetched": date.today().isoformat(),
        }
        have[it["id"]] = rec
        print(f"✓ {it['id']:12s} {rec['width']}×{rec['height']}  {lic:14s} {artist[:40]}")

    ledger["images"] = list(have.values())
    led_p.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Sổ cái → {led_p} ({len(ledger['images'])} ảnh)")


if __name__ == "__main__":
    main()
