#!/usr/bin/env python3
"""Lồng tiếng và căn chỉnh: tổng hợp giọng từng beat, lấy mốc thời gian mức từ, quy đổi các đánh dấu [[cue]] trong lời dẫn thành thời điểm.

Cách dùng:
    python3 scripts/tts.py <narration.json hoặc lesson.json> <thư mục đầu ra> [--gap 0.35] [--lead 0.4] [--lexicon lexicon.json] [--rate -10%]

Đầu vào (chọn một trong hai):
    lesson.json (đọc meta.voice và beats[].narration)
    hoặc {"voice": {"id": "...", "rate": "-10%"}, "lexicon": {...}, "beats": [{"id": "B001", "narration": "..."}]}
Từ điển cách đọc: {"văn gốc": "cách viết để TTS đọc"}, chỉ ảnh hưởng phát âm, mốc thời gian vẫn quy về văn gốc.

Đầu ra:
    <out>/audio/<beat>.mp3            lồng tiếng từng đoạn
    <out>/narration.wav               toàn bộ lời dẫn nối theo gap (48 kHz đơn âm)
    <out>/timings.json                điểm đầu/cuối của từng đoạn, thời gian từng từ (kèm khoảng ký tự trong văn gốc), thời điểm cue, tất cả đều là giây tuyệt đối
"""
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

CUE_RE = re.compile(r"\[\[([a-z][a-z0-9_-]*)\]\]")


def strip_cues(text):
    """Bỏ [[cue]], trả về (văn bản sạch, {cue: vị trí ký tự trong văn bản sạch})."""
    out, cues, pos = [], {}, 0
    for m in CUE_RE.finditer(text):
        out.append(text[pos:m.start()])
        cues[m.group(1)] = sum(len(p) for p in out)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), cues


def apply_lexicon(text, lexicon):
    """Thay cách phát âm theo từ điển; trả về (văn bản TTS, bảng ánh xạ), bảng ánh xạ đưa từng ký tự của văn bản TTS về vị trí trong văn gốc."""
    if not lexicon:
        return text, list(range(len(text) + 1))
    keys = sorted(lexicon, key=len, reverse=True)
    pat = re.compile("|".join(re.escape(k) for k in keys))
    tts, back, pos = [], [], 0
    for m in pat.finditer(text):
        for i in range(pos, m.start()):
            tts.append(text[i])
            back.append(i)
        rep = lexicon[m.group(0)]
        for j, ch in enumerate(rep):
            tts.append(ch)
            back.append(m.start() + min(j, len(m.group(0)) - 1))
        pos = m.end()
    for i in range(pos, len(text)):
        tts.append(text[i])
        back.append(i)
    back.append(len(text))
    return "".join(tts), back


async def synth_once(text, voice, rate):
    c = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    audio, words = bytearray(), []
    async for ch in c.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            words.append({"text": ch["text"], "start": ch["offset"] / 1e7, "end": (ch["offset"] + ch["duration"]) / 1e7})
    return bytes(audio), words


async def synth(text, voice, rate, tries=4):
    """edge-tts thỉnh thoảng gặp NoAudioReceived / mất kết nối, thử lại với độ lùi theo cấp số mũ."""
    for k in range(tries):
        try:
            return await synth_once(text, voice, rate)
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            print(f"  Thử lại {k + 1}: {type(e).__name__}", file=sys.stderr)
            await asyncio.sleep(1.5 * 2 ** k)


def locate(words, tts_text, back):
    """Định vị từng từ theo thứ tự vào văn bản TTS, rồi ánh xạ ngược về khoảng ký tự trong văn gốc."""
    i = 0
    for w in words:
        k = tts_text.find(w["text"], i)
        if k < 0:  # khi không tìm thấy thì lùi về nối ngay sau từ trước
            k = i
        w["i0"], w["i1"] = back[k], back[min(k + len(w["text"]), len(back) - 1)]
        i = k + len(w["text"])
    return words


def probe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    gap = float(sys.argv[sys.argv.index("--gap") + 1]) if "--gap" in sys.argv else 0.35
    lead = float(sys.argv[sys.argv.index("--lead") + 1]) if "--lead" in sys.argv else 0.4
    data = json.loads(src.read_text(encoding="utf-8"))
    if "meta" in data:  # lesson.json: từ điển cách đọc và tốc độ nói truyền từ dòng lệnh (bản thân lesson không chứa chi tiết phát âm)
        voice = {"id": data["meta"]["voice"], "rate": sys.argv[sys.argv.index("--rate") + 1] if "--rate" in sys.argv else "-10%"}
        lexicon = json.loads(Path(sys.argv[sys.argv.index("--lexicon") + 1]).read_text(encoding="utf-8")) if "--lexicon" in sys.argv else {}
    else:
        voice, lexicon = data["voice"], data.get("lexicon", {})
    (out / "audio").mkdir(parents=True, exist_ok=True)

    timings, t, parts = {"voice": voice, "beats": {}}, lead, []
    for b in data["beats"]:
        clean, cue_pos = strip_cues(b["narration"])
        tts_text, back = apply_lexicon(clean, lexicon)
        mp3 = out / "audio" / f"{b['id']}.mp3"
        audio, words = asyncio.run(synth(tts_text, voice["id"], voice.get("rate", "-10%")))
        mp3.write_bytes(audio)
        dur = probe_duration(mp3)
        locate(words, tts_text, back)
        for w in words:
            w["start"], w["end"] = round(t + w["start"], 3), round(t + w["end"], 3)
        cues = {}
        for name, k in cue_pos.items():
            nxt = next((w for w in words if w["i0"] >= k), None)
            cues[name] = nxt["start"] if nxt else round(t + dur, 3)
        timings["beats"][b["id"]] = {
            "file": f"audio/{b['id']}.mp3", "text": clean,
            "start": round(t, 3), "end": round(t + dur, 3), "duration": round(dur, 3),
            "words": words, "cues": cues,
        }
        parts.append((mp3, t))
        print(f"{b['id']}  {dur:5.2f}s  {len(clean):3d} chữ  cues={list(cues)}")
        t += dur + max(gap, b.get("gap", 0), b.get("min_hold_s", 0))
    total = round(t - gap + lead, 3)
    timings["total"] = total

    # Nối thành một lời dẫn: mỗi đoạn đặt theo điểm bắt đầu tuyệt đối
    inputs, filters = [], []
    for i, (mp3, start) in enumerate(parts):
        inputs += ["-i", str(mp3)]
        filters.append(f"[{i}:a]aresample=48000,adelay={int(start * 1000)}:all=1[a{i}]")
    mixin = "".join(f"[a{i}]" for i in range(len(parts)))
    filters.append(f"{mixin}amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total},atrim=0:{total}[out]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
                    "-map", "[out]", "-ac", "1", "-ar", "48000", str(out / "narration.wav")], check=True)
    (out / "timings.json").write_text(json.dumps(timings, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Tổng cộng {total:.2f}s → {out / 'timings.json'}")


if __name__ == "__main__":
    main()
