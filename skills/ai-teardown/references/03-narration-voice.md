# 03 · Lời dẫn và lồng tiếng

## narration.json

```json
{
 "voice": {
  "engine": "gemini",
  "model": "gemini-3.8-flash-tts",
  "voice": "Sulafat",
  "lang": "vi",
  "director": "Read the following Vietnamese narration like a friendly young science communicator giving an intro class to office workers: calm pace, every sentence clear, natural pauses between sentences, slight emphasis on key words. Do not add or skip any word.\n\n{text}"
 },
 "lexicon": {"PPT": "P P T", "GitHub": "Git Hub", "NLP": "N L P"},
 "beats": [{"id": "B01", "narration": "[[hi]]Bài trước, chúng ta đã……[[now]]Bài này, chúng ta sẽ……"}]
}
```

(`director` là chỉ dẫn diễn đọc viết bằng tiếng Anh, vì Gemini nghe chỉ dẫn tiếng Anh ổn định nhất; `{text}` là chỗ chèn lời dẫn của nhịp, còn lời dẫn vẫn viết bằng tiếng Việt. Ý nghĩa của `director` ở trên: "Đọc lời dẫn tiếng Việt sau đây như một blogger khoa học trẻ thân thiện đang giảng bài nhập môn cho người đi làm: tốc độ thong thả, mỗi câu rõ ràng, giữa các câu ngắt nghỉ tự nhiên, từ trọng điểm nhấn nhẹ; không thêm bớt từ nào".)

- Gemini không có nhân bản giọng: muốn đổi giọng thì đổi tên giọng có sẵn ở `voice` (ví dụ `Sulafat`, `Gacrux`) và chỉnh `director`.
- **Một bài**: 18–28 nhịp, 1200–2200 chữ (sau khi tăng tốc 1,15 lần là 4–7 phút). Loại dẫn nhập 9–10 nhịp, khoảng 750 chữ ≈ 2,5 phút.
- **Một nhịp**: 40–130 chữ, 2–4 `[[cue]]` (chữ thường tiếng Anh/chữ số/gạch dưới, đặt ở đầu mệnh đề). Phần tử hình ảnh dùng `"B03.cue"` hoặc `"B03@một-từ-nào-đó"` để căn đến thời điểm đọc đến chữ đó.
- Khẩu ngữ, câu ngắn, ngôi thứ hai. Phần đầu nối với bài trước, phần cuối báo trước bài sau + cảm ơn tác giả gốc + "hẹn gặp lại ở bài sau".
- Ít nhất một lần "tạm dừng suy nghĩ": một nhịp đặt câu hỏi, nhịp sau `[[answer]]` công bố đáp án.
- Không bịa: con số, tính năng, chữ trên giao diện, các bước theo bản gốc; bản gốc không viết thì không bổ sung. Trích dẫn đúng từng chữ.

## Điểm chính khi lồng tiếng Gemini

- Script `scripts/tts_gemini.py`; mặc định model `gemini-3.8-flash-tts`, giọng `Sulafat`, `lang: "vi"`. Đầu ra: `audio/<nhịp>.mp3`, `narration.wav`, `timings.json`.
- Khóa API lấy từ biến môi trường `GOOGLE_API_KEY` (hoặc `GEMINI_API_KEY`), hoặc file `~/.config/ai-teardown/gemini.env` (quyền 600, dòng `GOOGLE_API_KEY=...`); không ghi vào dự án, không in ra.
- Đổi giọng: chọn tên giọng có sẵn của Gemini (Sulafat, Gacrux...) và sửa `director`; không có nhân bản giọng hay thiết kế giọng.
- **`director` viết bằng tiếng Anh** (Gemini nghe ổn định nhất), có chỗ giữ `{text}`; lời dẫn trong `narration` vẫn là tiếng Việt. Nên giữ chỉ dẫn kiểu giảng bài (thong thả, ngắt nghỉ tự nhiên) để nhịp đọc không vội; con số "chữ/giây" của tiếng Trung không dùng được cho tiếng Việt, cần đo lại trên bản tổng hợp thật rồi mới chỉnh `scenes.speed` (ví dụ `1.15`, đổi tốc độ bằng atempo, cao độ không đổi).
- Gemini không trả thời gian từng từ → mỗi nhịp tổng hợp nguyên đoạn rồi dùng whisper.cpp trên máy lấy thời gian (`-l vi`), căn về văn bản gốc: dùng mô hình small trước, căn không được thì dùng medium. Với `lang` "vi" và "en", `words` trong `timings.json` là từng từ (theo dấu cách); `chars` vẫn là thời điểm từng ký tự; chỉ `lang` "zh" mới căn từng chữ Hán.
- Song song `--jobs` 2–3 luồng; gặp 429/500/503 script tự động lùi thời gian chờ và thử lại (chậm là bình thường).

## Bẫy cách đọc và lexicon

- Bẫy "số La Mã" của MiMo không còn với Gemini, script đã bỏ bước tự động tách chữ cái; từ viết tắt nào bị đọc lệch thì ghi vào lexicon (tách chữ cái hoặc viết cách đọc).
- Số phiên bản viết thành "0 chấm 155 chấm 1".
- Tên riêng tiếng Anh bị đọc lệch (GitHub, GEO, NLP, từ tự đặt) thì thêm vào lexicon, tách chữ cái hoặc thêm dấu cách.
- `odd_numbers` của kiểm tra đọc lại: con số ≥100 xuất hiện trong bản đọc lại mà văn bản gốc không có sẽ được báo bằng ⚠.

## Kiểm tra chất lượng đọc lại (bài nào cũng phải xem voice.log)

- Mỗi nhịp một dòng: thời lượng, số chữ, chữ/giây, tỷ lệ căn, thời gian tổng hợp, độ tương đồng đọc lại, khác biệt. Đọc lại (`--qa`) nay dùng whisper.cpp phiên âm lại, không còn ASR của MiMo.
- Đọc lại < 95% hoặc có ⚠: xóa `build/audio/<nhịp>.*` rồi chạy lại voice, chỉ tổng hợp lại những nhịp này; hai lần đều thấp thì sửa cách diễn đạt (đổi từ đồng nghĩa, tách câu dài) rồi tổng hợp lại.
- Khi khác biệt toàn là từ đồng âm / tên riêng bị whisper nghe sai, nghe lại bằng whisper cục bộ để xác nhận (`whisper-cli -m <medium> -l vi -nt -f build/audio/B07.wav`, có thể thêm `--prompt "tên riêng"`); đọc đúng rồi thì không cần làm lại. Tên người nhất định phải nghe lại.
- Gemini thỉnh thoảng đọc thừa, lặp hoặc bỏ sót từ (kể cả từ phủ định): đọc lại thấp thì tổng hợp lại nhịp đó; nghĩa bị ngược thì bắt buộc làm lại.

## Bản tiếng Anh

- narration: `voice.lang = "en"`, chọn giọng có sẵn của Gemini và viết `director` bằng tiếng Anh, whisper `-l en`, chia đoạn theo từ.
- scenes: `"lang": "en"` (bảng chữ giao diện chuyển sang tiếng Anh, phụ đề ngắt theo câu, rộng 52 ký tự), `"inlineCredits": false`, `"videoOnly": true` (chỉ xuất phim), `shotCredit` viết nguồn bằng tiếng Anh.
- Gemini tiếng Anh thỉnh thoảng đọc thừa/lặp một câu: đọc lại < 95% thì tổng hợp lại.
