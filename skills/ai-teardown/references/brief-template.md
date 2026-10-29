# Hướng dẫn "làm một bài học" cho trợ lý · Mẫu

Cách dùng: khi bắt đầu một series mới, sao chép phần "BRIEF series" bên dưới thành `examples/<系列>/BRIEF.md`, thay nội dung trong dấu ngoặc nhọn bằng nội dung của series này; khi giao việc cho trợ lý thì đính kèm thêm một đoạn "Mô tả nhiệm vụ bài này". Bản mẫu hoàn chỉnh xem `templates/series-sketch/BRIEF.md` (phiên bản thực tế dùng cho khoá nhập môn WorkBuddy).

## Mô tả nhiệm vụ bài này (viết mỗi lần giao việc cho trợ lý, phải tự đủ ý)

```
Bạn cần làm lời dẫn, lồng tiếng và dàn dựng hình ảnh cho bài thứ <N> của "<tên series>", không render thành phẩm.
Đọc kỹ toàn bộ <workspace>/examples/<系列>/BRIEF.md và làm đúng theo đó, rồi đọc SCENES_GUIDE.md cùng thư mục, tham khảo narration.json và scenes.json của lessons/<hai bài mới nhất>/.

Thông tin bài này:
- Thư mục bài: examples/<系列>/lessons/<NN> (n = <N>)
- Tiêu đề: <theo đăng ký trong series.json>
- Nguồn nội dung: <tên thư mục chương X của sách gốc / đường dẫn tài liệu nghiên cứu>; chạy ls trước để tìm tên thư mục thực tế
- Nhập ảnh minh hoạ: python3 scripts/wb_import.py examples/<系列>/lessons/<NN> "<tên thư mục>" --prefix <tiền tố>
- Trọng tâm nội dung: <nói ba phần nào; dùng hình ảnh gì (diagram / shot / dataviz)>
- Liên kết: mở đầu nối tiếp bài trước "<tiêu đề>", cuối bài giới thiệu bài sau "<tiêu đề>"
- Số chương: luôn viết theo tên thư mục
- Riêng tư: <lưu ý đặc biệt của bài này: tên tác giả, tài khoản, khoá bí mật trong ảnh chụp màn hình...>
- Nguồn: nguồn của bộ icon và thư viện minh hoạ chỉ ghi một lần ở credits cuối phim; ảnh chụp màn hình và nguồn nội dung trong sách vẫn ghi như thường

Hạn chế đã biết của mẫu (cần tránh):
1. Mỗi nhánh của recap ≤ 9 chữ
2. Tiêu đề stickers không đặt tên tiếng Anh dài, đặt vào sub; tick/cross ghi thời điểm
3. Tự động xuống dòng của quote sẽ cắt giữa từ, khi cần thì xuống dòng thủ công bằng \n
4. Nhãn diagram viết ngắn; tránh nét nối giao nhau bằng cách sắp xếp vị trí
5. shot ưu tiên dùng tips của nhân vật que, hạn chế dùng nhãn note
6. Nguồn của dataviz ghi ở src

Hoàn thành thì báo cáo theo định dạng trong BRIEF.
```

---

## BRIEF series (tham khảo nguyên mẫu, chỉnh sửa theo từng series)

# Khoá nhập môn WorkBuddy · Hướng dẫn đầy đủ để làm một bài học (dành cho trợ lý)

Thư mục gốc của kho: `~/Desktop/ai-teardown` (các lệnh bên dưới đều chạy ở đây). Thư mục series: `examples/workbuddy`.
**Đọc trước**: `examples/workbuddy/SCENES_GUIDE.md` (mẫu và các trường), rồi xem hai bài đã hoàn thành để tham khảo: `lessons/03/narration.json`, `lessons/03/scenes.json` (mới nhất, hiệu ứng đầy đủ nhất), `lessons/02/scenes.json`.

## Nguồn nội dung và giới hạn bắt buộc
- Nội dung chỉ lấy từ chương tương ứng trong cuốn mã nguồn mở «Sách xanh thực chiến WorkBuddy»: `examples/workbuddy/source/docs/bluebook/<篇>/<章>/index.md` (MIT, được trích dẫn, hình ảnh phải ghi nguồn).
- **Không bịa đặt**: số liệu, giá cả, tính năng, chữ trên giao diện, các bước đều lấy theo bản gốc; bản gốc không viết thì không bổ sung. Trích dẫn bản gốc phải đúng từng chữ, trường `from` của mẫu quote ghi "«Sách xanh thực chiến WorkBuddy»第 N 章".
- Mã QR cá nhân, thông tin liên hệ cá nhân, số nhóm, mã mời, khoá tài khoản (AppID/Secret/Token) trong bản gốc tuyệt đối không đưa lên hình; ảnh chụp màn hình có khoá thì hoặc không dùng, hoặc dùng crop cắt bỏ.
- Các bước liên quan đến cấp quyền, khoá bí mật, gửi tin ra ngoài thì nhắc ranh giới an toàn theo bản gốc; nhân vật que giảng bài có thể thêm một câu nhắc an toàn ngắn (tips, pose dùng "stop"), nhưng không thay tác giả phát biểu quan điểm.
- Khi chương rất dài (trên 10 nghìn chữ): chọn 3 phần cốt lõi nhất để nói rõ, không cần bao quát hết; với chương dạng ca thực tế thì nói theo mạch "bối cảnh → đã dùng gì (Skill/chuyên gia/connector) → giao nhiệm vụ thế nào → kết quả và nghiệm thu".

## Lời dẫn narration.json
- Phần `voice` chép nguyên khối từ voice trong `lessons/03/narration.json` (giọng Gemini Sulafat + `director` tiếng Anh kiểu giảng bài), `lexicon` thêm khi cần (từ viết tắt hay tên riêng bị đọc lệch thì ghi vào lexicon; số phiên bản viết thành "0 chấm 1 chấm 2").
- 18–28 nhịp, cả bài 1200–2200 chữ (sau khi tăng tốc 1.15 lần là 4–7 phút). Mỗi nhịp 40–130 chữ, mỗi nhịp 2–4 `[[cue]]` (chữ thường tiếng Anh/số/dấu gạch dưới, đặt ở đầu mỗi vế câu).
- Khẩu ngữ, câu ngắn, ngôi thứ hai; câu mở đầu nối tiếp bài trước ("Bài trước chúng ta……"), phần kết giới thiệu bài sau + cảm ơn tác giả cuốn sách xanh + "Hẹn gặp lại ở bài sau".
- Ít nhất một đoạn "tạm dừng suy nghĩ" (một nhịp đặt câu hỏi, nhịp sau dùng `[[answer]]` để công bố đáp án).

## Hình ảnh scenes.json
- Phần đầu tệp: `{"n": N, "title": "…", "series": "Khoá nhập môn WorkBuddy", "theme": "paper", "engine": "sketch", "skin": "notion", "presenter": "hp", "speed": 1.15, "author": "@Berryxia", "scenes": [...]}`
- Mỗi bài bắt buộc phải có: cover (kèm `iconImg: "host-avatar"` và một `illus`), ít nhất 1 câu vàng kinetic, 1 pan ("Bài này nói ba việc"), pause, recap, outro; khi dùng ảnh chụp màn hình để giảng thao tác thì dùng shot + marks khoanh chú thích; khi có quy trình/phân công/luồng dữ liệu thì dùng diagram (X6); khi có tình huống thì dùng say + minh hoạ illus.
- Icon: quy trình, danh sách, giải thích giao diện dùng IconPark (`icon-park:名字`, tên phải có trong `assets/iconsets/icon-park.json`); cảm xúc, đồ vật của nhân vật chính dùng Noto (loại như `robot`, chạy noto_emoji.py trước).
- Minh hoạ: `assets/illustrations/iconpark/catalog.json` có 88 hình (id, album, tên), chọn hình phù hợp rồi dùng `python3 scripts/illus.py examples/workbuddy/lessons/NN ip-x-y …`. Mỗi bài 2–4 hình, đừng lặp lại hình đã dùng ở các bài trước (bài 03 đã dùng ip-17-232, ip-2-12, ip-14-187).
- Động tác pose của nhân vật que: talk wave point idea think stop check cheer thumbsup type (mặc định: shot→point, pause→think, checklist→check, outro→wave); outro ghi `"pose": "cheer"`, câu "Hẹn gặp lại bài sau 👋" trong tips dùng wave.
- Credits của outro: nội dung và ảnh chụp màn hình (chương N MIT + địa chỉ kho) / minh hoạ thư viện minh hoạ IconPark (ByteDance) · icon IconPark, Noto Emoji / sơ đồ AntV X6 · lottie-web · rough.js / nhân vật que giảng bài avatar pixel @Berryxia · lồng tiếng Google Gemini (do AI tạo). Mỗi dòng không quá 40 ký tự. Nguồn của icon và thư viện minh hoạ chỉ ghi trên thẻ cuối phim này, trong các cảnh đừng viết thêm dòng chữ nhỏ kiểu "Minh hoạ: IconPark…" (runtime đã mặc định tắt phần ghi nguồn dưới minh hoạ); nguồn của nội dung và ảnh chụp màn hình trong sách vẫn ghi như thường.
- area của khoanh chú thích trên ảnh chụp là tỷ lệ theo ảnh gốc [x0,y0,x1,y1]: mở `build/chapter_sheet.jpg` xem ảnh thu nhỏ trước, rồi dùng Read mở ảnh gốc `examples/workbuddy/assets/img/<id>.png` để ước lượng toạ độ, sau khi build thì xem contact sheet để xác nhận đã khớp.

## Các bước (bước nào cũng phải làm)
1. Đọc bản gốc của chương và tổng quan ảnh minh hoạ:
   `python3 scripts/wb_import.py examples/workbuddy/lessons/NN "第 X 章 ……"` (chép nguyên tên thư mục chương; nhập ảnh chụp wbNN-01…, GIF chuyển thành clip, đồng thời tạo `build/chapter_sheet.jpg`)
2. Viết `narration.json`, bắt đầu lồng tiếng (sẽ xếp hàng thử lại, chậm là bình thường):
   `python3 scripts/make_lesson.py examples/workbuddy/lessons/NN voice > examples/workbuddy/lessons/NN/voice.log 2>&1`
   Lồng xong thì xem voice.log: nhịp nào "đọc lại" dưới 95%, hoặc xuất hiện "⚠ cách đọc đáng ngờ", thì xoá `lessons/NN/build/audio/<số nhịp>.*` rồi chạy voice lại một lần (chỉ tổng hợp lại những nhịp đó).
3. Chuẩn bị tư liệu: `python3 scripts/noto_emoji.py examples/workbuddy/lessons/NN robot light-bulb …`; `python3 scripts/illus.py examples/workbuddy/lessons/NN ip-…`
4. Viết `scenes.json`, tự kiểm tra: chạy `python3 scripts/check_scenes.py examples/workbuddy/lessons/NN` đến khi không còn lỗi (cảnh báo "chỉ có x giây" cũng phải sửa).
5. Dàn dựng:`rm -rf examples/workbuddy/lessons/NN/build/stills && python3 scripts/make_lesson.py examples/workbuddy/lessons/NN build`
   Dùng Read xem `lessons/NN/build/stills/scenes.png`, rồi xem từng khung hình đáng ngờ (`scenes-XXX.XX.png`): chữ tràn/chồng nhau, khoanh chú thích không khớp, ảnh chụp quá nhỏ không nhìn rõ, màn hình trống, nhân vật que che chữ. Sửa scenes.json rồi làm lại cho đến khi hài lòng.
6. **Không** chạy final (render), không xuất bản, không sửa mã dưới `runtime/ primitives/ scripts/`, không sửa `series.json` và thư mục của các bài khác. Mẫu có lỗi hoặc thiếu tính năng thì ghi vào báo cáo.

## Báo cáo (tin nhắn cuối cùng)
Một đoạn văn: số bài và tiêu đề, số nhịp và thời lượng ("tổng độ dài" trong đầu ra của build), đã dùng những ảnh chụp/minh hoạ/diagram nào, có nội dung bản gốc nào bị bỏ hoặc không nói đến không, những nhịp nào đã được tổng hợp giọng lại, các vấn đề đã biết còn tồn tại.
