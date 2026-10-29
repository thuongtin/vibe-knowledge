# 11 · Hấp tinh đại pháp: các cách làm hấp thụ từ dự án mã nguồn mở tương tự (2026-10-27)

Đã khảo sát 14 kho GitHub (3 sub-agent chỉ đọc và phân tích). **Giấy phép quyết định hấp thụ được bao nhiêu**:
- MIT (có thể tham khảo cách triển khai, ghi rõ nguồn): huashu-art-motion (trừ hình tượng Hoa Thúc / Clawd), bang-motion, khan-explainer, paper2video, anatomy-explainer, Paper-Cut, SketchNarrator, LuZhong-Li/vibe-knowledge-video-skill, earshot, lemo-opuscar.
- **Chỉ mượn ý tưởng, không chép mã và nguyên văn**: anything2explainer, video-talkcraft (PolyForm phi thương mại, đơn quảng cáo Douyin không được dùng mã của nó); opus-5-5-86-styles-in-motion (bản quyền tư liệu của Futurepedia); opus-video-style-library, worlds3/vibe-knowledge (không khai báo giấy phép).

**Sự thật quan trọng nhất**: LuZhong-Li đã đo thực tế 7 bộ Vibe Knowledge thật sự **7/7 đều không có lời dẫn**. Chúng ta đi theo hướng "có lời dẫn, nhịp nhanh kiểu blogger công nghệ, câu nào cũng có nguồn", đó là điểm khác biệt chứ không phải khuyết điểm.

## Một, khớp lời dẫn và hình ảnh (quy tắc cứng ghi vào film.js mỗi kỳ)

1. **Chưa đọc tới thì không lộ diện**: trước khi từ khóa neo được nói ra, phần tử hoàn toàn không nhìn thấy, không làm mờ để báo trước; nét bút, gạch chân chỉ được xuất hiện cùng lúc hoặc muộn hơn lời nói (kiểu bảng trắng muộn khoảng 0,5 giây). [talkcraft / khan / huashu: ngữ pháp bảng trắng]
2. **Căn khung hình xuất hiện**: phần tử xuất hiện rơi vào khoảng từ −0,2 đến +0,1 giây quanh điểm bắt đầu của từ neo; thời gian luôn lấy bằng `T("Bxx@từ")`, không gõ tay. [a2e / p2v]
3. **Công thức đếm số**: điểm bắt đầu của số cuộn = thời điểm nói ra con số − thời lượng cuộn, để con số vừa đúng lúc được đọc thì chốt lại; **dữ liệu thật có nguồn thì không cuộn qua giá trị trung gian** (khung hình giữa chừng sẽ xuất hiện con số mà nguyên văn không có), chỉ cuộn số "minh họa" hoặc tiến từng số nguyên. [huashu / p2v]
4. **Góc máy là dấu câu**: đẩy chậm, lia ngang, kéo xa dùng để chuyển cảnh; đẩy nhanh, đập vào chỉ dành cho lúc tiết lộ và con số then chốt; đẩy vào thì phải kéo ra, không đẩy vào liên tục ba góc máy. [huashu]
5. **Ngân sách nhấn mạnh**: từ khóa đập vào trong cả phim ≤4 lần, chũm chọe ngược ≤1 lần, xung kích toàn khung ≤3 lần. [talkcraft / earshot]
6. **Ngân sách tĩnh**: đứng yên lâu nhất ≤3 giây, nhịp cuối của mỗi góc máy sau khi vào vị trí thì giữ vững 0,5–0,75 giây rồi mới rời; không thêm trôi nổi chỉ để cho đủ chuyển động. [a2e]
7. **Phụ đề thô**: cả câu hiện ra, cả câu đi mất, không thêm hiệu ứng, không kèm dấu câu, mỗi khối ≤16 chữ; chữ trong hình chỉ đặt phần chắt lọc (từ khóa ≤8 chữ), không lặp lại phụ đề. [a2e / talkcraft]
8. **Người, vật, sách được lời dẫn nhắc tới thì bắt buộc phải có hình** (chân dung dùng bóng đen / bóng sách / bản đồ thay thế). [bang / p2v]
9. **Chừa đáy**: bản dọc, chữ ở y ≥ 0,8H có tổng chiều rộng ≤ 0,35W, nhường chỗ cho nút của nền tảng. [LuZhong-Li]

## Hai, 9 loại ngữ pháp giảng giải (huashu, MIT): chọn ngữ pháp theo đoạn, cả phim tối đa 2 loại

| Ngữ pháp | Cách giảng | Mẫu gốc / phong cách tương ứng của chúng ta |
|---|---|---|
| Kurzgesagt xuyên qua các thang đo | Khái niệm được vẽ thành một vật, kéo gần kéo xa theo logarit để xuyên qua các thang đo, chui vào vật thể thì hiện ra thế giới kế tiếp; mỗi câu lời dẫn ít nhất một lần đổi hình, cắt cứng sớm hơn đầu câu 0–0,2 giây | A phim khái niệm đoán đố · điểm sáng bầu trời sao |
| Vox tư liệu trên mặt bàn | Tư liệu thật trải trên bàn, bút dạ quang quét theo từ, đường đỏ đuổi theo thẻ kế tiếp, cắt cứng thẻ theo ngắt câu | Điều tra bằng hình ảnh · D phim một mạch chính |
| Bảng trắng | Nói một câu viết một câu (muộn 0,5 giây), mỗi luận điểm dịch sang một khối mới, kết thúc kéo xa nhìn toàn cảnh | C phim nguyên lý nỗi đau · phong cách mới "bảng đen phấn" |
| Storytime | Sau câu vô lý thì chừa 0,8–1,5 giây để phản ứng, sau tiếng cười thì đứng yên ≥0,9 giây | Phần tiết lộ của B phim lựa chọn tiến thoái lưỡng nan |
| Chữ động | Từ chính đập vào ở trọng âm, một tiết một màn hình, rút lui nhanh hơn xuất hiện | Bản tin phụ đề · E / F |
| Biến hình kiểu 3b1b | Nền đen chỉ đặt thứ đang được giảng, đối tượng trước biến hình thẳng thành đối tượng sau, gần như không cắt; viết ra vấn đề trước; màu sắc = khái niệm | A / C · phong cách mới "dữ liệu tối kiểu 3B1B" |
| Buổi ra mắt | Một màn hình một việc, ảnh chụp tràn khung, giảng đến đâu đẩy tới đó, con số chốt lại khi được nói ra | Đoạn ảnh chụp có nguồn |
| Biểu đồ tài chính | Dựng trục tọa độ trước, rồi mới mọc dữ liệu, chỉ đánh dấu một việc, đầu đường kẻ đi qua điểm sự kiện thì bật chú thích | Đoạn so sánh con số của B |
| Người giảng giải | Nhân vật hoạt hình giảng giải luân phiên giữa đứng bên cạnh giảng / con số đầy màn hình / so sánh trái phải / bước vào trong hình | F phim sáu mặt xoay vòng (cần tài nguyên nhân vật) |

## Ba, cấu trúc và xuất bản (LuZhong-Li, worlds3)

- **Khâu đặt tên**: khi khái niệm xuất hiện thì đặt tên + một dòng phụ đề tiếng Anh ("Hình dạng của vận may / FORMA FORTUNAE").
- **Bộ ba cuối phim**: thẻ tiêu đề quay lại → một câu hỏi tương tác → "manh mối tài liệu" trên màn hình (liệt kê thẳng 2–3 nguồn chính từ facts.md).
- **Nhãn góc minh họa**: "Minh họa: mô hình giúp bạn hiểu, không phải kết quả thí nghiệm".
- Trong 0,3 giây đầu mở phim chủ thể phải nhìn thấy được; điểm nhạc nền đột biến năng lượng đặt vào lúc tiết lộ, đoạn yên tĩnh đặt vào lúc suy ngẫm.
- Xuất bản: phần chính chỉ đặt một câu kết luận; phổ biến kiến thức chi tiết tách thành 2–3 mục đặt ở phần bình luận; cài sẵn câu hỏi ghim đầu; thẻ 4–5 cái; **ảnh bìa tải lên riêng, không nhúng vào đầu phim**, xuất ảnh thu nhỏ 540px để kiểm tra khả năng đọc.
- Công thức chọn đề tài: lát cắt đời sống + mô hình cứng cáp + người đoạt Nobel / người nổi tiếng bảo chứng + con số phản trực giác (ứng viên: cách ly của Schelling, nghịch lý Braess, nghịch lý sinh nhật…).

## Bốn, quy trình và kiểm tra chất lượng

1. **Làm mẫu trước**: làm 30 giây đầu hoặc một góc máy mẫu, để người dùng xác nhận phong cách, cỡ chữ, tốc độ nói rồi mới triển khai. [a2e / talkcraft]
2. **Duyệt phim độc lập có biên nhận**: giao việc duyệt phim cho sub-agent không tham gia sản xuất, từng góc máy thêm một dòng vào `review.md`, ghi "đã xem N/N góc máy" mới tính là duyệt xong; lỗi chia P0 / P1 / P2. Cử thêm một agent chỉ kiểm tra sự kiện, xuất MUST FIX / SHOULD FIX. [talkcraft / p2v]
3. **Đánh giá bên ngoài chỉ coi là giả thuyết**: ý kiến của mô hình thị giác hoặc agent duyệt phim phải dùng dụng cụ (OCR, đo đạc, trích khung) kiểm chứng rồi mới sửa. [LuZhong-Li: 9 ý kiến chỉ có 3 được xác nhận]
4. **Phân cảnh ghi "danh sách chưa hoàn thành"**: tránh việc gói phần chưa làm xong thành quyết định thiết kế. [a2e]
5. **Sổ cái nguồn**: cảnh | cách nói | nguồn (file + số dòng) | thiết lập, góc máy dữ liệu kèm dòng nguồn, sơ đồ minh họa ghi "minh họa". [p2v]. facts.md của chúng ta vốn đã có cấu trúc này.

## Năm, ứng viên phong cách mới (thư viện phong cách cần mở rộng, xếp theo mức đề xuất)

> 2026-10-27 đã làm thành phong cách: bảng đen phấn, toán học tối (trước là "dữ liệu tối 3B1B"), ghép mảnh bán sắc (trước là "Vox giấy ghép bán sắc"), bản vẽ xanh bằng sáng chế, mặt cắt đẳng cự, thanh hoa, mộc bản, bích họa Đôn Hoàng. Phần còn lại vẫn là ứng viên, xem 12-style-families.md.

| Phong cách | Trông như thế nào | Triển khai | Phù hợp | Nguồn / giấy phép |
|---|---|---|---|---|
| Bảng đen phấn | Bảng xanh đen #173E38, hạt phấn, vừa giảng vừa viết, chữ viết trên bảng tích lũy | SVG nét viền thuần mã + kết cấu bụi phấn; mỗi khái niệm một màu, cứ 5–6 nhịp thì xóa bảng một lần | Công thức, suy luận, vật lý | khan (MIT), SketchNarrator (MIT) |
| Dữ liệu tối 3B1B | Nền gần đen, 2–3 màu ngữ nghĩa, tiêu đề có chân, dữ liệu thật trải đầy | Mã thuần; biến hình tiếp sức; mỗi nhịp một thứ mới | Thống kê, AI, bài báo | paper2video (MIT) |
| Vox giấy ghép bán sắc | Giấy rách mép, băng dính, chấm bán sắc, nền màu phẳng | **Mức tăng cường**: tạo ảnh chốt bản → tách ảnh gốc thành 2–4 lớp → mã slap / slide / peel / drift | Xã hội, kinh tế, cơ chế lịch sử | Paper-Cut (MIT); cách làm xem bên dưới |
| Bản vẽ kỹ thuật / bằng sáng chế | Giấy trắng nét xanh Phổ, đường kích thước, đánh số FIG., khoanh chú thích bằng bút chì đỏ | Mã thuần, đường chiếu → đường vật thể → kích thước | Phát minh, máy móc cổ đại | Ý tưởng: thư viện 86 phong cách, talkcraft |
| Mặt cắt cơ khí đẳng cự | Thiết bị tinh xảo trên giấy xám nhạt, các chi tiết thật sự chuyển động, bốn góc có số đọc | Mã thuần, chỉ làm nổi bật bộ phận đang được giảng | Nguyên lý, cơ chế | anatomy-explainer (MIT) |
| Tranh minh họa tự nhiên khắc đồng | Nét khắc đồng + tô màu nhạt thủ công | Nét đan khắc từng nét, màu nhạt thấm vào chậm một nhịp | Động thực vật, bác vật học | Ý tưởng: thư viện phong cách 86 / 77 |
| Tranh Ukiyo-e cuộn / cuộn dài Trung Hoa | Cuộn dài nằm ngang, mở ra từ phải sang trái, các bản in màu lần lượt ép lên | Mã thuần hoặc tạo ảnh tách lớp | Một dòng thời gian, lịch sử Đông Á | Ý tưởng: thư viện phong cách 86 / 77 |
| Đèn đài hồ sơ | Bản gốc trải trên đèn đài ánh sáng lạnh, dùng kính lúp xem chi tiết | Biến thể của điều tra bằng hình ảnh | Khảo chứng sử liệu | Ý tưởng: thư viện phong cách 77 |
| Sơ đồ tàu điện | Tuyến đường chỉ đi 0° / 45° / 90°, các ga lần lượt sáng lên | Mã thuần | Lộ trình tiến hóa, các giai đoạn | Ý tưởng: thư viện phong cách 86 |
| Thống kê tượng hình ISOTYPE | Một biểu tượng đại diện cho số lượng cố định, đóng dấu từng hàng một | Mã thuần | Dân số, so sánh số lượng | Ý tưởng: thư viện phong cách 86 |
| Thanh hoa nhà Minh / mộc bản thời Dân Quốc | Nét cọ men xanh coban dưới men / nét khắc dao đen trắng | Mức tăng cường: tạo ảnh + mã dịch chuyển máy | Đồ vật, lịch sử cận đại | Ý tưởng: vox-ai-motion |
| Bích họa Đôn Hoàng | Nền đỏ đất, màu khoáng vật, dải lụa bay, bong tróc | Mức tăng cường: tạo ảnh + mặt nạ bong tróc bằng mã | Con đường tơ lụa, lịch sử Phật giáo | Ý tưởng: huashu (MIT) |

### Cách làm mức tăng cường của Vox giấy ghép (Paper-Cut, MIT)
① Mỗi góc máy trước hết viết xong bố cục hoàn chỉnh (vị trí chủ thể, khoảng trống, vùng an toàn của chữ, chất liệu giấy, kỹ thuật in), **tạo nguyên bức**, trước tiên xuất 1 khung đại diện cho người dùng duyệt; ② chỉ tách 2–4 kênh chuyển động (chủ thể > cơ chế > trang trí), cắt từ **ảnh gốc**, chỉ vá lỗ lộ ra sau khi cắt đi; không tạo lại chủ thể trên phông xanh; ③ từ chỉ động tác: slap (1.12–1.20→1 kèm xoay rồi chỉnh lại), slide, drop, peel (clip-path mở ra), stamp, drift 6–18px; chuyển động máy 3–6% đặt ở lớp ngoài; chuyển cảnh page-push; ④ phụ đề, con số, nhãn đều do mã chồng lên; ⑤ hiệu ứng âm thanh dùng tiếng giấy trượt, vỗ, ép (earshot: `swipe/paper`, `knock/wood`, `pro_tap/soft`).
