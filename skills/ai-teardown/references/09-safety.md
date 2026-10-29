# 09 · Quyền riêng tư, bản quyền và khóa API

## Khóa API
- Khóa MiMo chỉ đặt trong `~/.config/ai-teardown/mimo.env` (quyền 600). Không ghi vào dự án, narration, trang, đoạn trích nhật ký, bộ nhớ hay skill.
- Trong quay màn hình và ảnh chụp không được xuất hiện auth.json, API key, Token, AppID/Secret, email tài khoản.

## Ảnh chụp và quay màn hình
- Cắt bỏ hoặc không dùng: tên tài khoản cá nhân (tên tác giả ký trong sách có thể giữ), số điện thoại, mã QR, số nhóm, mã mời, email, tên người dùng trong đường dẫn máy, tên nội bộ của công ty/khách hàng, số cuộc họp.
- Khi cần che cục bộ thì lưu riêng một ảnh đã che rồi mới trích dẫn.
- Quay màn hình terminal: term_frames che mờ + rec_scan quét, bắt buộc làm trước khi phát hành; phát hiện dù chỉ một khung lộ tên người dùng cũng phải gỡ xuống và render lại.
- Khi quay màn hình đụng đến cấu hình trên máy người dùng: sao lưu trước, quay xong khôi phục, và báo cho người dùng.

## Ranh giới nội dung
- Không bịa: chức năng, con số, các bước mà bản gốc không viết thì không bổ sung; suy đoán phải ghi rõ.
- Loại đầu tư/y tế/pháp lý: theo ranh giới nhắc nhở trong bản gốc; bài đầu tư không đọc tên cổ phiếu cụ thể, giá, xếp hạng, lời khuyên giao dịch, phần kết trích nguyên văn các tuyên bố kiểu "không cấu thành lời khuyên đầu tư".
- Không dạy lách hạn chế khu vực, không dạy né quy tắc của nền tảng.
- Nhân vật giảng giải có thể thêm lời nhắc an toàn ngắn ("trước khi liên kết tài khoản, hãy xem rõ phạm vi ủy quyền"), nhưng không phát biểu quan điểm thay tác giả.

## Bản quyền và ghi công
- Sách/kho mã nguồn mở: xác nhận giấy phép (như MIT), ghi nguồn chương ở từng chỗ, cuối phim ghi địa chỉ kho mã.
- Nguồn của biểu tượng, hình minh họa, hiệu ứng động, lồng tiếng được cảm ơn thống nhất ở cuối phim.
- Ảnh trên mạng ghi nguồn và giấy phép; giấy phép không rõ thì không dùng.
- Khi cảm ơn một người cụ thể, cách diễn đạt phải khớp với sự thật (có nhiều tác giả thì viết "một trong các tác giả", và liệt kê các tác giả còn lại).
