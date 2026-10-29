#!/usr/bin/env python3
"""Lồng tiếng (Google Gemini TTS) + căn từng chữ (OpenAI whisper-1 qua API) + kiểm tra đọc lại (cùng bản phiên âm đó).

Cách dùng:
    python3 scripts/tts_gemini.py <narration.json> <thư-mục-đầu-ra> [--gap 0.8] [--lead 0.6] [--voice Sulafat] [--model gemini-3.8-flash-tts] [--director "…{text}"] [--qa] [--reuse] [--jobs 3]

narration.json: {"voice": {...}, "lexicon": {...}, "beats": [{"id", "narration"}]}, trong lời dẫn dùng [[cue]] để đánh dấu thời điểm.
Trong voice có thể viết {"engine": "gemini", "model": "gemini-3.8-flash-tts", "voice": "Sulafat", "lang": "vi"}; tham số dòng lệnh được ưu tiên.
`director` (khuôn có chỗ giữ {text}) mặc định là "{text}", tức chỉ gửi nguyên văn: gemini-3.8-flash-tts đọc to mọi chỉ dẫn chèn vào văn bản.
Mặc định: model gemini-3.8-flash-tts, giọng Sulafat, lang "vi" (tiếng Việt, căn theo từ). lang "en" cũng căn theo từ; lang "zh" căn theo từng chữ Hán.
Gemini không có nhân bản giọng: muốn đổi giọng thì đổi `voice` (tên giọng có sẵn của Gemini).
Khóa API: Gemini đọc từ GOOGLE_API_KEY (hoặc GEMINI_API_KEY) hoặc ~/.config/ai-teardown/gemini.env; OpenAI đọc từ OPENAI_API_KEY hoặc ~/.config/ai-teardown/openai.env.
Khóa không ghi vào bất kỳ file dự án nào, không in ra (thông báo lỗi đều được che khóa).

Gemini không trả về thời gian từng từ, nên mỗi nhịp được tổng hợp nguyên đoạn (ngữ điệu tự nhiên), rồi gửi lên OpenAI /v1/audio/transcriptions
(model whisper-1, verbose_json, timestamp_granularities[]=word) lấy thời gian từng TỪ; thời điểm từng ký tự được chia đều trong khoảng start..end của từ,
rồi căn theo ký tự về văn bản gốc. Lượt một dùng prompt ngắn (thuật ngữ), căn < 90% thì thêm lượt hai với prompt toàn văn.
Từ đầu câu / sau dấu ngắt được kéo về mốc hết khoảng lặng (ffmpeg silencedetect) vì whisper-1 cho chúng bắt đầu muộn ~0,15 s.
Chi phí: mỗi nhịp tốn 1–2 lần gọi OpenAI (tính theo thời lượng âm thanh); kết quả lưu ở audio/<beat>.asr.json, âm thanh và prompt không đổi thì không gọi lại.
Giới hạn: whisper-1 là model duy nhất của OpenAI trả timestamp từng từ và đã bị đánh dấu ngừng hỗ trợ (OpenAI báo tắt ngày 26/02/2027);
với lang "zh" whisper-1 phần lớn trả từng chữ Hán, nhưng đôi khi gộp 2–3 chữ thành một "từ" (大家好), khi đó thời điểm các chữ bên trong chỉ là chia đều.
Đầu ra: <out>/audio/<beat>.mp3, <out>/narration.wav, <out>/timings.json;
Trong timings, words của mỗi nhịp là {text, start, end, i0, i1} (từng từ với vi/en, từng chữ với zh), ngoài ra có chars (thời điểm bắt đầu của từng ký tự), cues tính bằng giây tuyệt đối.
--qa: dùng bản phiên âm whisper-1 của mỗi nhịp, so với văn bản gốc, báo ra chỗ đọc sai (Gemini thỉnh thoảng đọc thừa, lặp hoặc bỏ sót từ).
--jobs: số nhịp xử lý đồng thời, cả gọi Gemini lẫn OpenAI (mặc định 3; bị 429 thì script tự động lùi thời gian chờ, tôn trọng Retry-After).
--reuse: audio/<beat>.wav đã có thì không tổng hợp lại, chỉ căn lại (dùng khi sửa logic căn).
Mặc định cũng tái sử dụng: khi model, giọng, chỉ dẫn, văn bản của cùng một nhịp đều không đổi thì dùng luôn bản ghi lần trước (audio/<beat>.key lưu dấu vân tay).
"""
import base64
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
import threading
import unicodedata
import urllib.error
import urllib.request
import uuid
import wave
from pathlib import Path

CUE_RE = re.compile(r"\[\[([a-z][a-z0-9_-]*)\]\]")
PUNCT = set("，。！？；：、,.!?;:（）()「」『』“”\"'《》…—- 　")
# Phiên âm để căn: OpenAI whisper-1 là model duy nhất nhận timestamp_granularities[] (thời gian từng từ); OpenAI báo ngừng ngày 26/02/2027
ASR_URL = "https://api.openai.com/v1/audio/transcriptions"
ASR_MODEL = "whisper-1"
ASR_MAX_BYTES = 25 * 1024 * 1024   # giới hạn kích thước file tải lên của API
ASR_PROMPT_CHARS = 600             # whisper-1 chỉ dùng 224 token cuối của prompt; cắt bớt cho chắc, giữ phần cuối
DEFAULT_MODEL = "gemini-3.8-flash-tts"
DEFAULT_VOICE = "Sulafat"
TTS_URL = "https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent?key={key}"
# Khuôn văn bản gửi đi, {text} là lời dẫn của nhịp. Mặc định chỉ gửi nguyên văn: gemini-3.8-flash-tts coi trường text là lời thoại
# nguyên văn, chỉ dẫn diễn đọc chèn vào đó sẽ bị đọc to (đo thật 10/2026: 6/9 nhịp đọc cả đoạn chỉ dẫn tiếng Anh, có nhịp còn dịch ra tiếng Việt rồi đọc).
# Endpoint generateContent của Vertex không nhận systemInstruction hay speech_metadata cho model này; muốn đổi chất giọng thì đổi `voice`.
DEFAULT_DIRECTOR = "{text}"
WORD_LANGS = ("vi", "en")   # căn theo từ; các ngôn ngữ khác (zh) căn theo từng chữ


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def env(names=("GOOGLE_API_KEY", "GEMINI_API_KEY"), file="gemini.env"):
    """Khóa API: biến môi trường trước, sau đó ~/.config/ai-teardown/<file> (dòng TÊN=giá trị)."""
    key = next((os.environ[n] for n in names if os.environ.get(n)), "")
    f = Path.home() / ".config/ai-teardown" / file
    if not key and f.exists():
        for line in f.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip().removeprefix("export ").strip() in names and v.strip():
                key = v.strip().strip("\"'")
                break
    if not key:
        sys.exit(f"Thiếu {names[0]} (biến môi trường hoặc ~/.config/ai-teardown/{file})")
    return key


def openai_env():
    return env(("OPENAI_API_KEY",), "openai.env")


def redact(msg, key):
    """Che khóa trong thông báo lỗi (OpenAI trả lại vài ký tự đầu/cuối của khóa sai trong thông báo 401)."""
    if key:
        msg = msg.replace(key, "***")
    return re.sub(r"\b(sk|AIza)[-\w*]{4,}", r"\1-***", msg)


class Gate:
    """Điều tiết toàn cục: các luồng song song xếp hàng, hai lần bắt đầu yêu cầu cách nhau ít nhất gap giây (tránh 429)."""
    def __init__(self, gap):
        self.gap, self.last, self.lock = gap, 0.0, threading.Lock()

    def wait(self):
        with self.lock:
            w = self.last + self.gap - time.time()
            if w > 0:
                time.sleep(w)
            self.last = time.time()


TTS_GATE = Gate(1.0)
ASR_GATE = Gate(0.5)


def retry_wait(e, k):
    """Thời gian chờ trước lần thử k+1 sau HTTPError: tôn trọng Retry-After, 429 lùi dài hơn lỗi máy chủ."""
    ra = e.headers.get("Retry-After") if getattr(e, "headers", None) else None
    if ra and ra.replace(".", "", 1).isdigit():
        return min(120, float(ra) + 1)
    return min(60, 10 * (k + 1)) if e.code == 429 else 6 * (k + 1)


def call(key, model, voice, text, tries=8):
    """Một yêu cầu TTS → (mẫu âm thanh PCM int16 dạng bytes, tần số lấy mẫu). Địa chỉ yêu cầu có chứa khóa nên không bao giờ in ra."""
    body = {"contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    last = ""
    for k in range(tries):
        TTS_GATE.wait()
        req = urllib.request.Request(TTS_URL.format(model=model, key=key), data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        wait = 2 * (k + 1)
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
            part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"]), part.get("mimeType", "")
        except urllib.error.HTTPError as e:
            last = redact(f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}", key)
            if e.code not in (429, 500, 503):
                break
            wait = retry_wait(e, k)
        except (KeyError, IndexError, ValueError, urllib.error.URLError, TimeoutError) as e:
            last = type(e).__name__ + (" (không có âm thanh trong phản hồi, có thể bị chặn nội dung)" if isinstance(e, (KeyError, IndexError)) else "")
        print(f"  thử lại lần {k + 1} sau {wait}s: {last}", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"Gọi Gemini TTS thất bại: {last}")


def to_wav(data, mime, dest):
    """Gemini trả về PCM thô (audio/L16;rate=24000) hoặc một tệp có đầu tệp (thực tế 10/2026: audio/wav, RIFF 24 kHz mono); ghi ra WAV."""
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
    text = unicodedata.normalize("NFC", text)   # chuẩn hoá trước khi tính vị trí cue: văn bản NFD (dấu tách rời) đổi độ dài sau NFC
    out, cues, pos = [], {}, 0
    for m in CUE_RE.finditer(text):
        out.append(text[pos:m.start()])
        cues[m.group(1)] = sum(len(p) for p in out)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), cues


def apply_lexicon(text, lexicon):
    for k in sorted(lexicon or {}, key=len, reverse=True):
        text = text.replace(k, lexicon[k])
    return text


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


LANG = "vi"   # voice.lang của narration.json; "vi" = tiếng Việt (mặc định), "en" = tiếng Anh, "zh" = tiếng Trung


def multipart(fields, fname, blob, ctype):
    """Dựng thân multipart/form-data (không cần requests): fields là danh sách (tên, giá trị), cho phép trùng tên."""
    bnd = "----vk" + uuid.uuid4().hex
    out = io.BytesIO()
    for k, v in fields:
        out.write(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
        out.write(str(v).encode() + b"\r\n")
    out.write(f'--{bnd}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\nContent-Type: {ctype}\r\n\r\n'.encode())
    out.write(blob + f"\r\n--{bnd}--\r\n".encode())
    return out.getvalue(), f"multipart/form-data; boundary={bnd}"


def asr_audio(wav):
    """Âm thanh gửi lên: WAV 16 kHz mono (không có độ trễ bộ mã hoá như mp3); quá 25 MB (~13 phút) thì đổi sang mp3 48 kbps."""
    with tempfile.TemporaryDirectory() as td:
        for name, ctype, opts in (("a.wav", "audio/wav", ["-c:a", "pcm_s16le"]), ("a.mp3", "audio/mpeg", ["-b:a", "48k"])):
            f = Path(td) / name
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ar", "16000", "-ac", "1", *opts, str(f)], check=True)
            if f.stat().st_size <= ASR_MAX_BYTES:
                return name, f.read_bytes(), ctype
    raise RuntimeError(f"{wav}: âm thanh quá 25 MB kể cả khi nén mp3, hãy chia nhịp ngắn hơn")


def whisper_words(wav, prompt, key, model=ASR_MODEL, tries=6):
    """OpenAI /v1/audio/transcriptions → verbose_json {text, words: [{word, start, end}], ...}. Header có khóa, không bao giờ in ra."""
    fname, blob, ctype = asr_audio(wav)
    fields = [("model", model), ("response_format", "verbose_json"), ("timestamp_granularities[]", "word"), ("language", LANG), ("temperature", 0)]
    if prompt:
        fields.append(("prompt", prompt[-ASR_PROMPT_CHARS:]))
    body, content_type = multipart(fields, fname, blob, ctype)
    last = ""
    for k in range(tries):
        ASR_GATE.wait()
        req = urllib.request.Request(ASR_URL, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": content_type})
        wait = 2 * (k + 1)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = redact(f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}", key)
            if e.code not in (408, 409, 429, 500, 502, 503, 504):
                break
            wait = retry_wait(e, k)
        except (ValueError, urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = redact(f"{type(e).__name__}: {e}", key)
        print(f"  [openai] thử lại lần {k + 1} sau {wait}s: {last}", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"Gọi OpenAI {model} thất bại: {last}")


def words_to_chars(words):
    """Thời gian từng TỪ → (ký tự, start, end) cho từng ký tự: chia đều khoảng start..end của từ cho các chữ cái của nó
    (dấu câu nếu có dính trong từ thì lấy mốc của chữ liền trước). Với zh, một "từ" thường là vài chữ Hán, nên đây chỉ là ước lượng."""
    out = []
    for w in words:
        text = unicodedata.normalize("NFC", w.get("word", ""))
        s0 = float(w.get("start", 0.0))
        s1 = max(s0, float(w.get("end", s0)))
        chars = [c for c in text if not c.isspace()]
        n = sum(c not in PUNCT for c in chars) or 1
        k = 0
        for c in chars:
            if c in PUNCT:
                t = s0 + (s1 - s0) * k / n
                out.append((c, t, t))
                continue
            out.append((c, s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n))
            k += 1
    return out


def asr_terms(text):
    """Thuật ngữ cho prompt (vi/en): từ toàn chữ Latin không dấu có chữ hoa ở giữa, chữ số hoặc viết hoa toàn bộ (WorkBuddy, AI, GPT-4o, AGENTS.md).
    Phải là nguyên một từ: không cắt "Cu" ra khỏi "Cuốn"."""
    words = re.findall(r"(?<![^\W_])[A-Za-z][A-Za-z0-9]*(?:[.\-][A-Za-z0-9]+)*(?![^\W_])", text)
    return list(dict.fromkeys(w for w in words if any(c.isdigit() for c in w) or any(c.isupper() for c in w[1:]) or "." in w))


def whisper_chars(wav, prompt, key, model=ASR_MODEL):
    """Giao diện cũ cho align(): danh sách (ký tự, start, end) suy ra từ timestamp từng từ của OpenAI."""
    return words_to_chars(whisper_words(wav, prompt, key, model).get("words") or [])


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


def onsets(wav):
    """Các mốc giọng nói cất lên lại sau một khoảng lặng (ffmpeg silencedetect), tính bằng giây trong nhịp."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True)
    return [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]


def snap_onsets(text, rel, ons):
    """whisper-1 cho từ đầu câu / sau dấu ngắt bắt đầu muộn hơn lúc giọng thật sự cất lên (đo thật 10/2026: trung bình ~0,15 s, có chỗ 0,25 s);
    kéo các từ đó về mốc hết khoảng lặng gần nhất trong cửa sổ [t − 0,5 s, t + 0,1 s]. Với zh chỉ dời chữ Hán đầu tiên."""
    out = list(rel)
    for m in re.finditer(r"[^\W_]+", text):
        i = m.start()
        prev = text[:i].rstrip()
        if prev and prev[-1] not in ".?!,:;…，。！？；：、":
            continue
        cand = [o for o in ons if rel[i] - 0.5 <= o <= rel[i] + 0.1]
        if not cand:
            continue
        d = min(cand, key=lambda o: abs(o - rel[i])) - rel[i]
        for k in range(i, m.end() if LANG in WORD_LANGS else i + 1):
            out[k] = max(0.0, rel[k] + d)
        k = i - 1
        while k >= 0 and (text[k].isspace() or text[k] in PUNCT):   # dấu câu, khoảng trắng đứng trước không được muộn hơn từ vừa kéo
            out[k] = min(out[k], out[i])
            k -= 1
    for k in range(1, len(out)):   # giữ đơn điệu
        out[k] = max(out[k], out[k - 1])
    return out


CN_NUM = str.maketrans("零〇一二三四五六七八九", "00123456789")
# whisper hay viết số bằng chữ số ("bốn" → "4"); đổi cả hai phía về chữ số trước khi so (đổi đối xứng nên "năm" = năm tháng cũng không sai lệch)
VI_NUM = {"không": "0", "một": "1", "mốt": "1", "hai": "2", "ba": "3", "bốn": "4", "tư": "4", "năm": "5", "lăm": "5", "sáu": "6", "bảy": "7", "tám": "8", "chín": "9", "mười": "10"}


def qa_diff(text, heard):
    """So sánh đọc lại: bỏ dấu câu, thống nhất cách viết số rồi so, trả về (độ tương đồng, các đoạn khác biệt)"""
    if LANG == "vi":
        vi = lambda s: re.sub(r"[^\W\d_]+", lambda m: VI_NUM.get(m.group(0), m.group(0)), unicodedata.normalize("NFC", s.lower()))
    else:
        vi = lambda s: s.lower()
    f = lambda s: [c for c in vi(s).translate(CN_NUM) if c not in PUNCT and not c.isspace()]
    a, b = f(text), f(heard.replace("做", "作"))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = [("".join(a[i1:i2]), "".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    return sm.ratio(), diffs, len(b) / max(1, len(a))


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
    if director.strip() != "{text}":
        print("⚠ director có chỉ dẫn ngoài {text}: gemini-3.8-flash-tts đọc to mọi thứ trong văn bản, kể cả chỉ dẫn. "
              "Bỏ voice.director (mặc định chỉ gửi nguyên văn) trừ khi đã nghe thử và --qa không báo đọc thừa.", file=sys.stderr)
    lexicon = data.get("lexicon", {})
    key = env()
    okey = openai_env()   # kiểm tra sớm: thiếu khóa OpenAI thì dừng trước khi tốn lượt gọi Gemini
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

    # Bước hai: căn từng chữ bằng OpenAI whisper-1; dùng prompt ngắn (thuật ngữ) trước, căn < 90% thì thêm một lượt prompt toàn văn
    # (prompt toàn văn giúp viết đúng tên riêng nhưng đôi khi làm whisper bỏ qua một đoạn, nên giữ lượt nào căn được nhiều hơn).
    # Phản hồi được lưu ở audio/<beat>.asr.json theo dấu vân tay âm thanh, mỗi (model, lang, prompt) một bản: chạy lại không tốn thêm lần gọi.
    def transcribe(j, prompt):
        audio = hashlib.md5(j["wav"].read_bytes()).hexdigest()
        pkey = json.dumps([ASR_MODEL, LANG, prompt], ensure_ascii=False)
        cache_f = j["wav"].with_suffix(".asr.json")
        try:
            cache = json.loads(cache_f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            cache = {}
        if cache.get("audio") != audio:   # âm thanh đã tổng hợp lại: bỏ các bản phiên âm cũ
            cache = {"audio": audio, "by_prompt": {}}
        if pkey not in cache["by_prompt"]:
            d = whisper_words(j["wav"], prompt, okey)
            cache["by_prompt"][pkey] = {"text": d.get("text", ""), "words": d.get("words") or []}
            cache_f.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            j["asr_calls"] = j.get("asr_calls", 0) + 1
        return cache["by_prompt"][pkey]

    def align_one(j):
        clean = j["clean"]
        terms = "、".join(dict.fromkeys(re.findall(r"[A-Za-z][A-Za-z0-9.\-]*|《[^》]+》", clean))) if LANG == "zh" else ", ".join(asr_terms(clean))
        if LANG == "zh":
            short = "以下是普通话，用简体中文。" + (f"会提到：{terms}。" if terms else "")
        elif LANG == "vi":
            short = f"Đây là một câu tiếng Việt. Thuật ngữ: {terms}." if terms else "Đây là một câu tiếng Việt."
        else:
            short = f"An English sentence. Terms: {terms}." if terms else "An English sentence."
        rel, cover, heard = None, -1, ""
        for prompt in (short, clean):
            d = transcribe(j, prompt)
            if not d["words"]:
                print(f"  ⚠ {j['b']['id']}: OpenAI không trả words[] (model {ASR_MODEL} còn hỗ trợ timestamp_granularities không?)", file=sys.stderr)
            r2, c2 = align(clean, words_to_chars(d["words"]), j["dur"])
            if c2 > cover:
                rel, cover, heard = r2, c2, d["text"]
            if cover >= 0.9:
                break
        j["rel"], j["cover"] = snap_onsets(clean, rel, onsets(j["wav"])), cover
        if "--qa" in sys.argv:
            j["qa"] = (heard, *qa_diff(clean, heard))

    def work(j):
        synth(j)
        align_one(j)

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(jobs) as ex:  # Gemini và OpenAI có cổng điều tiết riêng, nhịp này đang căn thì nhịp khác vẫn tổng hợp được
        list(ex.map(work, jobs_list))

    # Bước ba (tuần tự): xếp thời gian tuyệt đối theo độ dài
    timings = {"voice": {"engine": "gemini", "model": model, "voice": voice, "lang": LANG, "director": director},
               "align": {"engine": "openai", "model": ASR_MODEL}, "beats": {}}
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
        status = ("dùng lại" if j["reused"] else f"tổng hợp {j['synth_s']:.1f}s") + f", gọi OpenAI {j.get('asr_calls', 0)} lần"
        n_words = len(re.findall(r"[^\W_]+", clean)) if LANG in WORD_LANGS else sum(not (c.isspace() or c in PUNCT) for c in clean)
        unit = "từ" if LANG in WORD_LANGS else "chữ"
        line = f"{b['id']}  {dur:5.2f}s  {n_words:3d} {unit}  {n_words / dur:.2f} {unit}/giây  căn {j['cover']:.0%}  {status}"
        if "qa" in j:
            heard, ratio, diffs, extra = j["qa"]
            odd = odd_numbers(clean, heard)
            line += (f"  đọc lại {ratio:.0%}" + (f"  ⚠ đọc thừa {extra - 1:.0%}" if extra > 1.2 else "")
                     + (f"  khác biệt {diffs[:4]}" if diffs else "") + (f"  ⚠ số đọc đáng ngờ {odd}" if odd else ""))
            report.append({"beat": b["id"], "heard": heard, "ratio": round(ratio, 3), "length_ratio": round(extra, 3), "diffs": diffs,
                           **({"odd_numbers": odd} if odd else {})})
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
    extra = [r["beat"] for r in report if r["length_ratio"] > 1.2]
    if extra:
        print(f"⚠ Các nhịp này đọc dài hơn văn bản gốc trên 20% (đọc thừa, lặp, hoặc đọc cả chỉ dẫn director): {', '.join(extra)}; xoá audio/<nhịp>.* rồi tổng hợp lại")
    odd = [r["beat"] for r in report if r.get("odd_numbers")]
    if odd:
        print(f"⚠ Các nhịp này khi đọc lại xuất hiện con số mà văn bản gốc không có, hãy nghe thử trước: {', '.join(odd)} (từ viết tắt hay con số bị đọc sai thì thêm cách đọc vào lexicon)")
    print(f"Tổng cộng {total:.2f}s → {out / 'timings.json'} (mất {time.time() - t_start:.0f}s, song song {jobs})")


if __name__ == "__main__":
    main()
