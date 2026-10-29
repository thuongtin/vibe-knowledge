# Bộ icon ngoại tuyến (định dạng Iconify JSON)

tabler, lucide, iconoir được sao chép từ `~/Desktop/inkflow/data/iconsets/`; IconPark lấy từ `@iconify-json/icon-park*` trên jsDelivr (2026-09-26). Khi render không cần kết nối mạng.

Các bài trong series mặc định dùng IconPark nhiều màu (tiền tố `icon-park:`), `runtime/iconify.js` sẽ đổi bốn màu cố định của nó sang bảng màu macaron.

| Tệp | Bộ icon | Số lượng | Giấy phép |
|---|---|---|---|
| tabler.json | Tabler Icons | 6232 | MIT |
| lucide.json | Lucide | 1834 | ISC |
| iconoir.json | Iconoir | 1682 | MIT |
| icon-park.json | IconPark nhiều màu (ByteDance) | 2658 | Apache-2.0 |
| icon-park-outline.json / -solid / -twotone | IconPark nét, đặc, hai màu | 2658 / 1970 / 1947 | Apache-2.0 |

Dùng `scripts/icons.py` để trích theo tên (như `tabler:robot`) vài icon mà phim dùng tới, đóng vào bundle.
