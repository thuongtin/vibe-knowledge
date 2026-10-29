# 03 · Lời dẫn và lồng tiếng

## narration.json

```json
{
 "voice": {
  "engine": "gemini",
  "model": "gemini-3.8-flash-tts",
  "voice": "Sulafat",
  "lang": "vi"
 },
 "lexicon": {"PPT": "P P T", "GitHub": "Git Hub", "NLP": "N L P"},
 "beats": [{"id": "B01", "narration": "[[hi]]Bài trước, chúng ta đã……[[now]]Bài này, chúng ta sẽ……"}]
}
```

(**Không viết `director`.** Trước đây có khối chỉ dẫn diễn đọc tiếng Anh chèn trước lời dẫn; đo thật 10/2026 với `gemini-3.8-flash-tts`, 6/9 nhịp đọc to cả đoạn chỉ dẫn, có nhịp còn dịch chỉ dẫn sang tiếng Việt rồi đọc. Model này coi văn bản gửi đi là lời thoại nguyên văn; endpoint `generateContent` của Vertex mà script dùng không nhận `systemInstruction` hay `speech_metadata.style`. `director` vẫn được đọc nếu có, mặc định là `"{text}"`, script sẽ cảnh báo khi có chữ ngoài `{text}`.)

- Gemini không có nhân bản giọng: muốn đổi giọng thì đổi tên giọng có sẵn ở `voice` (ví dụ `Sulafat`, `Gacrux`); chất giọng, nhịp đọc phụ thuộc giọng được chọn.
- **Một bài**: 18–28 nhịp, 1200–2200 chữ (sau khi tăng tốc 1,15 lần là 4–7 phút). Loại dẫn nhập 9–10 nhịp, khoảng 750 chữ ≈ 2,5 phút.
- **Một nhịp**: 40–130 chữ, 2–4 `[[cue]]` (chữ thường tiếng Anh/chữ số/gạch dưới, đặt ở đầu mệnh đề). Phần tử hình ảnh dùng `"B03.cue"` hoặc `"B03@một-từ-nào-đó"` để căn đến thời điểm đọc đến chữ đó.
- Khẩu ngữ, câu ngắn, ngôi thứ hai. Phần đầu nối với bài trước, phần cuối báo trước bài sau + cảm ơn tác giả gốc + "hẹn gặp lại ở bài sau".
- Ít nhất một lần "tạm dừng suy nghĩ": một nhịp đặt câu hỏi, nhịp sau `[[answer]]` công bố đáp án.
- Không bịa: con số, tính năng, chữ trên giao diện, các bước theo bản gốc; bản gốc không viết thì không bổ sung. Trích dẫn đúng từng chữ.

## Điểm chính khi lồng tiếng Gemini

- Script `scripts/tts_gemini.py`; mặc định model `gemini-3.8-flash-tts`, giọng `Sulafat`, `lang: "vi"`. Đầu ra: `audio/<nhịp>.mp3`, `narration.wav`, `timings.json`.
- Khóa Gemini lấy từ biến môi trường `GOOGLE_API_KEY` (hoặc `GEMINI_API_KEY`), hoặc file `~/.config/ai-teardown/gemini.env`; khóa OpenAI (căn chỉnh) lấy từ `OPENAI_API_KEY` hoặc `~/.config/ai-teardown/openai.env` (quyền 600, dòng `TÊN=...`). Không ghi vào dự án, không in ra; thông báo lỗi đều được che khóa.
- Đổi giọng: chọn tên giọng có sẵn của Gemini (Sulafat, Gacrux...); không có nhân bản giọng hay thiết kế giọng.
- Gemini trả `audio/wav` (RIFF, 24 kHz, mono, 16-bit); script vẫn nhận được PCM thô `audio/L16` nếu có.
- **Nhịp độ đo thật** (10/2026, bài `example-intro`, Sulafat, không director, trước `speed.py`): trung bình 3,5 từ (âm tiết)/giây, các nhịp 3,2–3,9; khoảng 15 ký tự/giây nếu đếm cả dấu cách. Với `scenes.speed` 1.15 thì khoảng 4 âm tiết/giây. Các con số "chữ/giây" cũ (5,5–6) là của tiếng Trung, không áp dụng cho tiếng Việt.
- Gemini không trả thời gian từng từ → mỗi nhịp tổng hợp nguyên đoạn rồi gửi lên OpenAI `POST /v1/audio/transcriptions` (`model=whisper-1`, `response_format=verbose_json`, `timestamp_granularities[]=word`, `language` = `voice.lang`, `prompt` = thuật ngữ). API chỉ trả thời gian theo **từ**: thời điểm từng ký tự được chia đều trong khoảng start..end của từ, rồi căn về văn bản gốc. Lượt một dùng prompt ngắn (thuật ngữ); căn < 90% thì thêm lượt hai với prompt toàn văn (whisper-1 chỉ dùng 224 token cuối của prompt). Từ đầu câu / sau dấu ngắt được kéo về mốc hết khoảng lặng (ffmpeg silencedetect) vì whisper-1 cho chúng bắt đầu muộn: đo thật, trung vị độ lệch đầu câu từ 192 ms xuống 5 ms, p90 từ 289 ms xuống 33 ms.
- Với `lang` "vi" và "en", `words` trong `timings.json` là từng từ (theo dấu cách); `chars` vẫn là thời điểm từng ký tự; chỉ `lang` "zh" mới căn từng chữ Hán. **Giới hạn với zh**: whisper-1 thường trả từng chữ Hán, nhưng đôi khi gộp 2–3 chữ thành một "từ" (ví dụ 大家好), khi đó thời điểm các chữ bên trong chỉ là chia đều, kém chính xác hơn căn theo token của whisper.cpp trước đây.
- **Chi phí và thời hạn**: mỗi lần lồng tiếng giờ gọi thêm OpenAI (1–2 lần mỗi nhịp, tính theo thời lượng âm thanh). Phản hồi được cache ở `build/audio/<nhịp>.asr.json` theo dấu vân tay âm thanh và prompt, chạy lại không gọi lại. `whisper-1` là model duy nhất có `timestamp_granularities[]`; OpenAI đã đánh dấu ngừng và báo tắt ngày 26/02/2027, khi đó phải chuyển sang cách căn khác.
- Giới hạn file tải lên 25 MB: script gửi WAV 16 kHz mono (~13 phút), quá thì chuyển sang mp3 48 kbps.
- Song song `--jobs` 2–3 luồng (cả Gemini lẫn OpenAI, mỗi bên có cổng điều tiết riêng); gặp 429/5xx script tự động lùi thời gian chờ (tôn trọng `Retry-After`) và thử lại, chậm là bình thường.

## Bẫy cách đọc và lexicon

- Bẫy "số La Mã" của MiMo không còn với Gemini, script đã bỏ bước tự động tách chữ cái; từ viết tắt nào bị đọc lệch thì ghi vào lexicon (tách chữ cái hoặc viết cách đọc).
- Số phiên bản viết thành "0 chấm 155 chấm 1".
- Tên riêng tiếng Anh bị đọc lệch (GitHub, GEO, NLP, từ tự đặt) thì thêm vào lexicon, tách chữ cái hoặc thêm dấu cách.
- `odd_numbers` của kiểm tra đọc lại: con số ≥100 xuất hiện trong bản đọc lại mà văn bản gốc không có sẽ được báo bằng ⚠.

## Kiểm tra chất lượng đọc lại (bài nào cũng phải xem voice.log)

- Mỗi nhịp một dòng: thời lượng, số từ, từ/giây (zh: chữ, chữ/giây), tỷ lệ căn, thời gian tổng hợp, số lần gọi OpenAI, độ tương đồng đọc lại, khác biệt. Đọc lại (`--qa`) dùng chính bản phiên âm whisper-1 của bước căn chỉnh (không tốn thêm lần gọi); số đọc bằng chữ ("bốn") và chữ số ("4") được coi là như nhau.
- `⚠ đọc thừa`: bản đọc lại dài hơn văn bản gốc trên 20% (Gemini đọc lặp, đọc thừa, hoặc đọc cả chỉ dẫn `director`) → xóa `build/audio/<nhịp>.*` rồi tổng hợp lại.
- Đọc lại < 95% hoặc có ⚠: xóa `build/audio/<nhịp>.*` rồi chạy lại voice, chỉ tổng hợp lại những nhịp này; hai lần đều thấp thì sửa cách diễn đạt (đổi từ đồng nghĩa, tách câu dài) rồi tổng hợp lại.
- Khi khác biệt toàn là từ đồng âm / tên riêng bị whisper nghe sai, nghe lại trực tiếp file `build/audio/<nhịp>.mp3` để xác nhận (hoặc xem `qa.json`; có thể thêm tên riêng vào lời dẫn để chúng vào prompt thuật ngữ); đọc đúng rồi thì không cần làm lại. Tên người nhất định phải nghe lại.
- Gemini thỉnh thoảng đọc thừa, lặp hoặc bỏ sót từ (kể cả từ phủ định): đọc lại thấp thì tổng hợp lại nhịp đó; nghĩa bị ngược thì bắt buộc làm lại.

## Bản tiếng Anh

- narration: `voice.lang = "en"`, chọn giọng có sẵn của Gemini (không viết `director`), OpenAI nhận `language=en`, chia đoạn theo từ.
- scenes: `"lang": "en"` (bảng chữ giao diện chuyển sang tiếng Anh, phụ đề ngắt theo câu, rộng 52 ký tự), `"inlineCredits": false`, `"videoOnly": true` (chỉ xuất phim), `shotCredit` viết nguồn bằng tiếng Anh.
- Gemini tiếng Anh thỉnh thoảng đọc thừa/lặp một câu: đọc lại < 95% thì tổng hợp lại.
