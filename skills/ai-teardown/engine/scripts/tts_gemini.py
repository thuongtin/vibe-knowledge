#!/usr/bin/env python3
"""Lồng tiếng (Google Gemini TTS) + căn từng chữ (whisper.cpp trên máy) + kiểm tra đọc lại (whisper.cpp).

Cách dùng:
    python3 scripts/tts_gemini.py <narration.json> <thư-mục-đầu-ra> [--gap 0.8] [--lead 0.6] [--voice Sulafat] [--model gemini-3.8-flash-tts] [--director "…{text}"] [--qa] [--reuse] [--jobs 3]

narration.json: {"voice": {...}, "lexicon": {...}, "beats": [{"id", "narration"}]}, trong lời dẫn dùng [[cue]] để đánh dấu thời điểm.
Trong voice có thể viết {"engine": "gemini", "model": "gemini-3.8-flash-tts", "voice": "Sulafat", "lang": "vi", "director": "chỉ dẫn diễn đọc bằng tiếng Anh, có chỗ giữ {text}"}; tham số dòng lệnh được ưu tiên.
Mặc định: model gemini-3.8-flash-tts, giọng Sulafat, lang "vi" (tiếng Việt, căn theo từ). lang "en" cũng căn theo từ; lang "zh" căn theo từng chữ Hán.
Gemini không có nhân bản giọng: muốn đổi giọng thì đổi `voice` (tên giọng có sẵn của Gemini) và sửa `director`.
Khóa API đọc từ biến môi trường GOOGLE_API_KEY (hoặc GEMINI_API_KEY), hoặc từ ~/.config/ai-teardown/gemini.env, không ghi vào bất kỳ file dự án nào, không in ra.

Gemini không trả về thời gian từng từ, nên mỗi nhịp được tổng hợp nguyên đoạn (ngữ điệu tự nhiên), rồi dùng whisper.cpp lấy thời gian từng chữ, căn theo ký tự về văn bản gốc.
Đầu ra: <out>/audio/<beat>.mp3, <out>/narration.wav, <out>/timings.json;
Trong timings, words của mỗi nhịp là {text, start, end, i0, i1} (từng từ với vi/en, từng chữ với zh), ngoài ra có chars (thời điểm bắt đầu của từng ký tự), cues tính bằng giây tuyệt đối.
--qa: mỗi nhịp dùng whisper.cpp phiên âm lại, so với văn bản gốc, báo ra chỗ đọc sai (Gemini thỉnh thoảng đọc thừa, lặp hoặc bỏ sót từ).
--jobs: số nhịp tổng hợp đồng thời (mặc định 3; bị 429 thì script tự động lùi thời gian chờ).
--reuse: audio/<beat>.wav đã có thì không tổng hợp lại, chỉ căn lại (dùng khi sửa logic căn).
Mặc định cũng tái sử dụng: khi model, giọng, chỉ dẫn, văn bản của cùng một nhịp đều không đổi thì dùng luôn bản ghi lần trước (audio/<beat>.key lưu dấu vân tay).
"""
import base64
import codecs
import hashlib
import difflib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
import wave
from pathlib import Path

CUE_RE = re.compile(r"\[\[([a-z][a-z0-9_-]*)\]\]")
PUNCT = set("，。！？；：、,.!?;:（）()「」『』“”\"'《》…—- 　")
# Mô hình whisper dùng để căn: small nhanh hơn medium hơn gấp đôi, tỷ lệ căn chỉ thấp hơn một hai điểm; nhịp nào căn không được thì dùng medium bổ sung
WHISPER_SMALL = Path.home() / "Library/Application Support/Memo/models/ggml-small.bin"
WHISPER_MODEL = Path.home() / "Library/Application Support/Murmur/models/ggml-medium-q5_0.bin"
DEFAULT_MODEL = "gemini-3.8-flash-tts"
DEFAULT_VOICE = "Sulafat"
TTS_URL = "https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent?key={key}"
# Chỉ dẫn diễn đọc bằng tiếng Anh (Gemini TTS nghe theo chỉ dẫn tiếng Anh ổn định nhất), {text} là lời dẫn của nhịp
DEFAULT_DIRECTOR = ("Read the following Vietnamese narration like a teacher telling students an interesting little story: friendly, natural, "
                    "a touch of curiosity, moderate pace, with natural pauses between sentences. Do not add or skip any word.\n\n{text}")
WORD_LANGS = ("vi", "en")   # căn theo từ; các ngôn ngữ khác (zh) căn theo từng chữ


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def env():
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    f = Path.home() / ".config/ai-teardown/gemini.env"
    if not key and f.exists():
        for line in f.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip() in ("GOOGLE_API_KEY", "GEMINI_API_KEY") and v.strip():
                key = v.strip().strip("\"'")
                break
    if not key:
        sys.exit("Thiếu GOOGLE_API_KEY (biến môi trường hoặc ~/.config/ai-teardown/gemini.env)")
    return key


import threading
_GATE = threading.Lock()
_LAST = [0.0]
MIN_GAP = 1.0  # Giữa hai lần bắt đầu yêu cầu cách nhau ít nhất mấy giây, tránh bị giới hạn tốc độ (429)


def call(key, model, voice, text, tries=8):
    """Một yêu cầu TTS → (mẫu âm thanh PCM int16 dạng bytes, tần số lấy mẫu). Địa chỉ yêu cầu có chứa khóa nên không bao giờ in ra."""
    body = {"contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    last = ""
    for k in range(tries):
        with _GATE:  # Điều tiết toàn cục: các luồng song song cũng xếp hàng gửi yêu cầu
            wait = _LAST[0] + MIN_GAP - time.time()
            if wait > 0:
                time.sleep(wait)
            _LAST[0] = time.time()
        req = urllib.request.Request(TTS_URL.format(model=model, key=key), data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        wait = 2 * (k + 1)
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
            part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"]), part.get("mimeType", "")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}"
            if e.code not in (429, 500, 503):
                break
            wait = min(60, 10 * (k + 1)) if e.code == 429 else 6 * (k + 1)
        except (KeyError, IndexError, ValueError, urllib.error.URLError, TimeoutError) as e:
            last = type(e).__name__ + (" (không có âm thanh trong phản hồi, có thể bị chặn nội dung)" if isinstance(e, (KeyError, IndexError)) else "")
        print(f"  thử lại lần {k + 1} sau {wait}s: {last}", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"Gọi Gemini TTS thất bại: {last}")


def to_wav(data, mime, dest):
    """Gemini trả về PCM thô (audio/L16;rate=24000) hoặc một tệp âm thanh có đầu tệp; ghi ra WAV."""
    if "L16" in mime or "pcm" in mime.lower():
        m = re.search(r"rate=(\d+)", mime)
        with wave.open(str(dest), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(int(m.group(1)) if m else 24000)
            w.writeframes(data)
    else:
        Path(dest).write_bytes(data)


def strip_cues(text):
    out, cues, pos = [], {}, 0
    for m in CUE_RE.finditer(text):
        out.append(text[pos:m.start()])
        cues[m.group(1)] = sum(len(p) for p in out)
        pos = m.end()
    out.append(text[pos:])
    return unicodedata.normalize("NFC", "".join(out)), cues


def apply_lexicon(text, lexicon):
    for k in sorted(lexicon or {}, key=len, reverse=True):
        text = text.replace(k, lexicon[k])
    return text


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


LANG = "vi"   # voice.lang của narration.json; "vi" = tiếng Việt (mặc định), "en" = tiếng Anh, "zh" = tiếng Trung


def whisper_chars(wav, prompt="", model=None):
    """whisper.cpp thời gian từng token → thời gian từng chữ (token có thể bị cắt giữa ký tự đa byte, dùng giải mã tăng dần để ghép lại).
    prompt đưa văn bản gốc / thuật ngữ: để whisper viết theo cách viết của văn bản gốc, tỷ lệ căn cao hơn nhiều."""
    with tempfile.TemporaryDirectory() as td:
        w16 = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(w16)], check=True)
        subprocess.run(["whisper-cli", "-m", str(model or WHISPER_MODEL), "-l", LANG, "-f", str(w16), "-ojf", "-of", str(Path(td) / "o"), "-np",
                        "--prompt", prompt or {"zh": "以下是普通话的句子。", "vi": "Đây là một câu tiếng Việt.", "en": "An English sentence."}.get(LANG, "")],
                       capture_output=True, check=True)
        d = json.loads((Path(td) / "o.json").read_bytes().decode("utf-8", "surrogateescape"))
    dec = codecs.getincrementaldecoder("utf-8")(errors="ignore")
    out = []
    for seg in d["transcription"]:
        for tk in seg.get("tokens", []):
            t = tk["text"]
            if t.startswith("[_") or t.startswith("<|"):
                continue
            for ch in unicodedata.normalize("NFC", dec.decode(t.encode("utf-8", "surrogateescape"))):
                if not ch.isspace():
                    out.append((ch, tk["offsets"]["from"] / 1000, tk["offsets"]["to"] / 1000))
    return out


def norm(ch):
    """Tiếng Việt: so khớp theo chữ cái gốc (bỏ dấu thanh, đ→d) vì whisper hay nghe sai dấu mà đúng âm; các ngôn ngữ khác chỉ hạ chữ thường."""
    ch = ch.lower()
    if LANG != "vi":
        return ch
    ch = ch.replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", ch) if not unicodedata.combining(c))


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
    src = {int(x.replace(",", "").replace(".", "")) for x in re.findall(r"\d[\d,.]*", text) if x.replace(",", "").replace(".", "").isdigit()}
    src |= {v for x in re.findall(r"[零〇一二三四五六七八九十百千万]+", text) if (v := cn_value(x)) is not None}
    bad = []
    for m in re.finditer(r"\d[\d.,]*|[零〇一二三四五六七八九十百千万]{2,}", heard):
        tok = re.sub(r"[.,]", "", m.group(0))
        if len(tok) < 2:
            continue
        v = cn_value(tok)
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
    vcfg = data.get("voice", {})
    if vcfg.get("engine", "gemini") != "gemini":
        sys.exit(f'narration.json ghi engine "{vcfg["engine"]}" nhưng script này chỉ chạy Gemini: đổi voice.engine thành "gemini" (và bỏ các khóa clone/style của MiMo)')
    global LANG
    LANG = vcfg.get("lang", "vi")
    model = arg("--model", vcfg.get("model", DEFAULT_MODEL))
    voice = arg("--voice", vcfg.get("voice", DEFAULT_VOICE))
    director = arg("--director", vcfg.get("director", DEFAULT_DIRECTOR))
    if "{text}" not in director:
        sys.exit("director phải có chỗ giữ {text}")
    lexicon = data.get("lexicon", {})
    key = env()
    (out / "audio").mkdir(parents=True, exist_ok=True)
    t_start = time.time()

    # Chuẩn bị cho từng nhịp: văn bản, vị trí cue, nội dung yêu cầu, dấu vân tay bộ nhớ đệm
    jobs_list = []
    for b in data["beats"]:
        clean, cue_pos = strip_cues(b["narration"])
        say = apply_lexicon(clean, lexicon)
        prompt = director.replace("{text}", say)
        digest = hashlib.md5(json.dumps([model, voice, director, say], ensure_ascii=False).encode()).hexdigest()
        jobs_list.append({"b": b, "clean": clean, "cue_pos": cue_pos, "prompt": prompt, "digest": digest,
                          "wav": out / "audio" / f"{b['id']}.wav", "mp3": out / "audio" / f"{b['id']}.mp3", "meta": out / "audio" / f"{b['id']}.key"})

    # Bước một (song song): tổng hợp. Nhịp nào giọng, ngữ khí, văn bản đều không đổi thì dùng luôn bản ghi lần trước
    def synth(j):
        t0 = time.time()
        reuse = j["wav"].exists() and ("--reuse" in sys.argv or (j["meta"].exists() and j["meta"].read_text() == j["digest"]))
        if not reuse:
            data_, mime = call(key, model, voice, j["prompt"])
            raw = j["wav"].with_suffix(".raw.wav")
            to_wav(data_, mime, raw)
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
        short = ("以下是普通话，用简体中文。" + (f"会提到：{terms}。" if terms else "")) if LANG == "zh" else (f"Thuật ngữ: {terms}." if LANG == "vi" and terms else f"Terms: {terms}." if terms else "")
        tries = [(short, WHISPER_SMALL if WHISPER_SMALL.exists() else None), (short, WHISPER_MODEL), (clean, WHISPER_MODEL)]
        rel, cover, heard = None, -1, ""
        for prompt, model in tries:
            wch = whisper_chars(j["wav"], prompt, model)
            r2, c2 = align(clean, wch, j["dur"])
            if c2 > cover:
                rel, cover, heard = r2, c2, "".join(c for c, _, _ in wch)
            if cover >= 0.9:
                break
        j["rel"], j["cover"] = rel, cover
        if "--qa" in sys.argv:
            j["qa"] = (heard, *qa_diff(clean, heard))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(synth, jobs_list))
    with ThreadPoolExecutor(2) as ex:  # Chạy nhiều whisper cùng lúc sẽ tranh GPU, ngược lại còn chậm hơn
        list(ex.map(align_one, jobs_list))

    # Bước ba (tuần tự): xếp thời gian tuyệt đối theo độ dài
    timings = {"voice": {"engine": "gemini", "model": model, "voice": voice, "lang": LANG, "director": director}, "beats": {}}
    t, parts, report = lead, [], []
    for j in jobs_list:
        b, clean, dur = j["b"], j["clean"], j["dur"]
        starts = [round(t + x, 3) for x in j["rel"]]
        words = []
        if LANG in WORD_LANGS:   # Tiếng Việt, tiếng Anh theo từ: mỗi từ một khoảng thời gian (phụ đề ngắt dòng theo từ, nhân vật nhép miệng theo từ)
            for m in re.finditer(r"[^\W_](?:[^\W_]|['’\-]|\.(?=[^\W_]))*", clean):
                i, i1 = m.start(), m.end()
                nxt = next((starts[k] for k in range(i1, len(clean)) if starts[k] > starts[i] and clean[k].isalnum()), round(t + dur, 3))
                words.append({"text": m.group(0), "start": starts[i], "end": min(nxt, round(t + dur, 3)), "i0": i, "i1": i1})
        for i, ch in enumerate("" if LANG in WORD_LANGS else clean):
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
        print(f"⚠ Các nhịp này khi đọc lại xuất hiện con số mà văn bản gốc không có, hãy nghe thử trước: {', '.join(odd)} (từ viết tắt hay con số bị đọc sai thì thêm cách đọc vào lexicon)")
    print(f"Tổng cộng {total:.2f}s → {out / 'timings.json'} (mất {time.time() - t_start:.0f}s, song song {jobs})")


if __name__ == "__main__":
    main()
