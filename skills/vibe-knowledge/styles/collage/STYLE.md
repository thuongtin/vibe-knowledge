# Cắt dán bán sắc · HALFTONE COLLAGE

> Họ: in ấn và giấy | Bậc: bản nâng cao · mỗi đoạn khoảng 2 ảnh sinh (mj-v8.2, 4 điểm/ảnh) | Ảnh phong cách: `still.jpg` | Mã nguồn mẫu: `_samples/styles4_film.js → collage()`

**Một câu**: Ảnh sinh được tách thành hai lớp "nền + chủ thể", chủ thể là mảnh giấy được đập xuống, băng dính, mảnh giấy ghi chú, số lớn bán sắc, con dấu đỏ, cả trang bị đẩy đi để sang trang kế.

| Mục | Cách làm |
|---|---|
| Ý đồ đạo diễn | Cắt dán trên bàn cho tin giải thích: tư liệu được đập lên bàn từng tờ, mỗi nhịp đều có mảnh giấy mới rơi xuống. |
| Chất liệu / Cách vẽ | Bản nâng cao: 2 ảnh cắt dán nguyên tấm mj-v8.2 → Vision tách tiền cảnh lấy lớp chủ thể → vá nền (vùng giấy xanh lục dùng màu đơn + nhiễu, vùng phức tạp dùng inpaint). Code: mảnh giấy rách mép (clip-path răng cưa), băng dính, số lớn chấm bán sắc (background-clip:text), con dấu. |
| Logic phối màu | Đất son #E9A85A · đỏ #D63A2F · xanh lục xám #8F9D83 · giấy #F4ECDD · mực #1D1A16 |
| Phông chữ | Geist 900 cho số lớn bán sắc + NotoSC 900 cho chữ trên mảnh giấy |
| Chuyển động | slap (1,18 → 1 + xoay về thẳng 0,22 giây), slide (eOutQuint 0,3 giây), băng dính trượt vào từ ngoài màn hình; cao trào cả trang page-push 0,35 giây, chủ thể mới bật lên từ dưới. |
| Ngữ pháp máy quay | Đẩy chậm 3% ở lớp ngoài; chuyển cảnh bằng đẩy cả trang. |
| Âm thanh | Mảnh giấy đập xuống bàn, băng dính xé kéo, con dấu; bộ gõ nhẹ vui. |
| Cảnh đặc trưng | Mảnh giấy cổng thành "bộp" một tiếng đập xuống, bị băng dính dán chặt; số "10" là chữ chấm bán sắc đỏ. |

## Sửa được đến mức nào (dùng khi đổi thành "phong cách của tôi")
- **Cứ yên tâm sửa**: đổi giấy nền, đổi màu băng dính
- **Sửa là mất chất**: sinh lại chủ thể trên phông xanh (sẽ không khớp với ảnh gốc)
- **Không được sửa**: vẽ phụ đề và số vào trong ảnh sinh

## Kết hợp
- Bản gốc phù hợp: điểm đau nguyên lý C, lựa chọn lưỡng nan B, một mạch chính D
- Không phù hợp: toán học thuần trừu tượng
- Tiền tố Renoise bản nâng cao: `editorial explainer paper collage, torn paper cutouts printed in halftone dots, masking tape strips, layered cutout drop shadows, flat muted background color, risograph grain, large plain flat area on the left third`
