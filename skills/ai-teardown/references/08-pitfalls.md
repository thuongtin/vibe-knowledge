# 08 · Những cái bẫy đã dẫm phải

## Render và tính xác định
- Bộ render Lottie SVG không xác định theo từng khung hình → chỉ dùng bộ render canvas.
- Ẩn lớp dùng `display:none`: khi lớp cha `visibility:hidden`, phần tử con `visibility:visible` sẽ xuyên qua và hiển thị (khung hình cuối của bản quay màn hình bị sót lại).
- X6 bắt buộc `async:false`, nếu không khi chụp từng khung hình thì nét nối chưa vẽ xong.
- Hyperframes thêm worker lại chậm hơn (mỗi worker tải trang mất khoảng 17 giây); chạy đồng thời tác vụ trình duyệt khác sẽ tụt xuống 5–8 fps. Render tuần tự, chạy nền, chồng lên với lúc viết bài tiếp theo.
- **final không chạy lại build**: sau khi sửa engine, các bài đã xếp hàng chưa render phải build thủ công một lần.
- Khi bảng điều khiển trình duyệt bị thu gọn thì rAF không chạy, trang sẽ đơ giả; xác minh bằng ảnh chụp headless của Playwright (`scripts/stills.py <preview.html> <out.png> t1 t2 … --cols N`).

## Các trường của trình biên dịch
- Trường để `shot` phát bản quay màn hình tên là `clip`; `flip` là cờ chuyển cảnh lật trang, dùng lẫn sẽ gây lỗi.
- Tham chiếu thời gian `"B01.reply-1"`: độ lệch âm không có phần thập phân từng bị coi là tên cue, quy tắc hiện nay là chỉ "dấu gạch nối + chữ cái" mới được tính là một phần của tên cue.
- tick/cross của `stickers` ghi thời điểm, ghi `true` sẽ báo "cách viết thời gian không đúng" mà check_scenes không phát hiện được.
- Số bài không phải số (intro, 03en) phải dùng `videoOnly`, nếu không final tìm series.json theo `int(số bài)` sẽ bị crash.

## Lồng tiếng
- Bẫy số La Mã của MiMo (CLI→151), đã tự động tách chữ cái; từ viết tắt chữ thường và tên riêng mới cho vào lexicon.
- Khi không thêm mô tả giọng giảng bài thì tốc độ nói quá nhanh; giọng nhân bản sau khi thêm mô tả nói chậm đạt khoảng 4 chữ/giây, rồi tăng tốc 1.15 lần.
- Khi whisper dùng toàn văn làm prompt, mô hình có thể bỏ qua một đoạn âm thanh → dùng small căn chỉnh trước, medium cứu vớt, cả hai lần đều thất bại thì mới cắt ngắn nhịp.
- MiMo gặp 429 khi đồng thời, thỉnh thoảng lỗi HTTP2 framing: script tự động lùi thời gian và thử lại, không cần can thiệp thủ công.

## Tư liệu
- SVG tĩnh của Noto có DOCTYPE/ENTITY sẽ bị Artifact từ chối (noto_emoji.py đã tự động loại bỏ).
- Đường dẫn Noto trên raw.githubusercontent bị 404 → dùng gstatic CDN.
- Ảnh liên kết ngoài bị CSP của Artifact chặn → đưa toàn bộ về cục bộ.
- Dung lượng bộ nhớ đệm trình duyệt hiển thị bởi `du` có thể là ảo ảnh do bản sao APFS clone, trước khi dọn chỗ hãy dùng `df` để xác minh; tổng hợp video dùng `cp -c` để clone không chiếm dung lượng.

## Xuất bản
- Giới hạn mỗi phiên bản 64MB / 255 tệp: video của trang bài học chia đợt đăng lên cùng một file_path; bản tương tác >200 tệp dùng files dạng danh sách + root.
- Khi xuất bản thỉnh thoảng gặp "Socket is closed": thử lại nguyên trạng (sẽ nhắc slug được giữ lại).
- Một phiên làm việc theo dõi tối đa 10 Artifact cùng lúc, vượt quá chỉ là không theo dõi phiên bản mới nữa, không ảnh hưởng việc xuất bản.

## Bố cục
- Câu dài ở dòng thứ hai của say, tone và màu nền của diagram, caption của diagram đè lên nguồn, chữ ở giữa recap bị tràn — đều đã sửa trong engine (xem phụ lục C của 04-scenes-sketch), khi đổi quy tắc bố cục đừng hoàn nguyên.
- Thư mục stills phải xoá sạch trước rồi mới xem contact sheet.
- Viết escape Unicode bốn chữ số (dấu gạch chéo ngược u + 4 chữ số thập lục phân) trong đầu vào của công cụ sẽ bị giải mã thành ký tự thực (kể cả ký tự độ rộng bằng không); khi cần biểu diễn dải ký tự trong regex thì dùng `codePointAt` để so sánh, hoặc ghép bằng `chr(92)`.
