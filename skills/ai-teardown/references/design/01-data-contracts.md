# 01 · Hợp đồng dữ liệu

Mỗi chủ đề một thư mục (như `examples/codex/`), năm file JSON nối thành cả dây chuyền. Schema nằm trong `schemas/`, kiểm tra bằng `scripts/check.py`.

```
brief.json ──► research/sources.json ──► research/facts.json ──► lesson/concepts.json ──► lesson/lesson.json
   lập dự án       đăng ký nguồn (có snapshot)   sổ sự thật (sự thật nguyên tử)   sơ đồ tổng · khái niệm · mục tiêu     giáo án (file nguồn duy nhất)
                                                                                                    │ lồng tiếng
                                                                                                    ▼
                                                                                        build/timings.json (tự động sinh)
```

## Năm file, mỗi file lo việc gì

| File | Ai viết | Trường chính | Hạ nguồn ai dùng |
|---|---|---|---|
| `brief.json` | Bước 1, xác nhận với người dùng | `subject.resolved` (thực thể sau khi phân biệt), `subject.not` (những thứ trùng tên bị loại trừ), `archetype`, `duration_s`, `depth_ceiling`, `voice`, `as_of` | Tất cả |
| `research/sources.json` | Bước 2 | `tier` (U/T1/T2/T3), `fetch_method`, `snapshot`, `sha256` | Đối chiếu bằng chứng của facts; danh sách nguồn ở màn kết |
| `research/facts.json` | Bước 3 | `claim`, `category`, `status`, `evidence[].quote` (phải tìm thấy nguyên văn trong snapshot), `numbers`, `terms` | Lời thoại, hình ảnh, giáo cụ "bấm vào hình để xem nguồn" |
| `lesson/concepts.json` | Bước 4 | `master_map` (node và đường nối của sơ đồ tổng, kèm `role` và `honesty`), `concepts[].prereqs`, `misconceptions`, `objectives` (câu hỏi đọc nguội) | Sắp xếp giáo án, sơ đồ tổng, kiểm tra mù đọc nguội |
| `lesson/lesson.json` | Bước 5, CP1 xác nhận | `chapters[].focus_node`, `beats[].move` (bốn nhịp), `narration` (kèm `[[cue]]`), `visual.primitive/params`, `facts` | Lồng tiếng, biên dịch thành sân khấu, giáo cụ |

## Quy ước

- **Số hiệu không bao giờ dùng lại**: nguồn `S01…`, sự thật `F001…`, khái niệm `C01…`, hiểu lầm `M01…`, mục tiêu `Q01…`, chương `CH01…`, beat `B001…`. Khi sự thật bị phiên bản mới thay thế, sự thật mới ghi `supersedes`.
- **Đánh dấu cue**: trong lời dẫn dùng `[[tên]]` để đánh dấu vị trí hành động hình ảnh cần khớp, ví dụ `Nó trước hết [[read]]đọc code, rồi [[test]]chạy test`. Mỗi dấu đánh dấu khai báo trong `beats[].cues` rằng nó kích hoạt hook primitive nào (`reveal:model`, `state:3`, `press`). Script lồng tiếng quy đổi dấu đánh dấu thành số giây tuyệt đối rồi ghi vào `timings.json`.
- **Bốn nhịp**: `move` nhận `ask` (hỏi: vì sao cần nó) → `show` (diễn) → `name` (gọi tên: đưa thuật ngữ) → `place` (đặt lại: đặt trở lại sơ đồ tổng và làm sáng), ngoài ra còn `hook`, `compare`, `recap`, `quiz`, `transition`, `end`.
- **Mỗi beat nhiều nhất đưa vào một khái niệm mới** (trường `concept` chỉ được điền một).
- **Mã hóa trung thực**: beat trích dẫn sự thật `inferred` / `undisclosed` thì hoặc `visual.honesty` đánh dấu đúng giá trị tương ứng, hoặc nói rõ trong lời dẫn ("suy đoán", "chính thức không công bố").

## check.py kiểm tra gì

| Loại | Kiểm tra | Mức |
|---|---|---|
| Schema | Năm file lần lượt qua JSON Schema 2020-12 | ERROR |
| Nguồn | id duy nhất; file snapshot tồn tại; sha256 khớp | ERROR / WARN |
| Sự thật | Trích đoạn tìm thấy nguyên văn trong snapshot (chuẩn hóa NFKC, bỏ qua khoảng trắng); `verified` cần ít nhất một T1 hoặc hai T2; giảng cơ chế (`how`) phải có T1; `conflict/inferred/undisclosed` phải ghi notes; loại `number` phải điền numbers | ERROR |
| Khái niệm | Điều kiện tiên quyết tồn tại và không có chu trình; node, đường nối, tham chiếu parent của sơ đồ tổng hợp lệ; khái niệm mà mục tiêu học tập tham chiếu tồn tại | ERROR |
| Giáo án | Thứ tự beat khi nối các chương khớp với beats; mỗi `[[cue]]` đều có khai báo và ngược lại; điều kiện tiên quyết đã giảng trước khi đưa khái niệm vào; `show/name/place/compare/recap` phải gắn sự thật; sự thật suy đoán và chưa công bố xử lý theo mã hóa trung thực; **mỗi con số trong lời dẫn đều tìm thấy được trong sự thật được trích** | ERROR |
| Nhịp độ | Số chữ lời thoại ÷ tốc độ nói mục tiêu lệch quá 15% so với `duration_s` | WARN |
| Phạm vi | Khái niệm trong giới hạn độ sâu mà không có beat nào đưa vào | WARN |

## timings.json (tự động sinh sau khi lồng tiếng)

```json
{
  "voice": {"id": "zh-CN-YunxiNeural", "rate": "-10%"},
  "beats": {
    "B001": {"file": "audio/B001.mp3", "text": "去掉 cue 的旁白", "start": 0.4, "end": 7.94, "duration": 7.54,
             "words": [{"text": "任务", "start": 0.76, "end": 1.05, "i0": 2, "i1": 4}],
             "cues": {"zoom": 4.13}}
  },
  "total": 32.12
}
```

`words[].i0/i1` là khoảng ký tự của văn bản gốc: phụ đề ngắt dòng theo nó, từ điển cách đọc có thay phát âm thì vẫn đối chiếu lại được với văn bản gốc.
