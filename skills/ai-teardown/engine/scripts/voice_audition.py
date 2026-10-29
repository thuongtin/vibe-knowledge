#!/usr/bin/env python3
"""Nghe thử lồng tiếng: theo một danh sách giọng, dùng Google Gemini TTS đọc cùng một đoạn văn và tính vài chỉ số khách quan cho từng giọng.

Cách dùng: python3 scripts/voice_audition.py <voices.json> <thư mục đầu ra> [--ref id giọng tham chiếu]

voices.json:
{"text": "đoạn văn cần đọc",
 "voices": [
   {"id": "sulafat", "name": "Sulafat · giọng giảng bài", "voice": "Sulafat"},
   {"id": "gacrux", "name": "Gacrux", "model": "gemini-3.8-flash-tts", "voice": "Gacrux"}
 ]}
model mặc định gemini-3.8-flash-tts, director mặc định lấy từ tts_gemini.py ("{text}": chỉ gửi nguyên văn, vì gemini-3.8-flash-tts đọc to mọi chỉ dẫn). So sánh nhiều giọng có sẵn của Gemini (Sulafat, Gacrux, …) thì mỗi giọng một dòng.
Giọng đã tạo rồi (thư mục đầu ra có <id>.wav) thì không gọi lại.

Đầu ra: <id>.wav, <id>.mp3 (chuẩn hóa độ ồn), metrics.json:
  thời lượng, chữ/giây, trung vị tần số cơ bản (phân biệt giọng nam nữ), độ lên xuống ngữ điệu (độ lệch chuẩn theo nửa cung),
  độ tương đồng âm sắc với giọng tham chiếu (cosine similarity của phổ log-mel trung bình, dùng để kiểm tra giọng thiết kế có nhất quán giữa các lần tạo).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tts_gemini import DEFAULT_DIRECTOR, DEFAULT_MODEL, DEFAULT_VOICE, call as tts_call, env, to_wav  # noqa: E402


def pcm(path, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def f0_track(x, sr=16000, fmin=70, fmax=400, hop=160, win=640):
    out = []
    w = np.hanning(win)
    for i in range(0, len(x) - win, hop):
        fr = x[i:i + win] * w
        if np.sqrt(np.mean(fr ** 2)) < 0.02:
            continue
        ac = np.correlate(fr, fr, "full")[win - 1:]
        lo, hi = sr // fmax, sr // fmin
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / (ac[0] + 1e-9) > 0.45:
            out.append(sr / k)
    return np.array(out)


def mel_profile(x, sr=16000, n_fft=512, hop=160, n_mels=40):
    """Phổ log-mel trung bình của các khung có tiếng, dùng làm 'dấu vân tay giọng'"""
    frames = np.lib.stride_tricks.sliding_window_view(x, n_fft)[::hop] * np.hanning(n_fft)
    spec = np.abs(np.fft.rfft(frames, axis=1)) ** 2
    energy = spec.sum(1)
    spec = spec[energy > np.percentile(energy, 40)]
    mel = lambda f: 2595 * np.log10(1 + f / 700)
    pts = 700 * (10 ** (np.linspace(mel(80), mel(7600), n_mels + 2) / 2595) - 1)
    bins = np.floor((n_fft + 1) * pts / sr).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for m in range(1, n_mels + 1):
        a, b, c = bins[m - 1], bins[m], bins[m + 1]
        fb[m - 1, a:b] = (np.arange(a, b) - a) / max(1, b - a)
        fb[m - 1, b:c] = (c - np.arange(b, c)) / max(1, c - b)
    prof = np.log(spec @ fb.T + 1e-10).mean(0)
    return prof - prof.mean()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    key = env()
    text = spec["text"]
    for v in spec["voices"]:
        wav = out / f"{v['id']}.wav"
        if wav.exists():
            continue
        t0 = time.time()
        prompt = v.get("director", DEFAULT_DIRECTOR).replace("{text}", text)
        data, mime = tts_call(key, v.get("model", DEFAULT_MODEL), v.get("voice", DEFAULT_VOICE), prompt)
        to_wav(data, mime, wav)
        print(f"✓ {v['id']:18s} đã tổng hợp {time.time() - t0:4.1f}s")
    ref_id = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else None
    profs, metrics = {}, []
    n = len([c for c in text if not c.isspace() and c not in "，。！？；：、,.!?;:“”「」"])
    for v in spec["voices"]:
        wav = out / f"{v['id']}.wav"
        mp3 = out / f"{v['id']}.mp3"
        if not mp3.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "128k", str(mp3)], check=True)
        x = pcm(wav)
        f0 = f0_track(x)
        dur = len(x) / 16000
        profs[v["id"]] = mel_profile(x)
        metrics.append({"id": v["id"], "name": v.get("name", v["id"]), "dur": round(dur, 2), "cps": round(n / dur, 2),
                        "f0": int(np.median(f0)), "gender": "giọng nữ" if np.median(f0) > 165 else "giọng nam",
                        "range_st": round(float(np.std(12 * np.log2(f0 / np.median(f0)))), 2)})
    if ref_id:
        r = profs[ref_id]
        for m in metrics:
            p = profs[m["id"]]
            m["sim_to_ref"] = round(float(np.dot(p, r) / (np.linalg.norm(p) * np.linalg.norm(r))), 3)
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=1), encoding="utf-8")
    for m in metrics:
        print(f"{m['id']:18s} {m['gender']} tần số cơ bản {m['f0']:3d}Hz  lên xuống {m['range_st']:.2f} nửa cung  {m['cps']:.2f} chữ/giây" + (f"  giống tham chiếu {m['sim_to_ref']:.3f}" if ref_id else ""))


if __name__ == "__main__":
    main()
