# 03 · Hệ thống thị giác

Mỗi tập chọn một hệ, viết vào film.js dạng `const TM = TH.xxx`, và chép tiền tố phong cách vẽ tương ứng vào `style_prefix` của assets.json.

| Hệ thống | Chuẩn đối chiếu | Phù hợp | Màu nền / màu nhấn | Tiền tố phong cách vẽ Renoise (viết bằng tiếng Anh cho mô hình) |
|---|---|---|---|---|
| `starfield` Điểm sáng sao trời | Điện Tử Trí Nhân "Học thuyết XX" | Khái niệm trừu tượng, thông tin, toán học, vũ trụ (khuôn A) | Xanh đen thẫm / vàng #f2c46d | `Cinematic dark night scene, deep navy and black, a single warm golden light source, fine film grain, minimal, vast negative space, no text` |
| `gufeng` Vector cổ phong | Iwanau "Nếu bạn sống thời cổ đại" | Lưỡng nan lịch sử (khuôn B) | Đen đất son màu đêm / đỏ son #d9472b + vàng | `Flat vector illustration, Chinese Tang dynasty, simple geometric characters without facial detail, red palace walls and lanterns, muted ink-paper texture, cinematic wide shot, no text` |
| `darkgold` Nét vàng tối | Mặc Hữu Ý Tư, FredTao | Nguyên lý điểm đau, một mạch chính (khuôn C / D) | Đen than / hổ phách #f0b44c | `Minimal line-art illustration, glowing amber lines on charcoal black, warm rim light, editorial, lots of empty space, no text` |
| `paper` Thủy mặc giấy bản | Đoạn gia phả trong lịch sử gia tộc opus | Văn hóa, văn học, lịch sử gia tộc, phần kết lịch sử công nghệ (khuôn D / F) | Giấy trắng ngà / chu sa #b23a2e | `Chinese ink wash painting on warm rice paper, sparse composition, soft grey washes, a single vermilion accent, no text, no seal` |
| `pixel` Pixel | Khảo Oa Oa, Hùng Miêu Sư Huynh | Vượt ải, phương pháp luận (khuôn E) | Chàm thẫm / vàng sáng #ffd23f | `16-bit pixel art, side view game scene, bold limited palette, crisp pixels, no text, no UI` |

## Phim mẫu đã kiểm chứng (2026-10-27)

Cả 5 bộ đều đã dùng code render cùng một đoạn mở đầu: `~/Desktop/vibe-knowledge/examples/vk/lessons/styles/film.js` (mỗi bộ một hàm vẽ: gufeng dùng bóng đen phân lớp của 01/scenes_base.js; starfield dùng bụi sao canvas + điểm sáng vàng vẽ đường + chữ Songti mảnh; darkgold dùng nét SVG màu hổ phách vẽ từng nét + thanh pin; paper dùng gradient giấy Tuyên + feGaussianBlur loang núi xa + feTurbulence mép bút lông + chữ Songti viết dọc + con dấu chu sa; pixel dùng canvas 240×135 phóng to 8 lần image-rendering:pixelated). Tập mới chọn bộ phong cách nào thì trước hết chép hàm tương ứng từ đây làm điểm khởi đầu.
Thành phẩm: `~/Desktop/Vibe知识大赏_视频/styles_风格样片集.mp4`, hình đối chiếu nằm cùng thư mục.
Lưu ý: số nhịp của timings tự định nghĩa bắt buộc phải là `B` + chữ số (engine chỉ nhận B\d+), nếu không trang sẽ báo "cách viết thời gian không đúng".

## Cắt dán thời đại (dành riêng cho khuôn D)

Cách làm của lịch sử gia tộc opus: mỗi thời đại một phong cách vẽ, nhưng thống nhất "ánh sáng điện ảnh ấm + hạt mịn + khổ rộng 16:9". Ví dụ:
- Tiền sử: `cave painting on rough rock wall, ochre handprints, torch light`
- Hy Lạp cổ đại: `ancient bronze mechanism under the Aegean sea, god rays, particles`
- Thời kỳ hoàng kim Hồi giáo: `Persian miniature painting style, House of Wisdom library, scholars`
- Trung Quốc cổ đại: `Chinese ink wash landscape, misty mountains`
- Cách mạng công nghiệp: `19th century Jacquard loom, warm workshop light, oil painting`
- Thế kỷ 20: `1950s Bell Labs, mid-century modern collage, Bauhaus shapes`
- Đương đại: `warm laptop glow in a dark room, cinematic shallow depth of field`

## Phông chữ và bố cục

- Tiếng Trung dùng NotoSC (900 từ khóa / 700 tiêu đề phụ / 500 nội dung chính), số dùng Geist, code dùng GeistMono (cine có sẵn).
- Từ khóa căn giữa hoặc căn trái tại x=110; bảng chương cố định ở góc trái trên (110, 70); nhãn AI cố định ở góc phải trên.
- Cổ văn viết dọc dùng vquote (nền giấy), đặt ở 1/4 bên phải.
