# 08 · Hai mức sản xuất: mức cơ bản (0 điểm) / mức nâng cao (chọn theo cảnh quay)

Nguyên tắc do người dùng đặt ra: **cái gì làm được bằng code thì làm bằng code, Renoise chỉ bổ sung những cảnh code làm không tốt**; lồng tiếng luôn dùng Google Gemini TTS (khóa API Google của người dùng, phí/hạn mức theo Google; không tốn điểm Renoise).
Mỗi kỳ hỏi rõ làm mức nào ngay ở xác nhận 1 (chọn chủ đề); với mức nâng cao thì trước xác nhận 2 liệt kê "danh sách cảnh quay nâng cao + điểm ước tính".

## Mức cơ bản · 0 điểm

| Lớp | Dùng gì |
|---|---|
| Lời dẫn | Google Gemini TTS (giọng có sẵn, mặc định Sulafat; chỉ dẫn diễn đọc `director`) + voice_post.py hậu kỳ giọng nói (tùy chọn) |
| Hình ảnh chính | **Opus viết trực tiếp minh hoạ SVG** (nhân vật vector phẳng / kiến trúc / đồ vật / đường viền bản đồ), dùng `layers` chia ba lớp xa, giữa, gần để tạo chuyển động thị sai; hạt, camera 3D, shader của cine (Particles, Tunnel, Liquid…) dùng cho khái niệm trừu tượng |
| Dữ liệu và thông tin | know.js: counter, bars, spread, trail, vquote, keyword, chapter, foot |
| Nhạc nền | **Mặc định: vibe-bgm đi kèm skill** (`tools/fit_bgm.py <out.wav> --lesson <thư mục kỳ>` cắt theo ô nhịp phù hợp độ dài phim, dùng chung cho cả hai mức); chỉ khi cần đổi bài mới dùng thư viện nhạc promo-video (`python3.12 ~/.claude/skills/promo-video/scripts/pick_music.py <out.wav> --mood … --seconds … --hit-at <giây hiện tên phim>`, cần numpy, chạy bằng python3.12); hoặc dùng bed.py của cine để tổng hợp theo sections |
| Hiệu ứng âm thanh | Tích hợp sẵn trong cine (slam whoosh riser impact chime tick shutter card …, ghi vào sfx) |
| Tư liệu | Có thể dùng tư liệu phạm vi công cộng / CC (tranh cổ Wikimedia Commons, ảnh sách cổ, ảnh NASA), ghi tên tác giả vào cuối phim và facts.md; không dùng ảnh không rõ nguồn gốc |

**Làm thế nào để mức cơ bản đạt chất lượng cao**:
- Mỗi cảnh có ít nhất ba lớp SVG (bóng hình viễn cảnh, chủ thể trung cảnh, vật che tiền cảnh), khi chuyển động có chiều sâu.
- Nhân vật dùng kiểu "hình học hoá không ngũ quan" (kiểu Iwanau), Opus vẽ ổn định, cả kỳ thống nhất, cũng không có rủi ro về chân dung.
- Mỗi chương một cảnh "bom tấn bằng code": hạt tụ thành chữ, điểm sáng biến hình, bản đồ lan toả, camera 3D xuyên qua, thay cho cảnh động của mức nâng cao.
- Bảng màu tuân thủ nghiêm hệ thống hình ảnh (03-visual-systems.md), hạt nhiễu và vignette do `bg()` kiểm soát thống nhất.

## Mức nâng cao · chọn theo cảnh quay, điểm kiểm soát được

**Xác định cảnh nào đáng dùng Renoise** (thoả mãn bất kỳ điều nào):
1. Cảnh tả thực mà code không vẽ được: hiện trường lịch sử, hiện tượng tự nhiên (bão sấm, lũ lụt, tinh vân), chất liệu thật (đồng thau, lụa, vân giấy sách cổ).
2. 1–3 khoảnh khắc cần được nhớ nhất trong cả phim: mở đầu lạnh, đảo chiều, cao trào.
3. Cần chuyển động thật: đám đông, dòng nước, lửa, máy móc vận hành.

Các cảnh còn lại (dữ liệu, bản đồ, chữ, biểu đồ, khái niệm trừu tượng, hoạt hình minh hoạ) **vẫn dùng code**.

| Cấp nâng cao | Nội dung | Điểm ước tính |
|---|---|---|
| Nhẹ | 3–8 ảnh minh hoạ then chốt (MJ) + 2–5 hiệu ứng âm thanh (nhạc nền dùng BGM mặc định, không tạo thêm) | ≈ 15–35 |
| Chuẩn | 6–10 ảnh minh hoạ + 2 cảnh động (Wan 3.0 720p 8s, khung đầu dùng ảnh minh hoạ) + 6 hiệu ứng âm thanh | ≈ 240–290 |
| Cao cấp | 10–14 ảnh minh hoạ + 3 Wan + 1 Seedance 2.5 (cảnh cao trào) + 8 hiệu ứng âm thanh | ≈ 590–690 |

Đơn giá xem 04-renoise.md (Midjourney 4/ảnh, GPT Image 13/ảnh, Wan 720p 8s 96, Seedance 720p 8s 256, Lyria 4/bài, hiệu ứng âm thanh 0.4/giây).
Trước mỗi lần tạo vẫn báo giá như thường và chờ người dùng xác nhận; ảnh và video tạo ra ưu tiên đặt vào các cảnh đã dựng bằng code để "thay ảnh nền", không đổi cấu trúc cảnh, nhờ vậy mức nâng cao và mức cơ bản có thể dùng chung một film.js (khi `const ENH = true` thì dùng plate/vclip, ngược lại dùng layers).

## Cách viết để một film.js dùng chung cho cả hai mức

```js
const ENH = false;   // mức nâng cao đổi thành true (assets/ có tệp tương ứng)
const scene01 = (s) => ENH
  ? plate(s, { src: A("img/a01.jpg") })                                   // ảnh minh hoạ Renoise
  : layers(s, [{ svg: SVG_SKY, depth: 0.15 }, { svg: SVG_PALACE, depth: 0.5 }, { svg: SVG_FG, depth: 1 }]);   // ba lớp do Opus vẽ tay
// trong render, chữ ký update của hai nhánh giống nhau: x.update(t, t0, t1, { … })
```
