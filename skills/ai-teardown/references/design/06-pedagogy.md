# 06 · Sổ tay phương pháp sư phạm

## Bậc thang độ sâu và ngân sách thời gian (mặc định 4 phút, giảng đến L4)

| Tầng | Nói gì | Chiếm khoảng | Trong 4 phút | Nguyên ngữ thường dùng |
|---|---|---|---|---|
| L0 Mở đầu | Một tình huống cụ thể, để người xem muốn biết "nó làm được thế nào" | 6% | 15 giây | Morph xem nhanh, Title |
| L1 Là gì | Định nghĩa một câu + một phép ví; sửa một hiểu lầm phổ biến | 10% | 25 giây | Analogy, Compare (myth) |
| L2 Dùng thế nào | Quy trình người dùng nhìn thấy: giao đi cái gì, nhận về cái gì | 12% | 30 giây | Morph, ChatUI |
| L3 Hoạt động thế nào | Sơ đồ tổng của hệ thống và cơ chế cốt lõi, đẩy dần từng tầng | 30% | 70 giây | SystemMap, Loop, Pipeline, Terminal |
| L4 Vì sao thiết kế như vậy | Các đánh đổi then chốt: cách huấn luyện, ranh giới an toàn, ngữ cảnh | 22% | 50 giây | Sandbox, Compare, Metric |
| L5 Ranh giới | Không làm được gì, khác loại tương tự ở đâu, điều gì chưa công khai | 12% | 30 giây | Compare, sương mù hoá phần chưa công bố |
| Kết | Sơ đồ tổng sáng toàn bộ, nhắc lại bằng một câu | 8% | 20 giây | ConceptMap, EndCard |

Dọc 60 giây giảng L0–L2 cộng 1 cơ chế; 8–12 phút giảng đến L5 và thêm bài kiểm tra nhỏ; dài hơn nữa thì tách thành loạt theo sơ đồ khái niệm.

## Bốn nhịp cho mỗi khái niệm

| Nhịp | `move` | Làm gì | Ví dụ (vòng lặp Agent của Codex) |
|---|---|---|---|
| Hỏi | `ask` | Vì sao cần nó | "Viết đúng code ngay một lần rất khó. Vậy nó biết mình viết đúng bằng cách nào?" |
| Diễn | `show` | Xem quá trình hoạt hình trước, chưa đưa thuật ngữ | Token chạy vòng: nghĩ một bước, ra tay, xem kết quả, vòng 2, vòng 3 |
| Gọi tên | `name` | Rồi mới đưa thuật ngữ, đặt lên hình ảnh đã xem hiểu | "Vòng này gọi là vòng lặp Agent." |
| Đặt về | `place` | Đặt về sơ đồ tổng và làm sáng | Máy quay kéo lại, vòng lặp trong nút Codex sáng lên |

## Quy tắc viết kịch bản

1. Một beat chỉ đưa vào một khái niệm mới; ví dụ cụ thể trước, khái quát trừu tượng sau.
2. Trước lần đầu xuất hiện của thuật ngữ phải có trải đường: quan hệ tiên quyết viết trong `concepts.json`, `check.py` tự kiểm thứ tự.
3. Văn nói, ngôi thứ hai, mỗi câu không quá 25 chữ (phụ đề một dòng 18 chữ, đọc xong trong hai dòng).
4. Con số chỉ được lấy từ sổ cái sự thật; `check.py` đối chiếu từng con số trong lời dẫn.
5. Tên sản phẩm tiếng Anh giữ nguyên; chỗ TTS đọc sai ghi vào từ điển phát âm `lexicon.json`, chỉ sửa phát âm không sửa phụ đề.
6. Trên hình đặt từ khoá không đặt cả câu; chú thích dán sát đối tượng, không lập khu chú giải riêng.
7. Thay đổi hình ảnh khớp đúng vào từ đang nói: chèn `[[cue]]` trong lời dẫn, sai số ≤ 0,2 giây.
8. Dùng làm tối và làm sáng để dẫn mắt (`dim`, `lit`); trang trí không liên quan đến khái niệm thì không thêm.
9. Mỗi phim xử lý ít nhất một hiểu lầm phổ biến (`misconceptions`), thường đặt ở L1 hoặc L5.

Căn cứ: các nguyên tắc học đa phương tiện của Mayer: tín hiệu, phân đoạn, huấn luyện trước, kề cận không-thời gian, dư thừa, cá nhân hoá.

## Tốc độ nói (đo thực tế)

edge-tts Vân Hi (`zh-CN-YunxiNeural`), `rate -10%`: lời dẫn bốn đoạn Spike trung bình khoảng 3,6 chữ/giây (gồm quãng ngắt), nằm ở mép trên của mục tiêu 3,3–3,6. Đoạn giảng dày đặc dùng `-12%`; kịch bản vlog của nhóm là 3,7–4,0, giảng nguyên lý phải chậm hơn một bậc.

## Nguyên mẫu đề tài và sơ đồ tổng mặc định

| Nguyên mẫu | Ví dụ | Sơ đồ tổng mặc định (nút · vai trò) | Thứ tự khái niệm điển hình |
|---|---|---|---|
| `agent` tác tử / trợ lý lập trình | Codex, Claude Code, Cursor, Manus | Bạn(user) → Agent(model) → môi trường(env); bên trong Agent: mô hình ⇄ vòng lặp ⇄ công cụ, bọc ngoài là hộp cát(boundary) | Là gì → dùng thế nào → vòng lặp → công cụ → hộp cát và phê duyệt → ngữ cảnh → ranh giới |
| `llm` mô hình ngôn ngữ lớn | GPT, DeepSeek, Qwen | Chữ → token → Transformer → token kế tiếp; huấn luyện: tiền huấn luyện → tinh chỉnh → học tăng cường | token → dự đoán từ kế tiếp → chú ý → các giai đoạn huấn luyện → cửa sổ ngữ cảnh → ảo giác |
| `reasoning` mô hình suy luận | dòng o, DeepSeek-R1 | Câu hỏi → chuỗi suy nghĩ → đáp án; huấn luyện: học tăng cường với phần thưởng có thể kiểm chứng | Nghĩ trước đáp sau → chuỗi suy nghĩ → phần thưởng → tính toán lúc kiểm thử → hạn chế |
| `generative-media` sinh ảnh / video | Sora, Veo, Seedance | Điều kiện văn bản → nhiễu → khử nhiễu từng bước → hình; không gian ẩn | Nhiễu → khử nhiễu → không gian ẩn → điều khiển điều kiện → nhất quán theo thời gian |
| `voice` giọng nói | TTS, ASR, giọng nói thời gian thực | Âm thanh ⇄ token; streaming; ngắt lời | Cắt lát → mã hoá → streaming → độ trễ → ngắt lời |
| `protocol` giao thức / framework | MCP, RAG, A2A | Ai gửi yêu cầu cho ai, theo thứ tự nào (sơ đồ tuần tự) | Vai trò → thông điệp → khám phá → gọi → ranh giới an toàn |

Nguyên mẫu chỉ cho khung xương mặc định, kết quả khảo sát có thể viết lại nó.

## Mục tiêu học tập và kiểm tra mù đọc nguội

- `objectives` trong `concepts.json` viết 5 câu hỏi, mỗi câu ứng với một khái niệm của L1–L4, chỉ xem kịch bản và khung hình then chốt là phải trả lời được.
- Trước khi ra phim, cử một agent con **chưa xem tài liệu khảo sát**: chỉ đưa nó toàn văn kịch bản và một khung hình giữa mỗi beat, cho nó trả lời 5 câu này.
- Một agent con khác chấm theo đáp án tham chiếu; ≥ 4/5 là đạt. Câu sai thì truy ngược về beat tương ứng, viết lại nhịp đó (thường là "diễn" chưa đủ trực quan hoặc "gọi tên" đến quá sớm).
