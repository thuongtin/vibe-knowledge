# Vẽ tay quá trình · HAND-DRAWN PROCESS

> Họ: Đồ giải và thiết kế | Cấp độ: cơ bản · 0 điểm | Ảnh phong cách: `still.jpg` | Mã phim mẫu: `_samples/styles10_film.js → sketch()`

**Một câu**: Một bàn tay cầm bút chì vẽ cho bạn xem suốt: bút chì phác → đường mực vẽ lại → bút dạ tô qua lại → chữ viết tay, máy quay đi theo tay, cuối cùng kéo xa xem toàn hình.

| Mục | Cách viết |
|---|---|
| Ý đồ đạo diễn | Phim giảng giải bảng trắng / vẽ tay (kiểu RSA Animate): khán giả xem không phải một thành phẩm mà là quá trình "vẽ ra", sự chú ý bị đầu bút dắt đi. |
| Chất liệu / cách vẽ | Một tờ giấy trắng ngà lớn hơn màn hình (2600×1460) + vân giấy chấm mịn; cùng một đường SVG vẽ hai lượt: trước là bản phác bút chì xám nhạt (lệch 3px, vẽ xong nhanh), rồi đường mực bút kim đen vẽ theo dash; chữ viết tay = chữ khải + clipPath mở từ trái sang phải; bút dạ = một nét to 46px quét qua lại trong clipPath của hình (chồng màu multiply); bàn tay SVG nguyên bản + bút chì thân vàng đầu đỏ, đầu bút cố định ở điểm cuối của nét hiện tại. |
| Logic phối màu | Giấy #FBF8F2 · bút chì #B9B2A6 · mực #23201C · đỏ chấm bài #D7392B · bút dạ: mái nhà #E46A4A / xu vàng #F2C14E / tường #F3D9B4 |
| Phông chữ | Chữ khải 700 (chữ viết tay) |
| Chuyển động | Bản phác bút chì 0,3 giây một nét lần lượt vẽ ra → đường mực vẽ từng nét theo thứ tự lời dẫn (mỗi nét 0,1–0,4 giây), đầu bút của tay dùng getPointAtLength đi theo; khi viết chữ tay đi theo mép clip; khi dừng bút tay nhấc lên 26px; tô màu tiến theo nét qua lại; cuối cùng tay trượt ra khỏi khung. |
| Ngữ pháp ống kính | Theo dõi kiểu bảng trắng: vẽ trên tờ giấy lớn, máy quay 0,42 giây trượt êm đến vùng kế tiếp, cuối cùng kéo xa về 0,66 lần để xem toàn hình. |
| Âm thanh | Bút chì sột soạt, bút dạ ken két, lật giấy; guitar gỗ hoặc ukulele nhẹ nhàng. |
| Cảnh đặc trưng | Tay gạch bỏ "10", dùng bút đỏ viết "50" lên trên, rồi bút dạ tô đầy xu vàng và mái nhà từng nét. |

## Có thể sửa đến mức nào (dùng khi làm thành "phong cách của tôi")
- **Cứ yên tâm sửa**: đổi màu giấy (bảng trắng / giấy kraft / giấy kẻ ô), đổi màu bút, đổi màu da và tay áo của bàn tay
- **Sửa là mất vị**: ngay từ đầu đã hiện bản vẽ nét hoàn chỉnh (mất quá trình)
- **Không được sửa**: bỏ tay và bút (thành hoạt hình nét vẽ thường)

## Cách phối
- Mẫu gốc phù hợp: nguyên lý điểm đau C, vượt ải E, một mạch chính D
- Không phù hợp: đề tài cần hình ảnh chân thực
- Tiền tố Renoise cấp tăng cường: `(cấp cơ bản không cần). Thủ pháp tham khảo cách làm công khai của hoạt hình bảng trắng như RSA Animate, tay, bút và hình ảnh đều là nguyên bản`
