# 04 · Biến hình UI một hình dạng (Morph)

Một hình dạng từ đầu đến cuối không bị cắt: kích thước, bo góc, màu viền đều do lò xo điều khiển; nội dung của mỗi trạng thái vào ra bằng hiệu ứng mờ ngắn, con trỏ dùng cú nhấp thật để thúc đẩy thay đổi. Chuyển từ chế độ one-shape của promo-video (`references/one-shape.md`, `spring.ts`, `examples/morph-loop`, `morph-promo`), cài đặt nằm trong `primitives/morph.js`.

## Khác biệt giữa bản giảng dạy và bản phim quảng bá

| | Bản phim quảng bá (promo-video) | Bản giảng dạy (bài phân tích tháo máy) |
|---|---|---|
| Nhịp điệu | Mỗi nhịp một động tác, đúng 7 ô nhịp | **Xem nhanh**: hai nhịp một trạng thái (120 BPM khoảng 1 giây), một câu lời dẫn lướt qua cả quy trình; **giảng giải**: mỗi trạng thái ít nhất một ô nhịp, làm tròn thành ô nhịp theo độ dài lời dẫn |
| Bắt đầu và kết thúc | Khung đầu = khung cuối, cả phim lặp vòng | Mọc ra từ nút trên sơ đồ tổng (`from` = hình học của nút), diễn xong co lại; nút dùng `open/close` để nhường chỗ; chỉ khi xuất riêng bản lặp vòng mới yêu cầu khung đầu cuối giống nhau |
| Trạng thái từ đâu ra | Soạn theo điểm bán hàng | Phải là các bước thật của sản phẩm, mỗi trạng thái gắn một sự thật; góc ghi "minh họa giao diện" |
| Màu sắc | Đen trắng thêm một màu nhấn | Viền theo màu vai trò "ai đang hành động": người dùng xanh lam, mô hình tím, công cụ xanh lục, ranh giới cam |
| Âm thanh | Âm thanh UI là nhân vật chính | Căn theo đỉnh đo thực tế, đặt dưới lời dẫn (-12 đến -22 dB) |
| Phông chữ | Geist, tiếng Trung quay về PingFang | Geist + Source Han Sans (độ đậm biến thiên, file cục bộ) |

## Cách định thời gian (cách đã chạy thông trong Spike)

1. Lời dẫn gọi tên từng trạng thái, và chèn cue ở phía trước: `Nhìn từ phía bạn: [[input]]bạn giao nhiệm vụ, [[run]]nó bắt đầu chạy, [[term]]chạy lệnh……`
2. Sau khi lồng tiếng, thời điểm cue chính là điểm chuyển trạng thái; sau đó làm tròn về lưới 0,25 giây (nửa nhịp của 120 BPM), độ lệch giữa hình và lời dẫn không quá 0,125 giây.
3. Hình dạng mọc ra từ nút 0,45 giây trước trạng thái đầu tiên, co lại 0,8 giây trước khi câu cuối kết thúc.
4. Mỗi trạng thái của máy quay zoom-to-fit: `z = min(0.52·W / w, 0.46·H / h, 2.0)`, tiêu điểm thấp hơn tâm hình dạng 34 px, để hình dạng nằm phía trên dải phụ đề.
5. Con trỏ đến vị trí cần nhấn sớm ít nhất 0,5 giây (giảm chấn tới hạn, không vọt quá), nhấn 0,12 giây; hình dạng đồng thời bị ép nhẹ xuống 0,985.

## Thư viện trạng thái

| Loại | Công dụng | Tham số | Trạng thái |
|---|---|---|---|
| `input` | Nhập yêu cầu | `text`, `typeAt`, `cps`, `sendAt` | ✅ |
| `loader` | Bắt đầu chạy, chờ | — | ✅ |
| `terminal` | Chạy lệnh | `lines[{kind,text,at}]`, `title` | ✅ |
| `diff` | Sửa code | `file`, `lines[{k,text,at}]` | ✅ |
| `approve` | Công tắc phê duyệt | `text`, `toggleAt` (nút tròn hai bên chạy lò xo LEAD/TRAIL) | ✅ |
| `toast` | Thông báo, bàn giao | `title`, `sub`, `icon` | ✅ |
| `chat` | Hội thoại xuất theo dòng chảy | `messages[]` | ○ |
| `button` / `check` / `island` / `player` / `scrub` / `slider` / `tabs` / `chart` / `cmdk` | Trạng thái UI thông dụng (cả hai ví dụ promo đều có, viết lại khi cần) | xem `Reel.tsx` của promo | ○ |

Thêm loại mới: thêm `build(state, ctx) → {el, render(dt)}` vào `KINDS`, `dt` là số giây kể từ khi vào trạng thái đó.

## Khoảng trống đã biết

- Biến hình biểu tượng (kiểu phát ↔ tạm dừng): chưa có cài đặt sẵn.
- Bố cục 9:16: kích thước hình dạng và máy quay phải tính lại cho màn hình dọc.
- Ở chế độ xem nhanh, các trạng thái như sửa code chỉ dừng khoảng 0,75 giây, đọc không kịp; đây là chủ ý (xem nhanh chỉ để tạo cảm giác thứ tự), muốn nhìn rõ thì dùng chế độ giảng giải hoặc CodeDiff độc lập.
