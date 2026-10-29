# Làm một bài “Claude Code làm video: bài điều phối Opus 5.5” (bản làm lại) — hướng dẫn cho trợ lý

Người dùng đã xem và công nhận: bản mẫu `showcase/opus-intro` (62 giây) và bài 1 `lessons/01` (video chỉ là một hàm). **Bài 1 chính là mẫu chuẩn**, bài bạn làm phải cùng đẳng cấp, cùng cách viết.

## Hướng đi (ý của người dùng)
- Nhân vật chính là **bản thân Opus 5.5**: giảng rõ vì sao nó điều phối video mạnh như vậy, cách dùng tốt hiệu ứng chuyển động của nó.
- Bản thân video phải là “quả bom”: mỗi khung hình đều do code tính theo thời gian thực, hình ảnh tác động mạnh (Three.js, GLSL, hạt, chuyển động camera, chữ lớn động), không phải ghép đoạn mẫu hiệu ứng, không phải phân tích bản quay màn hình.
- Phong cách công nghệ nền tối; chỉ tạo cú sốc camera (`hits`) ở 2–3 điểm then chốt, **đừng rung cả đoạn**; mỗi màn hình một thông tin hoàn chỉnh, hiệu ứng tác động lên nội dung, đừng chẻ chữ vụn ra.

## Bạn cần giao (đều nằm trong `lessons/<số bài>/`)
1. `narration.json`: 16–20 nhịp, 1100–1400 chữ (sau khi tăng tốc 1,15 lần thì khoảng 3,5–4 phút). Định dạng, giọng đọc, ghi chú giọng điệu chép y như `lessons/01/narration.json`.
2. Lồng tiếng: `cd ~/Desktop/ai-teardown && python3 scripts/make_lesson.py examples/claude-video/lessons/<số bài> voice > examples/claude-video/lessons/<số bài>/voice.log 2>&1`, rồi `python3 scripts/speed.py examples/claude-video/lessons/<số bài> 1.15`.
3. `film.js`: bảng cảnh quay, cách viết theo `lessons/01/film.js`. Tư liệu đặt trong `lessons/<số bài>/assets/`; cần cảnh 3D/shader mới thì viết trong `lessons/<số bài>/scenes/` (dành riêng cho bài này).
4. Bảng tiếp xúc: `python3 cine/tools/stills.py <số bài> lessons/<số bài>/stills/sheet.png B01+1 B02.a+1 …` (mỗi cảnh quay ít nhất 1 khung, hành động then chốt thêm khung), **tự mình xem từng tấm**, có chồng lấn, tràn khung, màn hình trống, chữ quá nhỏ, phụ đề bị che thì sửa đến khi hết.
5. Cuối cùng trả lời phiên chính (trong 200 chữ): số nhịp, số chữ, tổng thời lượng lồng tiếng, những nhịp có điểm đọc lại kiểm tra chất lượng dưới 95% và cách bạn xử lý, cảnh bạn hài lòng nhất và cảnh bạn kém chắc nhất.

**Không làm**: không render thành phẩm (record.py / finish.py do phiên chính chạy), không xuất bản, không sửa bất kỳ file nào trong `cine/engine/` và `showcase/` (thấy engine thiếu gì thì nói trong phần trả lời), không đụng vào bài khác.

## Bắt buộc đọc trước khi bắt tay làm
- `lessons/01/narration.json`, `lessons/01/film.js` (mẫu)
- `cine/engine/core.js` (một bài = seek(t); film.js xuất ra những gì), `narr.js` (cách viết thời gian), `ui.js` (thành phần và hàm hoạt họa), `scenes/*.js` (các cảnh dùng được)
- `PLAN-v2.md`, mục của bài bạn trong `series.json` (tiêu đề, móc câu, ý chính)
- Nguồn sự thật (bảng bên dưới). **Con số, tính năng, cách nói không có nguồn thì không lên màn hình, không đưa vào lời dẫn**; suy đoán phải nói “có thể”.

## Tra nhanh engine
- Trang: `http://127.0.0.1:8964/cine/index.html?lesson=<số bài>` (gốc server là `examples/claude-video`; chưa mở thì chạy `python3 -m http.server 8964 --directory ~/Desktop/ai-teardown/examples/claude-video` ở nền).
- film.js xuất ra:
  - `COLD`: số giây lời dẫn bị dời lùi ra sau = độ dài của “phần mở đầu bom” ở đoạn đầu (bài này tự render, thường 4–7 giây, không có lời dẫn, nhạc nền level 3 + hiệu ứng âm thanh). Đừng viết `COLD_SRC` (cái đó dùng để ghép đoạn bản mẫu, chỉ bài 1 và bài dẫn nhập dùng).
  - `meta`, `hits` (≤3 thời điểm), `blur` (các đoạn [bắt đầu, kết thúc] giây có chuyển động nhanh, khi render sẽ làm mờ chuyển động), `sfx` (điểm hiệu ứng âm thanh), `sections` (các đoạn nhạc nền), `build(ctx)` trả về mảng cảnh quay `{from, to, build(root), render(t, u)}`.
- Cách viết thời gian: `T("B07")` bắt đầu, `T("B07.ring")` đọc đến [[ring]], `T("B03@ba nghìn")` đọc đến một chữ nào đó, `T("B07.end")`, có thể thêm `+0.4`.
- Cảnh (`cine/engine/scenes`):
  - `Particles`: 260 nghìn hạt; đội hình `F.DUST/LINE/CLOUD/TITLE/CN/POINT`; `setText("title"|"cn", {lines:[{text, font, y}]})` đổi thành chữ bất kỳ; tham số render xem chú thích ở cuối file (from/to/p/stagger/delay/fly/burst/size/bright/dust/camX/Y/Z/lookX/lookY/sweep).
  - `Clock`: tác phẩm điêu khắc thời gian, `render(r, rt, thời gian cảnh, {speed, beat, gain, plate, camX, camY, camZ})`.
  - `Bars`: dãy cột theo nhịp, `{kicks:[giây], hats:[giây], big:[giây], camA, camY, camZ, lookY, grow}`.
  - `Showroom`: phòng trưng bày ba món (nút chrome / khối đa diện thủy tinh / quả cầu sáng), `{pos:[x,y,z], look:[x,y,z], fov}`; khi khởi tạo phải truyền `ctx.r`.
  - `Liquid`: ray marching kim loại lỏng, `{camA, collapse, glow, bg, zoom}`.
  - `Tunnel`: đường hầm mã nguồn, khi khởi tạo truyền vào một đoạn văn bản mã nguồn; `{dist, gain, roll, fov, glow}`.
  - Bức tường phân cảnh, tự kiểm tra bằng chụp khung, chọn khung mẫu trong bản mẫu đều ghép từ DOM + cảnh, code ở `showcase/opus-intro/src/shots_b.js`, cần thì **sao chép** sang bài của bạn rồi sửa, đừng import file đó.
- UI (`cine/engine/ui.js`): `appear / slam / typeText`, `codeCard` (`hl(i, on)` tô sáng dòng), `promptChip`, `quoteCard`, `sourceTag`, `pauseCard`, `recapMap`.
- Phụ đề do engine tự sinh (theo thời gian từng chữ của lời dẫn), ở khoảng y≈940–1030 trên màn hình; **vùng y>920 đừng đặt nội dung** (chữ nhỏ nguồn sourceTag ở y=1012 thì được, nhưng đừng tranh chỗ với phụ đề).
- Loại hiệu ứng âm thanh: slam, whoosh, whoosh-through, riser (cần t_to), impact, blip, click, tick, shutter, snap, chime, error, card (note_index), rewind. Level nhạc nền: 0 im lặng, 1 chỉ có lớp nền, 2 nhịp nhẹ, 3 đầy đủ (dùng cho phần mở đầu).

## Cách viết (giống bài 1)
- Nhịp đầu nối tiếp phần mở đầu lạnh (“Vừa rồi cái này...”), nhịp hai “Bài này nói ba việc”, giữa có một nhịp “Tạm dừng nghĩ một chút” + nhịp sau là `[[answer]]`, nhịp áp chót là ôn lại sơ đồ tư duy, nhịp cuối báo trước bài sau + “Hẹn gặp lại bài sau”. **Đừng bài nào cũng cảm ơn** (người dùng yêu cầu: lời cảm ơn chỉ đặt ở bài dẫn nhập và bài cuối).
- Câu ngắn kiểu nói; tên riêng tiếng Anh dùng ít, bắt buộc dùng thì đưa vào lexicon; con số viết theo cách đọc (“ba nghìn bảy trăm mười sáu”).
- Trích prompt của cộng đồng: mỗi lần ≤15 từ tiếng Anh, ghi rõ @tác giả, chữ nhỏ trong video “Trích từ awesome-opus5-5-videos của Yihui, bản quyền prompt thuộc về tác giả gốc”.
- **Dùng dữ liệu thật và tư liệu thật**: `timeline.json` của bản mẫu (124 BPM, 32 ô nhịp, thời điểm cue), `showcase/opus-intro/out/score_report.txt`, `assets/making/` (các khung “trước khi sửa / sau khi sửa” chụp thật trong quá trình làm bản mẫu, `fanqie_BRIEF.md` và `fanqie_STORYBOARD.md` do Opus 5.5 viết trong phiên thật), số đo thực tế của chúng ta (trình duyệt headless SwiftShader mỗi khung 67,9 ms so với Metal GPU 1,9 ms; cùng một t render hai lần chênh 0 điểm ảnh; bản mẫu 3716 khung, render khoảng 7 phút). Hình minh họa phải ghi “minh họa”.

## Nguồn sự thật
| Nguồn | Đường dẫn | Dùng được gì |
|---|---|---|
| Anthropic “Introducing Claude Opus 5.5” 2026-09-22 | `research/claude-code/snapshots/S41.txt` | Mô hình đầu tiên của họ 5.5; trong số nhiều mô hình Claude làm game từ một câu prompt, nó đạt điểm cao nhất về hình ảnh và độ hoàn thiện; người thử nghiệm: cách nó kiểm tra công việc của chính mình rất sáng tạo, vòng tự kiểm chứng dễ dựng hơn; chạy liên tục 18 giờ không lệch hướng; một phiên chỉ huy hơn chục phiên; đầu ra nhanh hơn Opus 5 hơn 30%; giá |
| Tài liệu nền tảng Claude, Models overview | `research/claude-code/snapshots/S14.md` | Ngữ cảnh 1M token ≈ 2,5 triệu ký tự; đầu vào văn bản và hình ảnh |
| Tài liệu Claude Code | `research/claude-code/facts.json` (mục C0xx) | Subagent, hooks, /model, effort, v.v. |
| Yihui awesome-opus5-5-videos | `research/yihui/prompt-patterns.md`, `awesome-stats.md`, `rights.md` | 475 video, 12 cách viết (câu ví dụ nguyên văn kèm tác giả) |
| Số đo thực tế của bản mẫu | `showcase/opus-intro/` (timeline.json, score_report.txt, src/) | Dữ liệu của chính khóa học này |

## Ý chính từng bài (tiêu đề, móc câu xem series.json)
| Số bài | Gợi ý phần mở đầu bom | Bắt buộc giảng | Tư liệu thật dùng được |
|---|---|---|---|
| 02 Làm đạo diễn trước, bắt tay làm sau | Bức tường phân cảnh 16 thẻ rơi vào vị trí theo nốt móc kép → chui vào một thẻ biến thành hình thật | Bảng phân cảnh (mỗi cảnh làm gì, dài bao lâu), bảng nhịp (BPM → số giây mỗi nhịp → lưới ô nhịp), nó viết kế hoạch trước rồi mới viết code, ngữ cảnh 1M | `fanqie_STORYBOARD.md` (phân cảnh nó viết trước trong phiên thật), timeline.json của bản mẫu |
| 03 Toán học của nhịp điệu | Sóng xung kích dãy cột theo nhịp + mỗi nhịp đập xuống một câu | Easing (vào chậm ra nhanh), lò xo vượt quá, so le, bám nhịp (124 BPM = mỗi nhịp 0,484 giây) | Hàm spring/ease trong bản mẫu (src/util.js), sai số trống kick trong score_report ≤5 ms |
| 04 Nhìn thấy tác phẩm của chính mình | Chụp khung → khung nhận diện → đánh dấu lỗi → tự sửa | Nó xem được hình; vòng khép kín render→chụp khung→xem→sửa; cho nó xem gì (chồng lấn, tràn khung, độ tương phản); sửa xong chụp lại | Ba cặp trước/sau trong `assets/making/` |
| 05 Cả bộ phim không lệch hướng | Trên một trục thời gian, track hình, track nhạc, track hiệu ứng âm thanh cùng sáng lên đồng bộ | Một bảng thời gian dùng chung cho hình và nhạc; chia việc theo ô nhịp giao cho subagent (nhạc nền của bản mẫu chính là do subagent viết song song); kiểm tra tiến độ tác vụ dài thế nào | timeline.json, score_report.txt |
| 06 Hạt | 260 nghìn hạt nổ tung rồi tụ thành tiêu đề bài này | Đội hình, chuyển tiếp (so le + easing), nhiễu loạn (nhiễu curl); viết prompt thế nào | `explode_v1_loop` → `explode_v2_shockwave` (sửa lỗi thật) |
| 07 Camera 3D | Phòng trưng bày tiến gần→quật máy→quay vòng + xuyên qua đường hầm mã nguồn | Đẩy, kéo, lia, quật, quay vòng, xuyên qua; mờ chuyển động (trung bình khung phụ, màn trập 180°); nói về thời lượng và easing thế nào | Đoạn mờ chuyển động trong record.py của bản mẫu |
| 08 Chất cảm của shader | Kim loại lỏng toàn màn hình → co sập thành điểm | Shader = mỗi điểm ảnh một đoạn chương trình; ray marching + hợp nhất mượt; đèn dải trong studio quyết định chất cảm kim loại; GPU so với render phần mềm | Số đo thực tế SwiftShader 67,9 ms so với Metal 1,9 ms |
| 09 Chữ động và chuyển cảnh | Tiêu đề chương đập xuống + ba cú match cut nối lại | Đập chữ, mặt nạ, từng chữ; mỗi màn hình một thông tin hoàn chỉnh; match cut (đường thẳng → trục thời gian, bản phác → hình ảnh, khung mẫu → toàn màn hình); chỉ dành cú sốc cho vài lần then chốt | Ba cú match cut trong bản mẫu |
| 10 Bí quyết prompt và tác phẩm tốt nghiệp | Cắt nhanh tất cả các cảnh “bom” của khóa học này | Tra nhanh 12 cách viết, danh sách cấm để bớt “mùi AI”, đòi khung mẫu trước rồi mới đòi cả phim, quy trình tác phẩm tốt nghiệp | prompt-patterns.md |
