# Khoá học làm quen WorkBuddy · Quy chuẩn dàn cảnh (engine vẽ tay + skin Notion + hiệu ứng chuyển động)

Mỗi bài một `lessons/NN/scenes.json`, trình biên dịch là `runtime/sketch.js` (primitives ở `primitives/sketch.js`, `primitives/motion.js`).

## Phần đầu file
```json
{"n": 2, "title": "…", "series": "WorkBuddy 上手课", "engine": "sketch", "skin": "notion", "presenter": "hp", "sticker": true,
 "speed": 1.15, "author": "@Berryxia", "scenes": [ … ]}
```
- `sticker: true` (**mặc định cho bài mới**): phong cách sticker, thẻ stickers biến thành sticker viền trắng (nghiêng ngẫu nhiên 1.5–3°, phóng to rơi xuống nảy lại, bóng đổ thu hẹp, ánh sáng quét qua), minh hoạ được bọc viền trắng cắt khuôn, emoji Noto trong thẻ cũng được viền trắng; nhãn không đủ chỗ thì tự thu nhỏ cỡ chữ. Tắt cho một trang: stickers ghi `"style": "card"`, say ghi `"illusSticker": false`.
- `engine: "sketch"` dùng engine vẽ tay; `skin: "notion"` là phong cách tối giản Notion (`"paper"` là phong cách sổ tay, dự phòng).
- `presenter: "host"`: nhân vật nhỏ thuyết minh ở góc phải dưới (avatar pixel của tác giả, biết chớp mắt, há miệng khi nói). Trang bìa và sơ đồ tổng kết cuối tự động không xuất hiện, từng cảnh có thể ghi `"host": "none"` để tắt.
- Cách ghi thời gian giống mùa hai: `"B03"`, `"B03.cue"`, `"B03@word"`, `"B03.end"`, đều có thể cộng trừ giây.

## Tài nguyên
- **Ba tầng phân công icon**: giao diện, quy trình, danh sách dùng **icon nét IconPark** (ghi `icon-park:robot`, Apache 2.0, vẽ từng nét, phối màu Notion; thiếu thì dùng `lucide:` / `tabler:`); nhân vật chính, cảm xúc, đồ vật dùng **emoji Noto** (ghi `robot`, có hoạt ảnh thì tự phát).
- **Minh hoạ**: thư viện minh hoạ IconPark 88 ảnh (`assets/illustrations/iconpark/`, tổng quan `_sheet.html`, danh sách `catalog.json`). `python3 scripts/illus.py lessons/NN ip-5-48 …` đặt vào thư mục bài học, trong cảnh `say` / `cover` ghi `"illus": "ip-5-48"`: viền nét + mảng màu mờ dần vào; nguồn chỉ ghi ở credits cuối phim (inlineCredits mặc định tắt).
- **Sơ đồ quy trình / cộng tác**: mẫu `diagram` (AntV X6, MIT): nút xếp theo col / row, đường nối tự đi góc vuông bo tròn, nút bật ra → đường nối được vẽ → nét đứt chảy.
- Icon: `python3 scripts/noto_emoji.py lessons/NN robot light-bulb …` (tên dùng tên tiếng Anh chữ thường nối bằng gạch ngang). Cái nào có hoạt ảnh chính thức sẽ được đặt đồng thời vào `lessons/NN/lottie/`, trong cảnh ghi cùng một tên thì **tự phát hoạt ảnh**, không có thì dùng ảnh tĩnh.
- Ảnh chụp màn hình Sách xanh: đặt vào `assets/img/`, đăng ký `credit` trong `images.json` ("Nguồn ảnh chụp: Sách xanh thực chiến WorkBuddychương X · MIT"), hình ảnh tự đánh dấu nguồn.
- Trích dẫn nguyên văn phải từng chữ, ghi rõ chương; **không bịa số liệu**, dữ liệu minh hoạ phải ghi "dữ liệu ví dụ".

## Trường chung (cảnh nào cũng có thể ghi)
| Trường | Tác dụng |
|---|---|
| `chapter` | Tên chương: breadcrumb ở góc trái trên + chuyển cảnh khi đổi trang |
| `src` | Chữ nhỏ nguồn ở góc trái dưới |
| `tips: [{text, at, until}]` | Lời của nhân vật thuyết minh (bong bóng), 6–16 chữ, nhắc lại ý chính lời dẫn, **không bịa quan điểm thay tác giả** |
| `cam: [[thời điểm, x, y, z], …]` | Camera zoom / lia / xoay; thời điểm có thể ghi giây (tính từ đầu cảnh) hoặc `"B02@word"` |
| `host` | `"right"` / `"none"` |

## Mẫu
| Mẫu | Công dụng | Tham số chính |
|---|---|---|
| cover | Trang bìa kiểu trang Notion | title (`\n` xuống dòng), question, iconImg (`host-avatar`), stickers (3 icon), props |
| kinetic | **Chữ lớn bật ra từng chữ** (câu vàng, chuyển ngoặt) | lines[{text (`*word*` màu nhấn), size, y, at, color}], lottie[{name, x, y, size, at}] |
| say | Chữ lớn thường (không bật chữ) | lines, emoji |
| stickers | Một hàng thẻ (3–5 thẻ) | title, items[{emoji, label, sub, at, tick/cross/circle}], caption, arrows |
| pan | **Camera lia qua một hàng thẻ** (liệt kê "ba việc") | cards[{emoji, title, sub}], cam, word (chữ lớn cuối) |
| quote | Khối trích dẫn Notion (nguyên văn) | text, from, emoji, textAt |
| shot | Ảnh chụp màn hình + khoanh chú thích vẽ tay (ghi clip để phát chuỗi khung quay màn hình) | img hoặc clip, crop, label, marks[{kind: circle/box/underline, area, at, note, side, color}] |
| flow | Quy trình (vòng icon + mũi tên + mũi tên làm lại) | nodes[{emoji, label, at, star}], back{from, to, label, at} |
| compare | So sánh trái phải (dấu gạch chéo / tích) | left/right{title, emoji, items, at} |
| checklist | Danh sách (đánh dấu hoặc đánh số) | items[{emoji, label, sub, at}], numbered, cols |
| note | Callout giải thích nhiệm vụ + nhãn bên phải | lines[{text, tag, tagColor, at}] |
| pause | Tạm dừng suy nghĩ (đếm ngược rồi công bố) | q, a, revealAt |
| diagram | **Sơ đồ quy trình/cộng tác X6** | title, nodes[{id, label, icon (icon-park:…), col, row, tone, at}], edges[{from, to, at, flow}], caption |
| iconwall | **Tường icon động** (2×3) | items[{lottie, label, at}] |
| dataviz | **Số cuộn + cột mọc lên + đường được vẽ** | count{label, to, prefix, suffix, sub}, bars{items}, line{values, labels}, note (ghi "dữ liệu ví dụ" hoặc nguồn dữ liệu) |
| map | **Bản đồ thế giới chấm + đường bay + điểm đánh dấu xung** (không vẽ biên giới quốc gia) | arcs[{from:[kinh, vĩ], to, at, color}], pins[{ll, label, at}], cam (zoom gần), note |
| recap | Sơ đồ tổng kết cuối | center, branches[{emoji, text, at}] |
| outro | Giới thiệu bài tiếp theo + cảm ơn tài nguyên mã nguồn mở | next, credits (mỗi dòng một mục, đừng quá dài), thanks |

## Gợi ý nhịp điệu
- Mỗi bài ít nhất dùng: 1 kinetic (câu vàng), 1 pan hoặc cam (cho camera chuyển động), 2–4 tips (nhân vật nói), một số khoanh chú thích ảnh chụp.
- Bài có số liệu (hạn mức, giá, so sánh hiệu suất) dùng dataviz; nói về khu vực / luồng chuyển quy trình dùng map.
- Tự kiểm: `python3 scripts/check_scenes.py lessons/NN`, rồi `make_lesson.py … build` xem bảng contact.
