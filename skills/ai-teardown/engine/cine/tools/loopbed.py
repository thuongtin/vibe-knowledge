#!/usr/bin/env python3
"""Bài trong kho nhạc phần lớn khoảng hai phút, một bài học bốn năm phút: nối dài bgm.wav đã được pick_music.py cắt sẵn bằng cách lặp theo ô nhịp.
Đoạn lặp bắt đầu từ ô nhịp thứ 8 sau điểm căn, kết thúc ở ô nhịp nguyên cuối cùng trước đoạn fade-out cuối bài; mối nối đặt trên vạch ô nhịp, dùng crossfade công suất đều dài một ô nhịp, lưới nhịp không đứt.
Cách dùng: python3 cine/tools/loopbed.py <bgm.wav> <đầu ra.wav> --seconds 340 --bpm 128.5 --anchor 7.44"""
import argparse
import math
import wave

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--seconds", type=float, required=True)
    ap.add_argument("--bpm", type=float, required=True)
    ap.add_argument("--anchor", type=float, required=True, help="--hit-at của pick_music.py: thời điểm này là vạch ô nhịp")
    a = ap.parse_args()
    with wave.open(a.src, "rb") as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).astype(np.float64)
    dur = len(x) / sr
    n = int(a.seconds * sr)
    if dur >= a.seconds:
        y = x[:n]
    else:
        bar = 4 * 60 / a.bpm
        ls = a.anchor + 8 * bar
        le = a.anchor + math.floor((dur - 4.0 - a.anchor) / bar) * bar     # tránh đoạn fade-out cuối bài
        if le - ls < 4 * bar:
            raise SystemExit("Bài quá ngắn, không gom được đoạn lặp từ 4 ô nhịp trở lên")
        xf = int(bar * sr)
        k = np.linspace(0, np.pi / 2, xf)[:, None]
        fin, fout = np.sin(k), np.cos(k)
        y = np.zeros((n + len(x), ch))
        first = x[: int(le * sr) + xf].copy()
        first[-xf:] *= fout
        y[: len(first)] += first
        body = x[int(ls * sr): int(le * sr) + xf]
        pos, step = int(le * sr), int(le * sr) - int(ls * sr)
        while pos < n:
            seg = body.copy()
            seg[:xf] *= fin
            seg[-xf:] *= fout
            y[pos: pos + len(seg)] += seg
            pos += step
        y = y[:n]
        print(f"Đoạn lặp {ls:.2f}–{le:.2f}s ({(le - ls) / bar:.0f} ô nhịp), nối thành {a.seconds:.1f}s")
    m = int(2.0 * sr)
    y[-m:] *= np.linspace(1, 0, m)[:, None]
    with wave.open(a.out, "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.clip(np.round(y), -32768, 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()
