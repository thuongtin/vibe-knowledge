# 04 · Lớp nâng cao Renoise: ảnh, video, nhạc nền, hiệu ứng âm thanh

Mọi việc tạo nội dung đều đi qua Renoise MCP (tên công cụ `mcp__…__estimate_cost / create_tasks / wait_tasks / download_results`).
**Quy tắc cứng khi tiêu tốn điểm**: liệt kê assets.json của cả kỳ thành một bảng (mô hình, prompt, tham số, số lượng, tổng giá estimate_cost, số dư) gửi cho người dùng, **chờ người dùng nói rõ trong cuộc trò chuyện là được** rồi mới create_tasks. Hộp thoại cấp quyền công cụ của host không tính là xác nhận; trước đó đã nói "tạo thẳng đi" cũng không tính. Đổi bất kỳ prompt, mô hình, số lượng nào đều phải báo giá lại và xác nhận lại.

## Kết nối Renoise (bản cơ bản không cần; khi làm bản nâng cao mà thiếu mới hướng dẫn)

**Xác định có hay chưa**: gọi thẳng `get_account`.
- Thành công → nói một câu cho qua "Renoise đã kết nối, số dư X điểm", rồi tiếp tục làm việc.
- Công cụ không tồn tại / báo chưa kết nối → thiếu, hướng dẫn theo phần dưới.
- Báo "disabled in connector settings" → không phải chưa cài, mà công cụ bị tắt, bảo người dùng vào cài đặt trình kết nối để bật.
- Báo chưa đăng nhập / ủy quyền hết hạn → không cần cài lại, đăng nhập ủy quyền lại (với Claude bấm "Connect" ở trình kết nối; Codex `codex mcp login renoise`).

**Chưa có tài khoản → đăng ký trước: [https://renoise.ai/mcp?utm_medium=xcom&utm_source=official](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)**. Đưa cho người dùng nguyên liên kết này, giữ tham số theo dõi utm, không viết lại thành trang chủ renoise.ai. Toàn bộ đăng nhập ủy quyền qua trình duyệt, không cần sao chép API key.

| Đang dùng | Cài thế nào |
|---|---|
| **Claude Code** | Lần lượt nhập `/plugin marketplace add ArcoCodes/renoise-plugins-official`, `/plugin install renoise@renoise-plugins-official`, lần gọi đầu tiên đăng nhập trên trình duyệt |
| **Claude desktop / claude.ai trên web** | Cài đặt → Trình kết nối (Connectors) → Add custom connector → tên `Renoise`, địa chỉ `https://renoise.ai/api/public/mcp` → đăng nhập renoise.ai bấm đồng ý |
| **Codex (CLI / desktop)** | `codex mcp add renoise --url https://renoise.ai/api/public/mcp`, rồi `codex mcp login renoise` |
| **OpenClaw** | `openclaw plugins install renoise --marketplace ArcoCodes/renoise-plugins-official` |
| **Các client khác hỗ trợ MCP từ xa** (WorkBuddy, Cursor, Windsurf, Cline, v.v.) | Thêm máy chủ từ xa `https://renoise.ai/api/public/mcp` vào cấu hình MCP, cách viết thường gặp `{"mcpServers": {"renoise": {"url": "https://renoise.ai/api/public/mcp"}}}` (tên trường theo tài liệu của client) |
| **Không chắc / muốn xem bản mới nhất** | renoise.ai/plugin liệt kê cách cài mới nhất cho từng client |

Đặt loại người dùng đang dùng lên đầu và ghi "khuyến nghị". Cài xong: nhóm Claude cần mở lại cuộc trò chuyện hoặc bấm kết nối lại ở trình kết nối, Codex mở lại phiên, rồi gọi `get_account` thêm một lần để xác nhận.

Trước khi bắt tay làm: `get_account` xem số dư; `load_skill model-routing` đọc quy tắc định tuyến (dưới đây là các kết luận skill này dùng, mô hình lấy theo list_models thời gian thực).

## Đơn giá (báo giá đo thực tế 2026-10-27, lấy theo estimate_cost)

| Tài nguyên | Mô hình | Đơn giá (điểm) | Dùng cho |
|---|---|---|---|
| Ảnh minh họa cảnh / không khí | `mj-v8.2` | 4 / ảnh | Cảnh thời đại, hình ảnh chính, không khí (họa phong tốt nhất) |
| Hình minh họa có cấu trúc, nền bản đồ, bố cục chính xác | `gpt-image-2.5-sunburst` 1k | 13 / ảnh | Bản đồ, mặt cắt đồ vật, bố cục cần chính xác |
| Nhiều ảnh nhất quán cùng nhân vật / cùng cảnh | `nano-banana-2` 1k | 8 / ảnh | Nhân vật trong series, cùng một địa điểm ở các thời điểm khác nhau |
| Cảnh quay động hình ảnh chính | `wan3.0-video` 720p 8s | 96 | Đa số cảnh quay động (khung đầu = ảnh minh họa đã tạo) |
| Cảnh quay động khó (chuyển động phức tạp, cảnh dài) | `seedance-2.5-byteplus` 720p 8s | 256 (1080p 576) | Một hai cảnh đảo ngược / cao trào |
| Cảnh quay đơn 4K | `flux-3-video` 4K 8s | 656 | Chỉ khi cần bản master 4K |
| Nhạc nền cả phim | `lyria-pro` | 4 / bài | **Mặc định không dùng**: Vibe Tri Thức Đại Thưởng bắt buộc dùng vibe-bgm (SKILL.md mục "BGM"); chỉ khi người dùng yêu cầu rõ ràng đổi bài mới tạo |
| Hiệu ứng âm thanh đơn | `eleven-sfx-v2` | 0,4 / giây | Tiếng chuông, lật sách, gió, đám đông |

Hoạt động của tài khoản: "kênh miễn phí" 480p/720p của Wan 3.0, Seedance 2.5, Kling 4.0 Omni đến 2026-11-02 (báo giá không nhất thiết hiển thị giảm giá, lấy theo khoản trừ thực tế).
**Ngân sách một kỳ**: theo các hạng nâng cao ở 08-tiers.md (nhẹ ≈25–40 / chuẩn ≈250–300 / hàng đầu ≈600–700). Chỉ nâng cao những cảnh code làm không tốt, còn lại vẫn làm bằng code.

## Quy trình

1. **Viết assets.json**: mỗi mục ghi rõ `use` (nhịp nào, dùng làm gì), `kind`, `model`, `ratio`, prompt. Prompt = `style_prefix` + nội dung ảnh này + `no text, no letters, no watermark`.
2. **Ảnh trước, video sau**: cảnh quay động luôn dùng ảnh minh họa đã tạo làm khung đầu (`references: [{ref: "task:<số task của ảnh>", role: "first_frame"}]`), bảo đảm tĩnh động nhất quán; vì vậy chia hai vòng báo giá: vòng một ảnh + nhạc nền + hiệu ứng âm thanh, vòng hai video (sau khi vòng một ra ảnh thì người dùng chọn ảnh). Cũng có thể liệt kê cả hai vòng vào bản xem trước một lần, xác nhận một lần (trong bản xem trước ghi rõ khung đầu của vòng hai lấy từ ảnh nào của vòng một).
3. **create_tasks** (mỗi lần ≤10 cái) → **wait_tasks** đến khi done → **download_results** (trả về một lệnh curl, chạy trên máy này, tải vào `lessons/NN/assets/_dl/`) → đổi tên theo `file` trong assets.json và đặt vào đúng chỗ, `status` đổi thành done, ghi lại số task.
4. **Video vào hình** (Wan 3.0 720p đo thực tế đầu ra có viền hộp thư đen thuần 66 pixel ở trên cùng, clip2frames.py sẽ tự phát hiện và cắt bỏ; tách xong lấy một khung xác nhận dòng đầu không phải màu đen): `python3 ~/.claude/skills/vibe-knowledge/tools/clip2frames.py assets/clips/v01.mp4 assets/clips/v01 --fps 30` → in ra số khung n → trong film.js `vclip(s, { dir: A("clips/v01"), n })`. Âm thanh môi trường của video gốc được lưu riêng ở `assets/clips/v01/audio.wav`, muốn dùng thì thêm một mục music: `{ src: P("clips/v01/audio.wav"), at, dur, gain: -20 }`.
5. **Nhạc nền**: BGM mặc định do hook bgm_force của finish.py xử lý bắt buộc (tự bổ sung, hiệu chỉnh theo giọng người); khi người dùng yêu cầu đổi bài, mục music đó ghi `bgm: true, user_request: "nguyên văn người dùng"`.
6. Ảnh đơn không hài lòng: chỉ làm lại đúng ảnh đó (báo giá mới, xác nhận mới), đừng làm lại cả loạt.

## Cách viết prompt

### Ảnh minh họa (Midjourney v8.2)
Mô tả thị giác bằng câu ngắn, không viết tài liệu yêu cầu:
`[style_prefix], [chủ thể], [môi trường], [ánh sáng], [bố cục: wide shot / low angle / negative space on the right for text], no text, no letters, no watermark`
- Chừa chỗ cho từ khóa: ghi rõ `negative space on the left/right/top`.
- 16:9; nhân vật không viết khuôn mặt cụ thể, viết bóng đen / bóng lưng / viễn cảnh, để giảm rủi ro "giống người thật nào đó".

### Bản đồ / hình minh họa (GPT Image 2.5 Sunburst)
```
USE: background plate for a documentary explainer
SCENE: antique paper map of Tang dynasty China, Yellow River and major prefectures as subtle ink lines
COMPOSITION: 16:9, map centered, wide margins, no labels
AVOID: any text, letters, numbers, legend, watermark
```
Địa danh, con số đều do code chồng lên (spread / keyword), không để mô hình viết chữ.

### Cảnh quay động (Wan 3.0 / Seedance 2.5)
Chế độ khung đầu, chỉ viết **sự thay đổi**, không mô tả lại hình tĩnh:
`[động tác của chủ thể / thay đổi của môi trường], [một chuyển động ống kính: slow push-in / slow dolly left], [thay đổi ánh sáng], no text, no subtitles`
- 8 giây là đủ, một cảnh một động tác; cần tự sự nhiều nhịp hoặc chuyển động dài, phức tạp hơn thì dùng Seedance 2.5.
- Âm thanh gốc mặc định bật, có thể dùng làm âm thanh môi trường; không dùng đối thoại.

### Nhạc nền (Lyria Pro)
```
Genre/style: cinematic documentary underscore, minimal piano and warm strings, subtle analog synth pad
Mood: curious, intimate, then awe at the reveal
Tempo: 72 BPM
Vocals: instrumental
Target length: ~3 minutes
Structure: [Intro] sparse piano (0:00–0:15) → [Build] strings enter at the title (~0:15) → [Verse] steady pulse under narration → [Break] near silence (~2:00) → [Climax] full but soft → [Outro] solo piano, ends on an unresolved note
Production: wide stereo, low-mid kept clean for voice, no drums in the first 15 seconds
```
- Ghi rõ "chừa dải tần giọng người" (low-mid kept clean for voice). Thời lượng chỉ là xấp xỉ, thực tế dùng loopbed / cắt để căn.
- Mỗi lần ra 2 bản cho người dùng chọn.

### Hiệu ứng âm thanh (ElevenLabs SFX)
Mô tả vật lý + độ dài thực: `a single temple bell struck once in a cold stone courtyard, long natural decay` · 3 giây. Mỗi mục một hiệu ứng.

## Bẫy đo thực tế (kỳ 01)

- Mỗi task Midjourney chỉ ra 1 ảnh 1456×816: muốn có ứng viên thì gửi thêm vài task; trước khi đưa vào thành phẩm dùng Real-ESRGAN x4plus của `~/tools/upscale-lab` phóng to rồi thu về 1080p.
- Tiền tố họa phong thống nhất sẽ lấn át mô tả của từng ảnh: ảnh thuộc thời đại khác (như thư phòng đời Tống) phải đổi tiền tố, nếu không sẽ bị vẽ thành thành lâu thời Chiến Quốc.
- Video khung đầu không nhất thiết diễn theo prompt: v02 không có cảnh "đóng cửa" mà đi vào một người mặc áo choàng, xem phim trước rồi mới quyết định dùng hay không, đừng mặc định là dùng được.
- Lyria sẽ làm các đoạn đúng theo mốc thời gian trong prompt (0:18 vào trống, 1:45 rút trống đều khớp), trong prompt nhất định phải ghi thời gian thực của lời dẫn.

## An toàn

- Không tạo khuôn mặt người thật còn sống, không bắt chước logo thương hiệu; nhân vật lịch sử ghi "Tạo hình nhân vật chỉ mang tính minh họa".
- Hình tạo ra luôn gắn nhãn góc "Hình minh họa AI / Hình do AI tạo" (plate, vclip mặc định có kèm).
- Không gửi tư liệu riêng của người dùng cho Renoise, trừ khi người dùng nói rõ muốn dùng.
