# 00 · Ghi chép chốt phương án

2026-09-26, người dùng xác nhận "cứ làm theo đề xuất".

| # | Hạng mục | Quyết định | Đưa vào thiết kế |
|---|---|---|---|
| 1 | Engine chính | Hyperframes là chính, Remotion làm đường tương thích | Nguyên thủy viết thành ES module độc lập với engine, được điều khiển qua `render(t)`; Hyperframes dùng bản 0.6.119 trong cache npx trên máy, không có mạng vẫn chạy được |
| 2 | Quy cách mặc định | 3–5 phút, 16:9 1920×1080, 30fps, tiếng Trung, hướng đến người không làm lập trình nhưng hiểu chút công nghệ | 9:16 là dàn trang lại, nguyên thủy có sẵn bố cục dọc |
| 3 | Lồng tiếng | Bắt đầu bằng edge-tts, bản chốt có thể đổi | Từ điển cách đọc `lexicon.json`; trục thời gian do lồng tiếng điều khiển |
| 4 | Hình thức tương tác của AE / AI | Nối cả hai: AE xuất Lottie, AI xuất SVG, làm tư liệu đưa vào nguyên thủy; thí nghiệm kéo thả kiểu AetherViz để sau M3 | Tham số nguyên thủy cho phép tài sản `lottie` / `svg` |
| 5 | Bài giảng tương tác | V1 làm bài giảng đồng bộ: chương, từng bước, nhấp vào hình xem nguồn, bài kiểm tra nhỏ | Nguyên thủy bắt buộc cung cấp `beats` (các điểm từng bước) và `hotspots(t)` (nhấp vào hình xem nguồn) |

## Các nguyên tắc xuyên suốt mọi tài liệu

1. **Cảnh chỉ nhận thời gian t.** Mọi giá trị hoạt ảnh đều là hàm thuần của thời gian, thống nhất dùng lò xo dạng đóng (`runtime/spring.js`).
2. **Không có nguồn thì không lên hình.** Mỗi câu trong kịch bản, mỗi phần tử trên hình đều gắn mã số sự thật; thông tin công khai chính thức vẽ nét liền, suy đoán vẽ nét đứt và ghi rõ, chưa công bố thì vẽ thành khối mờ sương.
3. **Một sơ đồ tổng, phóng to từng lớp.** Cả phim dùng chung một sơ đồ tổng hệ thống, chương chính là máy quay đẩy đến nút nào.
4. **Mỗi bước đều thành file.** Sửa bước nào thì chỉ chạy lại phần phía sau nó.
5. **Diễn trước rồi gọi tên.** Mỗi khái niệm đi theo bốn nhịp "hỏi · diễn · tên · quy".
