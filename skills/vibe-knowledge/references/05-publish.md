# 05 · Gói xuất bản

## Douyin #Vibe知识大赏 (sự kiện chính thức của @抖音科技, hạn chót 2026-10-31)

- **Tiêu đề bắt đầu bằng "Vibe知识大赏|"** (nguyên văn của ban tổ chức: dễ được họ nhìn thấy hơn), phía sau nối câu hỏi mở của kỳ này, ví dụ: `Vibe知识大赏|Vì sao sổ sách giả luôn bị con số 1 phản bội?`
- Chủ đề: bắt buộc kèm `#Vibe知识大赏`, đồng thời **@抖音科技**; có thể thêm `#vibecoding #claude #opus` và chủ đề theo môn học (`#历史冷知识 #统计学` …).
- Phần giới thiệu: dòng đầu lặp lại câu mở; dòng thứ hai một câu "Video này do Claude Opus 5.5 dàn dựng sản xuất, ảnh minh hoạ và cảnh động do Renoise tạo, nguồn sử liệu / dữ liệu xem chú thích trong phim"; cuối cùng đặt câu hỏi ở cuối phim để dẫn dắt bình luận.
- Ưu đãi của sự kiện: video chất lượng được 10 nghìn đến 100 nghìn+ lượt hiển thị, ban tổ chức "lật thẻ" bổ sung thêm lưu lượng.
- Khung hình: các tác phẩm top đầu phần lớn là ngang 16:9, có thể đăng thẳng; bản dọc (9:16) làm sau.

## Nội dung chính và khu bình luận (tiếp thu từ LuZhong-Li/vibe-knowledge-video-skill)

- Nội dung chính chỉ đặt một câu kết luận + câu hỏi mở; phần phổ cập chi tiết tách thành 2–3 ý đặt ở khu bình luận, sau khi đăng lập tức ghim một câu hỏi lên đầu.
- 4–5 thẻ (bắt buộc có #Vibe知识大赏).
- **Ảnh bìa làm thẳng thành khung hình mở đầu của phim** (quy tắc do người dùng đặt, 2026-10-28): `tools/cover_first.py <thành phẩm> <cover_16x9.jpg> <đầu ra>`, ảnh bìa dừng 0.5 giây rồi cắt cứng vào phim chính, âm thanh lùi toàn bộ 0.5 giây. Nền tảng mặc định lấy khung hình đầu làm ảnh bìa, không cần tải lên riêng. Xuất ảnh thu nhỏ rộng 540px để xem tiêu đề còn đọc rõ không.

## Ảnh bìa

- 16:9: khung hình hình ảnh chính (khung hình đẹp nhất của vclip / plate) + tiêu đề lớn bên trái (≤10 chữ) + tên series bằng chữ nhỏ.
- 3:4: cùng hình ảnh chính cắt giữa + tiêu đề phía trên.
- Dùng stills.py chụp một ảnh gốc 1920×1080 tại thời điểm của hình ảnh chính, rồi dùng PIL chồng chữ lên.

## Thư mục bàn giao

`~/Desktop/Vibe知识大赏_视频/第NN期_片名/`: Thành phẩm (bản chia sẻ, khung hình mở đầu đã là ảnh bìa), hai ảnh bìa, văn bản tiêu đề và giới thiệu `post.txt`, facts.md (nguồn để tra cứu).
