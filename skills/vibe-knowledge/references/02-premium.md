# 02 · Tiêu chuẩn tinh phẩm (qua từng mục trước khi giao mỗi kỳ)

Yêu cầu của người dùng: mỗi kỳ đều phải tinh xảo hơn các blogger hiện có, "tung ra là thiết kế tinh phẩm". Dưới đây là tiêu chuẩn cứng, không đạt thì không giao.

## Hình ảnh

1. **Bố cục ba lớp**: mỗi cảnh quay ít nhất có hai trong ba lớp "nền (ảnh minh họa / cảnh quay động / màu nền chủ đề) + động (vệt sáng, hạt, bộ đếm, đẩy kéo) + thông tin (từ khóa / số / xuất xứ)"; không có cảnh nào chỉ một dòng chữ đè lên nền đơn sắc.
2. **Không có hình ảnh đứng yên quá 3 giây**: ảnh minh họa luôn đẩy kéo lia dời (from/to của plate), từ khóa có hoạt ảnh vào ra, cảnh dài có ít nhất một chuyển động phụ (bụi sáng, thị sai, số nhảy).
3. **Mỗi chương ít nhất một cảnh "vương bài" thị giác chính**: bản nâng cao dùng cảnh quay động Renoise (vclip), bản cơ bản dùng code (hạt tụ thành chữ, điểm sáng biến hình, bản đồ lan rộng, xuyên 3D, thị sai SVG ba lớp); đặt ở các vị trí hook, đảo ngược, cao trào, những chỗ "cần được nhớ".
4. **Cả kỳ một hệ thống thị giác**: chủ đề (TH.*) + tiền tố họa phong thống nhất (style_prefix trong assets.json) + một bộ phông chữ, không pha trộn. Các thời đại khác nhau có thể đổi họa phong (bản gốc D), nhưng nhiệt độ màu và hạt phải thống nhất.
5. **Chữ**: từ khóa trên hình ≤8 chữ, cùng màn hình tối đa hai nhóm; phụ đề ở dưới 940–1030, chú thích cuối ở 1044, từ khóa không vào y>900; chữ Trung dùng NotoSC 900/700, số dùng Geist.
6. **Trong ảnh minh họa không được có chữ do AI tạo** (prompt viết no text, no letters, no watermark); mọi chữ Trung đều do code chồng lên. Ảnh tạo ra có chữ loạn thì làm lại hoặc cắt bỏ.
7. **Nhân vật, cảnh do AI tạo ghi "Hình minh họa AI"**; không tạo khuôn mặt người thật còn sống; nhân vật lịch sử ghi "Tạo hình nhân vật chỉ mang tính minh họa".

## Âm thanh

0. **Nhịp điệu (yêu cầu cứng người dùng chốt ngày 10-27: nhịp nhanh kiểu blogger công nghệ, không được tụt)**: tốc độ nói của thành phẩm 5,5–6 chữ/giây; quãng nghỉ giữa câu ≤0,35 giây; giữa các nhịp ≤0,25 giây (lồng tiếng dùng `--gap 0.2 --lead 0.3`, đừng dùng mặc định 0,8 của make_lesson); trong phần mô tả giọng điệu cấm viết "để trống, ngừng nghỉ, chậm lại"; trong 20 giây đầu thông tin cứ 2–3 giây lại tiến một bước (mười lạng vàng → không ai nhúc nhích → năm mươi lạng vàng → có người khiêng → chuyện thật → đến lượt bạn). Chuyển hình theo từng câu lời dẫn, đoạn đầu cứ 1,5–2 giây một cảnh.

1. **Phân lớp**: lời dẫn (Google Gemini TTS + hậu kỳ giọng voice_post, tùy chọn), nhạc nền (bản cơ bản dùng thư viện nhạc / tổng hợp; bản nâng cao Lyria Pro làm riêng theo đoạn của kỳ này), hiệu ứng âm thanh (engine có sẵn slam/whoosh/chime; bản nâng cao bổ sung ElevenLabs tạo từng cái), âm thanh môi trường (bản nâng cao dùng âm thanh gốc của video Renoise, ép xuống khoảng −20 dB làm nền).
2. Nhạc nền viết theo cấu trúc bản gốc: mở đầu lạnh để trống hoặc tối giản → B02 tại chỗ tên phim **đến lần đầu tiên** → giữa các chương nhấp nhô nhỏ → chỗ đảo ngược rút trống 1–2 giây → khi kết thúc quay lại câu hỏi chỉ còn một nhạc cụ.
3. Khoảnh khắc then chốt (tiết lộ, đảo ngược, câu vàng) một hiệu ứng âm thanh, cả phim ≤8 cái, đừng từ khóa nào cũng kêu.
4. Độ ồn: tổng thể khoảng −14,5 LUFS, true peak ≤ −1 dBTP (qa.py sẽ báo).

## Nội dung

1. Mỗi dòng trong facts.md đều có xuất xứ; đọc lại OCR (qa.py → ocr.txt) đối chiếu từng mục, số trên màn hình hoàn toàn khớp facts.md.
2. Rà soát đối kháng (mở một sub-agent khác, chỉ bắt ba loại lỗi): hook không trực diện, sự thật không có xuất xứ, chữ trên hình quá nhiều.
3. Câu hỏi ở phần kết phải là câu khán giả có thể trả lời bằng một từ (về / không về, chọn A / chọn B), thuận tiện cho tương tác ở phần bình luận.

## Thông số bàn giao

- 1920×1080 · 60fps bản master (cine record); bản chia sẻ CRF 23, bitrate chặn trên 6M (deliver.sh).
- Ảnh bìa: khung hình thẻ tiêu đề hoặc khung hình thị giác chính + tiêu đề lớn, mỗi tỉ lệ 3:4 và 16:9 một ảnh.
- Thẻ cuối phim 2,5 giây: tên phim + "Vibe Tri Thức Đại Thưởng · Phim này do Claude Opus 5.5 thực hiện".
