# Khóa nhập môn WorkBuddy · Hướng dẫn đầy đủ để làm một bài học (dành cho trợ lý)

Thư mục gốc kho mã: `~/Desktop/ai-teardown` (các lệnh bên dưới đều chạy ở đây). Thư mục series: `examples/workbuddy`.
**Đọc trước**: `examples/workbuddy/SCENES_GUIDE.md` (mẫu và trường), sau đó xem hai bài thành phẩm để tham khảo: `lessons/03/narration.json`, `lessons/03/scenes.json` (mới nhất, hiệu ứng đầy đủ nhất), `lessons/02/scenes.json`.

## Nguồn nội dung và giới hạn
- Nội dung chỉ lấy từ chương tương ứng của cuốn mã nguồn mở "Sách trắng thực chiến WorkBuddy": `examples/workbuddy/source/docs/bluebook/<phần>/<chương>/index.md` (MIT, được phép trích dẫn, trên hình phải ghi nguồn).
- **Không bịa**: con số, giá, tính năng, chữ trên giao diện, các bước đều theo bản gốc; bản gốc không viết thì đừng bổ sung. Trích dẫn bản gốc phải đúng từng chữ, trường `from` của mẫu quote viết "Sách trắng thực chiến WorkBuddy, chương N".
- Mã QR cá nhân, thông tin liên hệ cá nhân, số nhóm, mã mời, khóa tài khoản (AppID/Secret/Token) trong bản gốc tuyệt đối không đưa lên hình; ảnh chụp có khóa thì hoặc không dùng, hoặc dùng crop cắt bỏ.
- Với các bước liên quan đến ủy quyền, khóa, gửi tin ra ngoài, hãy nhắc ranh giới an toàn theo bản gốc; nhân vật giảng giải có thể thêm một câu nhắc an toàn ngắn (tips, pose dùng "stop"), nhưng không phát biểu quan điểm thay tác giả.
- Chương rất dài (trên 1 vạn chữ): chọn 3 phần cốt lõi nhất để giảng rõ, không cần bao quát hết; chương dạng ca sử dụng thì giảng theo "tình huống → đã dùng gì (Skill/chuyên gia/connector) → giao nhiệm vụ thế nào → kết quả và nghiệm thu".

## Lời dẫn narration.json
- `voice` chép nguyên đoạn voice của `lessons/03/narration.json` (giọng Gemini Sulafat + `director` tiếng Anh kiểu giảng bài), `lexicon` thêm khi cần (từ viết tắt hay tên riêng bị đọc lệch thì ghi vào lexicon; số phiên bản viết thành "0 chấm 1 chấm 2").
- 18–28 nhịp, cả bài 1200–2200 chữ (sau khi tăng tốc 1,15 lần là 4–7 phút). Mỗi nhịp 40–130 chữ, mỗi nhịp 2–4 `[[cue]]` (chữ thường tiếng Anh/chữ số/gạch dưới, đặt ở đầu mệnh đề).
- Khẩu ngữ, câu ngắn, ngôi thứ hai; câu mở đầu nối với bài trước ("Bài trước chúng ta……"), kết thúc báo trước bài sau + cảm ơn tác giả sách trắng + "hẹn gặp lại ở bài sau".
- Ít nhất một lần "tạm dừng suy nghĩ" (một nhịp đặt câu hỏi, nhịp sau `[[answer]]` công bố đáp án).

## Hình ảnh scenes.json
- Đầu file: `{"n": N, "title": "…", "series": "Khóa nhập môn WorkBuddy", "theme": "paper", "engine": "sketch", "skin": "notion", "presenter": "hp", "sticker": true, "speed": 1.15, "author": "@Berryxia", "scenes": [...]}`
- **Phong cách sticker là mặc định**: đầu file viết `"sticker": true` (thẻ = sticker viền trắng dán nghiêng, hình minh họa = viền trắng cắt khuôn, emoji Noto trong thẻ cũng viền trắng); trang nào không muốn sticker thì viết `"style": "card"` (stickers) hoặc `"illusSticker": false`.
- Mỗi bài bắt buộc dùng đến: cover (kèm `iconImg: "host-avatar"` và một `illus`), ít nhất 1 câu vàng kinetic, 1 pan ("bài này nói ba việc"), pause, recap, outro; khi giảng thao tác bằng ảnh chụp thì dùng shot + marks khoanh chú thích; khi có quy trình/phân công/luồng dữ liệu thì dùng diagram (X6); khi có tình huống thì dùng say + hình minh họa illus.
- Biểu tượng: quy trình, danh sách, giải thích giao diện dùng IconPark (`icon-park:tên`, tên phải có trong `assets/iconsets/icon-park.json`); cảm xúc, vật dụng của nhân vật chính dùng Noto (loại như `robot`, chạy noto_emoji.py trước).
- Hình minh họa: `assets/illustrations/iconpark/catalog.json` có 88 hình (id, album, tên), chọn hình phù hợp rồi dùng `python3 scripts/illus.py examples/workbuddy/lessons/NN ip-x-y …`. Mỗi bài 2–4 hình, đừng lặp lại đúng hình đã dùng ở các bài trước (bài 03 đã dùng ip-17-232, ip-2-12, ip-14-187).
- Động tác nhân vật pose: talk wave point idea think stop check cheer thumbsup type (mặc định: shot→point, pause→think, checklist→check, outro→wave); outro viết `"pose": "cheer"`, trong tips câu "hẹn gặp lại ở bài sau 👋" dùng wave.
- credits của outro: nội dung và ảnh chụp (chương N MIT + địa chỉ kho mã) / hình minh họa thư viện minh họa IconPark (ByteDance) · biểu tượng IconPark, Noto Emoji / sơ đồ quy trình AntV X6 · lottie-web · rough.js / nhân vật giảng giải ảnh đại diện pixel @Berryxia · lồng tiếng Google Gemini (do AI tạo). Mỗi dòng đừng quá 40 chữ Hán. Nguồn của biểu tượng, thư viện minh họa chỉ ghi trên thẻ kết này, trong các cảnh đừng viết thêm chữ nhỏ kiểu "Minh họa: IconPark…" nữa (runtime đã mặc định tắt phần nguồn dưới hình minh họa); nguồn của nội dung và ảnh chụp trong sách vẫn ghi bình thường.
- area của khoanh chú thích trên ảnh chụp là tỷ lệ ảnh gốc [x0,y0,x1,y1]: mở `build/chapter_sheet.jpg` xem ảnh thu nhỏ trước, rồi dùng Read mở ảnh gốc `examples/workbuddy/assets/img/<id>.png` để ước lượng tọa độ, sau khi build xem contact sheet để xác nhận đã căn đúng.

## Các bước (bước nào cũng phải làm)
1. Đọc nguyên văn chương và tổng quan ảnh minh họa:
   `python3 scripts/wb_import.py examples/workbuddy/lessons/NN "第 X 章 ……"` (tên thư mục chương chép nguyên; nhập ảnh chụp wbNN-01…, GIF thành clip, và tạo `build/chapter_sheet.jpg`)
2. Viết `narration.json`, bắt đầu lồng tiếng (sẽ xếp hàng thử lại, chậm là bình thường):
   `python3 scripts/make_lesson.py examples/workbuddy/lessons/NN voice > examples/workbuddy/lessons/NN/voice.log 2>&1`
   Lồng xong xem voice.log: nhịp nào "đọc lại" dưới 95%, hoặc xuất hiện "⚠ số đọc đáng ngờ" thì xóa `lessons/NN/build/audio/<số-nhịp>.*` rồi chạy lại voice (chỉ tổng hợp lại những nhịp này).
3. Chuẩn bị tư liệu: `python3 scripts/noto_emoji.py examples/workbuddy/lessons/NN robot light-bulb …`; `python3 scripts/illus.py examples/workbuddy/lessons/NN ip-…`
4. Viết `scenes.json`, tự kiểm tra: `python3 scripts/check_scenes.py examples/workbuddy/lessons/NN` cho đến khi không còn lỗi ("chỉ có x giây" cũng phải sửa).
5. Dàn cảnh: `rm -rf examples/workbuddy/lessons/NN/build/stills && python3 scripts/make_lesson.py examples/workbuddy/lessons/NN build`
   Dùng Read xem `lessons/NN/build/stills/scenes.png`, rồi xem từng khung đơn đáng ngờ (`scenes-XXX.XX.png`): chữ tràn/chồng lên nhau, khoanh chú thích chưa căn đúng, ảnh chụp quá nhỏ không nhìn rõ, màn hình trống, nhân vật che chữ. Sửa scenes.json rồi làm lại, đến khi hài lòng.
6. **Không** chạy final (render), không phát hành, không sửa mã dưới `runtime/ primitives/ scripts/`, không sửa `series.json` và thư mục của các bài khác. Mẫu có lỗi hoặc thiếu tính năng thì ghi vào báo cáo.

## Báo cáo (tin nhắn cuối cùng)
Một đoạn: số bài và tiêu đề, số nhịp và thời lượng ("tổng độ dài" in ra từ build), đã dùng những ảnh chụp/hình minh họa/diagram nào, có nội dung bản gốc nào bị bỏ hoặc không giảng không, voice đã tổng hợp lại những nhịp nào, các vấn đề đã biết còn tồn tại.
