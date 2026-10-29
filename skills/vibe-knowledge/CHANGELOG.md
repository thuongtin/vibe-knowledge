# Nhật ký cập nhật

## 2026-10-28 (chiều) · BGM bắt buộc

- Âm lượng BGM: khi có tiếng nói thấp hơn giọng người 10 dB (ban đầu định 14 dB, người dùng yêu cầu "cao hơn một chút" nên đổi thành 10). Lối thoát duy nhất để đổi bài: `bgm: true, user_request: "nguyên văn người dùng"`.
- Mỗi video đều phải có vibe-bgm: thêm tools/bgm_force.py, móc vào finish.py. Chưa đặt thì tự bổ sung; các bản nhạc nền nguyên đoạn khác bị vô hiệu; âm lượng hiệu chỉnh theo giọng người; ghi build/bgm.json.
- new_film.py khi tạo không gian làm việc sẽ tự gắn hook; qa.py thêm kiểm tra BGM (tương quan với phần đầu bản gốc), không có thì báo ⚠⚠.

## 2026-10-28 · Đúc kết từ kỳ 04 bản B "Không có tủ lạnh"

- **Độ dài do người dùng quyết định**: thêm references/13-duration.md và tools/duration.py. Chấm điểm năm mục phức tạp (số khái niệm, kiến thức nền, chuỗi nhân quả, mật độ bằng chứng, bất đồng / đảo ngược), chia bốn bậc (lướt nhanh / giảng sâu / tiêu chuẩn / đào sâu), mỗi bậc ghi rõ số chữ, số nhịp, độ tỉ mỉ, nói được đến đâu, phải cắt gì; bậc đề xuất xếp đầu; bậc người dùng chọn lệch độ phức tạp từ hai mức trở lên sẽ nhắc. Xác nhận 1 thêm câu hỏi "độ dài".
- **Nối ảnh bìa thành khung đầu**: thêm tools/cover_first.py (mặc định dừng 0.5 giây, `--hold` chỉnh được; có giới hạn đỉnh, chống đỉnh AAC vượt chuẩn). 05-publish.md đổi thành "ảnh bìa làm thẳng thành khung đầu của phim".
- **Kiểm tra báo đóng băng**: qa.py sẽ báo hình tĩnh >3 giây, >10 giây thì xác định là ghi hình gặp sự cố.
- **Thành phần mới của know.js**: `stamp` (ấn triện), `cutaway` (hình cắt nét vẽ, dùng thay cho ảnh khí vật AI vẽ không chuẩn), `tokens` (một hàng khối vuông, có thể tan biến).
- **An toàn hàng đợi render**: queue.txt chỉ được thêm vào cuối; đã có queue.sh đang chạy thì không khởi động cái thứ hai (các lệnh thường dùng trong SKILL.md đã sửa).
- **Danh sách bẫy**: thêm references/14-pitfalls.md, sắp xếp theo năm khâu: tạo, lồng tiếng, dàn dựng, render, giao.
