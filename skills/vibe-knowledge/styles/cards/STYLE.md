# Đấu bài · CARD BATTLE

> Họ: Game | Bậc: cơ bản · 0 điểm | Ảnh phong cách: `still.jpg` | Mã nguồn mẫu: `_samples/styles6_film.js → cards()`

**Một câu**: Trên bàn nhung xanh, thẻ bài lật mặt đánh ra: "Tiền thưởng 10" tấn công "Nghi ngờ" bị bật lại (MISS), đánh ra "×5" thì đập nát nghi ngờ và lật ra chữ "Tín".

| Mục | Cách làm |
|---|---|
| Ý đồ đạo diễn | Biến so sánh lực lượng trừu tượng thành va chạm chỉ số của thẻ bài, thắng ở lá nào nhìn là rõ. |
| Chất liệu / cách vẽ | Nền xanh nhung tia xuyên tâm + bàn bài nét đứt; thẻ lật 3D bằng CSS (preserve-3d + backface-hidden); mặt thẻ: tiêu đề, vùng minh hoạ, chỉ số ở dưới; tia tấn công. |
| Logic phối màu | Bàn #0F3B2E · mặt thẻ trắng kem #FDF7E8 · viền vàng #E9C46A · MISS đỏ #FF5A4E |
| Phông chữ | Tên thẻ NotoSC 900 + chỉ số Geist |
| Chuyển động | Thẻ lật mặt 0.4 giây; đánh bài trượt vào từ phía dưới; tia tấn công 0.25 giây; khi bị chặn thẻ mục tiêu rung + MISS bật ra; thẻ tăng cường rơi xuống, chỉ số thay đổi, phát sáng; thẻ mục tiêu lật. |
| Ngữ pháp ống kính | Cố định nhìn từ trên xuống. |
| Âm thanh | Xào bài, đập bài xuống bàn, tiếng vút tấn công, tiếng ting MISS, kèn chiến thắng. |
| Cảnh đặc trưng | "Tiền thưởng ATK 10" đánh vào "Nghi ngờ DEF ??" bật ra MISS; thêm "×5" thì thẻ nghi ngờ lật thành chữ "Tín" màu vàng. |

## Có thể sửa đến mức nào (dùng khi chỉnh thành "phong cách của tôi")
- **Cứ yên tâm sửa**: đổi tên thẻ và ý nghĩa chỉ số
- **Sửa là mất chất**: bịa chỉ số tuỳ ý thành "dữ liệu thật" (chỉ được là ẩn dụ)
- **Không được sửa**: bỏ va chạm (chỉ bày bài mà không đánh)

## Phối hợp
- Khuôn phù hợp: Lưỡng nan B, Nỗi đau + nguyên lý C
- Không phù hợp: thi từ, văn hoá
- Tiền tố Renoise bậc nâng cao: `(bậc cơ bản không cần)`
