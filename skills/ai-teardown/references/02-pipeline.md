# 02 · Quy trình và phát hành

## Cấu trúc thư mục

```
<không gian làm việc>/
  scripts/ runtime/ primitives/ schemas/ assets/     ← engine (engine/ của skill này)
  examples/<series>/
    series.json            dàn ý + dữ liệu trang khoá học
    BRIEF.md SCENES_GUIDE.md DECISIONS.md
    assets/img/            sổ ảnh images.json (ghi có khoá: scripts/ledger.py) + ảnh chụp màn hình, emoji, khung hình người nhỏ, khung hình quay màn hình
    source/                sách gốc / bản clone repo (nếu có)
    render.queue           hàng đợi render (mỗi dòng một số bài, END để kết thúc)
    publish/course/        trang khoá học index.html + video nén 720p + ảnh bìa
    publish/lessonNN/      bản tương tác (index.html, app.js, audio.mp3, img/)
    lessons/NN/
      narration.json scenes.json voice.log
      illus/ lottie/ data/  minh hoạ của bài này, hoạt hình Noto, chuỗi khung hình quay màn hình
      build/               audio/, timings.json, film.js, stills/scenes.png (contact sheet)
      hf/renders/lessonNN.mp4   thành phẩm 1080p
```

## Môi trường (một lần)

| Phụ thuộc | Vị trí / cách làm |
|---|---|
| Khoá Google Gemini TTS | biến môi trường `GOOGLE_API_KEY` (hoặc `GEMINI_API_KEY`), hoặc `~/.config/ai-teardown/gemini.env` (quyền 600, dòng `GOOGLE_API_KEY=...`). **Tuyệt đối không ghi vào dự án, trang web hoặc bộ nhớ** |
| Khoá OpenAI (căn chỉnh + đọc lại) | biến môi trường `OPENAI_API_KEY`, hoặc `~/.config/ai-teardown/openai.env` (quyền 600, dòng `OPENAI_API_KEY=...`). Dùng `POST /v1/audio/transcriptions`, model `whisper-1` (model duy nhất của OpenAI trả timestamp từng từ; OpenAI báo tắt ngày 26/02/2027). **Mỗi lần lồng tiếng tốn thêm phí OpenAI** (1–2 lần gọi mỗi nhịp, tính theo thời lượng âm thanh; kết quả được cache ở `build/audio/<nhịp>.asr.json`). Không còn cần whisper-cli hay mô hình ggml trên máy |
| Trình duyệt headless Playwright | `~/Library/Caches/ms-playwright/chromium_headless_shell-1243/…`(đầu `scripts/stills.py`, `export_cues.py`) |
| Hyperframes | `npx hyperframes@0.6.x` cài một lần, trong make_lesson `NPX` trỏ tới `~/.npm/_npx/<hash>/node_modules` (đổi máy phải sửa) |
| esbuild | `.bin/esbuild` trong cùng thư mục NPX |
| Nhạc nền | `~/.claude/skills/promo-video/assets/music`(nhạc mixkit miễn phí bản quyền, `BGM` của `make_lesson.py`, `LIB` của `mix.py`) |
| ffmpeg | cài bằng brew, không có drawtext cũng được |

Khi đổi máy, sửa các hằng số ở đầu `scripts/make_lesson.py`, `tts_gemini.py`, `stills.py`, `export_cues.py`, `mix.py` theo bảng trên.

## Ba giai đoạn của make_lesson

```bash
python3 scripts/make_lesson.py <thư mục bài> voice   # tổng hợp theo nhịp (song song 2–3 luồng, cache theo văn bản) → OpenAI whisper-1 lấy thời gian từng từ, căn từng chữ → dùng chính bản phiên âm đó chấm điểm đọc lại
python3 scripts/make_lesson.py <thư mục bài> build   # đổi tốc độ (scenes.speed, mặc định 1.15) → biên dịch scenes.json → esbuild đóng gói → preview.html → contact sheet
python3 scripts/make_lesson.py <thư mục bài> final   # trộn âm (nhạc nền -24dB) → render Hyperframes 1080p → bản nén 720p đưa vào trang khoá học → thư mục bản tương tác → cập nhật series.json và trang khoá học
```

- `scenes.json` ghi `"engine":"sketch"` thì tự động dùng `runtime/sketch.js`, nếu không thì dùng `runtime/lesson.js`.
- **final không chạy lại build**: sau khi sửa runtime/primitives, với các bài đã xếp hàng nhưng chưa render phải build thủ công.
- Render khoảng 12–15 phút/bài, chạy tuần tự là nhanh nhất (Hyperframes nhiều worker lại chậm; mở thêm tác vụ trình duyệt khác cùng lúc sẽ tụt xuống 5–8 fps).

## Hàng đợi render

```bash
nohup zsh scripts/render_queue.sh examples/<series> > <log> 2>&1 &   # chạy thường trực, khi hàng đợi trống thì cứ 20 giây xem một lần
echo 07 >> examples/<series>/render.queue
```
Trong log, mỗi dòng "bài N hoàn tất / thất bại" một dòng; dùng Monitor theo dõi log (grep hoàn tất|thất bại|Error|Traceback), hết hạn 30 phút phải gia hạn. Muốn dừng giữa chừng một bài: giết tiến trình con make_lesson của runner, runner sẽ ghi thất bại và tiếp tục bài kế, sau đó thêm lại số bài vào hàng đợi.

## Phát hành

- **Bản tương tác**: `python3 scripts/sketch_publish_files.py <thư mục bài>` in ra ánh xạ files (chỉ gồm ảnh dùng trong bài này + 80 khung hình người nhỏ). Artifact publish: `file_path=publish/lessonNN/index.html`, `root=` thư mục đó, files dùng dạng danh sách `[{"path": "app.js"}, …]` (khi >200 tệp thì dạng danh sách tiện nhất). Giới hạn 255 tệp, mỗi phiên bản 64MB.
- **Trang tổng khoá học**: `scripts/course_page.py series.json publish/course`; tổng dung lượng video thường vượt 64MB → cùng một file_path phát hành làm nhiều lần, mỗi lần chỉ kèm một lô video (tệp không kèm sẽ được giữ lại).
- Sau khi phát hành, gửi MP4 cho người dùng bằng SendUserFile; Artifact là liên kết riêng tư, muốn cho người khác xem phải bật trong Share của trang. Khi người dùng nói "không mở được", ưu tiên đưa đường dẫn thư mục cục bộ + liên kết https đầy đủ.
- **Tổng hợp cục bộ**: toàn bộ thành phẩm đặt tên theo "<số bài>_<tiêu đề>.mp4" rồi `cp -c` (clone APFS, không tốn dung lượng) vào một thư mục trên desktop, bài dẫn nhập dùng tiền tố `000_` để xếp đầu tiên.
- Thẻ của mỗi bài trên trang khoá học tự động kèm: lời dẫn, giới thiệu, điểm chính, thời lượng, video, liên kết "Bản tương tác" (`interactive` trong series.json).

## Ghi chép tiến độ

Mỗi khi phát hành một bài thì ghi lại liên kết bản tương tác (trong bộ nhớ hoặc README dự án), khi hoàn tất tất cả thì đưa cho người dùng một bảng tổng "số bài → liên kết".
