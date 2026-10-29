# Phương án “Khóa thực chiến phim quảng bá Opus 5.5: từ một câu đến thành phẩm” (2026-10-04)

## Lời người dùng và quyết định chốt
- Nguyên văn: “Làm một hướng dẫn về phim quảng bá, chính là phim thực chiến Opus 5.5 này... skill promo của chúng ta cũng đã làm một số phim quảng bá, bạn kết hợp năng lực của mình với GitHub hoặc một số phim hay để biên soạn.”
- Chốt: mở phần thực chiến mới, dẫn nhập + 8 bài; mọi phim quảng bá đã giao đều có thể dùng (khách đồng ý); quay 1 phiên thật (trước khi quay báo trước mức sử dụng dự kiến); giảng cả hai lộ trình (skill promo-video / Remotion, nói rõ về giấy phép; thuần code web).
- Giữ quy tắc của khóa điều phối: mỗi bài mở đầu bằng một đoạn “bom”; không có nguồn thì không lên màn hình; lời cảm ơn chỉ đặt ở bài dẫn nhập và bài cuối; làm xong một bài thì phát luôn.

## Khác biệt với khóa điều phối
- Hình ảnh khóa điều phối đều do code tính ra; nhân vật chính của khóa thực chiến là **thành phẩm thật**: 25 dự án, hơn 40 phiên bản chúng ta đã giao (kho nghiên cứu `examples/promo-course/research/`), phát trong khung “màn hình giám sát” ở trên hình (`clips` của `film.js` + `cine/tools/clips.py`, khi dựng thành phẩm thì ffmpeg chồng lên).
- Một sợi xuyên suốt: **một phiên thật**. Dùng Claude Code chuyên dụng cho khóa học (`~/claude-course/cc`, cấu hình độc lập, không đụng cấu hình hằng ngày), làm một phim quảng bá 30 giây cho sản phẩm hư cấu “Quanwen” (website `~/Desktop/quanwen-site`, cổng cục bộ 8930). Mỗi bài đặt bước tương ứng trong phiên này (terminal vẽ lại theo bản ghi phiên, tên người dùng trong đường dẫn đổi thành ~).

## Hai lộ trình
| | Lộ trình A: skill promo-video | Lộ trình B: thuần code web |
|---|---|---|
| Nền tảng | Remotion (React, mỗi khung do useCurrentFrame tính ra) | Three.js / Canvas / GLSL, cả phim là một seek(t), Playwright quay từng khung (HyperFrames là framework có sẵn) |
| Sở trường | Toàn bộ quy trình phim quảng bá: thẻ chọn kiểu, phân cảnh, khớp nhịp với kho nhạc, thành phần hiệu ứng, script kiểm tra chất lượng | 3D, shader, hạt, những hình ảnh chói lọi nhất (toàn bộ khóa điều phối, phim so sánh ong mật, STILLWATER) |
| Giấy phép | Mã nguồn Remotion công khai nhưng không phải giấy phép mã nguồn mở: cá nhân và công ty dưới 3 người miễn phí, từ 4 người trở lên phải mua giấy phép công ty | three.js MIT; HyperFrames Apache-2.0; Motion Canvas, Revideo MIT |

## Đại cương (dẫn nhập + 8 bài)
| # | Tiêu đề | Móc câu | Ba việc giảng | Ca chính | Bước trong phiên thật |
|---|---|---|---|---|---|
| 00 | Dẫn nhập: một câu đến thành phẩm | Cắt nhanh các điểm sáng của 25 dự án | Khóa học dạy gì, hai lộ trình, học thế nào | Tất cả | Trailer thành phẩm Quanwen |
| 01 | Bộ khung của một phim quảng bá | Ba giây đầu giữ người xem, hai giây cuối để họ nhớ | Móc câu→giá trị→điểm bán→chứng minh→kêu gọi hành động; các mức thời lượng và số chữ mỗi màn hình; câu đầu tiên nói thế nào | HiAPI, WorkBuddy v4, BeeGer v2 | Câu prompt đầu tiên + phân tích tư liệu của nó |
| 02 | Lấy tư liệu từ website | Đưa nó một địa chỉ web, Logo, bảng màu, ảnh chụp tự lấy | Nội dung và điểm bán (ưu tiên nguyên văn, con số phải xác nhận); bảng màu, font, Logo; ảnh sản phẩm và video trên website, thiếu gì thì hỏi | Renoise, BeeGer, Zaowu Matrix, Damao Edit, HiAPI | Nó đọc website, rút bảng màu, chụp ảnh sản phẩm |
| 03 | Thẻ chọn kiểu: bốn tầng chỉ chọn một lần | Không phải càng nhiều tính năng càng tốt | Bốn tầng (chế độ/tông/khung/tăng cường); đề xuất theo tín hiệu; ghi nhận phản hồi (phản hồi thật) | Bốn phiên bản WorkBuddy, BeeGer v1/v2, Xiaohu | Thẻ chọn kiểu nó viết |
| 04 | Phân cảnh và nhịp | Điểm cắt đi theo nhịp trống | Bảng phân cảnh bảy cột; tốc độ đọc; chọn nhạc khớp nhịp (lưới BPM, điểm năng lượng đến) | Bia thủ công 95 BPM, Xiaohu, ListenHub | Bảng phân cảnh của nó + chọn nhạc |
| 05 | Tầng hiệu ứng: hiệu ứng mọc trên sản phẩm | Hạt tụ lại thành khẩu hiệu trên ảnh chụp | Tư liệu ưu tiên; ba mức và bản đồ kỹ thuật; chuyển cảnh và đầu cuối hô ứng, “chưa đủ chói” thì tăng thế nào | WorkBuddy v4, YouWare v3, Renoise, WaytoAGI, Zaowu Matrix v2 | Kỹ thuật nó chọn trong Film.tsx |
| 06 | Camera và thiết bị | Mỗi lần chuyển động máy đều phải có lý do | Bảng chuyển động máy của đạo diễn; quy tắc (một chuyển động chính, CTA tĩnh và vững, chỉ đẩy ở khung then chốt); thiết bị 3D, một cú quay liền, 3D thuần code | DockLock, TOKEI, WorkBuddy một cú quay liền, phim so sánh ong mật, STILLWATER | Cách nó viết camera |
| 07 | Âm thanh: nhạc, hiệu ứng, lời dẫn | Âm thanh rơi vào khung tiếp xúc | Kho nhạc và giấy phép; hiệu ứng âm thanh và hai chỗ to nhất; lời dẫn và master | ListenHub, WorkBuddy một cú quay liền, Xiaohu, Bia thủ công | Ghi công nhạc nền và kiểm tra độ lớn của nó |
| 08 | Kiểm tra chất lượng, bàn giao và làm lại | Một câu đi vào, 30 giây đi ra | Duyệt phim kiểu bậc thầy và lấy khung chính xác; tuân thủ và bàn giao; làm lại, ghi nhận phản hồi + phát lại toàn bộ phiên thật và mức sử dụng | BeeGer v1→v2, Xiaohu, anh Ngư (nén hạt nhiễu) | Toàn bộ (gồm một vòng làm lại) |

## Phiên thật (quay sau khi người dùng xác nhận mức sử dụng)
- Thư mục dự án `~/Desktop/quanwen-promo/` (bắt đầu từ thư mục trống), website `http://127.0.0.1:8930`.
- Các lượt (`cc -p … --output-format stream-json`, các lượt sau dùng `-c` để nối tiếp cùng một phiên):
  1. “Dùng promo-video làm cho Quanwen một phim quảng bá 30 giây, website http://127.0.0.1:8930.”
  2. Trả lời các câu hỏi xác nhận của nó (ra mắt sản phẩm, nền tối công nghệ, 16:9, tiếng Trung, kho nhạc tích hợp), yêu cầu bảng phân cảnh.
  3. “Phân cảnh ổn, ra khung mẫu trước.”
  4. “Khung mẫu ổn, chọn nhạc khớp nhịp, ra thành phẩm.”
  5. Xem xong thành phẩm, đưa ra một góp ý sửa thật (làm lại).
- Dự kiến 40–70 phút (render chiếm phần lớn); quy đổi theo giá API khoảng 10–25 đô la. Mốc cơ sở: lần Pomodoro tập trung trước đó 9 phút, 41 lần gọi mô hình, đầu ra 41 nghìn, đọc cache 4,96 triệu, ghi cache 150 nghìn token, quy đổi khoảng 2,5 đô la; lần này đọc nhiều tài liệu hơn, code dài hơn, nhiều lượt hơn, ước tính gấp 4–8 lần. Người dùng gói đăng ký không bị trừ thêm tiền, chỉ chiếm hạn mức sử dụng.
- Trước khi quay sao lưu `~/.cache/promo-video/music-usage.json` (đã sao lưu vào `~/claude-course/music-usage.backup.json`), quay xong khôi phục, không ảnh hưởng việc chọn nhạc hằng ngày.
