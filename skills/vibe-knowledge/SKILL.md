---
name: vibe-knowledge
description: Vibe Knowledge Showcase, xưởng phim ngắn tri thức cao cấp, một điểm kiến thức → một video 45 giây đến 5 phút, có lời dẫn, mỗi câu có nguồn (Douyin #Vibe知识大赏 / mục tri thức). Từ 15 video viral được phân tích ngược ra 6 khuôn kịch bản (phim khái niệm đoán đố, phim lựa chọn lưỡng nan, phim nỗi đau + nguyên lý, phim một mạch chính, phim vượt ải, phim sáu mặt xoay vòng) → danh sách sự kiện có nguồn → bản lời dẫn + phản biện đối kháng → lồng tiếng bằng Google Gemini TTS (giọng có sẵn, mặc định Sulafat) → hai bậc hình ảnh: bậc cơ bản 0 điểm (Opus vẽ tay minh họa SVG nhiều lớp, hạt, thành phần dữ liệu, BGM mặc định cắt theo độ dài phim) / bậc nâng cao chọn theo từng cảnh dùng Renoise (ảnh Midjourney/GPT Image, cảnh quay động Wan 3.0/Seedance 2.5, hiệu ứng âm thanh ElevenLabs, báo giá trước rồi mới tạo) → dựng phim bằng code cine (zoom ảnh, video từng khung, từ khoá, bộ đếm, bản đồ lan tỏa, vệt sáng, cổ văn dọc, chú thích nguồn, nút lưỡng nan) → render từng khung 1080p60 → kiểm tra bằng OCR đọc lại → gói đăng bài (tiêu đề, chủ đề, ảnh bìa, mô tả). Kích hoạt khi làm một kỳ Vibe Knowledge Showcase / Vibe知识大赏 / video khoa học tri thức ngắn / biến khái niệm này thành video tri thức / giống Electronic Homo Sapiens, Iwanau, 墨有意思 / kiểu "nếu bạn sống ở thời cổ đại" / giải thích rõ một nguyên lý trong một hơi. Không dùng cho series bài học (ai-teardown), bình luận tài chính (finance-explainer), phim quảng bá thương hiệu (promo-video), người ảo xuất hiện dẫn chuyện (digital-human-koubo).
---

# Vibe Knowledge Showcase · Xưởng phim ngắn tri thức cao cấp

Một kỳ = một điểm kiến thức → một video ngắn cao cấp có lời dẫn (mặc định 16:9 1080p60). **Độ dài do người dùng quyết định**: trước tiên đề xuất bốn bậc theo độ phức tạp (lướt nhanh / giảng sâu / tiêu chuẩn / đào sâu), mỗi bậc ghi rõ nói chi tiết đến đâu, phải cắt gì (references/13-duration.md).
Engine tái sử dụng **cine** của ai-teardown (dựng phim bằng code `seek(t)` điều khiển theo lời dẫn), skill này thêm bốn thứ: **6 khuôn kịch bản** (cách kể), **thư viện phong cách** (diện mạo + cách kể, `styles/`, 44 bộ · 8 họ đã được kiểm chứng (mỗi họ ít nhất 3 bộ) + phong cách riêng của người dùng), **thư viện thành phần phim tri thức know.js**, **tầng nâng cao Renoise** (ảnh / video / nhạc / hiệu ứng âm thanh).

Một kỳ = **khuôn × phong cách × thủ pháp (≤2) × bậc**. Phong cách chia thành 8 họ: Phương Đông, Nền tối khái niệm, Sáng và đại chúng, In ấn và giấy, Minh hoạ và thiết kế, Dựng phim và phóng sự, Điện ảnh, Game; trong đó bích hoạ Đôn Hoàng, men xanh trắng, khắc gỗ, cắt dán bán sắc, trường quyển, đồng bản bảo tàng là phong cách bậc nâng cao (mỗi đoạn khoảng 2 ảnh tạo sinh). Phong cách có thể dùng của thư viện, sửa thành của riêng mình, hoặc làm từ đầu (references/09-style-studio.md).

**Hai bậc sản xuất** (references/08-tiers.md):
- **Bậc cơ bản · 0 điểm**: Opus vẽ tay minh hoạ SVG nhiều lớp + hạt / 3D + thành phần dữ liệu, lồng tiếng Google Gemini TTS (cần khóa API Google của người dùng, mức phí/hạn mức theo bảng giá của Google), **BGM mặc định** (xem bên dưới), **hiệu ứng âm thanh bằng code earshot** (references/10-earshot.md, dùng chung cho hai bậc).
- **Bậc nâng cao · chọn theo cảnh**: chỉ giao cho Renoise những cảnh mà code làm không tốt (cảnh thực tế, 1–3 khoảnh khắc cần được nhớ nhất, chuyển động thật), phần còn lại vẫn dùng code. Nhẹ ≈25–40 / tiêu chuẩn ≈250–300 / chủ lực ≈600–700 điểm, mỗi lần báo giá trước rồi mới tạo.
- Cùng một film.js dùng chung cho hai bậc (công tắc `ENH`: plate/vclip ↔ layers).

## BGM (bắt buộc, từ 2026-10-28, dùng chung cho hai bậc)

**Mỗi video đều phải có bài BGM này, âm lượng thống nhất** (người dùng quy định). **Ngoại lệ duy nhất: người dùng nói rõ trong hội thoại yêu cầu đổi bài**: bản nhạc đó ghi `bgm: true, user_request: "nguyên văn người dùng"`, nó sẽ đóng vai BGM, vibe-bgm nhường chỗ, âm lượng vẫn hiệu chỉnh như cũ; không ghi nguyên văn thì không công nhận. Việc bắt buộc được thực hiện ở khâu trộn âm: finish.py gắn hook `bgm_force.py`: film.js không đặt BGM thì tự động bổ sung theo độ dài phim; các bản nhạc nền nguyên đoạn ≥20 giây khác (Lyria, kho nhạc) đều bị vô hiệu; âm lượng BGM không theo gain ghi trong film.js, thống nhất hiệu chỉnh thành "khi có tiếng nói thấp hơn giọng người 10 dB" (người dùng yêu cầu âm lượng cao hơn một chút; ở chỗ ngắt nghỉ tự động nâng lên khoảng 2–4 dB), gain_curve chỉ giữ hình dạng lên xuống. qa.py sẽ kiểm tra trong phim thành phẩm có bài BGM này không, không có thì báo ⚠⚠, không được giao.

Tất cả Vibe Knowledge Showcase mặc định dùng cùng một bài BGM: `assets/music/vibe-bgm.m4a` (người dùng chỉ định, 112.9 BPM, 160 giây, lưới nhịp ở file .json cùng tên). Sau khi chốt lồng tiếng, một lệnh cắt theo độ dài phim, điểm cắt đều nằm trên vạch nhịp, phần đầu giữ nguyên bản gốc, phần cuối nối vào đoạn fade-out tự nhiên của bản gốc, phim dài hơn thì lặp theo 8 ô nhịp:

```bash
$CINE_PY ~/.claude/skills/vibe-knowledge/tools/fit_bgm.py $L/assets/audio/bgm.wav --lesson $L --tail 3   # tổng dài = lời dẫn + thẻ kết
# đồng thời xuất bgm.beats.json (số giây của từng nhịp / từng ô nhịp trong phim), film.js muốn khớp nhịp thì đọc file này
```

Trong film.js: `music.push({ src: P("audio/bgm.wav"), from: 0, at: 0, dur: END + TAIL, gain_curve: [[0, -11], [END, -11], [END + TAIL, -8]], fade_in: 0.3, fade_out: 1.8 })` (đoạn lời dẫn finish.py sẽ tự hạ thấp thêm).
Không tạo nhạc nền nguyên đoạn bằng Lyria nữa (có tạo cũng bị vô hiệu bắt buộc); Renoise chỉ dùng để làm hiệu ứng âm thanh ngắn.

## Lần dùng đầu và gợi ý phong cách (làm bước này trước)

- **Lần dùng đầu** (`~/.vibe-knowledge/welcomed` chưa tồn tại): chạy trước `python3 ~/.claude/skills/vibe-knowledge/tools/welcome.py`, tạo và mở "Bảng phong cách" cục bộ (`~/Desktop/vibe-knowledge/风格图鉴/index.html`: phim chớp phong cách, tuyển tập mẫu, thẻ phong cách nhóm theo họ, ba cách mở đầu, hai bậc, quy trình), sau đó giới thiệu trong hội thoại bằng 5–6 câu: khuôn × phong cách × bậc, mỗi trong 8 họ nêu một hai bộ, ba cách mở đầu, cuối cùng hỏi "muốn làm chủ đề nào trước?". Sau khi cập nhật thư viện phong cách thì tạo lại bằng `--force`.
- **Người dùng đưa chủ đề**: chạy trước `python3 ~/.claude/skills/vibe-knowledge/tools/recommend.py "<chủ đề>"`, nhận 3 bộ đề xuất rồi dùng AskUserQuestion hỏi (bộ đề xuất đầu xếp đầu và gắn "(đề xuất)", description ghi lý do và khuôn đi kèm; preview ghi một câu mô tả hình ảnh và đường dẫn ảnh phong cách), đồng thời dùng SendUserFile gửi 3 ảnh phong cách cho người dùng đối chiếu. Người dùng đã nêu tên phong cách thì bỏ qua bước đề xuất. Khi đề xuất phong cách bậc nâng cao, ghi rõ trong description của lựa chọn "cần tạo ảnh, khoảng 8 điểm/đoạn".
- Nguồn duy nhất của danh mục phong cách là `styles/catalog.json` (đề xuất, bảng phong cách, phim chớp đều đọc từ đây); thêm phong cách mới thì đồng bộ catalog.json, STYLE.md, still.jpg.

## Chủ trương cốt lõi (không được bỏ)

1. **Tiêu chuẩn cao cấp là ngưỡng cứng** (references/02-premium.md): bố cục ba lớp, không có hình tĩnh quá 3 giây, mỗi chương một cảnh "bom tấn" (bậc nâng cao: cảnh quay động Renoise / bậc cơ bản: hạt code, thị sai), âm thanh nhiều lớp, cả kỳ một hệ thống hình ảnh.
2. **Không có nguồn thì không lên màn hình**: số liệu, tên người, năm, trích dẫn đều đưa vào facts.md; hình minh hoạ phải ghi rõ; khi có bất đồng thì đặt hai thuyết song song.
3. **Lời dẫn kể chuyện, hình ảnh đưa từ khoá**: chữ trên hình ≤8 chữ mỗi nhóm, mỗi màn hình tối đa hai nhóm; nguyên câu giao cho lời dẫn và phụ đề tự động.
4. **Đoán trước rồi giảng, hoãn tiêu đề, một đạo cụ chính xuyên suốt, kết thúc bằng câu hỏi ngược** (quy tắc chung của các khuôn, references/01-templates.md).
6. **Quy tắc cứng khớp lời dẫn**: chưa đọc đến thì không xuất hiện, bộ đếm chốt ở lúc đọc đến, nhấn mạnh có ngân sách, tĩnh lâu nhất ≤3 giây (references/11-absorbed.md mục một).
5. **Làm được bằng code thì dùng code, tốn điểm thì phải xác nhận trước**: Renoise chỉ bổ sung những cảnh code làm không tốt; mọi việc tạo sinh đều liệt kê và báo giá trước, người dùng đồng ý rõ ràng trong hội thoại mới được gửi (references/04-renoise.md, 08-tiers.md). Lồng tiếng dùng Google Gemini TTS (khóa API của người dùng, phí/hạn mức theo Google).

## Không gian làm việc

```bash
python3 ~/.claude/skills/vibe-knowledge/tools/new_film.py <số kỳ> --template A --title "Định luật Benford"
#   không gian làm việc mặc định ~/Desktop/vibe-knowledge, series vk; lần đầu sẽ tự tạo series cine, cài know.js, vá công cụ ghi hình, đặt giọng lồng tiếng mặc định (Gemini Sulafat)
S=~/Desktop/vibe-knowledge/examples/vk; L=$S/lessons/<số kỳ>
```

Phụ thuộc: skill ai-teardown (engine cine, lồng tiếng make_lesson), `CINE_PY` (Python có numpy scipy pillow playwright; máy này là `/usr/local/bin/python3.12`, trước khi chạy phải xoá trống `PYTHONPATH=`, nếu không sẽ nạp PIL hỏng), khoá Google Gemini (`GOOGLE_API_KEY` hoặc `~/.config/ai-teardown/gemini.env`), Renoise MCP (chỉ bậc nâng cao cần; thiếu thì hướng dẫn theo mục "Kết nối Renoise" trong references/04-renoise.md, link đăng ký đưa nguyên văn https://renoise.ai/mcp?utm_medium=xcom&utm_source=official ), ffmpeg, swiftc (OCR).

## Quy trình (ba điểm xác nhận)

| Đoạn | Làm gì | Sản phẩm |
|---|---|---|
| ① Chọn chủ đề | Ba câu hỏi: có thể cho người xem đoán / chọn trước trong 3 giây không? Có đạo cụ xuyên suốt không? Có cú đảo ngược không? Đưa người dùng 3–5 ứng viên + khuôn đề xuất | Chủ đề |
| **Xác nhận 1** | Người dùng chọn chủ đề, khuôn, **độ dài** (trước tiên chạy `duration.py` đưa bốn bậc theo độ phức tạp, bậc đề xuất xếp đầu; bậc người dùng chọn lệch độ phức tạp từ hai mức trở lên thì phải nhắc), **phong cách** (của thư viện / của tôi / sửa một bộ / từ trống, xem 09-style-studio.md; mục đề xuất xếp đầu kèm ảnh phong cách), **làm bậc nào** (cơ bản / nâng cao nhẹ / tiêu chuẩn / chủ lực) | |
| ② Tra cứu | Danh sách sự kiện (phân cấp T1/T2/T3, trích nguyên văn, dùng ở nhịp nào) | `facts.md` |
| ③ Viết | Viết lời dẫn theo khung khuôn (giới hạn số chữ xem `_guide` của khung) → subagent phản biện đối kháng (móc câu, nguồn, số chữ) → sửa | `narration.json` |
| ④ Phân cảnh / danh sách tài nguyên | Phân cảnh hình ảnh từng nhịp (ghi rõ cảnh nào code làm, cảnh nào nâng cao); bậc nâng cao viết assets.json + báo giá estimate_cost; bậc cơ bản chọn nhạc | `assets.json` |
| **Xác nhận 2** | Người dùng xem bản lời dẫn + phân cảnh (+ danh sách cảnh nâng cao và báo giá), đồng ý rõ ràng mới tạo | |
| ⑤ Tạo | Bậc nâng cao: Renoise tạo ảnh + âm thanh trước → người dùng chọn ảnh → video (khung đầu dùng ảnh đã chọn) → tải về, đổi tên, clip2frames. Bậc cơ bản bỏ qua | `assets/` |
| ⑥ Lồng tiếng + nhạc | Trước tiên làm bản nghe thử mở đầu 15–20 giây để người dùng chốt giọng và tốc độ → `tts_gemini.py --gap 0.2` → `speed.py` → `check_timings.py` → `voice_post.py` (tùy chọn) → `fit_bgm.py` cắt BGM mặc định theo độ dài phim | `build/timings.json`, `assets/audio/bgm.wav` |
| ⑦ Dựng | film.js (thành phần know.js) → stills.py bảng contact xem từng ảnh (kể cả khung giữa chừng của hoạt ảnh) | `stills/` |
| ⑧ Render | queue.sh (record → finish → deliver) | Phim thành phẩm |
| ⑨ Kiểm tra | `qa.py` bảng contact + đối chiếu OCR đọc lại với facts.md + độ lớn âm; trong bảng contact cả đoạn hình không đổi = ghi hình gặp sự cố, ghi lại | `qa/` |
| **Xác nhận 3** | Người dùng xem phim thành phẩm; sửa xong thì xuất gói đăng bài, ảnh bìa dùng `cover_first.py` nối thành khung đầu | `post.txt`, ảnh bìa |

## Lệnh thường dùng

```bash
cd ~/Desktop/vibe-knowledge; S=examples/vk; L=$S/lessons/<số kỳ>
python3 scripts/tts_gemini.py $L/narration.json $L/build --gap 0.2 --lead 0.3 --qa --jobs 2 > $L/voice.log 2>&1   # lồng tiếng + căn từng chữ + đọc lại (giữa các nhịp chỉ chừa 0.2 giây, đừng dùng 0.8 mặc định của make_lesson)
python3 scripts/speed.py $L 1.1                                        # khi cần thì tăng tốc toàn bộ, mục tiêu 5.5–6 chữ/giây
(cd $S && python3 tools/check_timings.py <số kỳ>)                       # căn chỉnh có bị đứt không
python3 ~/.claude/skills/vibe-knowledge/tools/voice_post.py $L         # hậu kỳ giọng bằng ffmpeg (tùy chọn, ban đầu viết cho giọng nhân bản; với giọng Gemini không bắt buộc)
python3 ~/.claude/skills/vibe-knowledge/tools/clip2frames.py $L/assets/clips/v01.mp4 $L/assets/clips/v01   # tách khung video → in số khung
cd $S && $CINE_PY cine/tools/stills.py <số kỳ> lessons/<số kỳ>/stills/sheet.png 1 B01+1 B02.title B05.count+0.5 …
echo "<số kỳ>|<tên phim>|<giây ảnh bìa>" >> cine/queue.txt   # chỉ được thêm vào cuối! queue.txt dùng chung nhiều phiên
pgrep -f cine/tools/queue.sh || CINE_PY=$CINE_PY cine/tools/queue.sh   # hàng đợi đã chạy thì đừng khởi động cái thứ hai, nếu không hai luồng ghi hình sẽ ghi hỏng cùng một picture.mp4
python3 ~/.claude/skills/vibe-knowledge/tools/qa.py lessons/<số kỳ>/build/lesson<số kỳ>.mp4
python3 ~/.claude/skills/vibe-knowledge/tools/cover_first.py <phim thành phẩm.mp4> cover_16x9.jpg <bản giao.mp4>   # nối ảnh bìa thành khung đầu (0.5 giây), mỗi kỳ giao đều phải làm
```

Trong voice.log, nhịp đọc lại <95% thì xoá `build/audio/<nhịp>.*` rồi lồng lại; tên riêng dùng lexicon để ghi cách đọc.

## Các file tham khảo

| File | Nội dung |
|---|---|
| references/01-templates.md | 6 khuôn (bản có lời dẫn): mỗi nhịp làm gì, hình ảnh, tác phẩm đối chuẩn |
| references/02-premium.md | Tiêu chuẩn cao cấp: hình ảnh, âm thanh, nội dung, quy cách giao (trước khi giao rà từng mục) |
| references/03-visual-systems.md | 5 hệ thống hình ảnh + tiền tố phong cách vẽ Renoise + cắt dán theo thời đại |
| references/04-renoise.md | Tầng nâng cao Renoise: đơn giá, ngân sách, quy trình, cách viết prompt, an toàn |
| references/05-publish.md | Gói đăng bài: quy tắc tiêu đề hoạt động, chủ đề, ảnh bìa, mô tả, thư mục giao |
| references/06-benchmarks.md | Số liệu tác phẩm đối chuẩn và điểm chung |
| references/07-kit.md | API thành phần know.js |
| references/09-style-studio.md | Xưởng phong cách: bốn lối vào, mỗi lần một câu hỏi (đề xuất xếp đầu / bạn quyết / trò chuyện tự do), phép chia ba, tổng hợp → ảnh phong cách → demo → cố định vào ~/vibe-knowledge-styles/ |
| styles/INDEX.md | Danh mục thư viện phong cách: 44 bộ chia theo 8 họ (mỗi bộ STYLE.md + still.jpg, mã nguồn mẫu ở styles/_samples/) |
| references/13-duration.md | Độ dài và độ tỉ mỉ khi phân tích: chấm điểm năm mục phức tạp, bốn bậc độ dài (số chữ / số nhịp / độ tỉ mỉ / nói được đến đâu / phải cắt gì), quy tắc đề xuất, nhắc khi không khớp, thời gian dừng của ảnh bìa |
| references/14-pitfalls.md | Danh sách bẫy khi sản xuất (theo khâu): hàng đợi render dùng chung, ảnh khí vật AI sai cấu trúc, căn lồng tiếng bị đứt, tải Wan thất bại, CSS xoá màu nền, đỉnh AAC… |
| references/12-style-families.md | Họ phong cách và lộ trình mở rộng: vì sao 7 bộ trông mỏng, hai trục phong cách × thủ pháp, bảng chọn lọc 87 phong cách UI, mượn gì từ promo-video, bẫy phong cách bậc nâng cao (MJ vẽ thành khí vật, từ niên đại làm lệch trang phục, ESRGAN chia khối lệch, canvas chờ giải mã, bóng đổ Vision) |
| references/10-earshot.md | Hiệu ứng âm thanh code earshot (252 cái, MIT, 0 điểm): cài đặt, cách viết film.js, bảng đối chiếu vai trò phim tri thức → hiệu ứng, thời điểm căn chỉnh |
| references/11-absorbed.md | Hấp tinh đại pháp: quy tắc khớp lời dẫn của 14 dự án mã nguồn mở cùng loại, 9 kiểu ngữ pháp thuyết minh, mẹo cấu trúc và đăng bài, quy trình kiểm tra, 12 phong cách ứng viên mới, cách làm cắt dán giấy Vox, ranh giới giấy phép |
| references/08-tiers.md | Hai bậc sản xuất: bậc cơ bản 0 điểm làm sao đạt cao cấp, bậc nâng cao chọn cảnh thế nào, ngân sách, cách viết dùng chung hai bậc |
| templates/narration/A–F.json | Khung lời dẫn của 6 khuôn (giới hạn số chữ mỗi nhịp, [[cue]]) |
| templates/film.skeleton.js | Khung film.js (nhạc, hiệu ứng âm thanh, mở đầu lạnh, cách viết thẻ kết) |
| templates/facts.md / assets.json | Mẫu danh sách sự kiện, danh sách tài nguyên Renoise |
| tools/ | new_film.py, clip2frames.py, voice_post.py, qa.py (+ ocr.swift), recommend.py (đề xuất phong cách theo chủ đề), welcome.py (giới thiệu bảng phong cách lần đầu), style_reel.py (trục thời gian + lời dẫn của tuyển tập mẫu phong cách mới), vision_layers.swift (tách ảnh tạo sinh thành lớp chủ thể / lớp nền), earshot_render.py / patch_earshot.py (hiệu ứng âm thanh code), fit_bgm.py (cắt / lặp BGM mặc định theo ô nhịp và độ dài phim + bảng nhịp), cover_first.py (nối ảnh bìa thành khung đầu), duration.py (đưa đề xuất độ dài theo độ phức tạp); qa.py hiện sẽ báo hình tĩnh >3 giây |

Hợp đồng của chính engine cine, thành phần, hàng đợi render, các bẫy: `~/.claude/skills/ai-teardown/references/10-cine.md` (trước khi sửa engine phải đọc).
