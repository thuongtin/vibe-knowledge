# 10 · Engine dựng phim bằng code (cine)

Bài giảng phong cách "bom tấn": mỗi khung hình đều do code tính theo thời gian thực (Three.js, GLSL, 260 nghìn hạt, chữ lớn động bằng DOM, chuyển động máy quay), một bài học chính là một hàm `seek(t)`, cùng một t render hai lần chênh lệch 0 pixel. Đã kiểm chứng: "Claude Code làm video: khóa điều phối Opus 5.5" gồm bài dẫn nhập + 10 bài, "Khóa thực chiến phim quảng bá Opus 5.5" gồm bài dẫn nhập + 8 bài + bài bonus.

Khi nào dùng: các bài về điều phối AI, hiệu ứng động, làm video, tức loại bài mà "bản thân bộ phim chính là tác phẩm", hoặc bài thực chiến cần chèn đoạn phim thành phẩm thật, phiên làm việc thật. Giảng sách, giảng thao tác phần mềm thì phong cách sketch phù hợp hơn; lịch sử nhân vật, quay màn hình terminal dùng phong cách lesson.

## Thư mục

```
<không-gian-làm-việc>/examples/<series>/
  cine/                 bản sao engine (new_series.py --style cine sao chép sang)
    index.html          ?lesson=<số-bài> mở một bài; &capture là chế độ quay
    engine/             core.js (trục thời gian, điều phối cảnh quay, giao diện __film) narr.js (thời gian lời dẫn, phụ đề) ui.js (thành phần) util.js (easing, lò xo, el/css) post.js glsl.js
    engine/scenes/      particles clock bars showroom liquid tunnel
    tools/              clips stills record finish retail loopbed queue.sh deliver.sh browser.py
    audio/tools/        bed.py (tổng hợp nhạc nền + hiệu ứng âm thanh, hiệu chỉnh âm lượng theo level từng đoạn) score.py (thư viện tổng hợp và DSP)
    audio/sfx/          bản ghi âm gõ phím thật CC0 (hiệu ứng key)
    fonts/ vendor/      Geist, Noto Sans SC; three.js
    queue.txt           hàng đợi render: số-bài|tiêu đề|giây-làm-ảnh-bìa
    deliver.env         nơi giao: D=thư mục Desktop, WEB=thư mục trang khóa học, STRIP=tiền tố số bài bị bỏ khỏi tên file
  lessons/<số-bài>/        narration.json  film.js  assets/  scenes/ (cảnh dành riêng cho bài này)  build/ (sản phẩm lồng tiếng, quay, trộn âm)  stills/
  tools/                check_timings.py  update_series.py
  session/              bản ghi phiên làm việc thật (dùng cho bài thực chiến, xem 11-practice-course.md)
  publish/course/       trang khóa học (lesson<số-bài>.mp4/.jpg + index.html)
```

## Môi trường

- `CINE_PY`: một Python đã cài `numpy scipy pillow playwright` (finish.py cần scipy). Nếu chưa có thì `python3 -m venv ~/.venvs/cine && ~/.venvs/cine/bin/pip install numpy scipy pillow playwright`, rồi `~/.venvs/cine/bin/python -m playwright install chromium-headless-shell`.
- Trình duyệt headless bắt buộc chạy bằng GPU: `--use-angle=metal --enable-gpu --ignore-gpu-blocklist`(`tools/browser.py` đã kèm sẵn; SwiftShader mặc định chậm gấp 30 lần). Đường dẫn trình duyệt theo thứ tự: `CINE_CHROME` → chromium_headless_shell mới nhất trong cache của Playwright → mặc định của Playwright.
- Trang phải mở qua HTTP (ES module không dùng được file://): `python3 -m http.server 8964 --bind 127.0.0.1 --directory <thư-mục-series>`; `queue.sh` thấy chưa có dịch vụ sẽ tự khởi động một cái.
- Lồng tiếng giống sketch: `scripts/make_lesson.py <bài> voice` + `scripts/speed.py <bài> 1.15` (Google Gemini TTS, giọng mặc định Sulafat; khóa API chỉ đặt trong biến môi trường `GOOGLE_API_KEY` hoặc `~/.config/ai-teardown/gemini.env`).
- Nhạc nền từ thư viện cần cài skill promo-video (`pick_music.py`); không dùng thư viện thì tổng hợp bằng bed.py.
- ffmpeg, ffprobe.

## Hợp đồng của film.js

```js
import { clamp, lerp, eOutCubic, spring, el, css } from "../../cine/engine/util.js";
import { C, appear, slam, typeText, codeCard, sourceTag, pauseCard, recapMap, clipBox } from "../../cine/engine/ui.js";
import { Particles, F } from "../../cine/engine/scenes/particles.js";

export const COLD = 6.4;                         // độ dài đoạn mở đầu bom tấn: toàn bộ lời dẫn lùi ra sau chừng này giây
export const meta = { title: "Video chính là một hàm", n: 1 };
export let hits = [], blur = [], clips = [], music = [];
export const sfx = [], sections = [];

export async function build(ctx) {
  const T = (s) => ctx.narr.t(s);                // "B07" "B07.ring" "B03@ba nghìn" "B07.end" "B05+1.2"
  return [{ from: 0, to: COLD, build(root) { … }, render(t, u) { … } }, …];
}
```

- Cảnh quay `{ from, to, build(root), render(t, u) }`: build chỉ dựng DOM / cảnh một lần, render mỗi khung hình đặt trạng thái theo thời gian tuyệt đối t và tiến độ trong cảnh u, **không được phụ thuộc khung hình trước** (khi quay sẽ seek nhảy cóc).
- `hits`: cú sốc máy quay (tăng phơi sáng + chớp trắng cực ngắn + dịch chuyển), cả phim ≤3 cái; khi có đoạn clip trong khung hình thì không dùng.
- `blur`: đoạn giây `[bắt đầu, kết thúc]`, khi quay lấy trung bình 4 khung con để tạo mờ chuyển động (màn trập 180°).
- `sfx`: `{ t, type, … }`, các loại slam whoosh whoosh-through riser(t_to) impact blip click tick shutter snap chime error card(note_index) rewind key(enter).
- `sections`: các đoạn nhạc nền tổng hợp `{ t, t_to, level }`, level 0 im lặng, 1 trải nền, 2 nhịp nhẹ, 3 đầy đủ. Khi dùng toàn bộ nhạc thư viện thì viết một đoạn level 0.
- `clips`: đoạn phim thật `{ id, src, from, at, dur, x, y, w, h, audio: mute|duck|full, gain, fade, poster_at, seg }`; clips.py cắt sẵn, finish.py dùng ffmpeg chồng lên khung.
- `music`: nhạc nền thư viện `{ src, from, at, dur, gain | gain_curve: [[t, dB]…], fade_in, fade_out }`; đoạn có lời dẫn tự động hạ thấp thêm.
- Thành phần (ui.js): appear slam wipeUp typeText bigText kicker codeCard (`hl(i, on)`) promptChip quoteCard sourceTag pauseCard recapMap clipBox; bảng màu `C`.
- Cảnh: Particles (đội hình DUST/LINE/CLOUD/TITLE/CN/POINT, `setText` đổi chữ), Clock, Bars, Showroom (khi khởi tạo truyền `ctx.r`), Liquid, Tunnel. Tham số xem chú thích cuối mỗi file.

## Quy trình

```bash
cd <không-gian-làm-việc>; S=examples/<series>; L=$S/lessons/<số-bài>
python3 scripts/make_lesson.py $L voice > $L/voice.log 2>&1 && python3 scripts/speed.py $L 1.15
cd $S
python3 tools/check_timings.py <số-bài>                         # kiểm tra căn từng chữ có bị đứt không
$CINE_PY cine/tools/clips.py <số-bài>                            # khi có đoạn clip
$CINE_PY cine/tools/stills.py <số-bài> lessons/<số-bài>/stills/sheet.png 1.0 B01+1 B02.a+1 …   # bảng contact sheet, xem từng ảnh
echo "<số-bài>|<tiêu đề>|<giây-làm-ảnh-bìa>" >> cine/queue.txt; CINE_PY=$CINE_PY cine/tools/queue.sh    # clips → record → finish → deliver, chạy tuần tự
python3 tools/update_series.py && python3 ../../scripts/course_page.py series.json publish/course
```

- record.py: 1920×1080 60fps seek từng khung + chụp màn hình, truyền qua pipe cho ffmpeg (CRF 18) → `build/picture.mp4`. Bài có hạt đầy màn hình mất khoảng 1,5–2 lần thời gian thực.
- finish.py: đọc `__film` → `lesson.json` → bed.py tổng hợp nhạc nền và hiệu ứng âm thanh → lời dẫn nén nhạc nền xuống → chồng đoạn clip và nhạc thư viện → giới hạn đỉnh (chừa 1,5 dB, sau AAC không vượt 0) → `build/lesson<số-bài>.mp4`.
- retail.py `<số-bài> B18`: chỉ render lại phần hình từ một nhịp trở đi rồi nối vào picture.mp4 (dùng khi sửa vài nhịp cuối).
- deliver.sh: bản chia sẻ 1080p60 cho Desktop (CRF 23, bitrate tối đa 6M) + bản web 720p30 cho trang khóa học (giảm nhiễu, tối đa 520k, khoảng 2 MB/phút, mỗi file phải <15 MB) + ảnh bìa.
- Đa tác tử: mỗi trợ lý theo `BRIEF.md` trong thư mục series làm lời dẫn + lồng tiếng + film.js + bảng contact sheet cho một bài, không render, không sửa engine; phiên chính đối chiếu trích dẫn và con số, xếp hàng render, lấy khung và kiểm tra âm lượng, phát hành.

## Kiểm tra chất lượng

- Bảng contact sheet mỗi cảnh quay ít nhất 1 khung, **cũng phải xem các khung giữa chừng của hoạt ảnh** (khung tĩnh sẽ bỏ sót bóng mờ, vết tồn lưu).
- Lấy 6–12 khung của thành phẩm ghép lại để xem; `ffmpeg -nostats -i lesson.mp4 -vn -af ebur128=peak=true -f null -` để xem âm lượng: các bài đã giao nhìn chung khoảng −14,5 LUFS, đỉnh thực khoảng −0,9 dBFS, lệch nhiều thì kiểm tra lại khâu trộn âm.
- Đối chiếu từng trích dẫn và tên tác giả với nguồn gốc (trợ lý hay gán nhầm); mỗi con số trên màn hình đều phải truy được nguồn.

## Cạm bẫy

- `[[cue]]` chỉ dùng chữ thường, chữ số, dấu gạch dưới; không được đặt tên `end` (`B06.end` là cách viết dành riêng); cue viết hoa sẽ không được phân tích.
- Tên tiếng Anh trong lời dẫn đừng có dấu gạch nối ("promo-video" sẽ làm căn từng chữ đứt tại đó, các chữ phía sau bị dồn về cuối nhịp), hãy viết "promo video"; sau khi lồng tiếng chạy `check_timings.py`.
- `appear()` không được đổi display (sẽ phá căn giữa flex), dùng visibility; phụ đề đừng ngắt câu ở dấu thập phân của "5.5"; trong JS `41.0` chuyển thành chuỗi là `"41"`, ghép tên file phải dùng chuỗi.
- Đoạn clip luôn nằm trên cùng, không rung theo hits; không chữ hay mũi tên nào được đè lên khung clip; khung không được vào vùng y>920 (vùng phụ đề); w, h dùng số chẵn; điểm bắt đầu clip đừng rơi vào đoạn chuyển cảnh mờ của phim nguồn.
- Hạt: tần số nhiễu curl quá thấp thì cả đám sẽ trôi thành vòng kỳ quái; kích thước hạt đừng dùng chung số ngẫu nhiên với góc phương vị (gây khuyết hình quạt); chớp trắng đè lên hình tối sẽ bị xám, cú sốc dùng tăng phơi sáng + chớp trắng cực ngắn.
- 60fps + hạt/nhiễu hạt làm bitrate rất cao: khi giao hãy giới hạn bitrate tối đa, bản master đừng dùng CRF 16.
- Khi bảng trình duyệt trong ứng dụng bị thu gọn thì `document.hidden`, rAF không chạy, ảnh chụp bị đen: việc kiểm chứng luôn dùng công cụ quay headless.
- Bài nhạc thư viện ngắn hơn cả bài học: `loopbed.py` nối dài theo ô nhịp (lặp từ 8 ô nhịp sau điểm vào đến ô nhịp nguyên cuối cùng trước khi tắt dần, 1 ô nhịp crossfade công suất đều).
