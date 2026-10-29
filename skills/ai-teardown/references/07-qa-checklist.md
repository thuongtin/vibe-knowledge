# 07 · Danh sách kiểm tra chất lượng

## Sau khi lồng tiếng (voice.log)
- [ ] Mỗi nhịp đọc lại ≥ 95%, không có "⚠ 可疑读数"; nhịp thấp thì xoá `build/audio/<nhịp>.*` để tổng hợp lại, hai lần vẫn thấp thì sửa cách diễn đạt.
- [ ] Tên người, tên sản phẩm, chữ viết tắt, số phiên bản đã nghe lại bằng whisper-cli (khi cần thêm `--prompt "tên riêng"`).
- [ ] Không đọc thừa, lặp, sót hay thêm từ phủ định.
- [ ] Thời lượng cả bài nằm trong khoảng mục tiêu (build in ra "总长", tổng độ dài).

## Sau khi dàn cảnh (bảng tiếp xúc build + khung đơn)
- [ ] `check_scenes.py` không báo lỗi nào (cả "只有 x 秒", chỉ có x giây, cũng phải sửa).
- [ ] Trước hết `rm -rf build/stills` rồi mới build (khung cũ sẽ lẫn vào bảng tiếp xúc).
- [ ] Không chữ tràn, chồng, ngắt dòng tách từ; chữ giữa recap nằm trong hình elip.
- [ ] Khoanh chú trên ảnh chụp màn hình trúng đích; ảnh chụp không mờ, không quá nhỏ.
- [ ] Bong bóng của nhân vật que không che chữ then chốt; chữ nhỏ ghi nguồn không bị caption đè.
- [ ] Không có màn trống (phần tử đầu tiên của cảnh xuất hiện sớm nhất có thể).
- [ ] Khi máy quay đẩy kéo không cắt mất thẻ (trong bảng tiếp xúc "nửa tấm thẻ" có thể chỉ là khung giữa chừng của chuyển động máy quay, xác nhận bằng khung đơn).
- [ ] Loại hoạt hình phải xem khung giữa, không chỉ xem trạng thái tĩnh (bóng mờ, tàn dư thường ở giữa chuyển cảnh).
- [ ] Phần mở đầu nối bài trước, phần kết báo trước bài sau + lời cảm ơn, khớp với tiêu đề trong series.json.

## Riêng tư và bản quyền (xem 09-safety)
- [ ] Ảnh chụp/quay màn hình không có tài khoản tên người (chữ ký tác giả sách có thể giữ), số điện thoại, mã QR, email, khoá, Token, đường dẫn tên người dùng máy, tên nội bộ công ty.
- [ ] Bản quay màn hình đã chạy `rec_scan.py`.
- [ ] Trích dẫn đúng từng chữ, ghi chương; dữ liệu minh hoạ ghi "示例数据" (dữ liệu mẫu); nội dung đầu tư ghi "không cấu thành lời khuyên đầu tư", không đọc tên cổ phiếu, giá, xếp hạng.

## Sau khi ra phim
- [ ] Thời lượng khớp với tổng độ dài của build.
- [ ] Rút 6 khung (đầu, giữa, cuối) ghép lại xem: không khung đen, không lớp tàn dư, phụ đề bình thường.
- [ ] Danh sách tệp bản tương tác chỉ chứa ảnh bài này dùng (`sketch_publish_files.py`), tên chứa ":" đã bỏ qua.
- [ ] Sau khi đăng, gửi MP4 cho người dùng, ghi lại liên kết.
