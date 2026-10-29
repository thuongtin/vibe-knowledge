# Hộp thoại RPG · RPG DIALOGUE

> Họ: game | Bậc: bản cơ bản · 0 điểm | Ảnh phong cách: `still.jpg` | Mã nguồn mẫu: `_samples/styles6_film.js → rpg()`

**Một câu**: Cảnh pixel ở trên, hộp thoại xanh đậm ở dưới hiện chữ từng ký tự, trong menu lựa chọn ai cũng dừng ở "Chờ xem", con trỏ năm mươi vàng nhảy sang "Khiêng", hiện ra "Nhận 50 vàng!".

| Mục | Cách làm |
|---|---|
| Ý đồ đạo diễn | Biến lựa chọn lưỡng nan thành các tuỳ chọn trong RPG: khán giả tự nhiên nhập vai "mình sẽ chọn cái nào". |
| Chất liệu / Cách vẽ | Tranh pixel 240×90 phóng to 8 lần (dải màu bầu trời, cổng thành, dân làng, nhân vật chính) + hộp thoại viền đôi xanh đậm + bảng tên + menu lựa chọn + khung nhận vật phẩm. |
| Logic phối màu | Gradient xanh bầu trời đêm · hộp thoại #141A46 · viền trắng #F4F4F4 · con trỏ / vật phẩm nhận được #FFD84A |
| Phông chữ | NotoSC 700–900 (hội thoại 56px) |
| Chuyển động | Gõ chữ 22 ký tự/giây; ▼ nhấp nháy; con trỏ menu nhảy giữa các lựa chọn; khung nhận vật phẩm bật ra; nhân vật chính đi tới vác khúc gỗ lên. |
| Ngữ pháp máy quay | Cố định. |
| Âm thanh | Tiếng bíp gõ chữ, tiếng tích của con trỏ, âm kèn nhỏ khi nhận vật phẩm; nhạc nền 8-bit. |
| Cảnh đặc trưng | Menu lựa chọn "Khiêng / Chờ xem", con trỏ dừng ở "Chờ xem" — không ai nhúc nhích. |

## Sửa được đến mức nào (dùng khi đổi thành "phong cách của tôi")
- **Cứ yên tâm sửa**: đổi cảnh, đổi bảng tên
- **Sửa là mất chất**: hộp thoại hiện nguyên cả câu một lần
- **Không được sửa**: bỏ menu lựa chọn (đây là cốt lõi của lựa chọn lưỡng nan)

## Kết hợp
- Bản gốc phù hợp: lựa chọn lưỡng nan B, vượt màn E
- Không phù hợp: dữ liệu thuần tuý
- Tiền tố Renoise bản nâng cao: `(bản cơ bản không cần)`
