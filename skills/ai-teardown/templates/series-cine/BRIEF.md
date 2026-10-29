# Làm một bài "{Tên khóa học}" — hướng dẫn cho trợ lý (phim bằng mã · mẫu)

> Phiên chính điền đầy `{…}` rồi mới gửi cho trợ lý, bỏ các mục không dùng tới. Bốn bản hướng dẫn đã dùng thật nằm trong `examples-briefs/` (khóa dàn dựng, khóa thực chiến phim quảng bá, phim khái niệm ngành, bài bổ sung phân tích phim), trước khi viết hướng dẫn mới hãy xem qua một bản.

Bài mẫu: `examples-lessons/00` (dẫn nhập: chữ lớn bằng hạt, mở đầu cực mạnh, nhạc nền tổng hợp) và `examples-lessons/p08` (khóa thực chiến: mở đầu phát trọn một lượt phim thật, terminal của phiên làm việc thật, nhạc nền từ thư viện). {Bài người dùng đã duyệt, ví dụ `lessons/01`} là chuẩn mực của khóa này, bài bạn làm phải cùng chuẩn, cùng cách viết.

Thư mục gốc không gian làm việc: `{không gian làm việc}`; thư mục loạt bài: `{không gian làm việc}/examples/{tên loạt bài}` (các đường dẫn tương đối bên dưới đều tính từ thư mục loạt bài).
`$CINE_PY` = Python đã cài numpy, scipy, pillow, playwright: `{đường dẫn}`.

## Định hướng
- {Một câu: nhân vật chính của khóa này là gì, ví dụ "bản thân Opus 5.5", "các phim thành phẩm chúng tôi đã bàn giao"}
- Bản thân phim phải đẹp: 4–8 giây mở đầu là hình ảnh gây sốc do mã tính ra (hoặc dựng nhanh các đoạn phim thật) + tên khóa học đập xuống màn hình, khớp đúng điểm nhịp của nhạc nền.
- Chỉ dùng `hits` ở 2–3 điểm then chốt, đừng rung cả đoạn; khi trong hình có đoạn phim thì không dùng hits (đoạn phim được chồng lên ở hậu kỳ, sẽ không rung theo).
- Mỗi màn hình một thông tin trọn vẹn; hiệu ứng tác động lên nội dung, đừng xé nhỏ chữ.

## Bạn cần bàn giao (đều nằm trong `lessons/<số bài>/`)
1. `narration.json`: 16–20 nhịp, 1100–1400 chữ (sau khi tăng tốc 1,15 lần thì khoảng 3,5–4 phút). Định dạng, giọng đọc chép theo bài mẫu (`voice.clone` trỏ tới `../../voice/host-ref.wav`).
2. Lồng tiếng: `cd {không gian làm việc} && python3 scripts/make_lesson.py examples/{tên loạt bài}/lessons/<số bài> voice > examples/{tên loạt bài}/lessons/<số bài>/voice.log 2>&1`, rồi `python3 scripts/speed.py examples/{tên loạt bài}/lessons/<số bài> 1.15`, sau đó ở thư mục loạt bài chạy `python3 tools/check_timings.py <số bài>` để kiểm tra căn chỉnh từng chữ có bị đứt không. MiMo sẽ giới hạn tốc độ (429), script tự lùi lại và thử lại, hãy kiên nhẫn chờ.
3. Nhạc nền (chọn một trong hai):
   - Nền tổng hợp (mặc định): `sections` ghi các đoạn và level, finish.py sẽ dùng `cine/audio/tools/bed.py` để tổng hợp.
   - Thư viện nhạc: `$CINE_PY ~/.claude/skills/promo-video/scripts/pick_music.py lessons/<số bài>/assets/music/bgm.wav --track {bài nhạc} --seconds <tổng số giây của bài+2> --hit-at <giây mà tên khóa học đập xuống>`; nếu bài nhạc ngắn hơn cả bài học thì dùng `python3 cine/tools/loopbed.py <bgm.wav> <bgm_long.wav> --seconds <tổng số giây của bài> --bpm <BPM được in ra> --anchor <hit-at>` để nối dài theo từng ô nhịp. Ghi BPM được in ra và `credit.txt` vào chú thích trong film.js.
4. `film.js`: bảng góc máy, cách viết theo bài mẫu. Tư liệu để trong `lessons/<số bài>/assets/`; cảnh 3D/shader dành riêng cho bài này viết trong `lessons/<số bài>/scenes/`.
5. Đoạn phim (khi có clips): `$CINE_PY cine/tools/clips.py <số bài>` (cắt sẵn đoạn phim và ảnh bìa).
6. Contact sheet: `$CINE_PY cine/tools/stills.py <số bài> lessons/<số bài>/stills/sheet.png 1.0 B01+1 B02.a+1 …` (mỗi góc máy ít nhất 1 khung, giữa chừng hoạt ảnh thì bổ sung thêm vài khung), **tự mình xem từng ảnh**: chồng lên nhau, ra ngoài khung hình, màn hình trống, chữ quá nhỏ, phụ đề bị che thì sửa cho đến khi hết. Khung đoạn phim trong contact sheet hiển thị ảnh bìa, trong thành phẩm sẽ được thay bằng video thật.
7. Trả lời phiên chính (trong 200 chữ): số nhịp, số chữ, tổng thời lượng lồng tiếng, các nhịp đọc lại dưới 95% và cách xử lý, danh sách đoạn phim (phim nguồn + điểm bắt đầu + thời lượng), góc máy bạn hài lòng nhất và ít chắc chắn nhất.

**Không được làm**: không render thành phẩm (record.py / finish.py do phiên chính chạy), không xuất bản, không sửa bất kỳ file nào trong `cine/engine/`, `cine/tools/`, `cine/audio/` (thiếu gì thì nói trong câu trả lời), không đụng tới bài khác, không sửa skill khác.

## Phải đọc trước khi bắt tay làm
- `narration.json` và `film.js` của bài mẫu
- `cine/engine/core.js` (một bài học = seek(t); film.js xuất ra những gì), `narr.js` (cách viết thời gian), `ui.js` (thành phần và hàm hoạt ảnh), `scenes/*.js` (các cảnh dùng được)
- Mục của bài này trong `series.json` (tiêu đề, móc câu, ý chính) và các nguồn sự kiện bên dưới

## Tra nhanh engine
- Trang: `http://127.0.0.1:8964/cine/index.html?lesson=<số bài>` (gốc máy chủ là thư mục loạt bài; chưa bật thì chạy `python3 -m http.server 8964 --bind 127.0.0.1 --directory <thư mục loạt bài>` ở nền).
- film.js xuất ra:
  - `COLD`: số giây lời dẫn bị dời về sau = độ dài đoạn mở đầu cực mạnh của phần đầu phim (không có lời dẫn, nhạc nền level 3 + hiệu ứng âm thanh).
  - `meta` (`{ title, n }`), `hits` (≤3 thời điểm), `blur` (các đoạn `[bắt đầu, kết thúc]` tính bằng giây có chuyển động nhanh, render sẽ làm mờ chuyển động), `sfx` (điểm hiệu ứng âm thanh), `sections` (các đoạn nhạc nền tổng hợp), `clips` (đoạn phim thật), `music` (nhạc nền từ thư viện).
  - `build(ctx)` trả về mảng góc máy `{ from, to, build(root), render(t, u) }`; `ctx.narr` là trục thời gian lời dẫn, `ctx.r` là bộ render three.js, `ctx.post` là hậu kỳ.
- Cách viết thời gian: `T("B07")` nhịp này bắt đầu, `T("B07.ring")` đọc tới `[[ring]]`, `T("B03@三千")` đọc tới một chữ nào đó, `T("B07.end")` nhịp này kết thúc, có thể cộng thêm `+0.4`.
- Cảnh (`cine/engine/scenes`): `Particles` (260 nghìn hạt, đội hình `F.DUST/LINE/CLOUD/TITLE/CN/POINT`, `setText` đổi chữ tùy ý), `Clock` (tượng điêu khắc thời gian), `Bars` (dãy cột nhịp), `Showroom` (phòng trưng bày ba món, truyền `ctx.r` khi khởi tạo), `Liquid` (kim loại lỏng dò tia), `Tunnel` (đường hầm mã nguồn). Tham số xem chú thích ở cuối từng file.
- UI (`cine/engine/ui.js`): `appear / slam / typeText`, `codeCard` (`hl(i, on)` làm nổi bật dòng), `promptChip`, `quoteCard`, `sourceTag`, `pauseCard`, `recapMap`, `clipBox`.
- Phụ đề do engine tự tạo theo thời gian từng chữ của lời dẫn, ở y≈940–1030; **không đặt nội dung ở y>920** (chữ nhỏ ghi nguồn `sourceTag` ở y=1012 thì được).
- Các loại hiệu ứng âm thanh: slam, whoosh, whoosh-through, riser (cần `t_to`), impact, blip, click, tick, shutter, snap, chime, error, card (`note_index`), rewind, key (ghi âm phím bấm thật, `enter: true` là phím Enter). Level nhạc nền tổng hợp: 0 im lặng, 1 chỉ có nền, 2 nhịp nhẹ, 3 đầy đủ (dùng cho đoạn mở đầu).

## Cách dùng đoạn phim (thành phẩm thật)
- `clips.push({ id, src: đường dẫn tuyệt đối, from: giây bắt đầu của phim nguồn, at: xuất hiện ở giây thứ mấy của bài này, dur, x, y, w, h, audio: "mute", fade?, poster_at?, seg?, gain? })`.
- Khung dùng `clipBox(s, { x, y, w, h, poster: "../lessons/<số bài>/assets/clips/<id>.jpg", label, sub })`; đoạn phim được finish.py chồng vào trong khung, **luôn ở tầng trên cùng**: mọi chữ, mũi tên, chú thích đều không được đè lên khung đoạn phim; khung đoạn phim không được vào vùng y>920.
- `w`, `h` dùng số chẵn, tỷ lệ 16:9 (toàn màn hình 1920×1080; thường dùng 960×540, 640×360, 560×314); phim dọc muốn hiển thị trọn vẹn thì dùng khung 9:16 (như 304×540).
- Âm thanh mặc định là `mute`; muốn khán giả nghe tiếng gốc thì dùng `audio: "full"` (đoạn lời dẫn này để trống, `gain` tự định); `"duck"` là nhỏ hơn lời dẫn.
- Thời lượng đoạn phim ≤ độ dài còn lại của phim nguồn (xem bằng `ffprobe`); điểm bắt đầu đừng rơi vào đoạn chuyển cảnh mờ của phim nguồn. Giữa các đoạn phim cắt cứng thì dùng `fade: 0`, điểm cắt đặt trên điểm nhịp.
- Khi đoạn phim ngắn hơn góc máy thì dùng `seg`: phim nguồn chỉ phát `seg` giây, thời gian còn lại đứng hình ở khung cuối.

## Cách viết nhạc nền từ thư viện
`music = [{ src: đường dẫn tuyệt đối, from: 0, at: <giây bắt đầu vào>, dur: <độ dài cả bài + 0.6 − at>, gain_curve: [[0, -2], [COLD - 0.4, -2], [COLD + 0.8, -9], …], fade_in?, fade_out: 1.5 }]`, và `sections.push({ t: 0, t_to: độ dài cả bài + 0.6, level: 0 })` (tắt nền tổng hợp). Ở đoạn có lời dẫn, finish.py sẽ tự hạ nhạc nền thấp thêm.

## Cách viết
- Nhịp đầu nối tiếp đoạn mở đầu ("vừa rồi cái này…"), nhịp thứ hai "bài này nói ba việc", giữa bài có một nhịp "tạm dừng suy nghĩ" + nhịp kế tiếp `[[answer]]`, nhịp áp chót ôn lại bằng sơ đồ (`recapMap`), nhịp cuối giới thiệu bài sau + "hẹn gặp lại ở bài sau". **Đừng bài nào cũng cảm ơn** (lời cảm ơn chỉ đặt ở bài dẫn nhập và bài cuối).
- Câu ngắn kiểu nói chuyện; hạn chế tên riêng tiếng Anh, bắt buộc dùng thì cho vào `lexicon`; con số viết thành cách đọc ("三千七百一十六").
- **Tên `[[cue]]` chỉ dùng chữ thường, chữ số, gạch dưới, đừng đặt là `end`** (`B06.end` là cách viết được engine giữ riêng).
- **Tên tiếng Anh trong lời dẫn đừng có dấu gạch nối**: viết "promo video", đừng viết "promo-video" (dấu gạch nối sẽ làm căn chỉnh từng chữ bị đứt tại đó).
- Trích dẫn nội dung cộng đồng: mỗi lần ≤15 từ tiếng Anh, ghi rõ tác giả và nguồn.
- Cần ảnh minh họa (hình vẽ, sticker, sơ đồ) thì dùng Codex tạo ảnh: `codex exec --skip-git-repo-check "Tạo một ảnh: …. Sao chép vào thư mục hiện tại và đặt tên X.png" < /dev/null > log 2>&1` (bắt buộc có `< /dev/null`), không dùng emoji; sơ đồ ghi chú "minh họa".
- Tên người dùng máy cục bộ trong đường dẫn luôn viết thành `~`; khóa bí mật, file ủy quyền, email tài khoản không được lên hình.

## Nguồn sự kiện (con số, tính năng, cách nói không có nguồn thì không lên màn hình, không vào lời dẫn; suy đoán thì nói "có thể")
| Nguồn | Đường dẫn | Dùng được gì |
|---|---|---|
| {nguồn} | {đường dẫn} | {nội dung dùng được} |

## Ý chính của từng bài
| Số bài | Gợi ý mở đầu cực mạnh | Ba việc bắt buộc phải nói | Tư liệu thật dùng được |
|---|---|---|---|
| {số bài tiêu đề} | {mở đầu} | {ba việc} | {tư liệu} |
