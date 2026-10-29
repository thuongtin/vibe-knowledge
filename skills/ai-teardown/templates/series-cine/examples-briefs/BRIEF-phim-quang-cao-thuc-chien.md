# Làm một bài của "Khoá thực chiến video quảng bá Opus 5.5" — hướng dẫn cho trợ lý (BRIEF v3)

Người dùng đã công nhận cách viết và chất lượng của cả bộ bài dàn dựng (`lessons/00–10`). Mẫu của khoá thực chiến là **bài dẫn nhập `lessons/p00`** và **bài 1 `lessons/p01`**: bài bạn làm phải cùng chất lượng, cùng cách viết với chúng. Phương án khoá học xem `promo/PLAN.md`, dàn ý xem `promo/series.json`.

## Định hướng
- Nhân vật chính là **thành phẩm thật**: các video quảng bá chúng ta đã làm bằng Opus 5.5 (chỉ dùng bản cuối cùng, xem bảng dưới; khách hàng đã đồng ý cho trình chiếu). Mỗi bài dùng chúng để nói rõ một việc: vì sao đẹp, làm thế nào để Opus 5.5 + promo-video skill làm ra được.
- Một mạch xuyên suốt: **một phiên làm việc thật** (làm video quảng bá 30 giây cho sản phẩm hư cấu "圈问", được ghi lại trong `promo/session/`). Mỗi bài đặt bước tương ứng trong phiên đó: prompt thật, đầu ra thật, tệp thật.
- Bản thân video phải đẹp: 5–8 giây mở đầu là cắt nhanh các đoạn thật + tiêu đề làm bằng code, khớp đúng điểm nhịp của nhạc nền; chỉ dùng `hits` ở 2–3 điểm then chốt (và **khi có đoạn phim trên màn hình thì không dùng hits**, vì đoạn phim được chồng lên ở hậu kỳ, sẽ không rung theo).

## Yêu cầu mới của người dùng ngày 10-05 (bắt buộc làm theo)
- **Mọi tác phẩm chỉ dùng bản thành phẩm cuối cùng** (bảng dưới), không dùng bản cũ; ưu tiên dùng WorkBuddy nhập môn, WaytoAGI, YouWare, Renoise, 造物矩阵.
- **Không dùng video của Berryxia** (không xuất hiện ở bất kỳ đâu).
- Giảng theo phân loại ngành: sản phẩm AI, cộng đồng và thương hiệu cá nhân, trà sữa ăn uống, bách hoá, bán lẻ, sản xuất, thương mại điện tử, văn hoá du lịch đời sống. Các video ngành mới (喜茶, 无印良品, 比亚迪, bán lẻ, thương mại điện tử) đang làm, làm xong sẽ đặt ở `~/Desktop/brand-promos/<thương hiệu>/out/film.mp4`, phiên chính sẽ báo cho bạn biết có dùng được không.
- Cần ảnh minh hoạ (tranh, sticker, hình minh hoạ) thì dùng thẳng Codex để sinh ảnh: `codex exec --skip-git-repo-check "Tạo một hình: …. Sao chép vào thư mục hiện tại đặt tên là X.png" < /dev/null > log 2>&1` (bắt buộc có `< /dev/null`), đặt vào `lessons/<số bài>/assets/`. Không dùng emoji.

### Danh sách bản cuối cùng (đường dẫn đều nằm dưới `~/Desktop/`)
| Phân loại | Tác phẩm | Tệp |
|---|---|---|
| Sản phẩm AI | WorkBuddy nhập môn · phim chính v4 | workbuddy-promo/out/workbuddy-v4-4k-master.mp4 |
| Sản phẩm AI | WorkBuddy nhập môn · bản chạy quảng cáo | workbuddy-ad/out/workbuddy-ad-scenes-4k-master.mp4 |
| Sản phẩm AI | WorkBuddy nhập môn · bản một cú máy | workbuddy-oneshot/out/os-master.mp4 |
| Sản phẩm AI | YouWare v3 | youware-promo/out/youware-v3-hq.mp4 |
| Sản phẩm AI | YouWare phim năng lực PPT | youware-promo/out/ppt-2k.mp4 |
| Sản phẩm AI | YouWare phim chạy quảng cáo (Nhật / Trung / Anh) | youware-jp/out/jp-master.mp4 · zh-master.mp4 · en-master.mp4 |
| Sản phẩm AI | Renoise | renoise-promo/out/renoise-2k-v2.mp4 |
| Sản phẩm AI | HiAPI | hiapi-promo/out/hiapi-hq.mp4 |
| Sản phẩm AI | ListenHub | listenhub-promo/out/listenhub-hq.mp4 |
| Sản phẩm AI | BeeGer (bản 3D cuối cùng) | beeger-promo/out/beeger-3d-hq.mp4 |
| Sản phẩm AI | CelHive (v3) | celhive-promo/CelHive宣传片-2K.mp4 |
| Sản phẩm AI | 大猫剪辑 | mqscene-promo/out/damao-2k.mp4 |
| Sản phẩm AI | 知行猿 (chỉ có 540p) | mentalos-promo/film/out/film-preview.mp4 |
| Sản phẩm AI | 小互 (v2) | xiaohu-promo/out/xiaohu-hq-v2.mp4 |
| Sản phẩm AI | 精酿 BrewReel | brewreel-promo/BrewReel宣传片-2K.mp4 |
| Sản phẩm AI | VibeCafé × Vibe42 (chỉ có 540p) | vibe-promo/VibeCafe-Vibe42宣传片-预览.mp4 |
| Sản phẩm AI | DockLock | docklock-promo/out/docklock-2k.mp4 |
| Sản phẩm AI | TOKEI (bản cắt nhanh, 9:16) | tokei-promo/out/tokei-hype-2k.mp4 |
| Cộng đồng và thương hiệu cá nhân | WaytoAGI | waytoagi-promo/WaytoAGI宣传片-2K.mp4 |
| Cộng đồng và thương hiệu cá nhân | 造物矩阵 (bản ngầu) | zaowu-promo/out/zaowu-hype-hq.mp4 |
| Cộng đồng và thương hiệu cá nhân | 鱼总聊AI | yuzong-promo/out/yuzong-2k-hq.mp4 |
| Trà sữa ăn uống | 奈雪 | nayuki-promo/out/nx-master.mp4 |
| Trà sữa ăn uống | 黄但记1927 | huangdanji-promo/out/黄但记1927-探店快闪-30s-1080p.mp4 |
| Văn hoá du lịch đời sống | 顺德游玩的一天 | shunde-vlog/out/顺德游玩的一天-vlog-4K.mp4 |
| Văn hoá du lịch đời sống | Chàng trai tập gym ngày tập chân (9:16) | gym-boy/out/gym-master.mp4 |
| 3D web và so sánh mô hình | STILLWATER | lake-film/out/STILLWATER_功能展示_1080p.mp4 |
| 3D web và so sánh mô hình | So sánh con ong của ba mô hình | apis-promo/out/opus-gemini-astra-bee.mp4 |
| 3D web và so sánh mô hình | 华山论剑 | model-flash/out/mf-master.mp4 |
| Phiên làm việc thật | 圈问 30 giây (sau khi sửa bản) | quanwen-promo/out/film.mp4 (trước khi sửa bản: ai-teardown/examples/claude-video/promo/session/film_v1.mp4) |

Khi kể chuyện sửa bản (BeeGer, CelHive, 小互, rung cả đoạn) có thể dùng chữ và bản cũ còn tồn tại để so sánh, đây là chỗ duy nhất được phép xuất hiện bản cũ, và phải ghi "bản cũ".

## Phiên làm việc thật (đã quay xong, 5 lượt)
`promo/session/turn1.json … turn5.json`(prompt, từng lệnh gọi công cụ kèm số giây tương đối, toàn bộ chữ nó viết, thời gian và chi phí quy đổi của lượt này), `usage.json` (toàn bộ quá trình 48 lần gọi mô hình, 52 lần gọi công cụ, đầu ra 50 nghìn token, đọc cache 5,33 triệu, ghi cache 160 nghìn, quy đổi theo giá API 3,38 USD; 5 lượt tổng cộng khoảng 16 phút).
| Lượt | Chúng ta nói | Nó làm | Thời gian · quy đổi |
|---|---|---|---|
| 1 | Dùng promo-video làm video quảng bá 30 giây cho 圈问, website … | Đọc website → phân tích tư liệu → thẻ chọn kiểu → bảng phân cảnh 7 cảnh → hỏi 3 việc | 44 giây · $0.39 |
| 2 | Chọn A/A/được, cuối phim Logo dừng đủ 2 giây, xuất khung hình mẫu trước | Dựng dự án, chọn nhạc khớp nhịp (Techno Fest Vibes, 124 BPM, đoạn chính khớp tới Logo ở giây 3,4), viết Film.tsx, trích khung hình mẫu, tự nhìn ra 4 vấn đề và sửa | 7,5 phút · $1.93 |
| 3 | Xuất thẳng thành phẩm | Đẩy render xuống nền → phiên vừa kết thúc là render bị ngắt (cạm bẫy của chế độ headless `-p`) | 53 giây · $0.13 |
| 4 | Render bị ngắt, render lại ở tiền cảnh | Render ở tiền cảnh, phát hiện đỉnh −0.2 dBFS chỉ giới hạn biên độ track âm thanh, đối chiếu từng pixel 2,4 giây tĩnh cuối cùng | 2,8 phút · $0.40 |
| 5 | Hook quá yếu, phóng to, câu hỏi làm chữ lớn mỗi nhịp một câu | Chỉ sửa đoạn hook, trích khung hình mẫu, render lại, đối chiếu các cảnh khác không đổi từng pixel | 4 phút · $0.53 |
Mỗi bài dùng lượt nào: p02 lượt 1 (đọc website, trích phối màu) + đầu lượt 2 (lưu Logo); p03 thẻ chọn kiểu của lượt 1; p04 phân cảnh lượt 1 + chọn nhạc khớp nhịp lượt 2; p05 hiệu ứng chuyển động trong Film.tsx lượt 2 (`~/Desktop/quanwen-promo/src/`); p06 vận động ống kính trong Film.tsx; p07 chọn nhạc lượt 2 + giới hạn biên độ lượt 4; p08 lượt 3–5 (cạm bẫy, kiểm định chất lượng, sửa bản) và mức sử dụng toàn bộ quá trình.

## Bạn cần bàn giao (đều nằm trong `lessons/<số bài>/`, số bài p02…p07)
1. `narration.json`: 16–20 nhịp, 1100–1400 chữ. Định dạng, giọng chép y theo `lessons/p00/narration.json` (ở `style` đổi "bài dẫn nhập" thành "một bài học").
2. Lồng tiếng: `cd ~/Desktop/ai-teardown && python3 scripts/make_lesson.py examples/claude-video/lessons/<số bài> voice > examples/claude-video/lessons/<số bài>/voice.log 2>&1`, sau đó `python3 scripts/speed.py examples/claude-video/lessons/<số bài> 1.15`MiMo sẽ giới hạn tốc độ 429, kịch bản tự lùi lại thử lại, hãy kiên nhẫn chờ.
3. Nhạc nền: `showcase/opus-intro/.venv/bin/python ~/.claude/skills/promo-video/scripts/pick_music.py lessons/<số bài>/assets/music/bgm.wav --track <bài nhạc trong bảng dưới> --seconds <tổng số giây của bài+2> --hit-at <giây tiêu đề mở đầu đập xuống>`, ghi BPM được in ra và `credit.txt` vào chú thích của film.js.
4. `film.js`: cách viết theo `lessons/p00/film.js`. Tư liệu đặt vào `lessons/<số bài>/assets/`.
5. Đoạn phim: `/usr/local/bin/python3 cine/tools/clips.py <số bài>` (cắt gọn đoạn phim và ảnh bìa).
6. Contact sheet: `/usr/local/bin/python3 cine/tools/stills.py <số bài> lessons/<số bài>/stills/sheet.png 1.0 B01+1 B02.a+1 …` (mỗi cảnh ít nhất 1 khung hình), **tự xem từng tấm**: chồng lên nhau, tràn ra ngoài khung, màn hình trống, chữ quá nhỏ, phụ đề bị che thì sửa đến khi hết. Khung đoạn phim trong contact sheet hiển thị ảnh bìa, trong thành phẩm sẽ đổi thành video thật.
7. Trả lời phiên chính (trong 200 chữ): số nhịp, số chữ, tổng độ dài lồng tiếng, các nhịp đọc lại dưới 95% và cách xử lý, danh sách đoạn phim (phim gốc + điểm bắt đầu + thời lượng), cảnh bạn hài lòng nhất và cảnh bạn ít chắc chắn nhất.

**Không được làm**: không render thành phẩm (record.py / finish.py do phiên chính chạy), không phát hành, không sửa bất kỳ tệp nào trong `cine/engine/`, `cine/tools/`, `showcase/` (thiếu gì thì nói trong câu trả lời), không đụng đến bài khác, không sửa bất kỳ tệp nào trong `~/.claude/skills/promo-video`.

## Cách dùng đoạn phim (thành phẩm thật)
- `export let clips = []`, trong `build()` dùng `clips.push({ id, src: đường dẫn tuyệt đối, from: giây bắt đầu của phim gốc, at: xuất hiện ở giây thứ mấy của bài này, dur, x, y, w, h, audio: "mute", fade?, poster_at? })`. Hàm nhỏ `clip()` trong bài dẫn nhập có thể chép y nguyên.
- Khung vẽ bằng `clipBox(s, { x, y, w, h, poster: "../lessons/<số bài>/assets/clips/<id>.jpg", label, sub })`; đoạn phim do finish.py chồng vào trong khung. **Đoạn phim luôn ở lớp trên cùng**: bất kỳ chữ, mũi tên, chú thích nào cũng không được đè lên khung đoạn phim; khung đoạn phim không được vào vùng y>920 (vùng phụ đề).
- `w`, `h` dùng số chẵn, 16:9 (toàn màn hình 1920×1080; thường dùng 960×540, 640×360, 560×314, 540×304). Phim dọc (TOKEI, bản dọc của WorkBuddy) sẽ bị cắt giữa thành ngang, muốn hiển thị đầy đủ thì dùng khung 9:16 (ví dụ 304×540).
- Âm thanh của đoạn phim mặc định `mute`; muốn khán giả nghe một đoạn âm thanh gốc (ví dụ bài 7 nói về nhạc nền), dùng `audio: "full"`, đoạn lời dẫn này phải để trống, `gain` tự quyết định.
- Thời lượng đoạn phim ≤ độ dài còn lại của phim gốc (dùng `ffprobe` xem thời lượng phim gốc).
- Cắt cứng giữa các đoạn phim dùng `fade: 0`, điểm cắt đặt đúng điểm nhịp (cách viết `beat(i)` xem bài dẫn nhập).
- Khi đoạn phim ngắn hơn cảnh thì dùng `seg`: phim gốc chỉ phát `seg` giây, thời gian còn lại giữ nguyên ở khung hình cuối (ví dụ chỉ phát hook 3 giây của một video, khung được giữ đến khi cảnh này kết thúc).

## Phân bổ nhạc nền (không được đổi, tránh hai bài trùng bài)
| Số bài | Bài nhạc (`--track`) | Ghi chú |
|---|---|---|
| p01 | mixkit-162-minimal-techno-01.mp3 | 129 BPM, ngay đầu đã có năng lượng (Techno Fest Vibes nhường cho video của phiên làm việc thật) |
| p02 | mixkit-132-hazy-after-hours.mp3 | 123 BPM, năng lượng trung bình |
| p03 | mixkit-161-minimal-techno-02.mp3 | 128 BPM |
| p04 | mixkit-1012-take-this-higher.mp3 | 123 BPM, vào đoạn chính ở giây 11.25 (bài này vừa hay dùng nó để minh hoạ `--hit-at`) |
| p05 | mixkit-126-trap-electro-vibes.mp3 | 112 BPM, vào đoạn chính ở giây 10.5 |
| p06 | mixkit-32-driving-ambition.mp3 | 99 BPM, vào đoạn chính ở giây 9.5 |
| p07 | mixkit-173-better-times-are-coming.mp3 | 117.5 BPM |
| p08 | mixkit-33-motivating-mornings.mp3 | 123 BPM, vào đoạn chính ở giây 12 |

Trong film.js: `music = [{ src: đường dẫn tuyệt đối, from: 0, at: 0, dur: độ dài cả bài + 0.6, gain_curve: [[0, -2], [COLD - 0.4, -2], [COLD + 0.8, -9], …], fade_out: 1.5 }]`, và `sections.push({ t: 0, t_to: độ dài cả bài + 0.6, level: 0 })` (không dùng nền tổng hợp).

## Cách viết (giống bài dẫn nhập và bài 1)
- Nhịp đầu nối tiếp phần mở đầu ("vừa rồi cái này…"), nhịp hai "bài này nói về ba việc", một nhịp giữa "tạm dừng suy nghĩ" + nhịp sau `[[answer]]`, nhịp áp chót là sơ đồ ôn tập (`recapMap`), nhịp cuối xem trước bài sau + "hẹn gặp ở bài sau". **Không cảm ơn** (lời cảm ơn chỉ đặt ở bài dẫn nhập và bài cuối).
- Mỗi bài ít nhất một đoạn "phiên làm việc thật": terminal vẽ lại theo bản ghi thật trong `promo/session/` (theo cách viết `term()` của bài 1), chỉ lấy bước liên quan đến bài này; tên người dùng trong đường dẫn luôn viết thành `~`.
- Câu ngắn khẩu ngữ; hạn chế tên riêng tiếng Anh, bắt buộc dùng thì đưa vào lexicon; con số viết theo cách đọc.
- **Tên [[cue]] chỉ dùng chữ thường, chữ số, dấu gạch dưới, đừng đặt tên là `end`** (`B06.end` là cách viết dành riêng của engine, nghĩa là nhịp này kết thúc).
- **Tên tiếng Anh trong lời dẫn không được có dấu gạch nối**: viết "promo video", đừng viết "promo-video" (có gạch nối sẽ làm căn chỉnh từng chữ bị đứt ở đó, các chữ phía sau dồn hết về cuối nhịp). Sau khi lồng tiếng chạy một lượt `python3 promo/check_timings.py <số bài>` để kiểm tra có đứt không.
- Chữ trên màn hình mỗi màn một thông tin hoàn chỉnh; hiệu ứng tác động lên nội dung, đừng chẻ chữ vụn ra.

## Nguồn dữ kiện (không có nguồn thì không lên màn hình, không đưa vào lời dẫn; suy đoán thì nói "có thể")
| Nguồn | Đường dẫn | Dùng được gì |
|---|---|---|
| promo-video skill | `~/.claude/skills/promo-video/SKILL.md`, `references/*.md` | quy trình, thẻ chọn kiểu, bảng phân cảnh, các mức thời lượng, tốc độ đọc, nguyên tắc thiết kế, danh mục duyệt phim của bậc thầy, các mức hiệu ứng và bản đồ thủ pháp, bảng vận động ống kính, thư viện nhạc và uỷ quyền, lằn ranh tuân thủ |
| Ghi chép phản hồi (phản hồi thật của người dùng) | mục "Ghi chép phản hồi" của `references/style-router.md` | rung cả đoạn → phản cảm; nhạc hồi hộp → đổi sang house tươi sáng; nhịp chậm → làm lại nhịp nhanh; bản chạy quảng cáo đòi luôn 4K; bố cục bento dọc "không bằng trước" |
| Kho ca | `examples/promo-course/research/cases.md`(41 mục, `cases.json` cùng trường), `sheets/<id>.jpg` (contact sheet 1 khung hình/giây), `sheets/zoom/` | thời lượng, tỷ lệ khung hình, chọn kiểu bốn lớp, nhạc nền (đã xác minh bằng dấu vân tay âm thanh) của mỗi video, 183 đoạn phim ứng viên, 6 đoạn mạnh nhất, 3 câu chuyện sửa bản (BeeGer ba bản, CelHive ba bản, rung cả đoạn → HitCam, BrewReel có hai bản trước và sau khi sửa để cắt đối chiếu) |
| Phân tích skill | `examples/promo-course/research/skill.md` | mỗi bước của promo-video ứng với tài liệu nào, quy tắc nào |
| Tham khảo bên ngoài | `examples/promo-course/research/sources.md` | cấu trúc mẫu product-promo của HyperFrames, giấy phép Remotion (gồm Creators 25 USD mỗi người mỗi tháng), Revideo / Motion Canvas (MIT), giấy phép GSAP; **12 trích đoạn prompt video quảng bá của cộng đồng (mỗi mục ≤15 từ, kèm @tác giả và liên kết bài gốc, có thể trích dẫn trực tiếp)** |
| Ghi chép bàn giao | mục dự án trong bộ nhớ (phiên chính sẽ đưa các điểm chính trong phần mô tả bài của bạn) | ví dụ BeeGer v1→v2, 小互 đổi nhạc nền, 精酿 95 BPM |
| Giấy phép Remotion | `promo/sources/remotion-LICENSE.md` | miễn phí cho cá nhân, công ty vì lợi nhuận ≤3 người, tổ chức phi lợi nhuận; còn lại cần giấy phép doanh nghiệp |
| Phiên làm việc thật | `promo/session/` (turn*.jsonl, usage.json) | nguyên văn prompt, đầu ra của nó, thời gian, mức sử dụng |

## Lưu ý (tra ra từ nghiên cứu)
- WorkBuddy v4 dùng emoji hệ thống của Apple (trong quy tắc của skill thuộc vùng xám bản quyền): đừng phóng to hình ảnh emoji của nó để làm ví dụ tích cực.
- TOKEI có cảnh khởi động mecha kiểu Gundam, skin chân thực, WaytoAGI có Logo đối tác và ảnh chụp màn hình sản phẩm: chỉ dùng khung nhỏ, thời lượng ngắn, không làm cận cảnh toàn màn hình.
- Thành phẩm của 小互 v1, CelHive v1/v2, WorkBuddy v1 không còn trên ổ đĩa: kể về các lần sửa bản này chỉ có thể dùng chữ và các bản còn tồn tại, đừng nói "xin xem v1".

## Điểm chính từng bài
| Số bài | Gợi ý mở đầu cực mạnh | Ba việc bắt buộc phải nói | Ca chính |
|---|---|---|---|
| p02 Lấy tư liệu từ website | Ảnh chụp website bị tách thành bảng tư liệu: Logo, bảng màu, phông chữ, ảnh sản phẩm bay ra rồi rơi thành hình ảnh trong phim | Nội dung và điểm bán hàng (ưu tiên nguyên văn, con số phải xác nhận); phối màu phông chữ Logo (tính ra được); ảnh sản phẩm, video của website, thiếu gì thì hỏi | Renoise, BeeGer (Logo trong suốt đặt lên nền trắng), 造物矩阵 (Logo vector làm hiệu ứng viết và đóng dấu), 大猫剪辑 (website không có ảnh chụp → phim minh hoạ chức năng), HiAPI (video chính thức + hook curl) |
| p03 Thẻ chọn kiểu | Bốn bánh xe quay, khoá thành một thẻ chọn kiểu | Bốn lớp (chế độ/tông/khung xương/tăng cường≤2); đề xuất theo tín hiệu; ghi chép phản hồi | Bốn phiên bản WorkBuddy (cùng một sản phẩm bốn thẻ chọn kiểu), BeeGer v1 vs bản nhịp nhanh, 小互 |
| p04 Phân cảnh và nhịp | Dạng sóng + điểm cắt: đoạn phim thật cắt cứng theo nhịp trống | Bảng phân cảnh bảy cột; tốc độ đọc (chữ Hán khoảng 7 chữ/giây + 0,5 giây); chọn nhạc khớp nhịp (lưới BPM, điểm năng lượng đạt tới, `--hit-at`) | 精酿 (đo thực tế 95 BPM), 小互 (atempo căn theo lưới), nhạc nền của chính bài này |
| p05 Lớp hiệu ứng chuyển động | Hạt tụ lại trên ảnh chụp sản phẩm thành khẩu hiệu rồi nổ tung | Tư liệu là ưu tiên; ba mức và bản đồ thủ pháp; chuyển cảnh và đầu cuối hô ứng, "chưa đủ ngầu" thì tăng thêm thế nào | WorkBuddy v4, YouWare v3, Renoise (chèn chữ vào video), WaytoAGI (vòng Logo 2D→3D→2D), 造物矩阵 v1→bản ngầu |
| p06 Ống kính và thiết bị | Ống kính xuyên qua một bức tường phim 3D | Bảng vận động ống kính của đạo diễn; quy tắc vận động ống kính (một chuyển động chính, CTA tĩnh ổn định, HitCam chỉ cho 3–5 keyframe, không rung cả đoạn); thiết bị 3D, một cú máy, 3D thuần code | DockLock (ba màn hình CSS-3D), WorkBuddy một cú máy, TOKEI, phim so sánh con ong, phim mẫu của bài dàn dựng |
| p07 Âm thanh | Track âm thanh của một video tách thành ba lớp nhạc nền/hiệu ứng/lời dẫn lần lượt sáng lên | Thư viện nhạc và uỷ quyền (Mixkit được làm/không được làm); hiệu ứng âm thanh rơi vào khung hình tiếp xúc, hai chỗ to nhất; lời dẫn nhường chỗ và mastering | ListenHub (giọng chính thức điều khiển sóng âm), WorkBuddy một cú máy (lời dẫn clone), 小互 (đổi nhạc nền), ghi âm tiếng gõ phím thật của phim mẫu bài dàn dựng |
