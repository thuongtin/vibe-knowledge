#!/usr/bin/env python3
"""Kiểm tra chất lượng thành phẩm: python3 qa.py <thanh-pham.mp4> [--every 3] [--out qa/]
1) Cứ N giây lấy một khung ghép thành bảng contact sheet qa/sheet.jpg (xem từng ảnh: chữ tràn, đè phụ đề, màn hình trống, chữ loạn mã trong ảnh minh họa)
2) Vision OCR đọc lại từng dòng chữ trên màn hình → qa/ocr.txt (đối chiếu facts.md để kiểm tra con số, trích dẫn, nguồn)
3) Âm lượng: LUFS tổng thể / đỉnh thực (mục tiêu ≈ −14,5 LUFS, ≤ −1 dBTP)
5) Kiểm tra BGM (bắt buộc): lấy tương quan giữa phần đầu thành phẩm và phần đầu bản gốc vibe-bgm (phần đầu của fit_bgm giữ theo bản gốc), <0.12 thì coi là không có BGM; nếu cùng thư mục có bgm.json thì báo luôn tỷ lệ giọng người
4) Phát hiện đóng băng: hình ảnh gần như không đổi liên tục >3 giây thì cảnh báo (vi phạm "tĩnh tối đa ≤3 giây"; cả đoạn mấy chục giây không đổi = quay hỏng, ví dụ hai luồng quay ghi hỏng cùng một picture.mp4, phải quay lại)"""
import re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def arg(n, d): return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
SK = Path(__file__).resolve().parent
src = Path(sys.argv[1]); every = float(arg("--every", "3")); out = Path(arg("--out", str(src.parent / "qa")))
out.mkdir(parents=True, exist_ok=True); fr = out / "frames"; fr.mkdir(exist_ok=True)
for f in fr.glob("*.png"): f.unlink()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"fps=1/{every},scale=1600:-2", str(fr / "f_%04d.png")], check=True)
fs = sorted(fr.glob("f_*.png"))
ocr = SK / "ocr"
if not ocr.exists() or ocr.stat().st_mtime < (SK / "ocr.swift").stat().st_mtime:
    subprocess.run(["swiftc", "-O", str(SK / "ocr.swift"), "-o", str(ocr)], check=True)
txt = subprocess.run([str(ocr), *map(str, fs)], capture_output=True, text=True).stdout
lines, seen = [], []
for blk in txt.split("@@")[1:]:
    ls = blk.strip().split("\n"); i = int(re.search(r"(\d+)", ls[0]).group(1)); t = (i - 1) * every
    for l in ls[1:]:
        m = re.match(r"\[y([\d.]+) h([\d.]+)\] (.*)", l)
        if m and len(m.group(3).strip()) > 1 and m.group(3) not in seen[-30:]:
            seen.append(m.group(3)); lines.append(f"{int(t // 60)}:{t % 60:04.1f}  {m.group(3)}")
(out / "ocr.txt").write_text("\n".join(lines), encoding="utf-8")
w = 400; ims = [Image.open(f) for f in fs]; h = int(w * ims[0].height / ims[0].width); cols = 6
sheet = Image.new("RGB", (cols * w, ((len(ims) + cols - 1) // cols) * h), "black"); d = ImageDraw.Draw(sheet)
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
for i, im in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * h; sheet.paste(im.resize((w, h)), (x, y)); t = i * every
    d.rectangle([x, y, x + 70, y + 24], fill="black"); d.text((x + 4, y + 2), f"{int(t // 60)}:{int(t % 60):02d}", fill="yellow", font=font)
sheet.save(out / "sheet.jpg", quality=82)
r = subprocess.run(["ffmpeg", "-nostats", "-i", str(src), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
fz = subprocess.run(["ffmpeg", "-nostats", "-i", str(src), "-an", "-vf", "fps=10,scale=480:-2,freezedetect=n=0.002:d=3", "-f", "null", "-"], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", fz)]; durs = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", fz)]
if len(durs) < len(starts): durs.append(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout) - starts[-1])
frozen = [(a, d) for a, d in zip(starts, durs)]
(out / "freeze.txt").write_text("\n".join(f"{int(a // 60)}:{a % 60:04.1f}  tĩnh {d:.1f} giây" for a, d in frozen), encoding="utf-8")
print(f"→ {out/'sheet.jpg'}  {len(fs)} khung\n→ {out/'ocr.txt'}  {len(lines)} dòng\nÂm lượng {I[-1] if I else '?'} LUFS  đỉnh thực {P[-1] if P else '?'} dBTP")
if frozen:
    print(f"⚠ Hình ảnh tĩnh {len(frozen)} đoạn (>3 giây) → {out/'freeze.txt'}: " + ", ".join(f"từ {int(a // 60)}:{a % 60:04.1f} dài {d:.1f}s" for a, d in frozen[:6]))
    if any(d > 10 for a, d in frozen): print("⚠⚠ Có đoạn đóng băng hơn 10 giây, phần lớn là quay hỏng (quay song song / trang bị treo), hãy quay lại rồi mới giao")
else:
    print("Kiểm tra tĩnh: không có hình ảnh tĩnh quá 3 giây")
# ── Kiểm tra BGM bắt buộc ──
import numpy as np
def _pcm(f, t, sr=4000):
    b = subprocess.run(["ffmpeg", "-v", "error", "-t", str(t), "-i", str(f), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
ref = _pcm(SK.parent / "assets/music/vibe-bgm.m4a", 8); x = _pcm(src, 12); best, lag = 0.0, 0.0
for k in range(0, 4000 * 3, 20):
    seg = x[k:k + len(ref)]
    if len(seg) < len(ref): break
    c = float(np.dot(seg, ref) / (np.linalg.norm(seg) * np.linalg.norm(ref) + 1e-9))
    if c > best: best, lag = c, k / 4000
bj = src.parent / "bgm.json"
extra = ""
if bj.exists():
    import json as _j; r = _j.loads(bj.read_text(encoding="utf-8"))
    if r.get("voice_gap_db") is not None: extra = f"; khi nói giọng người cao hơn BGM {r['voice_gap_db']} dB, ở chỗ ngắt {r.get('gap_in_pauses_db')} dB" + (" (BGM tự động bổ sung)" if r.get("auto") else "")
user_bgm = r.get("user_bgm") if bj.exists() else None
if user_bgm:
    print(f"BGM: người dùng yêu cầu đổi thành {user_bgm[0]} ({user_bgm[1]}){extra}")
elif best >= 0.12:
    print(f"BGM: có vibe-bgm (tương quan {best:.2f}, từ {lag:.2f}s){extra}")
else:
    print(f"⚠⚠ BGM: không phát hiện vibe-bgm (tương quan {best:.2f}). Trừ khi người dùng yêu cầu đổi bài, mỗi phim của Vibe Knowledge đều bắt buộc có: xác nhận finish.py đã gắn hook bắt buộc (bgm_force.py --patch), chạy lại finish.py + deliver.sh")
