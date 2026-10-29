# 12 · Họ phong cách và lộ trình mở rộng (2026-10-27)

## 1. Vì sao khi chỉ có 7 bộ thì trông mỏng

1. **Độ sáng đơn điệu**: độ sáng trung bình (0–255) của 7 ảnh phong cách: Sao trời 12, Vàng sẫm 17, Tin tức phụ đề 47, Cổ phong 61, Pixel 61, Điều tra trực quan 135, Thuỷ mặc 180. 5 bộ nền tối, không có bộ nào sáng và bão hoà cao.
2. **Đổi lớp áo không đổi cách kể**: khác biệt chủ yếu ở bảng màu và chất liệu, ngôn ngữ ống kính đều là "đặt phần tử lên → mờ dần vào → zoom gần". Người xem phân biệt được phong cách là nhờ cách kể (tiếp sức biến hình, xuyên thang đo, vừa kể vừa viết, chụp những mảnh giấy), không nhờ bảng màu.
3. **Cả một họ bị bỏ trống**: họ Sáng và đại chúng, In ấn và giấy, trường phái Minh hoạ và thiết kế đều chưa có bộ nào.

Vì vậy việc mở rộng bổ sung theo "họ", mỗi bộ phong cách mới đồng thời quy định **diện mạo + cách kể** (hai dòng "Chuyển động" và "Cảnh chiêu bài" của STYLE.md).

## 2. Hai trục: phong cách × thủ pháp

- **Phong cách (diện mạo + cách kể, 44 bộ, 8 họ, mỗi họ ít nhất 3 bộ)**: thư mục `styles/` này, trường `fam` của `catalog.json`.
- **Thủ pháp (cách tổ chức ống kính có thể chồng lên bất kỳ phong cách nào)**: xem mục 5. Một kỳ phim chọn 1 phong cách + tối đa 2 thủ pháp.

| Họ | Phong cách | Bậc |
|---|---|---|
| Phương Đông | Cổ phong, Thuỷ mặc giấy nền, Tối giản chừa trắng, Bích hoạ Đôn Hoàng, Men xanh trắng, Khắc gỗ, Trường quyển | Ba bộ đầu cơ bản, bốn bộ sau nâng cao |
| Nền tối khái niệm | Điểm sáng sao trời, Nét vàng sẫm, Toán học nền tối, Neon cyber, Tối giản phát hành, Cực quang, Nét vàng Art Deco | Cơ bản |
| Sáng và đại chúng | Chữ hoa tạp kỹ, Memphis pop, Sổ tay vẽ nguệch ngoạc, Vaporwave, Đất sét kawaii | Cơ bản |
| In ấn và giấy | In lụa stencil, Ghép chữ báo cắt, Tạp chí biên tập, Poster công viên quốc gia, Cắt dán bán sắc | Cắt dán nâng cao, còn lại cơ bản |
| Minh hoạ và thiết kế | Bảng phấn, Quá trình vẽ tay, Bản vẽ blueprint bằng sáng chế, Mặt cắt đẳng cự, Chữ động lưới Thuỵ Sĩ, Sơ đồ tuyến tàu điện ngầm, Thống kê hình tượng, Đồng bản bảo tàng | Đồng bản nâng cao, còn lại cơ bản |
| Dựng phim và phóng sự | Tin tức phụ đề, Điều tra trực quan, Desktop cổ điển, Đèn hải đăng lưu trữ, Bao bì bản tin truyền hình | Cơ bản |
| Điện ảnh | Mở đầu bóng đen (kiểu Saul Bass), Thẻ chữ phim câm, Dựng phim kiến tạo chủ nghĩa | Cơ bản |
| Game | Pixel, Hộp thoại RPG, Đấu bài, Pixel đồng quê (kiểu Stardew Valley, hình ảnh nguyên bản) | Cơ bản |

Mẫu: `styles` (5 hệ thống hình ảnh), `styles2` (2 bộ Dựng phim và phóng sự), `styles3` (8 bộ bù họ trống), `styles4` (4 bộ bậc nâng cao), `styles5` (đợt 5, 8 bộ), `styles6` (đợt 6, 8 bộ), `styles7` (2 bộ bậc nâng cao Trường quyển / Đồng bản), `styles8` (Pixel đồng quê), `styles9` (5 bộ chốt danh sách ứng viên), `styles10` (Quá trình vẽ tay), tất cả dùng cùng một đoạn mở đầu B01 để render. Tuyển tập mẫu mới dùng `tools/style_reel.py <tên> <số đoạn>` để tạo trục thời gian và lời dẫn.

## 3. "Bộ sưu tập 87 phong cách thẻ web / UI" dùng thế nào

Đó là phong cách thẻ web, chuyển thẳng thành 87 phong cách video sẽ bị trùng lặp rất nhiều, và khi đề xuất cũng không chọn ra được. Cách xử lý:

| Xử lý | Phong cách (số là thứ tự trong danh sách gốc) |
|---|---|
| **Đã làm thành phong cách cả phim** | Cắt dán 19 / In stencil 33 → Cắt dán bán sắc, In stencil; Memphis 9 / Pop 70 / Memphis doanh nghiệp 87 → Memphis pop; Thuỵ Sĩ 6 / Bauhaus 24 / De Stijl Hà Lan 35 / Spiekermann 58 → Chữ động lưới Thuỵ Sĩ; Blueprint 38 / Minh hoạ kỹ thuật 62 → Bản vẽ blueprint bằng sáng chế; Đẳng cự 26 → Mặt cắt đẳng cự; Typography động 17 → cách kể của Chữ động lưới Thuỵ Sĩ; Pixel 18 → Pixel; Bản khắc 32 → Khắc gỗ; Thư pháp mực 42 → Thuỷ mặc giấy nền |
| **Đã làm ở đợt 5** | Cyberpunk 10 / Tân Tokyo 44 / Glitch 36 → Neon cyber; Wabi-sabi 39 / Hara Kenya 45 / Fukasawa Naoto 47 → Tối giản chừa trắng; Saul Bass 68 → Mở đầu bóng đen; Mac đời đầu 79 → Desktop cổ điển; Zine 82 → Ghép chữ báo cắt; Vẽ tay 11 / Vẽ nguệch ngoạc 14 → Sổ tay vẽ nguệch ngoạc; Escher 50 → Thống kê hình tượng, Sơ đồ tuyến tàu điện ngầm |
| **Đã làm ở đợt 6** | Cực quang 8 / Hologram 25 → Cực quang; Vaporwave 29 / Y2K 31 → Vaporwave; Hollywood thời hoàng kim 86 → Thẻ chữ phim câm; Kiến tạo chủ nghĩa → Dựng phim kiến tạo chủ nghĩa; promo-video keynote / editorial → Tối giản phát hành, Tạp chí biên tập; bổ sung họ Game: Hộp thoại RPG, Đấu bài |
| **Đã làm ở đợt 7 (bậc nâng cao)** | Ukiyo-e / Trường quyển Trung Hoa → Trường quyển; Đồ bản đồng bản bảo tàng → Đồng bản bảo tàng |
| **Đã làm ở đợt 9 (chốt danh sách ứng viên)** | Đất sét 13 / Kawaii 43 → Đất sét kawaii; Art Deco 22 / 71 → Nét vàng Art Deco; Poster công viên quốc gia 83 → Poster công viên quốc gia; Đèn hải đăng lưu trữ; Bao bì bản tin truyền hình (tên đài hư cấu) |
| **Chỉ dùng làm tham số "chất liệu thẻ", chồng lên bất kỳ phong cách nào** | Material Design 1, Phẳng 2, Neumorphism 3, Glassmorphism 4, Brutalism 5, Skeuomorphism 7, Đơn sắc 15, Bento 16, Nghệ thuật giấy 28, Phù sinh thiên niên kỷ 37, UI Thung lũng Silicon 75 |
| **Chỉ làm tham chiếu màu sắc / phông chữ** | Các trường phái Đức, Mỹ mà người xem khu vực tri thức tiếng Trung không quen: Werkbund 54, Berlin Techno 56, Jugendstil 57, Làn sóng mới Đức 59, Moriyer 60, Chữ Gothic 61, Thiết kế sinh thái 63, Kraftwerk 64, Dada 65, Chủ nghĩa lãng mạn 66, Lanbao 67, Eames 69, California hiện đại 72, Googie 73, Kitsch 74, Biểu hiện trừu tượng 76, Shaker 77, Ảo giác 78, Wright 80, Tiki 81, Cranbrook 84, Ván trượt 85, Hollywood 86, v.v. |
| **Không làm** | Phản thiết kế 34 (làm thành phim chỉ là xấu), Chủ nghĩa cực nhiều 20 (xung đột với "chữ trên hình ≤8 chữ") |

## 4. Mượn gì từ promo-video

| Thứ trong promo-video | Ở đây biến thành |
|---|---|
| Tông hình ảnh: Chữ hoa tạp kỹ (vlog Thuận Đức được đánh giá tốt), chữ động lưới Thuỵ Sĩ, cắt giấy | Chữ hoa tạp kỹ, Chữ động lưới Thuỵ Sĩ; cắt giấy gộp vào cách làm của Cắt dán bán sắc |
| Tông hình ảnh: keynote phát hành, aurora cực quang, editorial tạp chí, bento sáng | Đợt ứng viên tiếp theo (Tối giản phát hành, Cực quang); bento làm chất liệu thẻ |
| Biến hình liên tục của một hình (one-shape.md) | "Một đối tượng biến thành đối tượng tiếp theo" của Toán học nền tối |
| Gói mở rộng phong cách 01: xuyên thấu vô hạn / hé lộ phối cảnh / kể bằng dữ liệu / hoà tan chất lỏng | Trục thủ pháp (xem dưới) |
| Gói mở rộng phong cách 02: tiếp sức một ống kính | Trục thủ pháp |
| Icon động (lucide-animated), emoji động Noto | Trục thủ pháp (Chữ hoa tạp kỹ, Memphis có thể dùng trực tiếp) |

## 5. Trục thủ pháp (chồng lên bất kỳ phong cách nào, một kỳ tối đa 2 loại)

| Thủ pháp | Khi nào dùng | Xuất xứ |
|---|---|---|
| Xuyên thang đo (kiểu Kurzgesagt) | Từ một vật chui vào thế giới tiếp theo; bậc độ lớn, vũ trụ, tế bào | promo-video style-pack-01 InfiniteZoom; ngữ pháp 1 của 11-absorbed |
| Tiếp sức biến hình | Đối tượng trước trực tiếp biến thành đối tượng sau, gần như không cắt | one-shape.md; Toán học nền tối |
| Một ống kính tiếp sức | Một mạch xuyên suốt: đầu vào → sản phẩm → tiếp tục vận hành | style-pack-02 |
| Hé lộ phối cảnh | Cấu trúc bên trong máy móc / kiến trúc / cơ thể | style-pack-01 XRayReveal |
| Kể bằng dữ liệu | Dựng trục toạ độ trước rồi mới mọc dữ liệu, chỉ đánh dấu một việc | style-pack-01 DataStory; biểu đồ tài chính của 11-absorbed |
| Vật liệu trên bàn (kiểu Vox) | Sử liệu, bài báo, ảnh chụp màn hình bày trên bàn, bút dạ quang quét qua | Điều tra trực quan, Cắt dán bán sắc |
| Vừa kể vừa viết | Nói một câu viết một câu, bảng viết cộng dồn | Bảng phấn |
| Vẽ cho bạn xem (tay + bút) | Hiển thị quá trình vẽ: bản phác bút chì → nét mực → tô màu, tay đi theo đầu bút; có thể chồng lên mọi phong cách nét vẽ | Quá trình vẽ tay (addPath / addText / addFill + hand của styles10_film.js) |
| Icon động / emoji động | Các nút quy trình sáng lên lần lượt | promo-video animated-icons |

## 6. Những bẫy lần này (làm phong cách bậc nâng cao thì xem trước)

0. **Từ khoá đề xuất đừng viết một chữ đơn**: "聪明" sẽ trúng chữ "明" của Cổ phong (triều Minh). Trong catalog luôn viết từ hai chữ trở lên (triều Minh, đời Đường, thi từ…), recommend.py cũng đã bỏ qua từ đơn chữ.

1. **MJ vẽ "tranh trên đồ sứ nào đó" thành ảnh sản phẩm khí vật**: prompt viết porcelain painting thì ra ảnh sản phẩm của bát và đĩa. Phải viết `flat full-frame painting in ... style` và thêm `no bowl, no plate, no vase, no ceramic object`.
2. **Từ phong cách niên đại sẽ làm lệch thời đại nhân vật**: viết "1930s woodcut" thì nhân vật đội mũ cận đại. Thời đại nhân vật phải viết riêng cho rõ (`ancient Warring States China, long hemp robes, hair tied in topknots`), rồi thêm `no modern clothing, no caps`.
3. **Real-ESRGAN dùng mô hình x4plus kèm `-s 2` sẽ chia khối lệch** (ảnh như bị cắt thành ô vuông rồi ghép loạn). Chỉ cần phóng 1.3 lần thì dùng thẳng Lanczos kèm làm nét nhẹ; muốn phóng to thì dùng `-s 4` rồi thu nhỏ.
4. **Canvas vẽ ảnh phải chờ ảnh giải mã xong**: khi dùng canvas vẽ ảnh tạo sinh, khung đầu tiên có thể vẽ trước khi giải mã xong (xuất hiện lỗ đen). `redraw()` của styles4: chưa giải mã xong thì đăng ký vào `__vk.pend` một lần "sau khi giải mã dùng cùng t vẽ lại".
5. **Bóng đổ của Vision không nằm trong mặt nạ**: sau khi chủ thể bị tách đi, bóng đổ trên nền vẫn còn ở ảnh nền. Khi lấp lỗ, kéo mặt nạ theo hướng bóng đổ (dưới phải) lấy hợp rồi nở ra; giấy nền đơn sắc thì dùng màu trung vị cộng nhiễu để lấp, sạch hơn inpaint.
6. **Đầu ra `generateMaskedImage` của Vision bị lệch**: đổi sang dùng `generateScaledMaskForImage` chỉ xuất mặt nạ, rồi dùng PIL ghép (công cụ `tools/vision_layers.swift`).
8. **Khổ siêu rộng dùng Nano Banana 2**: Midjourney rộng nhất 16:9, trường quyển cần 4:1 thì dùng nano-banana-2 (2k, 12 điểm/ảnh, đắt hơn MJ); 4128×1024 co theo chiều cao 1080 thì rộng khoảng 4354, vừa đủ để trượt ngang.
7. **Khoét lỗ ngoài màn hình dùng destination-out, đừng dùng cắt evenodd**: khi nhiều vùng bong tróc chồng lên nhau, evenodd sẽ lấp lại phần chồng.
