# Quy chuẩn viết lời cho mùa hai «Khoá thực chiến AI: từ câu lệnh đến Codex» (dành cho tác tử viết văn án)

Chữ ký tác giả @Berryxia (đầu phim cuối phim tự thêm, trong văn án không cần đọc).

## Khán giả và giọng điệu
- Người đi làm biết chút về máy tính: biết cài phần mềm, hiểu thư mục, không biết viết code. Ít giảng kiến thức máy tính cơ bản, nhiều nói về tình huống công việc.
- Giọng điệu: như một blogger khoa học phổ thông thân thiện, gọn gàng, bình dị, cụ thể, không giọng quảng cáo, không chất đống tính từ. Những gì mùa một «Khoá nhập môn AI» đã giảng (token và dự đoán từng từ, tiền huấn luyện/tinh chỉnh, nhiệt độ và tính ngẫu nhiên, ảo giác, mốc kiến thức, cửa sổ ngữ cảnh, bản bình dân của gọi công cụ và vòng lặp tác tử, khung hợp tác 4D) chỉ nhắc lại bằng một câu.

## Kỷ luật sự thật (quan trọng nhất)
- Chỉ viết những sự thật tìm được căn cứ trong sổ cái nghiên cứu: `research/codex/` (Codex chính thức, mã sự thật X..), `research/concepts/` (khái niệm và câu lệnh, F..), `research/community/` (kinh nghiệm cộng đồng, chỉ được coi là "kinh nghiệm cộng đồng", điểm then chốt phải quay về đối chiếu với chính thức). Mỗi nhịp trong script.md ghi mã căn cứ.
- Giá, gói, tên mô hình, số phiên bản đều nói "tính đến tháng 9 năm 2026"; mục xung đột xử lý theo "lấy bản nào làm chuẩn" trong claims.md, không chắc thì không nói.
- Trung Quốc đại lục: nói đúng sự thật rằng khu vực được chính thức hỗ trợ không gồm Trung Quốc đại lục và Hồng Kông, Ma Cao, truy cập từ ngoài danh sách có thể bị khoá tài khoản; **không dạy bất kỳ cách nào vượt giới hạn khu vực**, cũng phải khuyên rõ không nên nạp hộ, mua mã xác thực, giao thông tin đăng nhập cho bên thứ ba. Đường kỹ thuật khả thi đặt ở mục 12 (Codex CLI + API mô hình nội địa / mô hình cục bộ).
- Trong hướng dẫn không trình diễn `--yolo`, `--dangerously-bypass-approvals-and-sandbox`, Full access; không trình diễn `untrusted`, `--full-auto`, `/personality`, `wire_api = "chat"` đã bị loại bỏ.
- Lệnh, tên khoá cấu hình, tên menu chép nguyên từng chữ theo văn bản chính thức.

## Sản phẩm (mỗi bài một thư mục `examples/ai-practice/lessons/NN/`)
1. `narration.json`: định dạng giống mùa một:
   `{"voice": {"engine": "gemini", "model": "gemini-3.8-flash-tts", "voice": "Sulafat", "lang": "vi"}, "lexicon": {}, "beats": [{"id": "B01", "narration": "[[hi]]……[[cue2]]……"}]}`
   - Không thêm `director` (chỉ dẫn diễn đọc): `gemini-3.8-flash-tts` đọc to mọi chỉ dẫn chèn vào lời dẫn. Đổi chất giọng bằng cách đổi `voice`.
   - Bẫy phát âm: từ viết tắt và tên riêng bị đọc lệch thì ghi vào lexicon; số phiên bản ghi vào lexicon đọc thành "0 chấm 155 chấm 1". Sau khi lồng tiếng xem trong voice.log có dòng cảnh báo "⚠" (đọc đáng ngờ) hay không.
   - Mỗi nhịp 60–140 chữ, mỗi nhịp 2–4 dấu `[[cue]]` (chữ thường tiếng Anh/số/gạch dưới, đặt ở đầu câu), hình ảnh chuyển theo cue.
   - Cả bài 2200–2800 chữ, 22–32 nhịp (lồng tiếng sẽ tăng tốc 1,15 lần, thành phẩm khoảng 8–10 phút).
   - Thuật ngữ tiếng Anh lần đầu xuất hiện thì kèm cách gọi tiếng Trung; lệnh trong lời dẫn chỉ đọc ý chính (ví dụ "nhập codex, nhấn Enter"), lệnh đầy đủ đặt trong các bước hình-chữ.
   - Nhịp đầu tiên của phần mở đầu dùng câu "嗨，欢迎来到 AI 实战课" (chào mừng đến khoá thực chiến AI) hoặc "欢迎回来" (chào mừng trở lại), giữ nguyên tiếng Trung vì lời dẫn đọc bằng tiếng Trung. Phần kết báo trước bài tiếp theo.
2. `script.md`: đầu trang là "Xin bạn đặc biệt xác nhận" (liệt kê các điểm không chắc, cần người phán đoán); sau đó từng nhịp: nguyên văn lời dẫn, gợi ý hình ảnh, mã căn cứ. Gợi ý hình ảnh phải cụ thể, và cố gắng dùng các loại hình có sẵn sau:
   - Chữ lớn đánh máy (statement), hàng biểu tượng (iconrow, có thể kèm mũi tên thành quy trình), hai cột đối chiếu trái phải (twocol), cửa sổ hội thoại (chat, minh hoạ giao diện), thẻ nhân vật/ảnh, thanh so sánh số (bars, số phải có nguồn), đường cong minh hoạ, sơ đồ quan hệ nhỏ (graph, ít dùng, tối đa mỗi bài một hình), sơ đồ tư duy kết bài (mindmap)
   - **Phát lại terminal (terminal)**: màn hình dòng lệnh Codex thật được ghi lại (xem recordings.json), có thể phóng to cục bộ, làm nổi bật vài dòng
   - **Thẻ bước (steps)**: bước đánh số + lệnh cần gõ (phông đơn cách) + "bạn sẽ thấy"
   - **Tạm dừng nghĩ một chút (pause)**: nêu một câu hỏi, đếm ngược 3 giây rồi công bố. Mỗi bài ít nhất 1 chỗ.
   - Khoảng mỗi 8 giây hình ảnh phải có thay đổi; đừng đầy màn hình sơ đồ quan hệ.
3. `steps.md`: **các bước hình-chữ cầm tay chỉ việc** (bản trên trang khoá học để gõ theo), đầy đủ hơn video: mỗi bước viết "làm gì → làm thế nào (lệnh dùng khối code, từng chữ) → bạn sẽ thấy → gặp lỗi thì sao", macOS và Windows khác nhau thì viết riêng, ghi mã căn cứ. Bài khái niệm (bài 1–5) viết thành "thí nghiệm nhỏ thực hành".
4. `extras.json`: `{"quiz": [{"q": "câu hỏi", "choices": ["A…","B…","C…"], "answer": 0, "why": "giải thích"}] ×3, "practice": {"title": "Bài tập thực hành", "steps": ["…"]}, "reading": [{"title": "", "url": "", "publisher": "", "why": "một câu nói vì sao đáng xem"}]}`. Đọc thêm chỉ đặt nguồn chính thức hoặc nguồn T1 (3–5 mục).
5. `recordings.json` (chỉ bài nào cần quay màn hình thật mới viết): `{"project": "tên thư mục dự án demo", "setup": ["lệnh shell chuẩn bị tệp trong ~/Desktop/codex-course-demo/<thư mục>, từng lệnh một"], "clips": [{"id": "r1", "used_by": "B07.cue", "purpose": "đoạn quay này muốn khán giả thấy gì", "cmd": "lệnh khởi động, như codex hoặc codex exec ...", "inputs": [{"type": "câu lệnh tiếng Trung cần nhập vào Codex"}, {"key": "enter"}, {"note": "dự kiến Codex sẽ làm gì, có thể xuất hiện lời nhắc phê duyệt nào, đáp lại thế nào"}], "expected": "khi thành công trên màn hình nên thấy gì"}]}`. Quay màn hình sẽ dùng Codex CLI thật trên Mac (macOS) của người dùng, dự án demo luôn đặt trong thư mục mới dưới `~/Desktop/codex-course-demo/`, trước hết git init và commit một lần. Câu lệnh dùng tiếng Trung, sát tình huống công việc, ngắn gọn dễ tái hiện (tránh tác vụ cần nối mạng cài phụ thuộc lớn).
6. `images.spec.json`: ảnh trên mạng cần dùng (Wikimedia Commons và các giấy phép mở khác), không có thì viết `{"images": []}`. Ảnh chụp màn hình chính thức của OpenAI đừng liệt kê vào (bản quyền), cần giao diện thì dùng phát lại terminal hoặc minh hoạ giao diện.

Viết xong mỗi bài, cuối script.md dùng một dòng ghi số chữ và số nhịp.
