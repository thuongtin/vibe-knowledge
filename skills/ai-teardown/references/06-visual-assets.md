# 06 · Tư liệu hình ảnh

## Phân công ba lớp icon

1. **Icon nét IconPark** (Apache 2.0): giao diện, quy trình, danh sách. Viết `icon-park:robot`, tên phải có trong `assets/iconsets/icon-park.json` (tra trước rồi mới dùng; thiếu thì dùng `lucide:` / `tabler:` / `iconoir:`). Tự động vẽ nét từng nét một + luân phiên bảng màu Notion.
2. **Noto emoji** (Google, CC BY 4.0): nhân vật chính, cảm xúc, đồ vật. `python3 scripts/noto_emoji.py <thư mục bài> robot light-bulb …` (tên tiếng Anh chữ thường nối bằng gạch ngang). Loại có hoạt hình chính thức sẽ đặt lottie.json vào `lottie/` của thư mục bài, trong cảnh ghi cùng tên là tự phát hoạt hình; SVG tĩnh đã bỏ DTD/ENTITY (nếu không Artifact sẽ từ chối). Hoạt hình nào hiệu ứng không đẹp (như stop-sign co thành chấm đỏ) thì xoá tệp lottie đó và dùng bản tĩnh.
3. **Thư viện minh hoạ IconPark** (88 hình, 22 album, ByteDance): `assets/illustrations/iconpark/` (`catalog.json`, `_sheet.html` tổng quan). `python3 scripts/illus.py <thư mục bài> ip-6-52 …`, trong cảnh `say`/`cover` ghi `"illus": "ip-6-52"`. Mỗi bài 2–4 hình, cố gắng không trùng với các bài trước (grep các id đã dùng trước). Lưu ý: thư viện minh hoạ không phải giấy phép mã nguồn mở (điều khoản của trang là cấp phép tiêu chuẩn), người dùng đã xác nhận được dùng cho series này; dùng cho dự án khác phải xác nhận lại.

## Sơ đồ quy trình: AntV X6 (MIT)

`assets/vendor/x6.min.js` (v3.1.8 UMD, `async:false` render đồng bộ đảm bảo xác định theo từng khung hình); định tuyến manhattan + nét nối bo góc; nút bật ra → nét nối được vẽ → nét đứt chảy. Các trường xem 04-scenes-sketch.

## Hiệu ứng chuyển động

- Lottie luôn dùng **bộ render canvas** (bộ render SVG không xác định theo khung hình, cùng một khung hình 15 lần có 13 lần không nhất quán).
- `primitives/motion.js`: lottie, vẽ nét icon, vẽ nét illus + hiện dần, diagram, count số chạy, bars, line, dotmap (chấm lưới đất liền Natural Earth, không vẽ biên giới quốc gia), kinetic bật ra từng chữ.

## Tư liệu ảnh chụp và quay màn hình

- Ảnh minh hoạ chương của sách / kho: `python3 scripts/wb_import.py <thư mục bài> "<tên thư mục chương>" --prefix wbNN`. Ảnh chụp được nhập thành `wbNN-XX.png` và ghi vào sổ cái; GIF được tách thành chuỗi khung hình 8fps đã loại trùng `flip-<prefix>-gXX-NNN.jpg` + `data/flip-*.json`, cảnh phát bằng `shot.clip` (trường tên là `clip`, **không được gọi là flip** — trình biên dịch dùng `s.flip` để chỉ chuyển cảnh lật trang); tạo `build/chapter_sheet.jpg` để xem tổng quan.
- Tư liệu mp4 không tự động nhập: dùng ffmpeg cắt một đoạn xuất khung hình 8fps, đặt tên giống như vậy để làm thành clip.
- Tải ảnh trên mạng: `scripts/fetch_images.py`, ghi nguồn và giấy phép; ưu tiên Wikimedia Commons, bộ sưu tập mở của bảo tàng, ảnh tin tức chính thức. Ảnh liên kết ngoài sẽ bị CSP của Artifact chặn, bắt buộc phải đưa về cục bộ.
- Sổ cái ảnh `assets/img/images.json`: mỗi ảnh có id, file, kích thước, artist, license, source, credit; ghi song song dùng `scripts/ledger.py` (khoá bằng fcntl). Credit của ảnh chụp ghi "Nguồn ảnh chụp: «tên sách» chương X · MIT", hình sẽ tự động ghi nhãn.
- Ảnh chụp cần che thì lưu riêng một bản đã làm mờ (như `wb10b-03m.png`), cảnh tham chiếu bản làm mờ.

## Nhân vật que giảng bài

- `presets/presenter/`: `hp-<pose>-1..8.png` (10 động tác), `host-avatar.png` (avatar ảnh bìa), mục trong sổ cái, `生图提示词.md` (prompt và yêu cầu kích thước đưa cho người dùng khi bổ sung động tác mới).
- Trước khi ghi động tác mới vào sổ cái, co giãn thống nhất theo chiều cao "đỉnh tóc → mép dưới" sao cho khớp với talk.
- Động tác mặc định: shot→point, pause→think, checklist→check, outro→wave; tips mặc định idea; `pose` của cảnh và `pose` trong tips có thể ghi đè.

## Quy tắc ghi nguồn (do người dùng quy định)

- Nguồn của icon, thư viện minh hoạ, thư viện hiệu ứng, lồng tiếng **chỉ ghi một lần trong credits của outro cuối phim**.
- Nguồn của nội dung và ảnh chụp trong sách **ghi ở từng chỗ** (`src` hoặc credit trong sổ cái).
- Mỗi dòng credits không quá 40 ký tự, thường dùng 5 dòng: nguồn nội dung (chương + MIT) / địa chỉ kho / minh hoạ và icon / sơ đồ và thư viện hiệu ứng / nhân vật que giảng bài và lồng tiếng (do AI tạo).
