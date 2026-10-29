# 05 · Hệ thống thị giác

Triển khai: `runtime/theme.js` (token chủ đề, cỡ chữ, khung hình và vùng an toàn), `runtime/stage.js` (style cơ bản).

## Hai bộ chủ đề

| token | Xanh bản vẽ tối `blueprint` (mặc định) | Biên tập sáng `editorial` |
|---|---|---|
| Màu nền `bg` | `#0A1024` + lưới mảnh 64 px + tối góc | `#ECEAE6` (xám ấm, giống hình đơn của promo) |
| Mặt `surface` / `surface2` | `#111A33` / `#17234A` | `#FFFFFF` / `#F5F3EF` |
| Đường `line` | `#2A3963` | `#D8D3CB` |
| Chữ `ink` / `ink2` / `ink3` | `#EAF0FF` / `#A9B5D6` / `#6F7CA3` | `#141414` / `#4A4843` / `#8A8680` |
| Nhấn `hl` | `#FFD84D` (token vòng lặp, điểm nóng của bài giảng) | Giống bên trái |

Bộ thứ ba tùy chọn "bảng đen vẽ tay" dùng lại kinh nghiệm chalk của InkFlow, làm sau M3.

## Màu theo vai trò (cố định toàn series, xem một tập là nhận ra)

| Vai trò | Blueprint | Editorial | Dùng cho |
|---|---|---|---|
| Người dùng `user` | `#5B8CFF` | `#2B62F0` | Bạn, đầu vào, thứ được giao cho bạn |
| Mô hình `model` | `#A57CFF` | `#7446EC` | Mô hình, suy nghĩ |
| Công cụ và hành động `tool` | `#2ED39A` | `#0B8F66` | Đọc file, chạy lệnh, sửa code |
| Môi trường và dữ liệu `env` | `#8E9CC0` | `#636B7D` | Kho mã, file, kết quả quan sát được |
| Ranh giới và rủi ro `boundary` | `#FF8A4C` | `#D2500F` | Sandbox, phê duyệt, giới hạn |

Mỗi vai trò còn có một màu nền nhạt `<role>-t`, dùng để tô nút. Màu thể hiện "ai đang hành động", không dùng để trang trí.

## Mã hóa trung thực

| Trạng thái | Cách vẽ | Nhãn |
|---|---|---|
| Công bố chính thức `official` | Viền nét liền | — |
| Suy đoán `inferred` | Viền nét đứt `12 9`; đường nối nét đứt `10 8` | "Suy đoán" |
| Chưa công bố `undisclosed` | Tô mờ bằng sọc chéo 45° | "Chưa công bố" |
| Tái hiện giao diện | — | "Minh họa giao diện" ở góc trên trái |

## Phông chữ và cỡ chữ (pixel ở 1920×1080)

- Phông chữ: Geist (Latin) + Noto Sans SC (Source Han Sans, chữ Trung), đơn cách dùng Geist Mono; cả ba đều là phông biến thiên độ đậm, đặt trong `assets/fonts`, render không cần mạng.
- Cỡ chữ: tiêu đề chương lớn 88, tiêu đề cấp hai 60, nhãn nút 34–40, nhãn thường 32, nhỏ nhất 28, phụ đề 44, code 26–30.
- Cỡ chữ thực tế trên màn hình = cỡ chữ thiết kế × tỉ lệ cảnh × tỉ lệ ống kính. Khi phóng to từng lớp, lớp kế tiếp dùng cỡ chữ thiết kế lớn hơn để bù tỉ lệ (Spike: lớp bên trong cỡ chữ thiết kế 40, tỉ lệ 0,16, ống kính 5,3–6,5, trên màn hình khoảng 34–42 px).
- 9:16 cỡ chữ × 1,2, văn bản chính không nhỏ hơn 40.

## Bố cục

| | 16:9 (1920×1080) | 9:16 (1080×1920) |
|---|---|---|
| Lề an toàn trái phải | 96 | 72 |
| Lề an toàn trên | 72 | 120 |
| Đường trên của dải phụ đề | 890 | 1500 |

Phụ đề: 44 px, độ đậm 500, nền viên thuốc tối bán trong suốt, mỗi dòng ≤ 18 chữ, ngắt dòng ở chỗ ngắt câu; từ khóa lên màn hình tối đa 3 từ mỗi beat, mỗi từ ≤ 8 chữ.

## Token chuyển động (`runtime/spring.js`)

| Tên | Tần số / giảm chấn | Dùng cho |
|---|---|---|
| `UI` | 2,1 Hz / 0,82 (vọt quá khoảng 1,5%) | Kích thước hình, bo góc, màu |
| `CURSOR` | 2,4 Hz / 1 (không vọt quá) | Con trỏ |
| `CAM` | 1,25 Hz / 0,95 | Đẩy kéo ống kính |
| `PRESS` | 5 Hz / 0,75 | Nảy lại khi nhấn |
| `LEAD` / `TRAIL` | 3,2 Hz / 0,86 · 1,7 Hz / 0,9 | Hai mép trước và sau của thanh chỉ thị, nút tròn của công tắc |
| `REVEAL` | 1,8 Hz / 0,9 | Phần tử xuất hiện, sáng lên |

Chuyển nội dung: mờ vào 0,18 giây (expo.out), mờ ra 0,1 giây. Một trạng thái đã ổn định thì dừng ít nhất 0,6 giây rồi mới đổi (chế độ giảng giải).

Cấm: nảy lại quá đà, hạt bùng nổ, quầng sáng, gradient trên giao diện, độ dày nét biểu tượng không nhất quán, nhịp trống, chuyển cảnh phô diễn không liên quan đến nội dung.

## Biểu tượng

Tập con biểu tượng nét của lucide (giấy phép ISC), nhúng trực tiếp trong `ICONS` của `runtime/dom.js`, lưới 24, độ dày nét 1,75. Biểu tượng thiếu thì lấy path từ lucide bổ sung vào, không tải tạm từ mạng.
