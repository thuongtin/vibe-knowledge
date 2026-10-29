# 14 · Danh sách bẫy khi sản xuất (theo khâu)

Mỗi mục đều là bẫy đã thực sự dẫm phải: hiện tượng → nguyên nhân → cách làm. Các bẫy liên quan đến phong cách (MJ vẽ "men lam" thành cái bát, từ chỉ niên đại làm lệch trang phục, ESRGAN chia khối bị lệch, canvas chờ giải mã, chiếu Vision) xem ở 12-style-families.md.

## Tạo ảnh (Renoise)

- **AI vẽ sai cấu trúc đồ vật** (hình băng giám 04b thừa cửa sổ kính): cổ vật, dụng cụ, máy móc, những thứ mà "cấu trúc chính là điểm kiến thức" thì ảnh AI dễ vẽ sai. Cách làm: cảnh này đổi sang dùng `cutaway` của know.js để vẽ mặt cắt nét bằng code, trên hình ghi "Minh họa bằng code", chú thích cuối ghi xuất xứ cổ vật. Ảnh AI chỉ dùng để dựng bối cảnh và không khí.
- **Wan 3.0 báo `InvalidParameter: Failed to download <url>`**: liên kết của ảnh khung đầu tạm thời không tải được. Cách làm: đổi idempotency key mới rồi gửi lại nguyên xi, thường là qua; lần thất bại đó có hoàn điểm hay không thì dùng get_account so sánh trước sau để xác nhận.
- **Phim Wan xuất ra tự có viền đen trên dưới** (trong 1282×718 mỗi bên trên dưới khoảng 40px): `clip2frames.py` sẽ tự cắt bỏ, trong info.json có ghi crop; `vclip` phủ đầy theo kiểu cover, không cần xử lý thêm.

## Lồng tiếng (MiMo)

- **Từ lặp lại trong cùng một nhịp sẽ làm căn chỉnh từng chữ bị đứt** (04b: "nhị chi nhật / tam chi nhật" mỗi cái xuất hiện hai lần, `check_timings.py` báo lỗi). Cách làm: viết lại thành cách nói không lặp ("đổi sang cách nói ngày nay: tháng Chạp đục băng, tháng Giêng cất vào hầm"), đừng cố chỉnh căn chỉnh.
- **Sau khi lexicon đổi một từ thành chữ đồng âm, căn chỉnh cũng có thể đứt** ("lăng âm" sau khi thay thì không khớp). Cách làm: trước hết lồng tiếng một lần không có lexicon, đọc lại thấy thực sự đọc sai rồi mới thêm.
- **Một nhịp chậm** (<5 chữ/giây) hoặc đọc lại <95%: xóa `build/audio/<nhịp>.*` rồi lồng lại riêng, thường một hai lần là bình thường.

## Dàn cảnh (film.js)

- **`css(node, { background: "" })` sẽ xóa sạch màu nền**, khối chỉ còn viền. Style có điều kiện luôn viết thành "cả hai nhánh đều cho giá trị đầy đủ": `background: melted ? "transparent" : FILL`.
- **Nền đen thuần diện rộng**: phần nền trống còn lại giữa chương (mấy giây của con dấu, bộ đếm) phải lót một lớp ảnh cảnh làm tối (brightness 0.3 + blur), nếu không nhìn vào sẽ tưởng bị sót cảnh.
- **Phụ đề cỡ chữ nhỏ**: `sub` của keyword chỉ bằng 0,28 lần cỡ chữ chính, ở 1080p khoảng 20px, không đọc rõ. Câu phụ cần đọc thì đặt thêm một keyword riêng (≥44px).
- **Chữ vẽ trên sương lạnh, ánh sáng chói** sẽ bị nuốt mất: thêm `text-shadow: 0 2px 18px rgba(0,0,0,0.9)`, hoặc đổi sang màu tương phản cao như vàng kim.

## Render

- **cine/queue.txt được nhiều phiên dùng chung**. Ghi đè bằng `>`, hoặc khởi động thêm một cái khi queue.sh đang chạy, đều làm hai tiến trình record.py cùng ghi vào một picture.mp4, kết quả là đóng băng lâu, hoặc dữ liệu H.264 bị hỏng thẳng (bản đầu của 04b bị đóng băng 80 giây). Cách làm: chỉ dùng `>>` để nối thêm; trước hết `pgrep -f cine/tools/queue.sh`, nếu có hàng đợi đang chạy thì giao cho nó; cũng có thể bỏ qua hàng đợi, chạy trực tiếp tuần tự record.py → finish.py → deliver.sh.
- **Chỉ đổi nhạc nền không cần quay lại hình**: sau khi sửa music trong film.js, chỉ chạy finish.py + deliver.sh (khoảng 1 phút). picture.mp4 không động.
- **Trước khi giao nhất định chạy qa.py**: hiện sẽ báo hình tĩnh >3 giây; đóng băng >10 giây về cơ bản là quá trình ghi hình có sự cố.

## Nhạc nền

- **BGM là bắt buộc**: hook bgm_force của finish.py sẽ tự bổ sung vibe-bgm, vô hiệu các bản nhạc nguyên đoạn khác, hiệu chỉnh âm lượng theo giọng người (khi nói thấp hơn giọng người 10 dB). Chỉ khi người dùng yêu cầu đổi bài mới đổi: mục nhạc ghi `bgm: true, user_request: "nguyên văn người dùng"`. Series mới do new_film.py gắn hook; series cũ chạy thủ công `python3 tools/bgm_force.py --patch <thư mục series>`.
- **Giá trị tuyệt đối của gain_curve viết tay không có giá trị**: 04b trước đây viết −11 dB, đo thực tế khi nói BGM chỉ thấp hơn giọng người 7,7 dB, hơi to; giờ luôn do hiệu chỉnh quyết định (10-28 chốt 14 dB trước, người dùng chê nhẹ, đổi thành 10 dB), đường cong chỉ lo phần lên xuống.
- **Thành phẩm có BGM hay không, qa.py sẽ đối chiếu**: lấy đoạn đầu thành phẩm tương quan với đoạn đầu bản nhạc gốc, ≥0,12 mới tính là có (thành phẩm có BGM đo thực tế 0,18–0,38, không có thì ≤0,08).
- **Sau khi BGM to lên, cover_first mã hóa lại AAC đỉnh có thể vọt tới −0,9 dB**: limiter đã thu về 0,79 (khoảng −2 dBFS), sau mã hóa true peak −1,2 đến −1,4 dB.

## Bàn giao

- **Ghép ảnh bìa thành khung hình đầu** (cover_first.py) sẽ mã hóa lại AAC, đỉnh bị nâng lên 0,5–1 dB; công cụ đã thêm limiter (khoảng −1,4 dBFS). Trước khi giao dùng ebur128 xem lại true peak có ≤ −1 dBTP không.
- **Chỉ đổi âm thanh cũng phải ghép lại ảnh bìa**: deliver.sh sẽ xuất bản không có ảnh bìa, trước khi ghi đè thư mục bàn giao nhớ chạy lại cover_first.py một lần.
