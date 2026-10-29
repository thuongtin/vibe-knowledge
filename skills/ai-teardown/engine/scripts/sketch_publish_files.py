#!/usr/bin/env python3
"""Một bài học của engine vẽ tay: tính ra những ảnh thực sự được bản tương tác dùng, xuất ánh xạ files (JSON) để xuất bản Artifact.
Cách dùng: python3 scripts/sketch_publish_files.py <thư mục bài>   (chạy ở thư mục gốc của kho)
"""
import json, re, sys
from pathlib import Path
L = Path(sys.argv[1]); sd = L.parent.parent; nn = L.name
spec = json.loads((L / "scenes.json").read_text()); txt = json.dumps(spec, ensure_ascii=False)
led = {i["id"]: i for i in json.loads((sd / "assets/img/images.json").read_text())["images"]}
lot = {f.stem for f in (L / "lottie").glob("*.json")} if (L / "lottie").exists() else set()
names = set(re.findall(r'"(?:emoji|name|icon)": "([a-z0-9-]+)"', txt))
for s in spec["scenes"]:
    names |= set(s.get("stickers", []))
    for side in ("left", "right"):
        if isinstance(s.get(side), dict) and s[side].get("emoji"): names.add(s[side]["emoji"])
names |= {"thinking-face"}
pre = "noto" if spec.get("skin") == "notion" else "emoji"
ids = {f"{pre}-{n}" for n in names - lot if ":" not in n}
ids |= set(re.findall(r'"(?:img|iconImg)": "([a-z0-9-]+)"', txt))
for s in spec["scenes"]:
    if s.get("clip"):
        fl = json.loads((L / f"data/flip-{s['clip']}.json").read_text()); ids |= set(fl["frames"])
if spec.get("presenter") == "hp":
    ids |= {i for i in led if i.startswith("hp-")}
elif spec.get("presenter"):
    ids |= {f"{spec['presenter']}-{k}" for k in ("0", "blink", "talk", "talk-blink")}
pub = sd / f"publish/lesson{nn}"
files = {"app.js": str(pub / "app.js"), "audio.mp3": str(pub / "audio.mp3")}
for v in sorted([*(pub / "video").glob("*.mp4"), *(pub / "video").glob("*.jpg")]) if (pub / "video").exists() else []:   # sticker video + ảnh bìa
    files[f"video/{v.name}"] = str(v)
for i in sorted(ids):
    if i in led and (pub / "img" / led[i]["file"]).exists():
        files[f"img/{led[i]['file']}"] = str(pub / "img" / led[i]["file"])
missing = sorted(i for i in ids if i not in led or not (pub / "img" / led[i]["file"]).exists())
if missing: print("Thiếu:", missing, file=sys.stderr)
print(json.dumps(files, ensure_ascii=False))
print(f"{len(files)} tệp", file=sys.stderr)
