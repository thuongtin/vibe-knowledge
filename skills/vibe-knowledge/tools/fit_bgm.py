#!/usr/bin/env python3
"""Cắt BGM mặc định của Vibe Tri Thức (assets/music/vibe-bgm.m4a) thành độ dài phim bất kỳ, các điểm cắt đều nằm trên vạch ô nhịp.
Cách dùng: $CINE_PY fit_bgm.py <đầu ra.wav> --seconds 95          # chỉ định tổng độ dài (thường = tổng độ dài lời dẫn + thẻ kết TAIL)
      $CINE_PY fit_bgm.py <đầu ra.wav> --lesson <thư mục số phát>      # đọc total trong build/timings.json, rồi cộng --tail (mặc định 3 giây)
      Tùy chọn --src bài nhạc khác (cùng thư mục phải có dữ liệu nhịp .json cùng tên), --xfade 0.08
Cách làm: phần đầu giữ nguyên bản gốc; từ ô nhịp thứ tail_bar đến cuối bài là đoạn kết tự nhiên của bản gốc, nối nguyên đoạn vào cuối.
  Phim ngắn hơn bản gốc: cắt đoạn đầu đến vạch ô nhịp gần mục tiêu nhất, rồi nối đoạn kết;
  Phim dài hơn bản gốc: lặp từng đoạn 8 ô nhịp trong khoảng loop_bars để kéo dài.
  Mối nối dùng crossfade công suất bằng nhau 80 mili giây; phần lẻ chênh lệch tổng độ dài được cắt bớt hoặc bù im lặng ở cuối (đoạn kết vốn đang fade out).
Đầu ra: <đầu ra.wav> (48 kHz stereo) + <đầu ra>.beats.json (thời điểm của từng nhịp / từng ô nhịp trong thành phẩm, film.js dùng để bám nhịp)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np

SR = 48000
SK = Path(__file__).resolve().parents[1]
args = sys.argv[1:]
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
out = Path(args[0])
src = Path(opt("--src", SK / "assets/music/vibe-bgm.m4a"))
meta = json.loads(src.with_suffix(".json").read_text(encoding="utf-8"))
if "--lesson" in args:
    L = json.loads((Path(opt("--lesson")) / "build/timings.json").read_text(encoding="utf-8"))["total"] + float(opt("--tail", 3))
else:
    L = float(opt("--seconds"))
xf = float(opt("--xfade", 0.08))

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
bar = meta["beat"] * meta["beats_per_bar"]
bt = lambda b: meta["t0"] + b * bar                      # điểm bắt đầu của ô nhịp thứ b (giây, bản gốc)
S = lambda t: int(round(t * SR))
tail0 = bt(meta["tail_bar"]); tail = y[S(tail0):]; tailL = len(tail) / SR

def splice(a, b):                                          # Nối bằng crossfade công suất bằng nhau
    n = min(S(xf), len(a), len(b))
    if n == 0: return np.concatenate([a, b])
    w = np.linspace(0, np.pi / 2, n)[:, None]
    mid = a[-n:] * np.cos(w) + b[:n] * np.sin(w)
    return np.concatenate([a[:-n], mid, b[n:]])

plan = []                                                   # (giây bắt đầu của bản gốc, giây kết thúc của bản gốc, số ô nhịp bắt đầu)
headT = L - tailL
if headT <= bt(meta["loop_bars"][1]):                      # Phim ngắn: cắt đoạn đầu đến vạch ô nhịp gần nhất
    nb = max(1, int(round((headT - meta["t0"]) / bar)))
    plan.append((0.0, bt(nb), 0))
else:                                                       # Phim dài: lặp đoạn giữa, mỗi đoạn 8 ô nhịp
    a, z = meta["loop_bars"]; plan.append((0.0, bt(z), 0))
    cur = bt(z); ph = meta["phrase_bars"]; b = a
    while cur + ph * bar <= headT + bar / 2:
        plan.append((bt(b), bt(b + ph), b)); cur += ph * bar; b = a + ((b - a + ph) % (z - a - ph + 1))
plan.append((tail0, len(y) / SR, meta["tail_bar"]))
mix, grid, n0 = None, [], S(xf)
for i, (a0, a1, b0) in enumerate(plan):
    seg = y[S(a0):S(a1)]
    start = 0.0 if mix is None else (len(mix) - min(n0, len(mix), len(seg))) / SR   # Điểm bắt đầu thực của đoạn này trong thành phẩm sau khi mối nối chồng lên nhau
    first = 0 if i == 0 else b0
    nbar = int(round((a1 - a0) / bar)) + (1 if i == len(plan) - 1 else 0)
    grid += [(start + (bt(first + k) - a0), first + k) for k in range(nbar)] if i else [(bt(k), k) for k in range(nbar)]
    mix = seg if mix is None else splice(mix, seg)
segs = plan
n = S(L)
if len(mix) >= n:
    mix = mix[:n]; f = min(S(1.5), n); mix[-f:] *= np.linspace(1, 0, f)[:, None]
else:
    mix = np.concatenate([mix, np.zeros((n - len(mix), 2), np.float32)])
out.parent.mkdir(parents=True, exist_ok=True)
pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "2", "-ar", str(SR), "-i", "-", str(out)], input=pcm, check=True)
bars = [round(t, 3) for t, _ in grid if t < L]
beats = sorted({round(t + k * meta["beat"], 3) for t in bars for k in range(meta["beats_per_bar"]) if t + k * meta["beat"] < L})
out.with_suffix(".beats.json").write_text(json.dumps({"src": src.name, "bpm": meta["bpm"], "length": round(L, 3), "bars": bars, "beats": beats}, ensure_ascii=False), encoding="utf-8")
print(f"BGM → {out}  {L:.2f}s  {meta['bpm']} BPM  ô nhịp {bar:.3f}s  mối nối {len(segs) - 1} chỗ (đều nằm trên vạch ô nhịp)  bảng nhịp → {out.with_suffix('.beats.json').name}")
