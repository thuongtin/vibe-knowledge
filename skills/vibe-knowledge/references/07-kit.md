# 07 · Thư viện component know.js (cài ở <series>/cine/engine/know.js)

Toàn bộ component: dựng DOM lúc build, trong render gọi `update` theo thời gian tuyệt đối t; không phụ thuộc khung trước. Thời gian viết theo vị trí lời dẫn: `T("B05")`, `T("B05.count")`, `T("B05@ba trăm chín mươi")`, `T("B05.end")`.

| Component | Công dụng | Cách viết |
|---|---|---|
| `TH.*` | Năm bảng màu hệ thống thị giác | `const TM = TH.gufeng` |
| `bg(ctx, TM, o)` | **Dòng đầu tiên trong render của mỗi cảnh quay**: xoá lớp WebGL thành màu nền chủ đề, đặt bloom / hạt / tối góc | `bg(ctx, TM, { grain: 0.03 })` |
| `layers` | **Chủ lực cấp cơ bản**: Opus viết tay SVG / ảnh cục bộ chia lớp xa trung gần, đẩy theo thị sai độ sâu | `sc = layers(s, [{ svg: SKY, depth: 0.15 }, { svg: HALL, depth: 0.5 }, { svg: FG, depth: 1 }]); sc.update(t, t0, t1, { pan: [-80, 0], zoom: [1, 1.06] })` |
| `plate` | Ảnh Renoise: đẩy kéo lia dịch + mờ vào mờ ra + tối góc + nhãn AI | `p = plate(s, { src: A("img/a01.jpg") }); p.update(t, t0, t1, { from: [1.04,0,0], to: [1.14,-40,0] })` |
| `vclip` | Video Renoise (sau khi clip2frames tách khung) vẽ từng khung lên canvas, phụ đề luôn nằm trên | `v = vclip(s, { dir: A("clips/v01"), n: 241 }); v.update(t, t0, t1, { rate: 1, loop: false })` |
| `keyword` | Từ khoá trên hình (≤8 chữ, vượt thì console cảnh báo) | `k = keyword(s, "Dư thừa = áo giáp", { y: 400, color: TM.accent }); k.update(t, at, out)` |
| `counter` | Số cuộn | `c = counter(s, { label: "Tử tù được thả về nhà", suffix: " người" }); c.update(t, [[t0,0],[t1,83],[t2,390]])` |
| `foot` / `foots` | Chú thích nguồn (dưới phụ đề y=1044) | `f = foot(s); foots(f, t, [[a, b, "«Tư trị thông giám» quyển 194"], …])` |
| `choice` | Nút lưỡng nan cuối phim | `ch = choice(s, [["Về","Đánh cược vào lòng tin"],["Không về","Trốn cả đời"]]); ch.update(t, at, { pick: 0, pickAt })` |
| `seriesCard` | Tiêu đề mở đầu loạt phim | `seriesCard(s, { series: "Nếu bạn sống thời cổ đại", ep: 1, title: "Thương Ưởng dựng cột", theme: TM }).update(t, at, out)` |
| `vquote` | Cổ văn dọc hiện từng chữ (nền giấy) | `vquote(s, { text: "Dân lấy làm lạ\nKhông ai dám dời", src: "«Sử ký · Thương Quân liệt truyện»" }).update(t, t0, t1, out)` |
| `trail` | Một vệt sáng lần lượt làm sáng các nút (mẫu gốc D) | `trail(s, { pts: [[200,700],…], labels: [...] }).update(t, t0, t1)` |
| `spread` | Rải điểm từ trung tâm ra bốn phía (lan bản đồ, lan truyền) | `spread(s, { cx, cy, n: 390 }).update(t, t0, t1, { back: 0 })` |
| `bars` | So sánh cột (Benford 1–9) | `bars(s, { values, labels, fmt: v => v.toFixed(1)+"%" }).update(t, t0, t1, { hl: 0 })` |
| `chapter` | Nhãn chương góc trên trái | `chapter(s, { n: 1, cn: "Đoán", en: "THE GUESS", theme: TM }).update(t, at, out)` |
| `ask` | Thẻ câu hỏi lớn (đầu / cuối phim) | `ask(s, "Đổi lại là bạn, bạn có dọn không?", { tag: "Nếu bạn sống thời cổ đại" }).update(t, at, out)` |

| `marker` | Bút dạ quang quét qua một đoạn chữ hoặc vùng (điều tra hình ảnh) | `marker(world, { x, y, w, h }).update(t, at)` |
| `ring` | Vòng đỏ vẽ tay được vẽ theo thứ tự nét | `ring(world, { cx, cy, rx, ry }).update(t, at)` |
| `focus` | Đẩy container gần tới một điểm và dừng hình (khung then chốt) | `focus(world, t, [[t0, {x, y, s: 1}], [t1, {x, y, s: 1.5}]])` |
| `capNews` | Tiêu đề lớn tin phụ đề, từ khoá đè khối vàng | `capNews(s, [["Thưởng", 0], ["mười vàng", 1]], { size: 150 }).update(t, at, out)` |
| `srcChip` | Nhãn nguồn trượt vào cạnh con số | `srcChip(s, "«Sử ký · Thương Quân liệt truyện»", { x, y }).update(t, at, out)` |
| `lowerThird` | Thanh tiêu đề tin tức (chuyên mục cố định) | `lowerThird(s, { tag: "VIBE Tri thức", title }).update(t, at, out)` |
| `stamp` | Đóng dấu xuống (điểm rơi của móc câu, kết luận then chốt) | `stamp(s, "Tam kỳ lăng", { x: 960, y: 200, size: 130 }).update(t, at, out)` |
| `cutaway` | Mặt cắt nét vẽ: đồ vật / cấu trúc AI vẽ không chuẩn thì dùng mã vẽ, nét được vẽ theo thứ tự, khối màu bật ra, nhãn mờ vào; hình ghi "minh hoạ bằng mã" | `cutaway(s, { x, y, w: 700, h: 600, lines: [{ d, color, width }], blocks: [{ x, y, w, h, fill, stroke }], labels: [["Ngoài · Phương giám", 596, 110, GOLD]] }).update(t, at, out)` |
| `tokens` | Một hàng khối nhỏ lần lượt bật ra, có thể "tan" chỉ còn khối keep (băng tan rồi, tiền tiêu rồi) | `tokens(s, { x, y, n: 6, size: 80 }).update(t, at, meltAt, keep, out)` |

Bố cục nguyên văn của điều tra hình ảnh: mỗi chữ đặt vào một ô cùng độ rộng (`width: 44px`), gạch trọng điểm và vẽ vòng có thể định vị chính xác theo "dòng thứ mấy, chữ thứ mấy" (xem styles/_samples/styles2_film.js).

Những cái cine có sẵn cũng đều dùng được: `appear slam typeText codeCard quoteCard sourceTag recapMap` (ui.js), `Particles Clock Bars Showroom Liquid Tunnel` (scenes/). Cảnh hạt tự vẽ WebGL trong render, thì đừng gọi bg nữa.

**Đường dẫn tài nguyên**: `const A = (f) => new URL(\`./assets/${f}\`, import.meta.url).href` (dùng cho trang); `const P = (f) => decodeURIComponent(new URL(...).pathname).slice(1)` (mục music dùng đường dẫn tương đối so với thư mục series, new_film.py đã vá cho finish.py).

**Đồng bộ ghi hình**: plate / vclip đăng ký ảnh chưa giải mã vào `window.__vk`; new_film.py đã vá record.py, stills.py, sau mỗi lần seek chờ giải mã xong mới chụp, nên bảng tiếp xúc và thành phẩm sẽ không có khung trống.
