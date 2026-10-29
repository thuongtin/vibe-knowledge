# Tin tức phụ đề · CAPTION NEWS

> Loại: Dựng phim và phi hư cấu (mới thêm, ý tưởng tham khảo Lemo-Opuscar) | Ảnh phong cách: `still.jpg` | Mã nguồn mẫu: `_samples/styles2_film.js → captionNews()`; thành phần capNews / srcChip

**Một câu**: tắt tiếng vẫn xem hiểu được: phụ đề siêu lớn làm nhân vật chính, từ khoá đè lên khối vàng, số chạy, nguồn trượt vào.

| Mục | Cách viết |
|---|---|
| Ý đồ đạo diễn | Nhanh, bắt mắt, thông tin rõ ràng; lướt feed là hiểu ngay. |
| Chất liệu / Cách vẽ | Hình ảnh hiện trường thật hoặc do AI tạo được làm tối (brightness 0.38) làm nền; chữ lớn đè lên trên. |
| Logic màu | Nền: hình ảnh đã làm tối · chữ #ffffff · khối vàng #ffd600 (chỉ đè từ khoá) · chữ đen #111 trên khối vàng. |
| Phông chữ | NotoSC 900, cỡ chữ 110–150, một câu mỗi màn hình. |
| Chuyển động | Từng từ bật vào (lệch nhau 0.16 giây), khối vàng quét đầy từ trái sang phải; số nhảy vào vị trí; nhãn nguồn trượt vào theo chiều ngang. |
| Ngữ pháp ống kính | Ảnh nền đẩy gần chậm, phụ đề cắt cứng khi đổi câu. |
| Âm thanh | Nhịp điện tử dồn dập hoặc không nhạc nền, hiệu ứng tích tắc đánh dấu từng từ khoá. |
| Cảnh đặc trưng | Từ khoá đè lên khối vàng + nhãn nguồn trượt vào bên cạnh. |

## Có thể sửa đến mức nào (dùng khi chuyển thành "phong cách của tôi")
- **Sửa thoải mái**: đổi màu khối vàng (màu thương hiệu), đổi tên chuyên mục ở góc, ảnh nền
- **Sửa là mất chất**: một màn hình đặt từ hai câu trở lên (mất khả năng đọc khi tắt tiếng)
- **Không được sửa**: bỏ phụ đề siêu lớn

## Kết hợp
- Mẫu gốc phù hợp: tin nóng nhanh, B có đảo chiều, A dạng dữ liệu; có thể chồng lên bất kỳ hệ thống hình ảnh nào để làm "chuyên mục tin nhanh"
- Không phù hợp: phim dài cần kể chuyện bằng nhiều hình ảnh
- Tiền tố Renoise của mức nâng cao: `(ảnh nền dùng tiền tố của hệ thống hình ảnh tương ứng, làm tối rồi mới dùng)`
