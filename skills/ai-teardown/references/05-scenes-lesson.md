# 05 · Bộ biên dịch mẫu (mùa một, hai): dàn cảnh

Áp dụng cho series không khai báo `engine` (mặc định `runtime/lesson.js`). Giỏi về nhân vật và lịch sử, phổ biến khái niệm, quay màn hình terminal thật. Thành phẩm tham khảo `templates/series-lesson/`.

## Đầu file

```json
{"n": 5, "title": "…", "series": "Khóa thực chiến AI", "theme": "mint", "speed": 1.15, "author": "@Berryxia", "scenes": [...]}
```
- `theme`: `macaron` (mặc định, macaron sáng màu) / `mint` (bạc hà) / `night` (ban đêm) / `editorial`.
- Cảnh: `{t, at, chapter?, year?, mascot?, ...}`, mỗi cảnh kéo dài đến khi cảnh tiếp theo bắt đầu; cảnh có `chapter` vào bằng chuyển cảnh vòng tròn màu; `year` hiển thị thước năm ở phía trên.

## Cách viết thời gian (dùng chung cho hai engine)

`"B03"` nhịp 3 bắt đầu nói · `"B03.first"` dấu [[first]] của nhịp 3 · `"B03@máy"` thời điểm đọc đến chữ "máy" · `"B03.end"` nói xong · đều có thể thêm độ lệch `"B03.first+0.4"`, `"B03@máy-0.2"`. Phần tử không viết at thì tự động so le theo thứ tự xuất hiện.

## Mẫu và trường

| Mẫu | Công dụng | Trường |
|---|---|---|
| opening | Mở đầu | title, titleAt, eyebrow, eyebrowAt, question, questionAt, icons |
| statement | Chữ lớn gõ dần | lines, icon, iconAt, tone, mascot, w, x, y |
| iconrow | Hàng biểu tượng / thành quy trình có mũi tên | title, items, arrows, caption, gap, size, wall, x, y |
| portrait | Thẻ ảnh nhân vật | photo |
| people | Ảnh đại diện nhiều người | people, peopleOut, credit, doc, term, size |
| chat | Cửa sổ hội thoại (minh họa giao diện) | mock, mockText, photo, w, x, y |
| timeline | Dòng thời gian | heading, events |
| bars | Thanh so sánh con số (con số bắt buộc có nguồn) | title, sub, items, max, src, photo, y |
| curve | Đường cong minh họa (ghi chú "không phải dữ liệu thật") | domain, points, labels, ticks, note, drawnBy |
| versus | Đối chiếu hai bên | lines, photos, vsAt |
| image | Ảnh lớn | photo, x, y |
| twocol | Hai cột trái phải | left, right, bottom, y |
| graph | Sơ đồ quan hệ nhỏ (mỗi bài tối đa một hình); chế độ ô vuông `cell` | nodes, edges, title, caption, cell, r, side… |
| terminal | Phát lại terminal thật | rec, from, to, rows, rate, hold, hi, zoom, label, title, doodles, w, x, y, maxH |
| shot | Ảnh chụp màn hình | img, crop, label, credit, push, doodles, w, h, x, y |
| steps | Thẻ các bước | title, items, w, x, y |
| pause | Tạm dừng suy nghĩ | q, a, revealAt, y |
| mindmap | Kết thúc bằng sơ đồ tư duy | center, branches, icon, next, celebrateAt |

`doodles` (terminal / shot): ghi chú kiểu chữ viết tay sổ tay, terminal định vị theo dòng và cột, shot định vị theo tỷ lệ ảnh gốc.

## Quay màn hình terminal (bài thực chiến)

- `scripts/term_record.py`: pty + pyte quay CLI thật (bước work tự động phê duyệt và ghi nhật ký); khi gõ prompt dài phải làm chậm lại (cps 13, dừng 1,8 giây trước khi Enter) và chờ "working" để xác nhận đã gửi.
- `scripts/term_frames.py`: che mờ ở tầng ô ký tự: email, key, tên người dùng máy thay bằng `myname`, xóa dòng nhắc hạn mức, `--drop` xóa tên MCP riêng tư và nhật ký khởi động; ghép cả màn hình để khớp xuyên các dòng.
- `scripts/term_cut.py` cắt đoạn chờ trống, `scripts/regen_recs.sh` tạo lại bằng một lệnh, **trước khi phát hành bắt buộc chạy `scripts/rec_scan.py` để quét quyền riêng tư**.
- Mép dưới cửa sổ terminal ≤ 355 (không đè thanh phụ đề), trình biên dịch đã tự kẹp lại.
- Quay màn hình sẽ tiêu hao hạn mức tài khoản của người dùng: trước khi làm hãy hỏi, sửa cấu hình của người dùng (như `~/.codex/config.toml`) thì phải sao lưu trước, quay xong khôi phục.

## Kinh nghiệm bố cục

- Màn hình trống ở đầu: treo tiêu đề vào cue đầu tiên của nhịp này.
- Cảnh đứng ngay sau opening mà vào quá sớm sẽ khiến phần mở đầu chỉ còn 1–2 giây (check_scenes sẽ báo).
- Chữ ở giữa versus quá dài sẽ đè lên ảnh.
- Sơ đồ quan hệ chỉ chiếm một phần thời gian hình ảnh, đừng để cả phim cứ kéo qua kéo lại trên một hình lớn (khán giả sẽ chóng mặt); đổi chủ đề thì dùng chuyển cảnh.
- Bài nào cũng phải có: chữ gõ dần, ảnh hoặc đoạn video, kết thúc bằng sơ đồ tư duy, biểu tượng hoặc hoạt ảnh nhỏ.
