# Bích họa Đôn Hoàng · DUNHUANG MURAL

> Họ: Phương Đông | Bậc: bản nâng cao · mỗi đoạn khoảng 2 ảnh sinh (mj-v8.2, 4 điểm/ảnh) | Ảnh phong cách: `still.jpg` | Mã nguồn mẫu: `_samples/styles4_film.js → dunhuang()`

**Một câu**: Một lớp vữa bong ra từng mảng để lộ bích họa, bức thứ hai bong ra từ phía bên kia, chữ dát vàng lấp lánh, khung bảng đề.

| Mục | Cách viết |
|---|---|
| Ý đồ đạo diễn | Mở ra kiểu khảo cổ: hình ảnh không phải "xuất hiện", mà được phát hiện dưới lớp vữa tường. |
| Chất liệu / Cách vẽ | Bản nâng cao: 2 bức bích họa mj-v8.2 (nền đỏ đất, lục đá, lam kim, vàng dát, nứt nẻ bong tróc). Code: lớp vữa ngoài màn hình (kết cấu nhiễu hạt) + 144 mảnh đa giác không đều bong ra theo thứ tự khoảng cách (destination-out) + viền mép bong. |
| Logic màu | Đỏ đất #8E2F1E · lục đá #2F6B5E · lam kim #2A4A8A · vữa #E3CFAE · gradient vàng dát #7A5518 → #FFF1B8 |
| Phông chữ | Songti 900 viết dọc; chữ vàng dát dùng gradient tuyến tính chảy background-clip:text; con số đặt vào khung "bảng đề" tối màu |
| Chuyển động | Vữa bong từ phần chính ra ngoài trong 1,5 giây rồi cả lớp mờ dần; ở cao trào bức bích họa thứ hai bong ra từng ô từ phía bên kia trong 0,55 giây; chữ vàng dát lấp lánh lặp vòng. |
| Ngữ pháp ống kính | Đẩy gần chậm + dịch ngang (Ken Burns 5%). |
| Âm thanh | Đá bong tróc, gió cát, chuông lạc đà; đàn cổ cầm / tỳ bà. |
| Cảnh đặc trưng | Từng mảng vữa vỡ rơi xuống, lộ ra cổng thành và đám đông; chữ vàng dát "năm mươi lượng vàng" đứng trong khung bảng đề. |

## Có thể sửa đến mức nào (dùng khi làm thành "phong cách của tôi")
- **Cứ yên tâm sửa**: đổi nội dung bích họa, đổi màu bảng đề
- **Sửa là mất vị**: bích họa quá đầy không chừa vùng vữa (chữ không có chỗ đặt)
- **Không được sửa**: dùng phông chữ không chân hiện đại cho chữ

## Cách phối
- Mẫu gốc phù hợp: D một mạch chính, B lựa chọn lưỡng nan
- Không phù hợp: công nghệ hiện đại, tin tức dữ liệu
- Tiền tố Renoise cấp tăng cường: `Dunhuang Mogao cave mural painting, earth-red ochre ground, malachite green and lapis lazuli blue mineral pigments, touches of gold leaf, flat frontal perspective, cracked and flaking plaster, faded fresco texture, plain empty wall on the left third`
