# 11 · Khóa thực chiến: phim thật + một phiên làm việc thật + phân tích phim theo ngành

Cách làm của "Khóa thực chiến phim quảng bá Opus 5.5" (dẫn nhập + 8 bài + 5 bài bổ sung, engine cine). Phù hợp với các khóa kiểu "dùng AI làm một loại tác phẩm": nhân vật chính là các tác phẩm đã bàn giao thật, một mạch xuyên suốt là một phiên làm việc thật, rồi bổ sung theo ngành vài phim khái niệm để phân tích cho học viên xem. Bản gốc của các bản hướng dẫn nằm trong `templates/series-cine/examples-briefs/`.

## Chốt trước (điểm xác nhận)
- Đối tượng, số bài, hai lộ trình giảng thế nào (ví dụ skill + Remotion nói rõ giấy phép, hoặc mã web thuần).
- **Tường tác phẩm chỉ dùng bản cuối**: tìm bản được bàn giao sau cùng của từng dự án (đối chiếu ba bên: tên file, thời gian sửa, nhật ký bàn giao), liệt kê thành bảng "phân loại | tác phẩm | file" ghi vào BRIEF; bản cũ chỉ xuất hiện khi kể chuyện chỉnh sửa phiên bản, và đánh dấu "bản cũ".
- Tác phẩm nào được đưa lên: tác phẩm của khách hàng phải được người dùng xác nhận là cho phép trình chiếu; người dùng nêu tên là không muốn thì tuyệt đối không xuất hiện (bao gồm tường phim dẫn nhập, trang khóa học, lời dẫn).
- Phân loại theo ngành: trước hết xếp các tác phẩm có sẵn vào nhóm, ngành còn thiếu thì dùng "phim khái niệm ngành" để bù (bên dưới).
- Ghi phiên làm việc thật mấy lần (thường 1 lần, khoảng 5 lượt), trước khi ghi báo mức tiêu thụ dự kiến.

## Phiên làm việc thật (`session/`, xem README)
- Phiên bản khóa học độc lập (thư mục cấu hình riêng, tắt tự động cập nhật, không mang định tuyến mô hình dùng hằng ngày), đăng nhập do chính người dùng thực hiện; skill cần dùng thì tạo liên kết mềm vào phiên bản đó.
- Dùng sản phẩm hư cấu + website chính thức demo cục bộ, tránh lấy công ty thật để demo; câu đầu tiên cố gắng ngắn ("Dùng X làm cho Y một phim quảng bá 30 giây, website chính thức …").
- Mỗi lượt `turn.sh` → `export.py` xuất turnN.json (prompt, lần gọi công cụ và số giây tương đối, chữ nó viết ra, thời gian dùng, chi phí), toàn bộ quá trình dùng `usage.py`. Trong khóa mỗi bài đặt bước tương ứng: terminal vẽ lại theo bản ghi, đường dẫn viết tên người dùng thành `~`.
- Tham chiếu thực đo: 5 lượt khoảng 16 phút, 48 lần gọi mô hình, 52 lần gọi công cụ, quy đổi theo giá API khoảng 3,4 USD.
- Lỗi: ở chế độ `-p`, render nền bị giết khi phiên kết thúc; `total_cost_usd` là giá trị tích lũy; mức dùng khử trùng theo message id; ghi cache tính theo giá cache 1 giờ (gấp 2 lần giá đầu vào).

## Phim khái niệm ngành (BRIEF-nganh-khai-niem.md)
- Mỗi ngành chọn một thương hiệu đại diện, một trợ lý làm một phim, theo promo-video skill làm từ website chính thức cho đến thành phẩm (28–30 giây).
- Tư liệu thương hiệu chỉ lấy từ website chính thức (Logo, ảnh sản phẩm, phông chữ, nội dung chữ), mỗi con số trên màn hình đều ghi lại câu gốc và trang; Codex chỉ vẽ bầu không khí, **không vẽ sản phẩm, cửa hàng, Logo**, không làm giả bất kỳ vật thể thật nào.
- Cuối phim tuyên bố "Phim khái niệm không chính thức · chỉ dùng để minh họa khóa học · không liên quan đến X chính thức"; lời dẫn và trang khóa học đều nói "phim khái niệm", không nói khách hàng, bàn giao.
- Mỗi phim viết `DECISIONS.md`: nguyên văn thẻ chọn phương án, bảng phân cảnh, nhạc nền và BPM, URL nguồn tư liệu, nguồn sự kiện, danh sách ảnh do AI tạo, các vấn đề đã sửa sau khi duyệt phim (trước → sau). File này chính là nguồn sự kiện cho các bài phân tích phim về sau.
- Trước khi bàn giao, bản master về RMS khoảng −17 dBFS, đỉnh −1 dBFS (promo-video `master_audio.py`).

## Mỗi bài chính khóa (BRIEF-phim-quang-cao-thuc-chien.md)
- Mở đầu 5–8 giây dựng nhanh đoạn phim thật + tên khóa học do mã tạo, khớp điểm nhịp nhạc nền; mỗi bài nói ba việc + một nhịp tạm dừng + sơ đồ ôn lại + giới thiệu bài sau.
- Nhạc nền mỗi bài một bài hát, không lặp lại, `pick_music.py --hit-at` căn đoạn chính vào tên khóa học, bài ngắn thì `loopbed.py` nối dài; trước khi ghi khóa học sao lưu `~/.cache/promo-video/music-usage.json`, làm xong hết thì khôi phục.
- Giảng quy tắc thì trích nguyên văn skill (file + tên tiểu mục), giảng ví dụ thì trích nhật ký bàn giao; prompt cộng đồng mỗi lần ≤15 từ tiếng Anh, kèm tác giả và liên kết.

## Bài bổ sung: phân tích một phim theo ngành (BRIEF-bo-sung-phan-tich-phim.md)
- Mở đầu phát trọn một lượt phim khái niệm (kèm âm thanh gốc, lời dẫn để trống), tên khóa học "Bổ sung · <ngành>: phân tích <thương hiệu>" + nhãn nhỏ "Phim khái niệm không chính thức · chỉ dùng để minh họa khóa học".
- Ba việc: tư liệu website chính thức → hình ảnh trong phim và lý do chọn thẻ; phân cảnh, nhạc nền, góc máy xuất sắc nhất (đoạn phim + trích đoạn mã); duyệt phim đã sửa gì, giữ tuân thủ thế nào.
- Chỉ giảng những gì nhìn thấy được trong DECISIONS.md, mã và khung mẫu; suy đoán thì nói "có thể". Bài cuối nói "bài bổ sung đến đây là hết".

## Trang khóa học
- `stages` của `series.json` chia đoạn (dẫn nhập / chính khóa / bổ sung), `sample` đặt thành phẩm của phiên làm việc thật; `tools/update_series.py --prefix p` điền video, ảnh bìa, thời lượng và trạng thái lên mạng; `scripts/course_page.py` xuất trang; cập nhật tại chỗ cùng một Artifact (cùng một đường dẫn file).
- Chân trang ghi rõ: tác phẩm thật được khách hàng đồng ý cho trình chiếu; phim khái niệm không chính thức; sản phẩm demo là hư cấu.

## Cảm ơn và ghi công
- Lời cảm ơn chỉ đặt ở bài dẫn nhập và bài cuối; các bài ở giữa không cảm ơn.
- Giấy phép phải nói rõ: ví dụ Remotion cá nhân, công ty vì lợi nhuận ≤3 người, phi lợi nhuận thì miễn phí, còn lại cần giấy phép công ty; thư viện nhạc Mixkit không được dùng cho truyền hình, phát thanh, trò chơi, không được phân phối lại riêng phần nhạc.
