---
name: ai-teardown
description: Xưởng làm loạt bài giảng "Khóa Mổ xẻ AI": nhập một chủ đề (sản phẩm AI, dự án mã nguồn mở/sách, lịch sử nhân vật, hướng dẫn phần mềm), tạo ra loạt video giảng giải bằng tiếng Trung đi từ nông đến sâu, câu nào cũng có nguồn + bản tương tác cho từng bài + trang tổng hợp khóa học. Quy trình: thu thập tài liệu → xác nhận đối tượng và thời lượng → đại cương → lời dẫn từng bài (giọng nhân bản MiMo + căn chỉnh từng chữ) → dàn cảnh scenes.json (engine vẽ tay tối giản kiểu Notion / engine mẫu macaron, biểu tượng và minh họa IconPark, emoji động Noto, sơ đồ AntV X6, nhân vật giảng giải pixel, khoanh chú thích ảnh chụp, quay màn hình terminal) hoặc phim bằng mã film.js (engine cine: Three.js, hạt, shader, chồng đoạn phim thật, nhạc nền từ thư viện) → render từng khung 1080p bằng Hyperframes / GPU không đầu → xuất bản Artifact → trang tổng hợp khóa học + video dẫn nhập. Kích hoạt: làm loạt bài giảng / làm video khóa học / biến một cuốn sách hay một dự án mã nguồn mở thành khóa học / video phổ biến kiến thức / video dạy học / bản đồ khóa học / video dẫn nhập / giáo án tương tác / "khóa mổ xẻ", "khóa làm quen", "khóa thực chiến", "khóa dàn dựng" / phim giảng giải cực mạnh / dùng phiên làm việc thật và thành phẩm để dạy người khác làm video. Không dùng cho: một phim quảng bá đơn lẻ (dùng promo-video), một infographic đơn lẻ, viết bài thuần túy.
---

# Khóa Mổ xẻ AI · Xưởng làm loạt bài giảng

Một chủ đề → cả một bộ khóa học: video giảng giải 4–7 phút cho mỗi bài (MP4 1080p), trang web tương tác cùng nguồn (có thể tạm dừng, bấm vào hình để xem nguồn), trang tổng hợp khóa học gồm đại cương và video, cộng thêm video dẫn nhập 2–3 phút.

Các thành phẩm đã kiểm chứng (cùng một bộ engine):
- Mùa 1 "Khóa nhập môn AI" 12 bài (chủ đề macaron/bạc hà, lịch sử nhân vật + khái niệm)
- Mùa 2 "Khóa thực chiến AI: từ prompt đến Codex" 13 bài (quay màn hình terminal thật + giảng giải bằng nét vẽ nguệch ngoạc)
- "Khóa làm quen WorkBuddy" 25 bài + dẫn nhập (phong cách vẽ tay tối giản kiểu Notion, chuyển thể từ sách mã nguồn mở, nhân vật giảng giải pixel)
- "Claude Code làm video: khóa dàn dựng Opus 5.5" dẫn nhập + 10 bài, "Khóa thực chiến phim quảng bá Opus 5.5" dẫn nhập + 8 bài + bài bổ sung theo ngành (engine phim bằng mã cine: mỗi khung hình do mã tính ra, chồng đoạn phim thật, một phiên làm việc thật xuyên suốt khóa)

## Nguyên tắc cốt lõi (không được bỏ)

1. **Không có nguồn thì không lên màn hình**: con số, tính năng, bước thực hiện, trích dẫn đều phải truy được về nguồn; trích dẫn đúng từng chữ, ghi rõ chương; suy đoán phải nói "có thể"; dữ liệu minh họa ghi rõ "dữ liệu ví dụ".
2. **Một nguồn hai đầu ra**: cùng một bộ narration.json + scenes.json xuất đồng thời MP4 và bản tương tác.
3. **Từ nông đến sâu, mỗi bài nói ba việc**: mở đầu "bài này nói ba việc", giữa bài có ít nhất một "tạm dừng suy nghĩ", cuối bài ôn lại bằng sơ đồ + giới thiệu bài sau.
4. **Chốt trước rồi mới làm**: tài liệu, đối tượng, thời lượng, đại cương, giọng đọc, phong cách hình ảnh đều phải để người dùng xác nhận trước rồi mới sản xuất hàng loạt.
5. **Quyền riêng tư và bản quyền**: thông tin cá nhân, mã QR, khóa bí mật, tên người dùng máy cục bộ trong ảnh chụp đều phải cắt bỏ hoặc che mờ; nguồn thư viện biểu tượng, minh họa được ghi thống nhất ở thẻ cảm ơn cuối phim, nguồn của nội dung sách và ảnh chụp được ghi từng chỗ.

## Không gian làm việc

Engine nằm trong `engine/` của skill này. Tạo không gian làm việc và loạt bài trước:

```bash
python3 ~/.claude/skills/ai-teardown/engine/scripts/new_series.py ~/Desktop/<không-gian-làm-việc> <tên-loạt-bài> --style sketch --title "Tên khóa học"
```

- `--style sketch`: Notion tối giản + engine vẽ tay + nhân vật giảng giải pixel + **phong cách sticker (mặc định cho khóa mới, đầu file scenes.json có `"sticker": true`)** (khuyên dùng; để giảng về phần mềm, sách, dự án mã nguồn mở).
- `--style lesson`: trình biên dịch mẫu (chủ đề macaron/bạc hà/ban đêm, giỏi về nhân vật, dòng thời gian, quay màn hình terminal).
- `--style cine`: engine phim bằng mã (cảnh tối với hình ảnh "cực mạnh": hạt, góc máy 3D, shader, chữ lớn động; có thể chồng đoạn phim thật, nhạc nền từ thư viện; chỉ xuất video, không xuất bản tương tác). Dùng cho các khóa như dàn dựng AI, hiệu ứng, làm video mà "bản thân bộ phim chính là tác phẩm", hoặc khóa thực chiến. Chi tiết xem `references/10-cine.md`, cách làm khóa thực chiến xem `references/11-practice-course.md`.
- Nếu đã có không gian làm việc (dự án gốc ở `~/Desktop/ai-teardown`) thì tạo loạt bài ngay trong đó.
- Thư mục bài học phải nằm trong không gian làm việc: `<không-gian-làm-việc>/examples/<loạt-bài>/lessons/<NN>/`.

Phụ thuộc môi trường và cấu hình một lần xem mục "Môi trường" trong `references/02-pipeline.md` (khóa MiMo, mô hình whisper, Playwright, Hyperframes, esbuild, thư viện nhạc nền).

## Quy trình (sáu giai đoạn, ba điểm xác nhận)

| Giai đoạn | Làm gì | Đầu ra | Chi tiết |
|---|---|---|---|
| ① Tra cứu | Thu thập tài liệu, phân cấp T1 chính thức / T2 thứ cấp uy tín / T3 cộng đồng, ghi sự kiện và nguồn | `research/`, `landscape.md` | references/01-workflow.md |
| **Xác nhận 1** | Đối tượng, thời lượng, số bài, giọng đọc (nghe thử trước), phong cách hình ảnh (làm bản mẫu trước) | `DECISIONS.md` | |
| ② Đại cương | Đại cương: tiêu đề mỗi bài, một câu dẫn, giới thiệu, các ý chính, thời lượng → bản nháp trang tổng hợp khóa học | `series.json` → trang khóa học | |
| **Xác nhận 2** | Người dùng xem đại cương và chốt | | |
| ③ Viết | narration.json cho mỗi bài (18–28 nhịp, 1200–2200 chữ, đánh dấu `[[cue]]`) → lồng tiếng MiMo + kiểm tra bằng đọc lại | `build/audio/` | references/03-narration-voice.md |
| ④ Dàn cảnh | Dàn cảnh scenes.json → check_scenes → build contact sheet và xem từng khung | `build/stills/scenes.png` | references/04, 05 |
| ⑤ Render | Hàng đợi render tuần tự → trích khung kiểm tra | `hf/renders/lessonNN.mp4` | references/02-pipeline.md |
| ⑥ Xuất bản | Artifact bản tương tác, trang tổng hợp khóa học (>64MB thì xuất bản theo từng đợt), video dẫn nhập, thư mục tổng hợp video cục bộ | liên kết + thư mục | references/02-pipeline.md |
| **Xác nhận 3** | Cho người dùng xem thành phẩm bài 1, sửa mẫu theo phản hồi rồi mới làm hàng loạt | | |

Khi làm hàng loạt thì dùng đa tác tử: mỗi trợ lý dựa vào `BRIEF.md` trong thư mục loạt bài để làm "lời dẫn + lồng tiếng + dàn cảnh" cho một bài (không render, không xuất bản, không sửa mã engine), phiên chính chịu trách nhiệm kiểm tra, xếp hàng render, xuất bản. Mở 3 trợ lý mỗi lần. Mẫu BRIEF xem `references/brief-template.md` (loạt cine dùng `templates/series-cine/BRIEF.md`).

Với loạt cine thì dàn cảnh và render đổi thành: viết `lessons/NN/film.js` → xem contact sheet bằng `cine/tools/stills.py` → `cine/queue.txt` + `cine/tools/queue.sh` (clips → record → finish → deliver), lệnh xem `references/10-cine.md`.

## Lệnh thường dùng (chạy ở thư mục gốc của không gian làm việc)

```bash
L=examples/<loạt-bài>/lessons/NN
python3 scripts/make_lesson.py $L voice > $L/voice.log 2>&1   # lồng tiếng + căn chỉnh whisper + MiMo đọc lại
python3 scripts/check_scenes.py $L                              # tự kiểm tra cảnh
rm -rf $L/build/stills && python3 scripts/make_lesson.py $L build   # dàn cảnh + contact sheet
echo NN >> examples/<loạt-bài>/render.queue                         # xếp vào hàng đợi render (runner xem 02-pipeline)
python3 scripts/sketch_publish_files.py $L                      # tính các file cần tải lên cho bản tương tác
python3 scripts/course_page.py examples/<loạt-bài>/series.json examples/<loạt-bài>/publish/course
```

## Cổng kiểm tra chất lượng (bài nào cũng phải qua)

- voice.log: nhịp nào đọc lại < 95% hoặc xuất hiện "⚠ có số đọc đáng ngờ" thì xóa `build/audio/<nhịp>.*` rồi tổng hợp lại; tên riêng, từ viết tắt thì nghe lại bằng whisper-cli để xác nhận.
- Contact sheet + các khung đơn đáng ngờ: chữ tràn/chồng lên nhau, khoanh chú thích lệch, màn hình trống, nhân vật che chữ, chữ nhỏ ghi nguồn bị đè.
- Trích 6 khung từ thành phẩm ghép thành ảnh ghép và xem lại một lượt rồi mới xuất bản.
- Toàn văn danh sách xem `references/07-qa-checklist.md`; các lỗi đã gặp xem `references/08-pitfalls.md` (bắt buộc đọc trước khi sửa engine).

## Tài liệu tham khảo

| File | Nội dung |
|---|---|
| references/01-workflow.md | Quy trình sáu giai đoạn, cách hỏi ở các điểm xác nhận, phân công đa tác tử, bản đồ khóa học/video dẫn nhập |
| references/02-pipeline.md | Cấu trúc thư mục, phụ thuộc môi trường, ba đoạn của make_lesson, hàng đợi render, xuất bản và trang khóa học, tổng hợp video |
| references/03-narration-voice.md | Cách viết lời dẫn, lồng tiếng và nhân bản giọng MiMo, lexicon, kiểm tra bằng đọc lại, bản tiếng Anh |
| references/04-scenes-sketch.md | Toàn bộ mẫu và trường của engine vẽ tay (giao diện Notion), nhân vật giảng giải, góc máy |
| references/05-scenes-lesson.md | Mẫu của trình biên dịch mẫu (mùa 1, 2), quay màn hình terminal, nét vẽ nguệch ngoạc |
| references/06-visual-assets.md | Biểu tượng, minh họa, emoji động Noto, X6, nhập ảnh chụp và sổ cái, quy tắc ghi công |
| references/07-qa-checklist.md | Danh sách kiểm tra chất lượng trước khi xuất bản |
| references/08-pitfalls.md | Các lỗi đã gặp và cách sửa |
| references/09-safety.md | Quy tắc về quyền riêng tư, bản quyền, khóa bí mật, che mờ khi quay màn hình |
| references/10-cine.md | Engine phim bằng mã cine: thư mục, môi trường, hợp đồng film.js, thành phần và cảnh, đoạn phim và nhạc nền từ thư viện, hàng đợi render, kiểm tra chất lượng, các lỗi |
| references/11-practice-course.md | Cách làm khóa thực chiến: tường tác phẩm chỉ dùng bản cuối, ghi phiên làm việc thật và mức tiêu thụ, phim khái niệm ngành (tuân thủ), bài bổ sung phân tích phim, trang khóa học |
| references/brief-template.md | Mẫu hướng dẫn "làm một bài học" cho trợ lý |
| references/design/ | Tài liệu thiết kế gốc 00–09 (hợp đồng dữ liệu, hợp đồng cảnh, nguyên thủy, hệ thống hình ảnh, phương pháp sư phạm, nguồn tin, cổng kiểm tra chất lượng) |
| templates/series-sketch/ | BRIEF, SCENES_GUIDE, ví dụ series.json của loạt vẽ tay kiểu Notion, hai bài thành phẩm (bài 17, dẫn nhập) |
| templates/series-lesson/ | BRIEF, DECISIONS, ví dụ series.json của loạt dùng trình biên dịch mẫu, một bài thành phẩm |
| templates/series-cine/ | Mẫu BRIEF của loạt cine, bốn bản hướng dẫn đã dùng thật (khóa dàn dựng, khóa thực chiến phim quảng bá, phim khái niệm ngành, bài bổ sung phân tích phim), film.js của hai bài thành phẩm, check_timings / update_series, công cụ ghi phiên làm việc thật |
| engine/cine/ | Bản thân engine cine (new_series.py --style cine sao chép vào thư mục loạt bài) |
| presets/ | Nhân vật giảng giải pixel 10 động tác × 8 khung (+ sổ cái, prompt tạo ảnh), tham chiếu giọng nhân bản đã khóa |
