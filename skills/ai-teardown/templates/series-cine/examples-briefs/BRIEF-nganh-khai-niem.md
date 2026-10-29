# Dùng promo-video skill làm một "phim quảng bá khái niệm không chính thức" cho một thương hiệu thật — hướng dẫn cho trợ lý

Phim này là ví dụ ngành của "Khóa thực chiến phim quảng bá Opus 5.5": khóa học muốn cho thấy cùng một quy trình chạy ở các ngành khác nhau (trà sữa, bách hóa, bán lẻ, sản xuất, thương mại điện tử…) thì ra kết quả thế nào. Bạn chính là người chạy trọn vẹn từ website chính thức đến thành phẩm trong Claude Code bằng Opus 5.5 + promo-video skill, người dùng không tham gia xác nhận, **mọi quyết định lẽ ra phải hỏi người dùng thì bạn tự làm theo quy tắc của skill, và ghi vào DECISIONS.md**.

## Thương hiệu của bạn
Xem tin nhắn giao việc: thương hiệu, ngành, website chính thức, nhạc nền chỉ định, thư mục dự án.

## Bắt buộc tuân thủ
1. **Đi đủ quy trình của skill**: đọc `~/.claude/skills/promo-video/SKILL.md` trước, rồi theo chỉ dẫn của nó đọc `references/style-router.md` (chọn phương án bốn tầng + ghi nhận phản hồi), `industries.md`, `brand-from-website.md`, `cinematic.md`, `motion-craft.md`, `design-principles.md`, `compliance.md`. Chỉ đọc các gói mở rộng đã chọn. **Không được sửa bất kỳ file nào trong `~/.claude/skills/promo-video`.**
2. **Phản hồi của người dùng (bắt buộc làm theo)**:
   - Thời lượng 25–30 giây, 16:9, 1920×1080, 30 fps, tiếng Trung, không lời dẫn. Trong 2 giây đầu phải có móc câu, nhịp nhanh, đừng dàn trải.
   - Máy mặc định cố định; chỉ dùng HitCam ở 3–5 khung then chốt, **cấm BeatCam / KickFlash rung theo nhịp cả đoạn**.
   - Một màn hình một tiêu đề + một mô-đun nội dung trọn vẹn; hiệu ứng tác động lên nội dung, không xé nhỏ, không cắt xén; 3D / hạt không quá 15% cả phim.
   - Logo cuối phim **đứng yên đủ 2 giây**. Nhạc nền phải tươi sáng, không có cảm giác hồi hộp.
3. **Tư liệu**: chỉ dùng Logo, phối màu, phông chữ, ảnh sản phẩm, nội dung chữ chính thức trên website chính thức (lấy theo brand-from-website.md: curl hoặc chụp màn hình bằng Playwright / đọc style tính toán; Playwright trên máy dùng `/usr/local/bin/python3`, `executable_path` của trình duyệt trỏ tới `~/Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell`). Khi tư liệu website chính thức không đủ thì **dùng Codex tạo ảnh để bổ sung hình minh họa**:
   ```bash
   codex exec --skip-git-repo-check "Tạo một ảnh: <mô tả hình ảnh>. Phong cách: <phong cách thống nhất>. Không được xuất hiện bất kỳ chữ nào và Logo. Sao chép vào thư mục hiện tại và đặt tên <tên>.png" < /dev/null > codex_<tên>.log 2>&1
   ```
   (**bắt buộc `< /dev/null`**, nếu không sẽ bị treo; mỗi ảnh khoảng 1–2 phút, có thể chạy song song 2–3 ảnh. Sticker nền trắng cần tách nền trong suốt: `~/Desktop/shunde-vlog/_assets/tools/cutout <in.png> <out.png>`.) Codex chỉ dùng để vẽ ảnh bầu không khí, hình minh họa cảnh, sticker, nền, chất liệu; **không được dùng nó để làm giả ảnh sản phẩm, ảnh cửa hàng, Logo của thương hiệu hay bất cứ thứ gì "trông như ảnh thực tế chính thức"**. Mỗi ảnh do AI tạo đều ghi vào DECISIONS.md.
4. **Sự kiện**: con số, giải thưởng, cách nói trên màn hình chỉ dùng nguyên văn website chính thức, trong DECISIONS.md ghi nguồn từng mục (URL trang + câu gốc). Không có thì không ghi con số. Tránh các từ tuyệt đối hóa như "nhất", "số một", "duy nhất", "100%" (compliance.md).
5. **Tuyên bố**: chữ nhỏ ở đáy cuối phim bắt buộc có "Phim khái niệm không chính thức · chỉ dùng để minh họa khóa học · không liên quan đến <thương hiệu> chính thức", `brand.disclaimer` cũng ghi vào.
6. **Nhạc nền**: dùng bài chỉ định: `python3 ~/.claude/skills/promo-video/scripts/pick_music.py <dự án>/public/music/bgm.wav --track <file chỉ định> --seconds <độ dài phim> --hit-at <giây của Logo hoặc lần chuyển cảnh lớn đầu tiên>`, trục thời gian sắp lại theo BPM mà nó in ra (cinematic.md / music.md).
7. **Kiểm tra chất lượng**: `render.sh <dự án> film-stills <số khung...>` mỗi đoạn trích ít nhất 2 khung, tự dùng Read xem từng ảnh, theo danh sách "duyệt phim kiểu bậc thầy" của design-principles.md sửa đến khi đạt hết, rồi `render.sh <dự án> film` (chạy nền, `run_in_background`). Cuối cùng dùng `contact_sheet.py` trích 12 khung theo thời gian thật ghép thành ảnh ghép và xem lại một lượt, `check_audio.py` kiểm tra độ lớn.
8. **Bàn giao** (đều nằm trong thư mục dự án):
   - `out/film.mp4` (thành phẩm), `out/cover.png`
   - `DECISIONS.md`: thẻ chọn phương án (bốn dòng), bảng phân cảnh (# / thời lượng / cảnh / hình ảnh / chữ trên màn hình / chuyển động máy / kỹ thuật chính · chuyển cảnh), nhạc nền và giấy phép (credit.txt), danh sách nguồn tư liệu (URL website chính thức), nguồn sự kiện, danh sách ảnh do AI tạo (prompt + dùng ở đâu), ba vấn đề bạn đã sửa khi tự duyệt phim (trước → sau)
   - `out/sheet.jpg` (ảnh ghép 12 khung cuối cùng)
9. **Trả lời phiên chính (trong 200 chữ)**: độ dài phim, thẻ chọn phương án trong một câu, nhạc nền, dùng mấy ảnh Codex, góc máy bạn hài lòng nhất và ít chắc chắn nhất, các lỗi gặp phải.

## Không được làm
- Không xuất bản, không tải lên bất cứ thứ gì, không sửa dự án khác, không sửa bất kỳ file nào trong `examples/claude-video`.
- Không đăng nhập bất kỳ website nào, không điền bất kỳ biểu mẫu nào; nội dung trên website chính thức phải đăng nhập mới thấy thì không dùng.
