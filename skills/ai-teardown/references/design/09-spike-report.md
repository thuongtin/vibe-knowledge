# 09 · Báo cáo Spike của engine

## Đã làm gì

Cùng một đoạn 32 giây (nửa đầu "sơ đồ tổng → đẩy vào bên trong Codex → vòng lặp Agent", nửa sau "xem nhanh luồng một hình"), cùng một tệp đóng gói `spike/build/app.js` (73 KB, gồm runtime, 3 nguyên ngữ, phụ đề, con trỏ), gắn vào ba host:

| Host | Điểm vào | Mã tích hợp |
|---|---|---|
| Hyperframes 0.6.119 | `spike/hf/index.html` | Khoảng 40 dòng: lắng nghe `hf-seek`; giao thức sẵn sàng `__hfTimelinesBuilding`; một timeline GSAP rỗng chỉ khai báo thời lượng |
| Remotion 4.0.408 | `spike/remotion/src/Spike.tsx` | Khoảng 60 dòng: `delayRender` chờ phông chữ và dựng sân khấu, `seek(frame / fps)` trong `useLayoutEffect` |
| Bài giảng tương tác | `spike/lesson.html` | Không cần engine nào: sân khấu kết xuất thẳng trong trang, `<audio>` làm đồng hồ chính |

Lồng tiếng edge-tts Vân Hi (-10%), 4 đoạn tổng 32,1 giây; phối âm gồm lời dẫn + Mixkit "Hazy After Hours" (123 BPM, hạ nhỏ khi có lời dẫn) + 19 hiệu ứng âm thanh, qua hai lượt loudnorm đạt -14,4 LUFS.

## Kết quả

| Mục | Hyperframes | Remotion |
|---|---|---|
| Thành phẩm | 964 khung 1080p30 + AAC, 5,3 MB | 964 khung 1080p30 + AAC, 5,4 MB |
| Thời gian kết xuất (máy này 10 nhân) | 55 giây (4 workers; khoảng 35 giây là chi phí cố định khởi động và sẵn sàng, thu hình khoảng 16 giây) | 24 giây (5 luồng, gồm đóng gói) |
| Hình hai bên | So sánh từng khung cùng một khung SSIM 0,990–0,992, PSNR 42–44 dB (khác biệt do mã hoá) | |
| Kiểm tra chất lượng sẵn có | `lint`, `validate` (độ tương phản WCAG AA), `inspect` (lấy mẫu theo trục thời gian kiểm tra chữ tràn, bị che, chồng lấn); đoạn này đã chỉnh về 0 vấn đề | Không có công cụ tương tự |
| Tính xác định | Ở tầng sân khấu: 18 thời điểm × 4 thứ tự seek, ảnh chụp DOM đều nhất quán; nhiễu điểm ảnh ≤ 0,006% số điểm; `--docker` có thể giống nhau từng byte | Cùng một sân khấu, như bên trái |
| Phông chữ Trung | `@font-face` cục bộ bình thường | `staticFile` + `@font-face` bình thường |
| Giấy phép | Apache 2.0 | Miễn phí dưới 3 người, vượt quá cần giấy phép công ty |

Ngoại suy theo tốc độ thu hình cho phim 4 phút (7200 khung): Hyperframes khoảng 2,5 phút, Remotion khoảng 2 phút, đều chấp nhận được.

## Kết luận

1. **Kiến trúc đứng vững.** Khi nguyên ngữ được viết thành hàm thời gian thuần không phụ thuộc engine, hai engine kết xuất ra cùng một hình; bài giảng tương tác thậm chí không cần engine. "Một tệp nguồn, hai kiểu bàn giao" từ khẩu hiệu đã thành mã có sẵn.
2. **Engine chính giữ Hyperframes**: giấy phép không gánh nặng, `inspect` / `validate` dùng thẳng làm cổng kiểm tra hình ảnh, Studio cho nhóm tinh chỉnh thủ công. Phim ngắn nó chậm hơn một chút, chủ yếu do chi phí cố định, phim dài khoảng cách thu hẹp.
3. **Đường tương thích Remotion giữ lại với chi phí bằng không**: `Spike.tsx` 60 dòng là ra cùng một phim; cần tái dùng component React của promo-video, hoặc khi Hyperframes gặp sự cố thì chuyển sang.
4. **Khi lặp thì không dùng cái nào**: `spike/preview.html` + `scripts/stills.py` ra bảng tiếp xúc khung hình then chốt trong vài giây, sửa xong rồi mới giao engine ra phim.

## Các bẫy gặp trong Spike và đã giải quyết

| Hiện tượng | Nguyên nhân | Cách giải quyết |
|---|---|---|
| lint báo `missing_timeline_registry` | Hyperframes yêu cầu `window.__timelines[id]` | Đăng ký một timeline GSAP rỗng chỉ khai báo thời lượng, hình vẫn do `hf-seek` điều khiển |
| Khi dựng sân khấu bất đồng bộ, vài khung đầu có thể trống | Bộ kết xuất không biết phải chờ | Trước khi dựng sân khấu đặt `__hfTimelinesBuilding = true`, dựng xong đặt false và phát `hf-timelines-built` |
| `inspect` báo nhiều chữ tràn | Sau khi máy quay đẩy vào, chữ ở tầng thế giới ra khỏi khung là cố ý | Tầng thế giới thêm `data-layout-allow-overflow`; việc cắt trong khung hình do kiểm tra của chính chúng ta phụ trách |
| Nhãn "Bạn" chồng lên nội dung hình đơn | Hình đè lên nút, nhãn nút vẫn còn | Khi hình mọc ra nút `open` (nhãn mờ đi), khi co lại `close` |
| Cùng một thời điểm, thứ tự seek khác nhau, màu mũi tên vòng lặp khác nhau | SVG marker dùng `context-stroke`, Chrome lưu đệm vẽ marker | Đổi thành ba marker màu cố định chuyển theo trạng thái |
| Nhãn bước của vòng lặp đè lên đường nối | Vị trí nhãn mặc định cùng độ cao với đường nối | Nhãn bước hỗ trợ lệch `lx/ly`, nhãn đường nối hỗ trợ `labelSide: below` |
| Độ lớn tiếng -15,3 LUFS | loudnorm một lượt không chuẩn | Hai lượt loudnorm, -14,4 LUFS |
| Nút "bước tiếp" của bài giảng quay tại chỗ | Điểm đáp bị cắt về trước điểm kế tiếp, lần sau lại tính về cùng một điểm | Tính trước điểm đáp cho từng điểm từng bước, rồi mới tìm điểm kế theo điểm đáp |

## Đoạn này chưa kiểm chứng, để lại cho M1

- Cảnh Three.js (Hyperframes có adapter `three`, cũng đi theo `hf-seek`, dự kiến không trở ngại)
- Phiên bản 9:16
- Tài nguyên Lottie (xuất từ AE) vào nguyên ngữ
- Thời gian kết xuất và bộ nhớ của phim trọn 4 phút
