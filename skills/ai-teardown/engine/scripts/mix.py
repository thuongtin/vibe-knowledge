#!/usr/bin/env python3
"""Trộn âm: lời dẫn + nhạc nền (tự nhường khi có lời dẫn) + hiệu ứng âm thanh (căn theo đỉnh đo thực), chuẩn hoá độ lớn tổng thể.

Cách dùng: python3 scripts/mix.py <narration.wav> <cues.json> <out.wav> [--bgm file[,file2,...]] [--bgm-gain -22] [--lufs -14]
cues.json: {"duration": giây, "sfx": [{"t": giây, "name": "click", "gain": -12}]}
File hiệu ứng lấy từ thư viện hiệu ứng miễn phí dùng thương mại của promo-video; nhạc nền mặc định lấy từ kho nhạc Mixkit của nó.
"""
import json, subprocess, sys
from pathlib import Path

LIB = Path.home() / ".claude/skills/promo-video/assets"
PEAK = {"key-8": 0.092, "cut": 0.157, "paper-place-1": 0.046, "paper-place-2": 0.05, "swish-1": 0.039,
        "swish-2": 0.118, "swish-3": 0.062, "whoosh": 0.264, "riser": 1.198}

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

def main():
    narr, cues_p, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    cues = json.loads(cues_p.read_text(encoding="utf-8"))
    dur = float(cues["duration"])
    bgms = [Path(b) for b in arg("--bgm", str(LIB / "music/mixkit-132-hazy-after-hours.mp3")).split(",")]
    bgm_gain = float(arg("--bgm-gain", "-22"))
    lufs = float(arg("--lufs", "-14"))
    if len(bgms) > 1:
        # Nhiều bài nhạc nền: lần lượt crossfade nối thành một bản (bài học dài mà lặp một bài dễ nhàm)
        joined = out.with_suffix(".bgm.wav")
        ins = sum([["-i", str(b)] for b in bgms], [])
        chain, last = [], "[0:a]"
        for i in range(1, len(bgms)):
            nxt = f"[x{i}]" if i < len(bgms) - 1 else "[bgmcat]"
            chain.append(f"{last}[{i}:a]acrossfade=d=4:c1=tri:c2=tri{nxt}")
            last = nxt
        subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(chain), "-map", "[bgmcat]", "-ar", "48000", "-ac", "2", str(joined)], check=True)
        bgm = joined
    else:
        bgm = bgms[0]
    inputs = ["-i", str(narr), "-stream_loop", "-1", "-i", str(bgm)]
    f = [
        "[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[vo][key]",
        f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume={bgm_gain}dB,"
        f"afade=t=in:d=1.2,afade=t=out:st={max(0, dur - 1.8)}:d=1.8[bgm0]",
        # khi lời dẫn xuất hiện nhạc nền bị hạ khoảng 8 dB
        "[bgm0][key]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450:makeup=1[bgm]",
    ]
    mixes = ["[vo]", "[bgm]"]
    for i, c in enumerate(cues.get("sfx", [])):
        fn = LIB / "sfx" / f"{c['name']}.wav"
        if not fn.exists():
            print(f"Bỏ qua hiệu ứng bị thiếu {fn.name}", file=sys.stderr)
            continue
        start = max(0.0, c["t"] - PEAK.get(c["name"], 0.0))
        idx = 2 + len(mixes) - 2
        inputs += ["-i", str(fn)]
        f.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={c.get('gain', -14)}dB,"
                 f"adelay={int(start * 1000)}:all=1[s{i}]")
        mixes.append(f"[s{i}]")
    f.append(f"{''.join(mixes)}amix=inputs={len(mixes)}:normalize=0:duration=first,"
             f"apad=whole_dur={dur},atrim=0:{dur}[out]")
    pre = out.with_suffix(".pre.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(f), "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(pre)], check=True)
    # loudnorm hai lượt: đo trước, rồi chuẩn hoá tuyến tính theo giá trị đo (một lượt sẽ lệch hơn 1 LU)
    ln = f"loudnorm=I={lufs}:TP=-2.0:LRA=11"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(pre), "-af", f"{ln}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln2 = (f"{ln}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
           f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(pre), "-af", ln2, "-ar", "48000", "-ac", "2", str(out)], check=True)
    pre.unlink()
    if len(bgms) > 1:
        bgm.unlink()
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    summary = [l.strip() for l in r.stderr.splitlines() if l.strip().startswith(("I:", "Peak:", "LRA:"))]
    print(f"{len(mixes) - 2} hiệu ứng → {out}  ", " · ".join(summary[-3:]))

if __name__ == "__main__":
    main()
