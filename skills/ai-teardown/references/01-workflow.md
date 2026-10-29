# 01 · Quy trình và điểm xác nhận

## ① Tra cứu: thu thập tài liệu

- Phân cấp nguồn tin: **T1** tài liệu chính thức / sách gốc / kho chính thức; **T2** truyền thông uy tín, bài báo, bảo tàng và bách khoa; **T3** hướng dẫn cộng đồng, blog (chỉ làm manh mối, phải quay lại đối chiếu với T1).
- Mỗi sự kiện ghi: câu nguyên văn, URL nguồn, ngày, cấp độ. Con số, giá cả, tên mô hình ghi rõ "tính đến ngày nào đó".
- Sản phẩm nghiên cứu đặt ở `examples/<loạt-bài>/research/`: `landscape.md` (tổng quan + 2–3 bản nháp đại cương), `facts.json`.
- Khi đề tài là một cuốn sách mã nguồn mở / kho mã: `git clone` về `examples/<loạt-bài>/source/`, ảnh của chương nhập bằng `scripts/wb_import.py` (xem 06-visual-assets).
- Website không đọc được: khối mã GitHub dùng liên kết raw; một số website chính thức chỉ đọc được bằng trình duyệt; trang video trên máy thường không mở được, đừng giả vờ đã xem.

## Xác nhận 1: đối tượng, thời lượng, giọng đọc, phong cách hình ảnh

Hỏi rõ một lần, kèm phương án đề xuất:
- **Đối tượng**: đại chúng chưa có nền tảng / dân văn phòng biết chút máy tính / lập trình viên.
- **Thời lượng**: số bài × số phút mỗi bài (thực đo 4–7 phút là dễ chịu nhất; sau khi tăng tốc 1,15 lần thì mỗi giây khoảng 5 chữ).
- **Giọng đọc**: trước hết dùng `scripts/voice_audition.py` tạo 4–16 bản nghe thử cho người dùng chọn; chốt xong thì dùng bản ghi tạo lần đầu làm tham chiếu nhân bản, khóa cả loạt bài (presets/voice/host-ref.wav chính là được tạo ra như vậy).
- **Phong cách hình ảnh**: trước hết làm bản mẫu 40–60 giây (cùng một đoạn nội dung), đừng chỉ đưa mô tả. Hiện có: Notion tối giản vẽ tay (sketch/notion), giấy sổ tay (sketch/paper), macaron / bạc hà / ban đêm (lesson).
- Quyết định ghi vào `DECISIONS.md`.

## ② Đại cương: đại cương và trang khóa học

- `series.json.lessons[]`: `n, title, hook (một câu dẫn, tốt nhất là câu hỏi), intro (bài này nói ba việc), points (4–6 ý chính), minutes`.
- Trang khóa học làm bản nháp trước (`status: "draft"`, `status_label: "Đại cương chờ xác nhận"`), mỗi bài hiển thị "đang sản xuất".
- Chương dài (trên 1 vạn chữ) chỉ chọn 3 khối cốt lõi nhất để giảng; hai chương ngắn có thể gộp thành một bài; loại đọc ngoài giờ có thể làm thành một bài.
- Số chương lấy theo **tên thư mục mục lục** của sách gốc (tiêu đề index.md có thể lệch 1).

## Xác nhận 2: người dùng xem đại cương

Sửa xong mới bắt đầu viết. Sau đó các bước "viết" và "dàn cảnh" có thể làm hàng loạt song song.

## ③④ Viết và dàn cảnh: phân công đa tác tử

- Phiên chính: đưa cho mỗi trợ lý một bản mô tả nhiệm vụ tự đủ (thư mục bài học, tiêu đề, tên thư mục chương nguồn, lệnh nhập, tiêu đề các bài trước sau để nối mạch, yêu cầu về quyền riêng tư, các hạn chế đã biết của mẫu), mỗi lần 3 trợ lý, chạy ở nền.
- Trợ lý: làm đúng theo `BRIEF.md` của thư mục loạt bài, chỉ động vào thư mục bài học của mình; không render, không xuất bản, không sửa mã engine, không sửa series.json; lỗi của mẫu ghi vào báo cáo.
- Sau khi phiên chính nhận báo cáo: nghe lại các nhịp đáng ngờ (file `build/audio/<nhịp>.mp3`, đối chiếu `qa.json`), chạy lại build để xem contact sheet, khi cần thì tự sửa scenes.json, rồi xếp vào hàng đợi render, đồng thời giao bài kế tiếp.
- "Hạn chế của mẫu" mà trợ lý báo cáo phải tổng hợp thành "lỗi đã biết" trong bản mô tả nhiệm vụ của đợt sau, và sửa trong engine càng sớm càng tốt (sửa xong thì với các bài đã xếp hàng nhưng chưa render, hãy chạy lại build — final sẽ không chạy lại build).

## ⑤⑥ Render và xuất bản

Xem 02-pipeline.md. Mỗi bài xong: trích khung kiểm tra → xuất bản bản tương tác → gửi MP4 cho người dùng → ghi tiến độ.

## Xác nhận 3: thành phẩm bài 1

Phản hồi của người dùng sau khi xem bài 1 thường sẽ làm thay đổi mẫu (phối màu, mật độ hiệu ứng, nhân vật, nguồn biểu tượng), sửa xong mới làm hàng loạt. Mọi phản hồi về phong cách do người dùng đưa ra đều ghi lại, làm mặc định cho tất cả các bài sau.

## Video dẫn nhập (bản đồ khóa học) và trang tổng hợp khóa học

Sau khi làm xong tất cả thì bổ sung một video dẫn nhập 2–3 phút:
1. Mở đầu cảm ơn (tác giả gốc / dự án mã nguồn mở; người mà người dùng nêu tên cảm ơn đặt lên đầu, lời lẽ khớp với sự thật: nhiều tác giả thì viết "một trong các tác giả", và liệt kê các tác giả khác).
2. Đây là gì (định vị một câu về cuốn sách/dự án gốc, trích dẫn nguyên văn).
3. Vì sao học (so sánh với cách làm thông thường, compare).
4. Bản đồ khóa học (thẻ stickers chia nhóm theo trạm/thiên, mỗi thẻ ghi phạm vi số bài + 3 từ khóa).
5. Học xong nắm được gì (numbered checklist, 4 mục).
6. Học thế nào (thời lượng mỗi bài, tạm dừng suy nghĩ, bản tương tác, bắt tay làm ngay).
7. "Hẹn gặp lại ở bài 0".

Thư mục bài dẫn nhập có thể dùng tên không phải số (như `lessons/intro`), scenes.json ghi `"videoOnly": true` (final không tìm số bài trong series.json, không làm bản tương tác); ảnh bìa dùng `eyebrow` / `props` để ghi đè "Bài N". Trang khóa học dùng `series.json.sample` (heading, sub, video, poster, changes[{k,v}]) gắn ở phía trên cùng.

## Gói học tập (tăng cường tùy chọn)

Thẻ từng bài trên trang khóa học có thể thêm: 3 mục tiêu học tập ("học xong bạn có thể…"), sơ đồ tư duy của bài (sinh từ cấu trúc chapter/pan/recap trong scenes.json), ba câu hỏi sau bài (đáp án gập lại được), bài tập thực hành (bản mô tả nhiệm vụ có thể sao chép), liên kết mở rộng từ nguyên văn; cấp độ loạt bài thì thêm sơ đồ tư duy tổng, lộ trình học theo vai trò, đánh dấu tiến độ. Tất cả đều phát sinh từ lời dẫn và nguyên văn, không bịa thêm.
