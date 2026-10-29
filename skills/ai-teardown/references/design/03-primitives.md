# 03 · Primitive giảng dạy (13 cái đầu tiên)

Primitive = thành phần hoạt họa có thể tái sử dụng, có tham số, điều khiển theo thời gian; giao diện xem `02-scene-contract.md`.
Trạng thái: ✅ đã triển khai và đã dùng trong Spike hoặc trong video Codex hoàn chỉnh · ◐ triển khai một phần · ○ mới chỉ có đặc tả.
Tham số thực tế lấy theo chú thích đầu mã nguồn; chỗ nào khác với bảng này đã ghi chú ở cột trạng thái (cập nhật sau video hoàn chỉnh ngày 2026-09-26).

| Primitive | Giảng về | Tham số chính | Điểm từng bước / cue hook | Bấm vào hình để xem nguồn | Trạng thái |
|---|---|---|---|---|---|
| **SystemMap Sơ đồ tổng** | Gồm những gì, ai gọi ai | `nodes[{id,label,sub,role,x,y,w,h,icon,honesty,facts,ghost,labelAt}]`, `edges[{from,to,label,labelSide,bend,both,honesty,facts}]`, `reveal`, `lit`, `dim`, `open`/`close` | `reveal:<id>`, `open:<id>` | Node, nhãn đường nối | ✅ |
| **Loop Vòng lặp** | Thực hiện lặp đi lặp lại đến khi thỏa điều kiện | `steps[{label,role,angle,lx,ly}]`, `arrivals[]` (thời điểm token đến từng bước), `passAt`, `passLabel`, `title` | `step:<i>`, `pass` | Tâm vòng tròn | ✅ |
| **Morph Hình dạng đơn** | Một quy trình sản phẩm chạy hết như thế nào | Xem `04-morph.md` | `state:<i>` | Từng trạng thái | ✅ (6 loại trạng thái) |
| **Pipeline Đường ống** | Dữ liệu chảy qua những khâu nào theo thứ tự nào | `stages[{label,role,icon,facts}]`, `packets[{t0,t1,label}]` (khối dữ liệu di chuyển trong đường ống), `active[[t,i]]` | `stage:<i>` | Từng khâu | ○ |
| **Terminal Cửa sổ lệnh** | Thực tế nó đã chạy lệnh gì, thấy output gì | `lines[{kind:cmd\|out\|err\|ok,text,at}]`, `prompt`, `cps`, `title` | `line:<i>` | Toàn bộ cửa sổ | ◐ (trạng thái terminal bên trong Morph) |
| **ChatUI Hội thoại** | Người dùng giao việc thế nào, nó trả lời ra sao | `messages[{role:user\|assistant\|tool,text,at,cps}]`, `skin` | `msg:<i>` | Từng tin nhắn | ○ |
| **CodeDiff Thay đổi code** | Nó đã sửa những đoạn code nào | `file`, `lines[{k:" "\|"+"\|"-",text,at}]`, `highlight[]` | `line:<i>` | Tiêu đề file | ✅ `cards.js`, tham số thực tế `file`, `lines`, `actions` (nút bấm), `checks` (mục kiểm tra) |
| **Cursor Con trỏ** | Người dùng đã bấm gì, kéo gì trên giao diện | `keys[[t,x,y]]` (tọa độ thế giới), `presses[[t0,t1]]`, `visible[[t0,t1]]` | Thời điểm nhấn xuống | — | ✅ (lớp phủ tầng màn hình) |
| **Sandbox Ranh giới quyền** | Nó được đụng vào gì, không được đụng vào gì, việc gì cần bạn duyệt | `frame{w,h}`, `gates[{label,state:open\|closed\|ask,facts}]`, `askAt` (thời điểm hiện hộp thoại duyệt) | `gate:<i>`, `ask` | Từng cổng | ✅ `sandbox.js`; trạng thái cổng thực tế là `scoped/closed/removed/open`, hộp thoại duyệt là `ask{title,sub,at,buttons,pressAt}` |
| **Analogy Ví von** | Trước hết dùng thứ quen thuộc để ví von, rồi biến hình thành cấu trúc thật | `from{asset: svg\|lottie, label}`, `pairs[{from,to}]` (vật ví von ↔ bộ phận thật), `morphAt` | `pair:<i>`, `morph` | Từng cặp ánh xạ | ◐ `cards.js` mới chỉ làm hàng đối chiếu `rows[{icon,from,to,role,at}]`; vật ví von SVG/Lottie và biến hình chưa làm |
| **Compare So sánh và hiểu lầm** | Khác gì so với loại tương tự; hiểu lầm thường gặp so với sự thật | `mode: side\|myth`, `left/right{title,items[]}`, `myth{text,strikeAt}`, `truth{text,facts}` | `row:<i>`, `strike` | Từng hàng, câu sự thật | ✅ `cards.js`: chế độ myth (gạch bỏ rồi hiện sự thật), chế độ side (hai cột trái phải, `winnerAt` làm nổi bật bên thắng) |
| **Metric Thẻ số liệu** | Tốt đến mức nào, lớn đến mức nào | `value`, `unit`, `label`, `facts` (bắt buộc, và sự thật phải có `numbers`), `countAt` | `count` | Toàn bộ thẻ (bắt buộc có huy hiệu nguồn) | ○ |
| **ConceptMap Bản đồ khái niệm** | Chốt lại: đặt toàn bộ những gì vừa giảng trở lại sơ đồ tổng | `from: master_map`, `order[{node,summary,t}]` | `node:<id>` | Từng node | ◐ Phần chốt cả video dùng trực tiếp `lit` của SystemMap để làm sáng từng node theo lời dẫn, không làm riêng |

## Bổ sung cho series bài giảng (2026-09-26, thêm theo phản hồi sau khi xem video)

Người dùng xem xong video Codex hoàn chỉnh nói: "toàn là sơ đồ quan hệ qua lại, xem hoa mắt", "cần hiệu ứng gõ chữ, robot, icon nhỏ, kết bằng sơ đồ tư duy", "có thể làm nhân vật và lịch sử". Các primitive dưới đây đều không cần di chuyển camera, chuyển cảnh dùng hiệu ứng chuyển (`overlays.wipe`).

| Primitive | Giảng về | Tham số chính | File | Trạng thái |
|---|---|---|---|---|
| **Mascot Robot dẫn chuyện** | Nối cảnh, đặt câu hỏi, chỉ vào trọng điểm, reo hò khi kết | `spots[[t,x,y,size]]` (đổi vị trí khi chuyển cảnh), `poses[[t,pose]]` (idle/wave/point-l/point-r/cheer/present), `talk` (thời gian từng từ của lời dẫn, mở miệng theo từ), `look` | `mascot.js` | ✅ |
| **Typer Chữ gõ** | Tiêu đề, câu hỏi, trích dẫn, từ khóa | `lines[{text,at,cps,size,weight,color,hl}]`, `*từ*` được tô nổi rồi bút dạ quang vạch ra; `box: bubble\|card`, `tail`, `src` chữ nhỏ ghi nguồn; con trỏ chạy theo | `typer.js` | ✅ |
| **IconRow Hàng icon** | Vài nhân vật hoặc vài việc xuất hiện song song | `items[{icon,label,sub,color,at} \| {kind:wall} \| {kind:arrow}]`, `title` | `typer.js` | ✅ |
| **Portrait Thẻ nhân vật** | Giới thiệu nhân vật, ảnh lịch sử | `src,w,h,pos,tilt`, `name,sub` (gõ chữ), `credit` (ghi tác giả và giấy phép, bắt buộc), `kb` từ từ zoom vào | `portrait.js` | ✅ |
| **Timeline Dòng thời gian** | Mạch lịch sử, tiến hóa phiên bản | `events[{year,title,sub,img,pos,zoom,credit,icon,color,at}]`, `heading`; đường tiến độ chạy theo sự kiện mới nhất | `timeline.js` | ✅ |
| **MindMap Sơ đồ tư duy** | Kết thúc mỗi bài | `center{label,icon,color,at}`, `branches[{label,sub,icon,color,side,y,at}]`, `celebrate` rắc sao | `mindmap.js` | ✅ |
| **Floaties Icon nhỏ trôi nổi** | Thêm sinh khí cho phần mở đầu, tiêu đề lớn | `items[{icon,x,y,size,color,at}]` | `floaties.js` | ✅ |

Đi kèm:
- `runtime/typing.js`: phần chung của mọi hiệu ứng gõ chữ (nhịp điệu, bật vào, tô nổi, gợi ý âm thanh gõ phím).
- `runtime/iconify.js`: icon mã nguồn mở (tabler / lucide / iconoir, ngoại tuyến ở `assets/iconsets/`), nét có thể tự vẽ ra; dùng `scripts/icons.py` để rút theo tên vào bundle.
- `overlays.wipe`: chuyển cảnh bằng hai lớp hình tròn màu macaron, cảnh được chuyển đúng khoảnh khắc màu phủ kín.
- `theme.js`: thêm `macaron` (mặc định của series bài giảng), `mint`, `night`; mọi chủ đề đều có sáu ô màu `--m1…--m6` (màu chính, `-t` nền nhạt, `-d` chữ màu đậm).
- `scripts/fetch_images.py`: lấy ảnh từ Wikimedia Commons, chỉ nhận phạm vi công cộng, CC0, CC BY, CC BY-SA, tự động ghi lại tác giả và giấy phép.

## Thành phần cơ bản (không tính vào 13 cái)

| Thành phần | Tác dụng | Trạng thái |
|---|---|---|
| Captions Phụ đề | Ngắt dòng theo mốc thời gian từng từ, mỗi dòng ≤ 18 chữ, ngắt ở chỗ ngắt câu | ✅ |
| Tag Nhãn góc | “Minh họa giao diện”, “Suy đoán”, “Bản mẫu Spike” | ✅ |
| Title Thẻ chương | Tiêu đề chữ lớn ở đầu chương | ✅ `cards.js` |
| SourceBadge Huy hiệu nguồn | “Nguồn · bên phát hành” cạnh thẻ số liệu, ảnh chụp | ○ |
| EndCard Màn kết | “Thông tin tính đến YYYY-MM-DD” + các nguồn chính | ✅ `cards.js` |
| Layers Thẻ tầng | Vài tầng chồng lên nhau từ trên xuống (như thứ tự gộp của AGENTS.md), `litAt` làm sáng tầng gần bạn nhất | ✅ `cards.js` (thêm trong video hoàn chỉnh) |
| ChapterLabel Nhãn chương | Góc trên trái “Chương n · tiêu đề” | ✅ `overlays.js` |
| TermCard Thẻ thuật ngữ | Khi thuật ngữ mới xuất hiện lần đầu, đưa ra một câu giải thích dễ hiểu | ✅ `overlays.js` |
| Backdrop Màn làm tối | Khi thẻ tầng màn hình xuất hiện thì làm tối tầng thế giới | ✅ `overlays.js` |

## Bảng chọn loại (dành cho mô hình điều phối: hình dạng nội dung → primitive)

| Lời thoại đang nói | Dùng |
|---|---|
| X gồm A, B, C / A gọi B | SystemMap |
| Lặp đi lặp lại việc gì đó cho đến khi... | Loop |
| Chuỗi thao tác từ lúc người dùng giao việc đến lúc nhận kết quả | Morph (xem nhanh) hoặc ChatUI + Terminal + CodeDiff (giảng giải) |
| Dữ liệu lần lượt đi qua vài khâu xử lý | Pipeline |
| Nó làm được / không làm được gì, việc gì cần duyệt | Sandbox |
| Một thuật ngữ mới xuất hiện lần đầu | Analogy (ví von trước) → primitive tương ứng (rồi xem cấu trúc thật) |
| Mọi người tưởng... thực ra... | Compare (chế độ myth) |
| Điểm benchmark, giá, số tham số | Metric |
| Chốt cả video | ConceptMap |

Bài học từ InkFlow: chỉ liệt kê các loại thì mô hình sẽ không biết chọn loại mới; phải đưa bảng đối chiếu "hình dạng nội dung → loại".

## Checklist khi viết primitive mới

- [ ] `create` chỉ dựng DOM; `render(t)` ghi lại toàn bộ thuộc tính mà nó phụ trách
- [ ] Mọi giá trị hoạt họa đều lấy từ `spring.js` / `ease.js`
- [ ] Chuyển chữ có cửa sổ vào ra riêng
- [ ] Màu chỉ dùng biến chủ đề; màu vai trò thể hiện "ai đang hoạt động"
- [ ] Cung cấp `beats`; phần tử có sự thật thì cung cấp `hotspots`
- [ ] Hai bố cục 16:9 và 9:16
- [ ] Chạy qua kiểm thử xác định (DOM nhất quán) trong `spike/preview.html` và Hyperframes `inspect` (0 vấn đề)
