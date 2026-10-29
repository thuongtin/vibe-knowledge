#!/usr/bin/env python3
"""Lồng tiếng (Xiaomi MiMo TTS) + căn từng chữ (whisper.cpp trên máy) + kiểm tra đọc lại (MiMo ASR).

Cách dùng:
    python3 scripts/tts_mimo.py <narration.json> <thư-mục-đầu-ra> [--gap 0.8] [--lead 0.6] [--voice 茉莉] [--style "…"] [--clone mau.wav] [--qa] [--reuse] [--jobs 3]

narration.json giống với tts.py: {"voice": {...}, "lexicon": {...}, "beats": [{"id", "narration"}]}, trong lời dẫn dùng [[cue]] để đánh dấu thời điểm.
Trong voice có thể viết {"engine": "mimo", "model": "mimo-v2.5-tts", "voice": "茉莉", "style": "mô tả giọng điệu giảng bài"}; tham số dòng lệnh được ưu tiên.
Nhân bản giọng: {"engine": "mimo", "clone": "ban_ghi_mau.wav", "style": "…"} hoặc --clone. Cả khóa dùng cùng một bản ghi mẫu, mỗi nhịp nghe đều như cùng một người.
Khóa API đọc từ biến môi trường MIMO_API_KEY / MIMO_BASE_URL, hoặc từ ~/.config/ai-teardown/mimo.env, không ghi vào bất kỳ file dự án nào.

MiMo không trả về thời gian từng từ, nên mỗi nhịp được tổng hợp nguyên đoạn (ngữ điệu tự nhiên), rồi dùng whisper.cpp lấy thời gian từng chữ, căn theo ký tự về văn bản gốc.
Đầu ra giống tts.py: <out>/audio/<beat>.mp3, <out>/narration.wav, <out>/timings.json;
Trong timings, words của mỗi nhịp là {text, start, end, i0, i1} từng chữ, ngoài ra có chars (thời điểm bắt đầu của từng chữ), cues tính bằng giây tuyệt đối.
--qa: mỗi nhịp dùng MiMo ASR phiên âm một lần, so với văn bản gốc, báo ra chỗ đọc sai.
--jobs: số nhịp tổng hợp đồng thời (mặc định 3; MiMo gửi liên tục quá nhiều sẽ bị 429, script tự động lùi thời gian chờ).
--reuse: audio/<beat>.wav đã có thì không tổng hợp lại, chỉ căn lại (dùng khi sửa logic căn).
Mặc định cũng tái sử dụng: khi giọng, ngữ khí, văn bản của cùng một nhịp đều không đổi thì dùng luôn bản ghi lần trước (audio/<beat>.key lưu dấu vân tay).
"""
import base64
import codecs
import hashlib
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CUE_RE = re.compile(r"\[\[([a-z][a-z0-9_-]*)\]\]")
PUNCT = set("，。！？；：、,.!?;:（）()「」『』“”\"'《》…—- 　")
# Mô hình whisper dùng để căn: small nhanh hơn medium hơn gấp đôi, tỷ lệ căn chỉ thấp hơn một hai điểm; nhịp nào căn không được thì dùng medium bổ sung
WHISPER_SMALL = Path.home() / "Library/Application Support/Memo/models/ggml-small.bin"
WHISPER_MODEL = Path.home() / "Library/Application Support/Murmur/models/ggml-medium-q5_0.bin"
DEFAULT_STYLE = "像老师给学生讲一个有意思的小故事：亲切、自然、带一点好奇，语速适中，句子之间自然停顿。"


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def env():
    key, base = os.environ.get("MIMO_API_KEY"), os.environ.get("MIMO_BASE_URL")
    f = Path.home() / ".config/ai-teardown/mimo.env"
    if (not key or not base) and f.exists():
        for line in f.read_text().splitlines():
            k, _, v = line.partition("=")
            if k == "MIMO_API_KEY" and not key:
                key = v.strip()
            if k == "MIMO_BASE_URL" and not base:
                base = v.strip()
    if not key:
        sys.exit("Thiếu MIMO_API_KEY (biến môi trường hoặc ~/.config/ai-teardown/mimo.env)")
    return key, base or "https://api.xiaomimimo.com/v1"


import threading
_GATE = threading.Lock()
_LAST = [0.0]
MIN_GAP = 4.0  # Giữa hai lần bắt đầu yêu cầu cách nhau ít nhất mấy giây: MiMo giới hạn tốc độ khi gửi liên tục (429)


def call(key, base, body, tries=10):
    last = ""
    for k in range(tries):
        with _GATE:  # Điều tiết toàn cục: các luồng song song cũng xếp hàng gửi yêu cầu
            wait = _LAST[0] + MIN_GAP - time.time()
            if wait > 0:
                time.sleep(wait)
            _LAST[0] = time.time()
        r = subprocess.run(["curl", "-sS", "--max-time", "240", "-X", "POST", f"{base}/chat/completions",
                            "-H", f"Authorization: Bearer {key}", "-H", "Content-Type: application/json",
                            "--data-binary", "@-"], input=json.dumps(body, ensure_ascii=False), capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            if "choices" in d:
                return d
            last = str(d.get("error"))
        except Exception:  # noqa: BLE001
            last = (r.stdout or r.stderr)[:200]
        wait = min(60, 12 * (k + 1)) if "429" in last else 2 * (k + 1)  # MiMo bị giới hạn tốc độ khi gửi liên tục
        print(f"  thử lại lần {k + 1} sau {wait}s: {last}", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"Gọi MiMo thất bại: {last}")


def strip_cues(text):
    out, cues, pos = [], {}, 0
    for m in CUE_RE.finditer(text):
        out.append(text[pos:m.start()])
        cues[m.group(1)] = sum(len(p) for p in out)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), cues


# Từ viết tắt in hoa chỉ gồm chữ cái số La Mã, MiMo sẽ đọc như số La Mã: CLI→151, MD→1500, CC→200, LM→950. Tách thành từng chữ cái thì sẽ đọc từng chữ
ROMANISH = re.compile(r"(?<![A-Za-z])[IVXLCDM]{2,4}(?![A-Za-z])")


def apply_lexicon(text, lexicon):
    for k in sorted(lexicon or {}, key=len, reverse=True):
        text = text.replace(k, lexicon[k])
    return text if LANG == "en" else ROMANISH.sub(lambda m: " ".join(m.group(0)), text)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


LANG = "zh"   # voice.lang của narration.json; "en" = bài học tiếng Anh


def whisper_chars(wav, prompt="", model=None):
    """whisper.cpp thời gian từng token → thời gian từng chữ (token có thể bị cắt giữa ký tự đa byte, dùng giải mã tăng dần để ghép lại).
    prompt đưa văn bản gốc: để whisper dùng chữ giản thể, theo cách viết của văn bản gốc, tỷ lệ căn cao hơn nhiều."""
    with tempfile.TemporaryDirectory() as td:
        w16 = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(w16)], check=True)
        subprocess.run(["whisper-cli", "-m", str(model or WHISPER_MODEL), "-l", LANG, "-f", str(w16), "-ojf", "-of", str(Path(td) / "o"), "-np",
                        "--prompt", prompt or ("以下是普通话的句子。" if LANG == "zh" else "An English sentence.")],
                       capture_output=True, check=True)
        d = json.loads((Path(td) / "o.json").read_bytes().decode("utf-8", "surrogateescape"))
    dec = codecs.getincrementaldecoder("utf-8")(errors="ignore")
    out = []
    for seg in d["transcription"]:
        for tk in seg.get("tokens", []):
            t = tk["text"]
            if t.startswith("[_") or t.startswith("<|"):
                continue
            for ch in dec.decode(t.encode("utf-8", "surrogateescape")):
                if not ch.isspace():
                    out.append((ch, tk["offsets"]["from"] / 1000, tk["offsets"]["to"] / 1000))
    return out


def norm(ch):
    return ch.lower()


def align(text, wch, dur):
    """Thời điểm bắt đầu của từng chữ trong văn bản gốc (tương đối so với nhịp này). Chữ khớp được thì dùng thời gian whisper, không khớp thì nội suy theo vị trí giữa các điểm đã biết trước và sau."""
    idx = [i for i, c in enumerate(text) if c not in PUNCT and not c.isspace()]
    a = [norm(text[i]) for i in idx]
    b = [norm(c) for c, _, _ in wch if c not in PUNCT]
    bt = [t0 for c, t0, _ in wch if c not in PUNCT]
    known = {}
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            known[blk.a + k] = bt[blk.b + k]
    # Đơn điệu hóa: thỉnh thoảng whisper nhảy lùi
    last = 0.0
    for k in sorted(known):
        known[k] = max(known[k], last)
        last = known[k]
    anchors = [(-1, 0.0)] + sorted(known.items()) + [(len(a), dur)]
    times = [0.0] * len(a)
    for (k0, t0), (k1, t1) in zip(anchors, anchors[1:]):
        for k in range(k0 + 1, k1):
            times[k] = t0 + (t1 - t0) * (k - k0) / (k1 - k0)
        if 0 <= k1 < len(a):
            times[k1] = t1
    start = [0.0] * len(text)
    j = 0
    for i, c in enumerate(text):
        if j < len(idx) and idx[j] == i:
            start[i] = times[j]
            j += 1
        else:  # Dấu câu, khoảng trắng: đi theo sau chữ đứng trước
            start[i] = start[i - 1] if i else 0.0
    return start, len(known) / max(1, len(a))


def asr(key, base, wav):
    b64 = base64.b64encode(Path(wav).read_bytes()).decode()
    d = call(key, base, {"model": "mimo-v2.5-asr", "messages": [{"role": "user", "content": [{"type": "input_audio", "input_audio": {"data": b64, "format": "wav"}}]}]})
    return d["choices"][0]["message"]["content"] or ""


CN_NUM = str.maketrans("零〇一二三四五六七八九", "00123456789")


def qa_diff(text, heard):
    """So sánh đọc lại: bỏ dấu câu, thống nhất cách viết số rồi so, trả về (độ tương đồng, các đoạn khác biệt)"""
    f = lambda s: [c for c in s.lower().translate(CN_NUM) if c not in PUNCT and not c.isspace()]
    a, b = f(text), f(heard.replace("做", "作"))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = [("".join(a[i1:i2]), "".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    return sm.ratio(), diffs


def cn_value(tok):
    """\"六万三千八百四十\" → 63840; chuỗi toàn chữ số (kể cả kiểu đọc từng chữ số như \"一五五\") ghép theo từng chữ số; không nhận ra thì trả về None"""
    t = tok.translate(CN_NUM)
    if t.isdigit():
        return int(t)
    total, sec, num = 0, 0, 0
    for c in t:
        if c.isdigit():
            num = int(c)
        elif c in "十百千":
            sec += (num or 1) * {"十": 10, "百": 100, "千": 1000}[c]; num = 0
        elif c == "万":
            total += (sec + num) * 10000; sec = num = 0
    return total + sec + num


def odd_numbers(text, heard):
    """Con số xuất hiện trong bản đọc lại mà văn bản gốc không có = phần lớn là đọc sai (ví dụ CLI bị đọc như số La Mã thành \"一百五十一\", AGENTS.MD thành \"一千五百\")"""
    src = {int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", text)}
    src |= {v for x in re.findall(r"[零〇一二三四五六七八九十百千万]+", text) if (v := cn_value(x)) is not None}
    bad = []
    for m in re.finditer(r"[0-9零〇一二三四五六七八九十百千万]{2,}", heard):
        v = cn_value(m.group(0))
        if v is not None and v not in src and v >= 100:
            bad.append(m.group(0))
    return bad


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    gap = float(arg("--gap", 0.8))
    lead = float(arg("--lead", 0.6))
    jobs = int(arg("--jobs", 3))
    data = json.loads(src.read_text(encoding="utf-8"))
    vcfg = data.get("voice", {}) if data.get("voice", {}).get("engine") == "mimo" else {}
    global LANG
    LANG = data.get("voice", {}).get("lang", "zh")
    model = arg("--model", vcfg.get("model", "mimo-v2.5-tts"))
    voice = arg("--voice", vcfg.get("voice", "茉莉"))
    style = arg("--style", vcfg.get("style", DEFAULT_STYLE))
    clone = arg("--clone", vcfg.get("clone"))
    ref_digest = None
    if clone:
        ref = Path(clone) if Path(clone).is_absolute() else (src.parent / clone)
        model = "mimo-v2.5-tts-voiceclone"
        clone_url = "data:audio/wav;base64," + base64.b64encode(ref.read_bytes()).decode()
        ref_digest = hashlib.md5(ref.read_bytes()).hexdigest()
    lexicon = data.get("lexicon", {})
    key, base = env()
    (out / "audio").mkdir(parents=True, exist_ok=True)
    t_start = time.time()

    # Chuẩn bị cho từng nhịp: văn bản, vị trí cue, nội dung yêu cầu, dấu vân tay bộ nhớ đệm
    jobs_list = []
    for b in data["beats"]:
        clean, cue_pos = strip_cues(b["narration"])
        say = apply_lexicon(clean, lexicon)
        msgs = ([{"role": "user", "content": style}] if style else []) + [{"role": "assistant", "content": say}]
        if clone:
            body = {"model": model, "messages": msgs, "audio": {"format": "wav", "voice": clone_url}}
        else:
            body = {"model": model, "messages": msgs, "audio": {"format": "wav", **({"voice": voice} if voice and "voicedesign" not in model else {})}}
        digest = hashlib.md5(json.dumps([model, ref_digest or voice, style, say], ensure_ascii=False).encode()).hexdigest()
        jobs_list.append({"b": b, "clean": clean, "cue_pos": cue_pos, "body": body, "digest": digest,
                          "wav": out / "audio" / f"{b['id']}.wav", "mp3": out / "audio" / f"{b['id']}.mp3", "meta": out / "audio" / f"{b['id']}.key"})

    # Bước một (song song): tổng hợp. Nhịp nào giọng, ngữ khí, văn bản đều không đổi thì dùng luôn bản ghi lần trước
    def synth(j):
        t0 = time.time()
        reuse = j["wav"].exists() and ("--reuse" in sys.argv or (j["meta"].exists() and j["meta"].read_text() == j["digest"]))
        if not reuse:
            d = call(key, base, j["body"])
            raw = j["wav"].with_suffix(".raw.wav")
            raw.write_bytes(base64.b64decode(d["choices"][0]["message"]["audio"]["data"]))
            # Cắt khoảng lặng đầu cuối, nhịp điệu do gap điều khiển
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse",
                            "-ar", "48000", "-ac", "1", str(j["wav"])], check=True)
            raw.unlink()
            j["meta"].write_text(j["digest"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(j["wav"]), "-b:a", "160k", str(j["mp3"])], check=True)
        j["dur"], j["reused"], j["synth_s"] = probe(j["wav"]), reuse, time.time() - t0

    # Bước hai (song song): căn từng chữ; dùng prompt ngắn trước, căn không được thì dùng prompt toàn văn (prompt toàn văn đôi khi làm whisper bỏ qua một đoạn)
    def align_one(j):
        clean = j["clean"]
        terms = "、".join(dict.fromkeys(re.findall(r"[A-Za-z][A-Za-z0-9.\-]*|《[^》]+》", clean)))
        short = ("以下是普通话，用简体中文。" + (f"会提到：{terms}。" if terms else "")) if LANG == "zh" else (f"Terms: {terms}." if terms else "")
        tries = [(short, WHISPER_SMALL if WHISPER_SMALL.exists() else None), (short, WHISPER_MODEL), (clean, WHISPER_MODEL)]
        rel, cover = None, -1
        for prompt, model in tries:
            r2, c2 = align(clean, whisper_chars(j["wav"], prompt, model), j["dur"])
            if c2 > cover:
                rel, cover = r2, c2
            if cover >= 0.9:
                break
        j["rel"], j["cover"] = rel, cover
        if "--qa" in sys.argv:
            heard = asr(key, base, j["wav"])
            j["qa"] = (heard, *qa_diff(clean, heard))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(synth, jobs_list))
    with ThreadPoolExecutor(2) as ex:  # Chạy nhiều whisper cùng lúc sẽ tranh GPU, ngược lại còn chậm hơn
        list(ex.map(align_one, jobs_list))

    # Bước ba (tuần tự): xếp thời gian tuyệt đối theo độ dài
    timings = {"voice": {"engine": "mimo", "model": model, "voice": None if clone else voice, "clone": str(clone) if clone else None, "style": style}, "beats": {}}
    t, parts, report = lead, [], []
    for j in jobs_list:
        b, clean, dur = j["b"], j["clean"], j["dur"]
        starts = [round(t + x, 3) for x in j["rel"]]
        words = []
        if LANG == "en":   # Tiếng Anh theo từ: mỗi từ một khoảng thời gian (phụ đề ngắt dòng theo từ, nhân vật nhép miệng theo từ)
            import re as _re
            for m in _re.finditer(r"[A-Za-z0-9](?:[A-Za-z0-9'’\-]|\.(?=[A-Za-z0-9]))*", clean):
                i, i1 = m.start(), m.end()
                nxt = next((starts[k] for k in range(i1, len(clean)) if starts[k] > starts[i] and clean[k].isalnum()), round(t + dur, 3))
                words.append({"text": m.group(0), "start": starts[i], "end": min(nxt, round(t + dur, 3)), "i0": i, "i1": i1})
        for i, ch in enumerate(clean if LANG == "zh" else ""):
            if ch.isspace() or ch in PUNCT:
                continue
            nxt = next((starts[k] for k in range(i + 1, len(clean)) if starts[k] > starts[i]), round(t + dur, 3))
            words.append({"text": ch, "start": starts[i], "end": min(nxt, round(t + dur, 3)), "i0": i, "i1": i + 1})
        cues = {name: next((w["start"] for w in words if w["i0"] >= k and clean[w["i0"]] not in PUNCT), round(t + dur, 3)) for name, k in j["cue_pos"].items()}
        timings["beats"][b["id"]] = {"file": f"audio/{b['id']}.mp3", "text": clean, "start": round(t, 3), "end": round(t + dur, 3),
                                     "duration": round(dur, 3), "words": words, "chars": starts, "cues": cues, "align": round(j["cover"], 3)}
        status = "dùng lại" if j["reused"] else f"tổng hợp {j['synth_s']:.1f}s"
        line = f"{b['id']}  {dur:5.2f}s  {len(clean):3d} chữ  {len(clean) / dur:.2f} chữ/giây  căn {j['cover']:.0%}  {status}"
        if "qa" in j:
            heard, ratio, diffs = j["qa"]
            odd = odd_numbers(clean, heard)
            line += f"  đọc lại {ratio:.0%}" + (f"  khác biệt {diffs[:4]}" if diffs else "") + (f"  ⚠ số đọc đáng ngờ {odd}" if odd else "")
            report.append({"beat": b["id"], "heard": heard, "ratio": round(ratio, 3), "diffs": diffs, **({"odd_numbers": odd} if odd else {})})
        print(line)
        parts.append((j["mp3"], t))
        t += dur + max(gap, b.get("gap", 0), b.get("min_hold_s", 0))
    total = round(t - gap + lead, 3)
    timings["total"] = total

    inputs, filters = [], []
    for i, (mp3, start) in enumerate(parts):
        inputs += ["-i", str(mp3)]
        filters.append(f"[{i}:a]aresample=48000,adelay={int(start * 1000)}:all=1[a{i}]")
    mixin = "".join(f"[a{i}]" for i in range(len(parts)))
    filters.append(f"{mixin}amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total},atrim=0:{total}[out]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
                    "-map", "[out]", "-ac", "1", "-ar", "48000", str(out / "narration.wav")], check=True)
    (out / "timings.json").write_text(json.dumps(timings, ensure_ascii=False, indent=1), encoding="utf-8")
    if report:
        (out / "qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    odd = [r["beat"] for r in report if r.get("odd_numbers")]
    if odd:
        print(f"⚠ Các nhịp này khi đọc lại xuất hiện con số mà văn bản gốc không có, hãy nghe thử trước: {', '.join(odd)} (khi từ viết tắt bị đọc như số La Mã, hãy tách thành từng chữ cái trong lexicon)")
    print(f"Tổng cộng {total:.2f}s → {out / 'timings.json'} (mất {time.time() - t_start:.0f}s, song song {jobs})")


if __name__ == "__main__":
    main()
