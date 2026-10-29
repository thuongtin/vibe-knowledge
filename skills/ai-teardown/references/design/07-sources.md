# 07 · Chính sách nguồn tin, định tuyến thu thập và sổ sự kiện

## 1. Phân cấp nguồn tin

| Cấp | Bao gồm | Có thể làm căn cứ cho |
|---|---|---|
| U Người dùng cung cấp | Tài liệu, ảnh chụp màn hình, ghi màn hình, liên kết do người dùng đưa | Ưu tiên dùng; mâu thuẫn với T1 thì liệt kê cho người dùng quyết, không lặng lẽ ghi đè |
| T1 Chính thức | Trang web chính thức và trang sản phẩm, tài liệu chính thức, blog và ghi chú phát hành chính thức, changelog, GitHub chính thức (dự án mã nguồn mở thì đọc thẳng mã nguồn), bài báo và system card chính thức, thông báo từ tài khoản chính thức, video demo chính thức, đầu ra thực của sản phẩm đã cài trên máy | Cơ chế, tính năng, số liệu, ngày tháng, giao diện |
| T2 Bên thứ ba có uy tín | Bài báo bình duyệt và arXiv, truyền thông kỹ thuật có ký tên, phân tích sâu của chuyên gia được công nhận | Bối cảnh và diễn giải; số liệu cần hai T2 độc lập đối chứng |
| T3 Cộng đồng | Diễn đàn, X, Reddit, blog cá nhân | Chỉ làm bằng chứng phụ cho "người dùng nói gì", không làm căn cứ cho cơ chế và số liệu |

## 2. Quy tắc sử dụng

1. Nói về "bên trong hoạt động thế nào" (`category: how`) phải có T1; không có T1 thì `status` chỉ có thể là `inferred` hoặc `undisclosed`, hình ảnh xử lý theo mã hoá trung thực.
2. Số liệu lên màn hình (điểm benchmark, giá, số tham số, thời lượng) phải có trường `numbers`, hình ảnh kèm nhãn góc ghi nguồn.
3. Mâu thuẫn cùng cấp thì lấy bản phát hành mới nhất; bản thân mâu thuẫn ghi vào `status: conflict` và `notes`, đồng thời nhắc người dùng ở CP1.
4. Mỗi sự kiện ghi `as_of`; cuối phim cố định một màn hình "Thông tin tính đến YYYY-MM-DD".
5. Giao diện ưu tiên dựng lại bằng HTML, góc ghi "giao diện minh hoạ"; ảnh chụp chính thức chỉ làm tham chiếu, không đưa thẳng lên màn hình. Logo chỉ dùng để nhận diện.
6. Sản phẩm đã cài trên máy có thể lấy đầu ra thực không có tác dụng phụ (như `--help`, `--version`) làm T1, `fetch_method: local`.

## 3. Định tuyến thu thập (theo thử nghiệm thực trên máy)

| Nguồn | Cách đọc | Lý do |
|---|---|---|
| Trang chính thức chống cào mạnh như openai.com | `get_page_text` của trình duyệt tích hợp; không được thì dùng Playwright | Jina, curl, WebFetch đều trả về 403 (dotey-writer thử thực tế) |
| GitHub | `api.github.com` + `raw.githubusercontent.com` | Jina làm mất khối mã; curl thỉnh thoảng đứt SSL, thử lại 3 lần |
| Trang tài liệu, blog | curl đọc thẳng → jina-reader → firecrawl | |
| Tài khoản X chính thức | `api.fxtwitter.com` | Đọc thẳng x.com ẩn danh trả về 403 |
| Video chính thức | Trích phụ đề, khung hình chính lưu riêng | Hình ảnh chỉ làm tham chiếu |
| Tìm kiếm toàn mạng | agent-reach, exa-search, tìm kiếm GitHub | WebSearch trên máy này không dùng được |

## 4. Bản chụp nhanh

- Mỗi nguồn một bản chụp nhanh: `research/snapshots/<SID>.md` (nội dung thuần văn bản, đầu file ghi URL, thời gian thu thập, phương pháp), có thể kèm ảnh chụp trang `<SID>.png`.
- `sources.json` ghi `sha256` (băm của file bản chụp), sau này chạy lại khảo sát có thể dựa vào đó để biết nguồn có thay đổi không.

## 5. Tách sự kiện nguyên tử thế nào

- Một sự kiện chỉ nói một việc, một câu tiếng Trung, trong 60 chữ; có thể được đối chiếu bằng một câu "đúng / sai".
- `evidence.quote` trích nguyên văn (có thể là tiếng Anh), trong 400 chữ, ghi rõ vị trí `where` (tên tiểu mục, số dòng).
- Danh từ riêng đưa vào `terms`, dùng cho từ điển cách đọc và đối chiếu từng chữ.
- Đánh số: nguồn `S01…`, sự kiện `F001…`, đã phát hành thì không dùng lại; sự kiện bị phiên bản mới thay thế thì sự kiện mới ghi `supersedes`.

## 6. Nguồn lên màn hình thế nào

| Vị trí | Định dạng | Ví dụ |
|---|---|---|
| Thẻ dữ liệu, điểm benchmark | Nhãn góc phải dưới | `Nguồn · Tài liệu OpenAI Codex` |
| Dựng lại giao diện | Nhãn góc trái trên | `Giao diện minh hoạ` |
| Cấu trúc suy đoán | Khung nét đứt + nhãn | `Suy đoán` |
| Phần chưa được công bố | Khối mờ sương + nhãn | `Chưa công bố` |
| Cuối phim | Một màn hình liệt kê các nguồn chính | `Thông tin tính đến 2026-09-26` |
| Mô tả video | Danh sách nguồn đầy đủ, kèm liên kết | Tạo từ `sources.json` |
