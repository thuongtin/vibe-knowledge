# 04 · Dàn dựng cảnh cho engine vẽ tay (skin Notion)

Áp dụng cho series có `"engine": "sketch"` (bộ WorkBuddy nhập môn). Trình biên dịch `runtime/sketch.js`, primitive `primitives/sketch.js`, `primitives/motion.js`. Phần dưới đây trước tiên là nguyên văn quy phạm dành cho trợ lý trong series (SCENES_GUIDE), sau đó là phần bổ sung: tra nhanh toàn bộ trường và các quy tắc bố cục đã được sửa.

---

# WorkBuddy nhập môn · Quy phạm dàn dựng hình ảnh (engine vẽ tay + skin Notion + hiệu ứng chuyển động)

Mỗi bài có một `lessons/NN/scenes.json`, trình biên dịch là `runtime/sketch.js` (primitive nằm ở `primitives/sketch.js`, `primitives/motion.js`).

## Phần đầu tệp
```json
{"n": 2, "title": "…", "series": "WorkBuddy nhập môn", "engine": "sketch", "skin": "notion", "presenter": "hp", "sticker": true,
 "speed": 1.15, "author": "@Berryxia", "scenes": [ … ]}
```
- `sticker: true` (**mặc định cho bài mới**): phong cách sticker — thẻ của stickers biến thành sticker viền trắng (nghiêng ngẫu nhiên 1.5–3°, phóng to rơi xuống nảy lại, bóng đổ co chặt, ánh sáng quét qua), minh hoạ được bọc viền trắng cắt khuôn, emoji Noto trong thẻ cũng được vẽ viền trắng; nhãn không vừa thì tự co cỡ chữ. Tắt cho một trang: stickers ghi `"style": "card"`, say ghi `"illusSticker": false`.
- `engine: "sketch"` dùng engine vẽ tay; `skin: "notion"` là phong cách tối giản Notion (`"paper"` là phong cách sổ tay, dự phòng).
- `presenter: "host"`: nhân vật nhỏ dẫn giải ở góc dưới phải (ảnh đại diện pixel của tác giả, biết chớp mắt, mở miệng khi nói). Trang bìa và sơ đồ ôn tập cuối bài tự động không xuất hiện, từng cảnh có thể ghi `"host": "none"` để tắt.
- Cách ghi thời gian giống mùa hai: `"B03"`, `"B03.cue"`, `"B03@từ"`, `"B03.end"`, đều có thể cộng trừ ± giây.

## Tư liệu
- **Phân công ba lớp biểu tượng**: giao diện, quy trình, danh sách dùng **biểu tượng nét IconPark** (ghi `icon-park:robot`, Apache 2.0, vẽ từng nét, phối màu Notion; thiếu thì dùng `lucide:` / `tabler:`); nhân vật chính, cảm xúc, đồ vật dùng **emoji Noto** (ghi `robot`, có hoạt ảnh thì tự phát).
- **Minh hoạ**: thư viện minh hoạ IconPark 88 hình (`assets/illustrations/iconpark/`, tổng quan `_sheet.html`, danh sách `catalog.json`). `python3 scripts/illus.py lessons/NN ip-5-48 …` đặt vào thư mục bài, trong cảnh `say` / `cover` ghi `"illus": "ip-5-48"`: vẽ nét đường viền + khối màu mờ vào; nguồn chỉ ghi ở credits cuối phim (inlineCredits mặc định tắt).
- **Sơ đồ quy trình / cộng tác**: mẫu `diagram` (AntV X6, MIT): nút xếp theo col / row, đường nối tự đi góc vuông bo tròn, nút bật ra → vẽ đường nối → nét đứt chảy.
- Biểu tượng: `python3 scripts/noto_emoji.py lessons/NN robot light-bulb …` (tên dùng tên tiếng Anh chữ thường nối bằng gạch ngang). Cái nào có hoạt ảnh chính thức sẽ được đặt đồng thời vào `lessons/NN/lottie/`, trong cảnh ghi cùng một tên thì **tự phát hoạt ảnh**, không có thì dùng ảnh tĩnh.
- Ảnh chụp màn hình Sách xanh: đặt vào `assets/img/`, đăng ký `credit` trong `images.json` ("Nguồn ảnh chụp màn hình: 《WorkBuddy 实战蓝皮书》Chương X · MIT"), hình ảnh tự ghi nguồn.
- Trích dẫn nguyên văn phải từng chữ, ghi rõ chương; **không bịa số liệu**, dữ liệu minh hoạ phải ghi rõ "Dữ liệu ví dụ".

## Trường dùng chung (cảnh nào cũng có thể ghi)
| Trường | Tác dụng |
|---|---|
| `chapter` | Tên chương: breadcrumb ở góc trên trái + chuyển trang |
| `src` | Chữ nhỏ nguồn ở góc dưới trái |
| `tips: [{text, at, until}]` | Lời của nhân vật dẫn giải (bong bóng), 6–16 chữ, nhắc lại ý chính của lời dẫn, **không bịa quan điểm thay tác giả** |
| `cam: [[thời điểm, x, y, z], …]` | Ống kính đẩy kéo lia dịch; thời điểm có thể ghi bằng giây (tính từ đầu cảnh) hoặc `"B02@từ"` |
| `host` | `"right"` / `"none"` |

## Mẫu
| Mẫu | Công dụng | Tham số chính |
|---|---|---|
| cover | Trang bìa kiểu trang Notion | title (`\n` xuống dòng), question, iconImg (`host-avatar`), stickers (3 biểu tượng), props |
| kinetic | **Chữ lớn bật ra từng chữ** (câu vàng, bước ngoặt) | lines[{text (`*từ*` màu nhấn), size, y, at, color}], lottie[{name, x, y, size, at}] |
| say | Chữ lớn thường (không bật chữ) | lines, emoji |
| stickers | Một hàng thẻ (3–5 thẻ) | title, items[{emoji, label, sub, at, tick/cross/circle}], caption, arrows |
| pan | **Ống kính lia qua một hàng thẻ** (liệt kê "ba việc") | cards[{emoji, title, sub}], cam, word (chữ lớn ở cuối) |
| quote | Khối trích dẫn Notion (nguyên văn) | text, from, emoji, textAt |
| shot | Ảnh chụp màn hình + khoanh chú thích vẽ tay (ghi clip để phát chuỗi khung hình quay màn hình) | img hoặc clip, crop, label, marks[{kind: circle/box/underline, area, at, note, side, color}] |
| flow | Quy trình (vòng tròn biểu tượng + mũi tên + mũi tên làm lại) | nodes[{emoji, label, at, star}], back{from, to, label, at} |
| compare | So sánh trái phải (dấu X / dấu tick) | left/right{title, emoji, items, at} |
| checklist | Danh sách (đánh dấu hoặc đánh số) | items[{emoji, label, sub, at}], numbered, cols |
| note | Callout mô tả nhiệm vụ + nhãn bên phải | lines[{text, tag, tagColor, at}] |
| pause | Tạm dừng suy nghĩ (đếm ngược rồi công bố) | q, a, revealAt |
| diagram | **Sơ đồ quy trình/cộng tác X6** | title, nodes[{id, label, icon (icon-park:…), col, row, tone, at}], edges[{from, to, at, flow}], caption |
| iconwall | **Tường biểu tượng động** (2×3) | items[{lottie, label, at}] |
| dataviz | **Số cuộn + cột mọc lên + đường vẽ ra** | count{label, to, prefix, suffix, sub}, bars{items}, line{values, labels}, note (ghi "Dữ liệu ví dụ" hoặc nguồn dữ liệu) |
| map | **Bản đồ thế giới chấm điểm + đường bay + điểm đánh dấu xung** (không vẽ biên giới quốc gia) | arcs[{from:[kinh, vĩ], to, at, color}], pins[{ll, label, at}], cam (đẩy gần), note |
| recap | Sơ đồ ôn tập cuối bài | center, branches[{emoji, text, at}] |
| outro | Xem trước bài sau + cảm ơn tư liệu mã nguồn mở | next, credits (mỗi dòng một mục, đừng quá dài), thanks |

## Gợi ý nhịp điệu
- Mỗi bài ít nhất dùng: 1 kinetic (câu vàng), 1 pan hoặc cam (cho ống kính chuyển động), 2–4 tips (nhân vật nói), một số khoanh chú thích trên ảnh chụp màn hình.
- Bài có số liệu (hạn mức, giá cả, so sánh hiệu quả) dùng dataviz; nói về địa lý / luồng quy trình dùng map.
- Tự kiểm: `python3 scripts/check_scenes.py lessons/NN`, rồi `make_lesson.py … build` xem contact sheet.

---

## Bổ sung A · Toàn bộ công tắc ở phần đầu tệp

| Trường | Tác dụng |
|---|---|
| `n` | Số bài (bìa ghi "Bài N"); bài dẫn nhập và các bài không đánh số dùng `eyebrow`/`props` để ghi đè |
| `skin` | `notion` (trắng tinh, Geist+Noto không chân, màu chữ/màu nền Notion, callout, breadcrumb, chuyển cảnh chớp trắng) / `paper` (giấy sổ tay, LXGW WenKai, băng dính giấy nhớ) |
| `skin: "cream"` | Bố cục Notion + nền kem #FAF6EE + nhấn vàng champagne (bài đào tạo thẩm mỹ y khoa / thương hiệu cao cấp; `SKINS.cream`, logic mẫu giống notion) |
| `presenter` cách ghi khác | `"<tiền tố>"`: trong assets/img của series có bốn khung `<tiền tố>-0/-blink/-talk/-talk-blink` (như nữ giảng viên do Renoise tạo `lady`), mở miệng theo chữ, chớp mắt, nổi tips; `"emoji:<tên>"`: dùng một emoji Noto làm người dẫn giải |
| `presenterSmooth` | Khi người dẫn giải là minh hoạ (không phải pixel) thì ghi true: thu phóng mượt, to hơn một cỡ 300px |
| `presenter` | `hp`: nhân vật nhỏ pixel 10 động tác (talk wave point idea think stop check cheer thumbsup type, mỗi động tác 8 khung hình, talk mở miệng theo chữ, khung 4 chớp mắt); `host`: ảnh đại diện đơn kiểu cũ |
| `sticker` | **Bài mới mặc định true**: phong cách sticker (xem trên); bài cũ không ghi = kiểu thẻ ban đầu |
| `speed` | Đổi tốc độ lời dẫn, mặc định ghi 1.15 |
| `lang` | `en` chuyển chữ giao diện và cách ngắt phụ đề sang tiếng Anh |
| `inlineCredits` | Mặc định tắt: dưới minh hoạ không kèm chữ nhỏ nguồn, nguồn thư viện biểu tượng/minh hoạ chỉ vào credits cuối phim; `true` mới ghi từng chỗ |
| `shotCredit` | Tiền tố nguồn ảnh chụp màn hình (dùng cho bản tiếng Anh) |
| `noCaptions` | Tắt phụ đề |
| `videoOnly` | final chỉ xuất phim: không làm bản tương tác, không sửa series.json (dùng cho bài dẫn nhập, bản tiếng Anh) |

## Bổ sung B · Tra nhanh trường của mẫu (lấy trình biên dịch làm chuẩn)

| Mẫu | Trường |
|---|---|
| cover | title, titleAt, eyebrow, eyebrowAt, question, questionAt, iconImg, illus, stickers, photo (notion/cream cũng hỗ trợ: ảnh lớn bo góc bên phải + chữ nhỏ nguồn, photoW/photoX/photoY), photoAt, props, coverBg |
| say | lines, illus, illusAt, illusSticker, emoji, emojiAt, underline, dy |
| stickers | title, items[{emoji, label, sub, at, rot, tick/cross (ghi thời điểm, không được ghi true)}], caption, arrows, style (sticker / card), w, h, y |
| quote | text, textAt, from, emoji, stamp, size, w, y, cps |
| shot | img hoặc clip, clipDelay, loop, crop, label, marks[{kind, area, at, note, side, color}], rot, w, h, x, y |
| flow | nodes[{emoji, label, at, star}], back{from, to, label, at}, caption, gap, title, y |
| compare | left/right{title, emoji, at, items}, neutral, h, y |
| checklist | title, items[{emoji, label, sub, at}], numbered, cols, rowH, y |
| note | title, lines[{text, tag, tagColor, at}], mono, size, lh, w, x, y, cps, textAt |
| pause | q, a, revealAt, emoji |
| recap | center, branches[{emoji, text, at}] (tối đa 6 mục) |
| outro | next, thanks, thanksAt, credits[] |
| kinetic | lines[{text, size, y, at, color, weight}], lottie[{name, x, y, size, at}] |
| iconwall | title, items[{lottie, label, at}], cols |
| dataviz | title, count{label, to, prefix, suffix, sub}, bars{items}, line{values, labels}, note |
| map | title, arcs, pins, cam, note |
| diagram | title, nodes[{id, label, icon, col, row, tone, bg, at}], edges[{from, to, at, label, color, flow}], caption, captionY, colGap, rowGap, nodeW, nodeH, h, y |
| pan | cards[{emoji, title, sub}], word, cam |
| Dùng chung | chapter, src, tips[{text, at, until, pose}], pose, cam[[t, x, y, z]], host |

## Bổ sung C · Quy tắc bố cục (đúc kết sau khi vấp lỗi)

- **say**: dòng thứ hai chữ lớn 96px, câu dài sẽ tự xuống dòng, các dòng bên dưới dịch xuống theo số dòng ước tính; vẫn nên giữ dòng thứ hai ≤ 10 chữ.
- **diagram**: nút ghi `tone` màu nền thì tự lấy màu giấy nhớ cùng tông (không cần ghi `bg`); nhãn quá dài biểu tượng sẽ đè chữ → viết nhãn ngắn hoặc tăng `nodeW`; đường nối không chỉ định được cạnh xuất phát, dựa vào việc xếp col/row để tránh cắt nhau (hai hàng hình rắn thường dùng); `caption` mặc định y=298, nằm phía trên chữ nhỏ nguồn.
- **recap**: elip trung tâm tự mở rộng theo độ dài chữ `center`; nhánh thứ 5, 6 (ngay trên/ngay dưới) toả ra từ mép elip; mỗi nhánh ≤ 9 chữ, nếu không sẽ xuống dòng.
- **stickers**: tên tiếng Anh dài đừng đặt vào tiêu đề thẻ (sẽ xuống dòng), đặt vào sub; khi có 5 thẻ mỗi thẻ rộng khoảng 300px, nhãn ≤ 5 chữ.
- **quote**: tự xuống dòng sẽ cắt giữa từ, khi cần thì tự thêm `\n`.
- **shot**: nhãn `note` dễ đè lên chữ của ảnh gốc, ưu tiên dùng `tips` của nhân vật nhỏ để giải thích; `area` của khoanh chú thích là tỷ lệ của ảnh gốc [x0,y0,x1,y1], xem ảnh gốc trước rồi ước lượng; trước khi khoanh dùng `crop` cắt bỏ vùng riêng tư.
- **dataviz**: `note` ở góc dưới phải sẽ bị nhân vật nhỏ che, nguồn đổi sang ghi `src` (góc dưới trái).
- **cam**: ống kính đẩy gần sẽ cắt mất thẻ, khi stickers có một hàng 4 thẻ thì đừng đẩy; pan chính là ống kính lia thẻ chuyên dụng.
- Đầu cảnh phải nhanh chóng có thứ gì đó xuất hiện (tiêu đề gắn vào cue đầu tiên của nhịp này), nếu không trên contact sheet sẽ là màn hình trống.
- tips của nhân vật nhỏ 6–16 chữ, nhắc lại ý chính của lời dẫn, không phát biểu quan điểm thay tác giả; nhắc nhở an toàn dùng `pose: "stop"`.

## Bổ sung D · Primitive nhóm sticker (`k: "group"`)

group của `primitives/sketch.js`: toạ độ phần tử con tính theo tâm nhóm, cùng làm hoạt ảnh "ấn xuống" (from hệ số phóng to mặc định 1.3 → 1, spin góc nghiêng quay về thẳng mặc định 8°, rot là góc cuối cùng).
- `card: true` + `w/h/color`: thẻ sticker viền trắng (viền trắng 10px, bo góc 30, bóng đổ co chặt theo lúc rơi xuống, sau khi định vị thì ánh sáng quét qua).
- `filter: "diecut"` + `edge`: vẽ một vòng viền trắng cắt khuôn quanh cả nhóm (drop-shadow trắng 8 hướng + nét viền mảnh + bóng đổ), dùng cho minh hoạ, emoji.
- Mẫu khác muốn sticker hoá: bọc vài phần tử ban đầu vào một group (đổi toạ độ thành tương đối so với tâm nhóm) là được. Hiện stickers, minh hoạ của say/cover đã nối; pan, recap, checklist vẫn kiểu ban đầu.
