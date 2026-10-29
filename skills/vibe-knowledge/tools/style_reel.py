#!/usr/bin/env python3
"""Trục thời gian và lời dẫn của tuyển tập phim mẫu phong cách: sao chép đoạn mở đầu B01 của tập 01 ("一根木头…五十金") N lần, trước mỗi đoạn chừa một thẻ tên phong cách.
Cách dùng (trong <loạt-bài>/lessons):python3 style_reel.py styles3 8 [--src 01] [--card 1.8] [--tail 0.6]
Đầu ra: <tên>/build/timings.json (B01…BNN, cue ten/nobody/fifty dịch chuyển theo) + <tên>/build/narration.wav.
Mỗi đoạn trong film.js: a = i*SEG, h = a+card (bắt đầu trình diễn), z = (i+1)*SEG; SEG = END / N."""
import copy, json, subprocess, sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
name, nseg = args[0], int(args[1])
SRC, CARD, TAILG = opt("--src", "01"), opt("--card", 1.8), opt("--tail", 0.6)
(Path(name) / "build").mkdir(parents=True, exist_ok=True); (Path(name) / "stills").mkdir(exist_ok=True)
src = json.load(open(f"{SRC}/build/timings.json", encoding="utf-8")); b = src["beats"]["B01"]
a0, a1 = max(0, b["start"] - 0.25), b["end"] + 0.3
SEG = CARD + (a1 - a0) + TAILG
beats = {}
for i in range(nseg):
    off = i * SEG + CARD - a0; nb = copy.deepcopy(b)
    nb["start"] = round(b["start"] + off, 3); nb["end"] = round(b["end"] + off, 3)
    if "chars" in nb: nb["chars"] = [round(c + off, 3) for c in nb["chars"]]
    nb["cues"] = {k: round(v + off, 3) for k, v in b["cues"].items()}
    for w in nb.get("words", []): w["start"] = round(w["start"] + off, 3); w["end"] = round(w["end"] + off, 3)
    beats[f"B{i+1:02d}"] = nb
out = {k: v for k, v in src.items() if k not in ("beats", "total")}; out.update(beats=beats, total=round(nseg * SEG, 3))
json.dump(out, open(f"{name}/build/timings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fc = f"[0:a]asplit={nseg}" + "".join(f"[i{i}]" for i in range(nseg)) + ";" + ";".join(
    f"[i{i}]atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,adelay={int(CARD*1000)}|{int(CARD*1000)},apad=pad_dur={TAILG}[s{i}]" for i in range(nseg)
) + ";" + "".join(f"[s{i}]" for i in range(nseg)) + f"concat=n={nseg}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/build/narration.wav", "-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{name}/build/narration.wav"], check=True)
c = b["cues"]
print(f"SEG {SEG:.2f}s  total {out['total']}s  mỗi đoạn: thẻ {CARD}s → trình diễn h; ten=h+{c['ten']-a0:.2f} nobody=h+{c['nobody']-a0:.2f} fifty=h+{c['fifty']-a0:.2f} lời dẫn dừng ở h+{a1-a0:.2f}")
