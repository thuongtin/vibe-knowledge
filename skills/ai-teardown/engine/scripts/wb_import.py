#!/usr/bin/env python3
"""Nhập hình minh hoạ của một chương trong Sách xanh vào series WorkBuddy: PNG/JPG → assets/img/wb<NN>-<số thứ tự>.png (ghi vào sổ, kèm nguồn chương); GIF → chuỗi khung hình 8fps đã loại trùng, thư mục bài data/flip-<tên>.json, trong cảnh shot ghi "clip": "<tên>".
Cách dùng: python3 scripts/wb_import.py <thư mục bài> "<tên thư mục chương>" [--prefix wb04]
In ra id và kích thước của từng hình, đồng thời tạo build/chapter_sheet.jpg trong thư mục bài (tổng quan ảnh thu nhỏ của mọi hình minh hoạ, dùng để xem hình rồi quyết định crop / vị trí khoanh chú thích).
"""
import sys, json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts")); from ledger import add_images

L = Path(sys.argv[1]).resolve(); sd = L.parent.parent; nn = L.name
chap = sys.argv[2]
pre = sys.argv[sys.argv.index("--prefix") + 1] if "--prefix" in sys.argv else f"wb{nn}"
book = sd / "source/docs/bluebook"
cdir = next(p for p in book.glob(f"*/{chap}")) if not (book / chap).exists() else book / chap
src = cdir / "assets"
short = chap.split(" ", 2)[-1] if chap.startswith("第") else chap
credit = f"Nguồn ảnh chụp màn hình: 《WorkBuddy 实战蓝皮书》{chap.split(' ')[0]} {chap.split(' ')[1] if len(chap.split(' '))>1 else ''} · MIT".replace("  ", " ")
credit = f"Nguồn ảnh chụp màn hình: 《WorkBuddy 实战蓝皮书》{chap} · MIT"
items, thumbs = [], []
(L / "data").mkdir(parents=True, exist_ok=True); (L / "build").mkdir(exist_ok=True)
files = sorted(src.glob("*")) if src.exists() else []
for k, f in enumerate(files, 1):
    ext = f.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".webp"):
        iid = f"{pre}-{k:02d}"; im = Image.open(f).convert("RGB"); w, h = im.size
        if w > 2400: im = im.resize((2400, round(h * 2400 / w)), Image.LANCZOS); w, h = im.size
        im.save(sd / "assets/img" / f"{iid}.png", optimize=True)
        items.append({"id": iid, "file": f"{iid}.png", "width": w, "height": h, "artist": "Các tác giả của WorkBuddy 实战蓝皮书", "license": "MIT", "source": "github.com/AlephAITech/WorkBuddyGuide", "credit": credit})
        print(f"Hình {iid}  {w}×{h}  ← {f.name}"); t = im.copy(); t.thumbnail((600, 380)); thumbs.append((iid, t))
    elif ext == ".gif":
        name = f"{pre}-g{k:02d}"; g = Image.open(f); durs, frames = [], []
        for i in range(g.n_frames): g.seek(i); durs.append(g.info.get("duration", 100)); frames.append(g.convert("RGB").copy())
        starts, acc = [], 0
        for d in durs: starts.append(acc); acc += d
        seq, uniq, prev, T = [], [], None, 0
        W0 = frames[0].size[0]; H0 = frames[0].size[1]; W = min(1100, W0); H = round(H0 * W / W0)
        gitems = []
        while T < acc:
            i = max(j for j, s in enumerate(starts) if s <= T); im = frames[i].resize((W, H), Image.LANCZOS)
            if prev is not None and ImageChops.difference(im, prev).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox() is None: seq.append(seq[-1])
            else:
                iid = f"flip-{name}-{len(uniq):03d}"; im.save(sd / "assets/img" / f"{iid}.jpg", quality=78); uniq.append(iid); seq.append(iid); prev = im
                gitems.append({"id": iid, "file": f"{iid}.jpg", "width": W, "height": H, "artist": "Các tác giả của WorkBuddy 实战蓝皮书", "license": "MIT", "source": "github.com/AlephAITech/WorkBuddyGuide", "credit": credit.replace("ảnh chụp màn hình", "bản quay màn hình")})
            T += 125
        items += gitems
        json.dump({"fps": 8, "frames": seq, "w": W, "h": H}, open(L / "data" / f"flip-{name}.json", "w"))
        print(f"Clip quay màn hình \"{name}\"  {acc/1000:.1f} giây, {len(uniq)} khung hình  ← {f.name}"); t = frames[len(frames)//2].copy(); t.thumbnail((600, 380)); thumbs.append((f"clip:{name}", t))
    elif ext == ".mp4":
        print(f"Video (chưa nhập, có thể dùng ffmpeg trích khung hình làm clip): {f.name}")
add_images(sd, items)
if thumbs:
    cols = 3; rows = (len(thumbs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 610, rows * 410), "white"); d = ImageDraw.Draw(sh)
    for k, (n, t) in enumerate(thumbs):
        x, y = (k % cols) * 610, (k // cols) * 410; sh.paste(t, (x + 5, y + 24)); d.text((x + 6, y + 4), n, fill=(220, 0, 0))
    sh.save(L / "build/chapter_sheet.jpg", quality=80); print("Tổng quan: ", L / "build/chapter_sheet.jpg")
