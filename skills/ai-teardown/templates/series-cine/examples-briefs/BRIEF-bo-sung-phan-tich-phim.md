# Làm một bài "Bổ sung · phân tích một phim theo ngành" — hướng dẫn cho trợ lý

Phần chính khóa của khóa thực chiến phim quảng bá (dẫn nhập + bài 1–8) đã bàn giao, người dùng đã duyệt. Bây giờ thêm 5 bài bổ sung, mỗi bài phân tích một **phim khái niệm ngành không chính thức** mà chúng ta mới làm cho khóa này, số bài p09–p13. Cách viết, engine, quy tắc của phần chính khóa giữ nguyên toàn bộ: **đọc trọn `promo/BRIEF.md` trước** (engine, đoạn phim, nhạc nền, cách viết, nguồn sự kiện, hai quy tắc mới về tên cue và dấu gạch nối đều ở trong đó), rồi đọc bài mẫu `lessons/p08/film.js` (bài 8: mở đầu phát trọn một lượt thành phẩm, kèm âm thanh gốc, giống phần mở đầu của bài bạn làm) và `lessons/p03/film.js` (bài 3: cách đưa nguyên văn thẻ chọn phương án, bảng phân cảnh lên màn hình). Thư mục làm việc `/Users/you/Desktop/ai-teardown/examples/claude-video`.

Để ít bị đứt kết nối: mỗi lần chỉ đọc vài dòng file cần thiết, mỗi lần xem tối đa 2 ảnh, lệnh càng ngắn càng tốt.

## Mỗi bài phân tích gì (tư liệu đều nằm trong dự án riêng của phim đó)
`~/Desktop/brand-promos/<thương hiệu>/`:
- `out/film.mp4` (thành phẩm, 28–30 giây), `out/sheet.jpg` (ảnh ghép 12 khung), `out/stills/`
- `DECISIONS.md`: **nguồn sự kiện chính của bài này**: nguyên văn thẻ chọn phương án, bảng phân cảnh, nhạc nền và BPM, nguồn tư liệu (URL website chính thức), nguồn sự kiện (câu gốc và trang của từng con số trên màn hình), danh sách ảnh do AI tạo, các vấn đề nó tự sửa khi duyệt phim (trước → sau)
- `src/`: mã hình ảnh (chọn 1–2 đoạn mã thật đưa lên màn hình để giảng góc máy xuất sắc nhất); `public/`: tư liệu nó lấy từ website chính thức (Logo, ảnh sản phẩm, phông chữ) và ảnh Codex

## Cấu trúc (14–16 nhịp, 950–1200 chữ, sau khi tăng tốc 1,15 lần khoảng 3,5 phút)
- **Mở đầu**: phát trọn một lượt thành phẩm (đoạn phim toàn màn hình `audio: "full"`, `gain: -1`, lời dẫn của đoạn mở đầu này để trống, nhạc nền hạ về 0), phát xong thì tên khóa học đập xuống: "Bổ sung · <ngành>: phân tích <thương hiệu>", bên dưới một dòng móc câu, thêm một nhãn nhỏ "Phim khái niệm không chính thức · chỉ dùng để minh họa khóa học". `COLD` = độ dài phim + khoảng 3 giây.
- B01 nối tiếp: phim vừa rồi được tạo ra thế nào (trợ lý theo promo video skill làm từ website chính thức cho đến thành phẩm, người dùng không tham gia xác nhận).
- B02 bài này nói ba việc: ① website chính thức đã cho gì, nó chọn thẻ nào ② phân cảnh, nhạc nền và góc máy xuất sắc nhất ③ duyệt phim đã sửa gì, giữ tuân thủ thế nào.
- Việc thứ nhất: tư liệu website chính thức → hình ảnh trong phim (trái là ảnh gốc trên website, phải là khung hình đó trong thành phẩm, dùng ảnh trong `public/` và đoạn phim thành phẩm); vì sao nó chọn thẻ như vậy (mặc định của ngành so với dáng vẻ của chính website thương hiệu, trích nguyên văn DECISIONS).
- Giữa bài một nhịp "tạm dừng suy nghĩ" + nhịp kế tiếp `[[answer]]` (ví dụ: nếu áp phong cách dựng nhanh công nghệ nền tối cho thương hiệu này thì sẽ ra sao?).
- Việc thứ hai: bảng phân cảnh (trích nguyên văn vài dòng) + BPM và điểm khớp nhịp + 1–2 góc máy xuất sắc nhất (đoạn phim + trích đoạn mã).
- Việc thứ ba: các vấn đề nó đã sửa khi duyệt phim (trước → sau, mục 7/8 của DECISIONS, có khung mẫu cũ thì đặt cạnh nhau); tuân thủ: tuyên bố cuối phim, nguồn website chính thức của con số trên màn hình, không dùng từ tuyệt đối hóa, Codex chỉ vẽ bầu không khí.
- Nhịp áp chót ôn lại bằng sơ đồ (`recapMap`); nhịp cuối giới thiệu bài bổ sung kế tiếp (p13 kết thúc nói "bài bổ sung đến đây là hết"). **Đừng cảm ơn**.

## Các bài
| Số bài | Thương hiệu · ngành | Dự án | Nhạc nền bài này (`--track`) |
|---|---|---|---|
| p09 | HeyTea · trà sữa | brand-promos/heytea | mixkit-644-upbeat-jazz.mp3 |
| p10 | MUJI · bách hóa | brand-promos/muji | mixkit-813-magical-moment.mp3 |
| p11 | Hema · bán lẻ | brand-promos/retail | mixkit-158-happy-times.mp3 |
| p12 | BYD · sản xuất | brand-promos/byd | mixkit-677-epical-drums-02.mp3 |
| p13 | JD.com · thương mại điện tử | brand-promos/jd | mixkit-1147-midnight-funk.mp3 |

Nhạc nền vào từ lúc phát xong thành phẩm, tên khóa học đập xuống (`music.at` = trước tên khóa học một chút, `--hit-at` căn vào tên khóa học), trong lúc thành phẩm mở đầu phát âm thanh gốc thì nhạc nền không vang; đoạn có lời dẫn hạ thấp theo BRIEF. BPM ghi trong thư viện nhạc không nhất thiết chính xác, lấy theo cái `pick_music.py` in ra, khi cần thì tự đo thực tế theo trống bass. Bài nhạc ngắn hơn cả bài học thì dùng `cine/tools/loopbed.py` để nối dài (cách dùng xem đầu file).

## Quy tắc (nhấn mạnh thêm ngoài BRIEF.md)
- Đây là **phim khái niệm không chính thức**: lời dẫn và hình ảnh đều phải nói rõ, không nói "khách hàng", "bàn giao"; tư liệu thương hiệu chỉ lấy từ website chính thức, con số trên màn hình theo đúng nguồn trong DECISIONS từng mục một.
- Giảng việc "nó" đã làm phải có căn cứ: chỉ giảng những gì nhìn thấy được trong DECISIONS.md, mã và khung mẫu. Suy đoán thì nói "có thể".
- Cần ảnh minh họa (hình minh họa, sticker) thì dùng Codex tạo ảnh (lệnh xem BRIEF.md), không dùng emoji.
- Bàn giao và những việc không được làm giống BRIEF.md: không render, không xuất bản, không sửa engine và công cụ, không sửa bất kỳ file nào trong brand-promos. Làm xong thì trả lời tôi theo mục 7 của BRIEF.
