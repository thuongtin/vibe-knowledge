# 03 · Lời dẫn và lồng tiếng

## narration.json

```json
{
 "voice": {
  "engine": "mimo",
  "clone": "../../voice/host-ref.wav",
  "style": "你在录一节给职场人听的软件入门课。像一位亲切、干脆的年轻科普博主，语速从容，每句话讲清楚，句与句之间留出停顿，重点词稍微加重。"
 },
 "lexicon": {"PPT": "P P T", "GitHub": "Git Hub", "NLP": "N L P"},
 "beats": [{"id": "B01", "narration": "[[hi]]上一节，我们……[[now]]这一节，讲……"}]
}
```

(Ví dụ trên giữ nguyên tiếng Trung vì `style` và `narration` là nội dung đưa cho TTS đọc bằng tiếng Trung. Ý nghĩa của `style`: "Bạn đang thu một bài nhập môn phần mềm cho người đi làm. Như một blogger khoa học thân thiện, dứt khoát, tốc độ thong thả, mỗi câu nói rõ ràng, giữa các câu chừa chỗ ngắt, từ trọng điểm nhấn nhẹ hơn".)

- Đường dẫn `clone` tương đối so với thư mục bài học; giọng có sẵn thì viết kiểu `"voice": "白桦"`.
- **Một bài**: 18–28 nhịp, 1200–2200 chữ (sau khi tăng tốc 1,15 lần là 4–7 phút). Loại dẫn nhập 9–10 nhịp, khoảng 750 chữ ≈ 2,5 phút.
- **Một nhịp**: 40–130 chữ, 2–4 `[[cue]]` (chữ thường tiếng Anh/chữ số/gạch dưới, đặt ở đầu mệnh đề). Phần tử hình ảnh dùng `"B03.cue"` hoặc `"B03@một-từ-nào-đó"` để căn đến thời điểm đọc đến chữ đó.
- Khẩu ngữ, câu ngắn, ngôi thứ hai. Phần đầu nối với bài trước, phần cuối báo trước bài sau + cảm ơn tác giả gốc + "hẹn gặp lại ở bài sau".
- Ít nhất một lần "tạm dừng suy nghĩ": một nhịp đặt câu hỏi, nhịp sau `[[answer]]` công bố đáp án.
- Không bịa: con số, tính năng, chữ trên giao diện, các bước theo bản gốc; bản gốc không viết thì không bổ sung. Trích dẫn đúng từng chữ.

## Điểm chính khi lồng tiếng MiMo

- Giao diện là chat/completions: nội dung đặt trong tin nhắn assistant, mô tả ngữ khí đặt trong tin nhắn user; trả về WAV mono 24kHz (base64).
- Giọng có sẵn: mimo_default, 冰糖, 茉莉 (nữ), 苏打, 白桦 (nam); tiếng Anh Mia, Chloe, Milo, Dean. voicedesign có thể tạo giọng theo mô tả, voiceclone cần âm thanh mẫu.
- **Bắt buộc thêm mô tả ngữ khí giảng bài**: không thêm thì mỗi giây 5–6,5 chữ, quá vội; thêm vào thì khoảng 4 chữ/giây, rồi dùng `scenes.speed: 1.15` đổi tốc độ (atempo, cao độ không đổi).
- Không có mốc thời gian từng từ → mỗi nhịp tổng hợp nguyên đoạn rồi dùng whisper-cli lấy thời gian token: dùng mô hình small trước, căn không được thì dùng medium; **nhất định phải kèm `--prompt văn-bản-gốc`** (nếu không sẽ ra chữ phồn thể, tỷ lệ căn 65%); token có thể bị cắt giữa ký tự đa byte, phải giải mã UTF-8 tăng dần.
- Song song 2–3 luồng, bị giới hạn 429 sẽ tự động lùi thời gian chờ và thử lại (chậm là bình thường).

## Bẫy cách đọc và lexicon

- **Số La Mã**: từ viết tắt in hoa chỉ gồm I V X L C D M sẽ bị đọc thành số (CLI→一百五十一, MD→一千五百, CC→二百). `tts_mimo.py` đã tự động tách thành từng chữ cái (quy tắc ROMANISH); cli/md viết thường cũng bị đọc lệch, hãy ghi vào lexicon.
- Số phiên bản viết thành "0 点 155 点 1" (chữ 点 là cách đọc dấu chấm trong tiếng Trung).
- Tên riêng tiếng Anh bị đọc lệch (GitHub, GEO, NLP, từ tự đặt) thì thêm vào lexicon, tách chữ cái hoặc thêm dấu cách.
- `odd_numbers` của kiểm tra đọc lại: con số ≥100 xuất hiện trong bản đọc lại mà văn bản gốc không có sẽ được báo bằng ⚠.

## Kiểm tra chất lượng đọc lại (bài nào cũng phải xem voice.log)

- Mỗi nhịp một dòng: thời lượng, số chữ, chữ/giây, tỷ lệ căn, thời gian tổng hợp, độ tương đồng đọc lại, khác biệt.
- Đọc lại < 95% hoặc có ⚠: xóa `build/audio/<nhịp>.*` rồi chạy lại voice, chỉ tổng hợp lại những nhịp này; hai lần đều thấp thì sửa cách diễn đạt (đổi từ đồng nghĩa, tách câu dài) rồi tổng hợp lại.
- Khi khác biệt toàn là chữ đồng âm / tên riêng bị ASR nghe sai, dùng whisper cục bộ nghe lại để xác nhận (`whisper-cli -m <medium> -l zh -nt -f build/audio/B07.wav`, có thể thêm `--prompt "tên riêng"`); đọc đúng rồi thì không cần làm lại. Tên người nhất định phải nghe lại (ví dụ: 苍何 → đọc lại ra 仓颉 là đáng ngờ, nghe lại là 苍和 = cāng hé, đúng).
- MiMo thỉnh thoảng đọc thừa, lặp lại hoặc thêm một từ phủ định ("不"), nghĩa bị ngược thì bắt buộc làm lại.

## Bản tiếng Anh

- narration: `voice.lang = "en"`, giọng có sẵn `Dean` (nam Mỹ), whisper `-l en`, chia đoạn theo từ.
- scenes: `"lang": "en"` (bảng chữ giao diện chuyển sang tiếng Anh, phụ đề ngắt theo câu, rộng 52 ký tự), `"inlineCredits": false`, `"videoOnly": true` (chỉ xuất phim), `shotCredit` viết nguồn bằng tiếng Anh.
- MiMo tiếng Anh thỉnh thoảng đọc thừa/lặp một câu: đọc lại < 95% thì tổng hợp lại.
