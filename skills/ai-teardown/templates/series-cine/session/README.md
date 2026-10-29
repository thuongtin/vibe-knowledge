# Quay phiên làm việc thật (mạch xuyên suốt của bài thực chiến)

Mỗi bài trong khoá thực chiến đều đặt bước tương ứng trong "một phiên làm việc thật": prompt thật, đầu ra thật, tệp thật và thời gian thật. Quay một lần, dùng cho cả khoá.

## Chuẩn bị
1. Một bản Claude Code **dành riêng cho khoá học**: thư mục cấu hình riêng, tắt tự động cập nhật, không mang theo định tuyến mô hình dùng hằng ngày (`cc.example` là ví dụ kịch bản khởi động). Việc đăng nhập do chính người dùng thực hiện trong terminal.
2. Các skill cần dùng được đặt vào phiên bản khoá học bằng liên kết mềm: `ln -s ~/.claude/skills/promo-video <thư mục cấu hình khoá học>/skills/promo-video`.
3. Một trang web demo của **sản phẩm hư cấu** (trang tĩnh, đặt trong `SITE_DIR`), tránh dùng công ty thật để trình diễn.
4. Sửa `session.env`: thư mục dự án (bắt đầu từ thư mục trống), kịch bản khởi động, thư mục cấu hình, trang web demo.
5. **Trước khi quay hãy báo mức sử dụng dự kiến** (tham khảo: bài thực chiến video quảng bá 5 lượt khoảng 16 phút, 48 lần gọi mô hình, quy đổi theo giá API khoảng 3,4 USD), người dùng xác nhận rồi mới quay.
6. Trạng thái trên máy sẽ bị thay đổi thì sao lưu trước, quay xong khôi phục (ví dụ `~/.cache/promo-video/music-usage.json`).

## Quay
```bash
session/turn.sh 1 "Dùng promo-video làm một video quảng bá 30 giây cho <sản phẩm>, website http://127.0.0.1:8930."
session/turn.sh 2 "<trả lời câu hỏi xác nhận của nó>"            # từ các lượt sau tự động --continue để nối vào cùng một phiên
python3 session/export.py        # turnN.jsonl → turnN.json: prompt, từng lệnh gọi công cụ kèm số giây tương đối, đoạn chữ nó viết, thời gian và chi phí của lượt này
python3 session/usage.py > session/usage.json   # mức sử dụng toàn bộ quá trình (loại trùng theo message id, ghi cache tính theo giá cache 1 giờ)
```

## Cạm bẫy
- Ở chế độ `-p`, nó đẩy việc render xuống nền, lượt này vừa kết thúc là tiến trình render bị giết (thành phẩm thiếu moov, không mở được). Cần render thì phải yêu cầu rõ ràng nó chạy ở tiền cảnh.
- Khi dùng `--continue`, `total_cost_usd` trong result của mỗi lượt là giá trị luỹ kế của cả phiên; `export.py` đã quy đổi thành phần tăng thêm của lượt này.
- Cùng một câu trả lời sẽ bị tách thành nhiều dòng trong bản ghi phiên, mức sử dụng phải loại trùng theo message id, nếu không sẽ bị tính dư gấp nhiều lần.
- Mọi đường dẫn xuất hiện trong hình ảnh đều thay tên người dùng trên máy bằng `~` (`export.py` đã xử lý); tệp uỷ quyền, khoá bí mật, email tài khoản không được xuất hiện trong bất kỳ hình ảnh nào.
