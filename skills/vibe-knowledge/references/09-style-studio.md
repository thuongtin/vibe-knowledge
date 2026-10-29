# 09 · Xưởng phong cách: dùng bộ trong thư viện, sửa thành của mình, làm từ trang trắng

Cấu trúc quy trình tham khảo bản cập nhật 2026-10-22 của Lemo-Opuscar ("Sửa phong cách thành của riêng bạn"), viết lại theo bối cảnh phim tri thức của skill này. Nguyên tắc giống lời kết của nó: **phong cách chỉ là phương tiện, nội dung mới là quan trọng nhất** — có chủ đề và danh sách dữ kiện trước, rồi mới chọn phong cách.

## Lối vào (hỏi cùng lúc ở bước xác nhận 1, dùng AskUserQuestion)

1. **Dùng phong cách trong thư viện làm một tập** (mặc định) — liệt kê `styles/INDEX.md`, theo chủ đề đề xuất một bộ xếp đầu tiên, kèm ảnh phong cách.
2. **Dùng phong cách của tôi làm một tập** — chỉ xuất hiện khi `~/vibe-knowledge-styles/` đã có phong cách, xếp đầu tiên.
3. **Sửa một bộ phong cách trong thư viện, lưu thành của tôi**.
4. **Làm một phong cách mới từ trang trắng** — người dùng mô tả bằng lời của mình, hoặc đưa một ảnh / một đoạn phim; chọn trong thư viện bộ gần nhất làm "nền kỹ thuật", nói rõ vì sao chọn nó, người dùng gật đầu hoặc đổi bộ khác.

Người dùng cũng có thể nói thẳng trong một câu: "Đổi Cổ phong sang màu thương hiệu của tôi", "Làm từ đầu một phong cách bảng đen phấn trắng, ấm hơn một chút, chậm hơn một chút".

## Mỗi lần một câu hỏi để chốt phương án (khi sửa phong cách / làm phong cách mới)

- **Mỗi lần chỉ hỏi một câu**, mỗi câu 2–4 lựa chọn, **phương án đề xuất xếp đầu và nêu lý do**; lựa chọn cuối cùng luôn là "Trò chuyện tự do".
- Người dùng nói "bạn quyết đi": các câu còn lại điền theo đề xuất, liệt kê thành một bảng cho họ xem.
- Chọn "Trò chuyện tự do": không hỏi từng câu nữa, đổi thành một danh sách (đã chốt / chưa chốt, mỗi mục chưa chốt kèm đề xuất), người dùng muốn nói mục nào trước thì nói mục đó.
- Khoảng 8–10 câu, theo thứ tự này:
  1. **Dùng để làm gì**: series nào, đăng lên nền tảng nào, khung hình (16:9 / 9:16 / 3:4), có màu thương hiệu / logo / nhân vật cố định / giọng đọc cố định hay không.
  2. **Muốn sửa chỗ nào** (khi sửa phong cách trong thư viện): trước hết dùng ví dụ của chính bộ phong cách này để giải thích cách chia ba mức —
     - **Cứ yên tâm sửa**: phối màu (đổi màu trong logic gốc), phông chữ, nhanh chậm, âm thanh và nhạc cụ, thêm hoặc đổi một cảnh đặc trưng;
     - **Sửa là mất chất**: chất liệu và cách vẽ, bản thân logic phối màu, ngữ pháp máy quay — sửa được, nhưng phải nói rõ sẽ mất đi điều gì;
     - **Không được sửa**: bản chất và cách vẽ nền tảng của phong cách — sửa là thành bộ khác, nên đổi nền.
     (Cách chia ba mức của mỗi bộ được ghi trong `styles/<key>/STYLE.md`.)
  3. **Hỏi chi tiết từng mục**: chỉ hỏi những mục cần động đến: chất liệu, phối màu, phông chữ, chuyển động, ống kính, âm thanh, cảnh đặc trưng, mỗi mục đưa 2–3 hướng cụ thể.
  4. **Kết hợp với bản gốc nào**: đề xuất 1–2 bản (xem mục "Kết hợp" trong từng STYLE.md).
  5. **Đặt tên**: tên tiếng Việt, tên tiếng Anh.

## Tổng hợp → ảnh phong cách → demo → chốt lưu

1. **Bảng tổng hợp**: mỗi mục "trước khi sửa / sau khi sửa / cái giá", người dùng gật đầu mới bắt tay làm.
2. **Ảnh phong cách**: xuất một ảnh bằng chính code vẽ thật; với phong cách sửa từ thư viện, cùng một khung hình đặt bản gốc và bản mới cạnh nhau (trái bản gốc, phải bản mới), xuất ảnh bằng stills.py rồi ghép bằng PIL. Hai vòng vẫn chưa đúng thì nói thẳng và đề nghị đổi nền.
3. **Phim demo 15–30 giây**: dùng lại lời dẫn mở đầu của tập 01 (cách làm của `lessons/styles`: cắt một câu từ lời dẫn đã lồng tiếng, ghép thành trục thời gian, số nhịp B01…), mỗi chỗ sửa xuất hiện ít nhất một lần, cảnh đặc trưng nhất định phải xuất hiện; làm xong tự kiểm một vòng, khi bàn giao ghi rõ "mỗi chỗ sửa ở giây thứ mấy".
4. **Chốt lưu**: chỉ khi người dùng nói rõ "chốt lưu" mới ghi vào; mọi thứ trước đó chỉ nằm trong thư mục dự án lần này.

```
~/vibe-knowledge-styles/<tên>/
  STYLE.md       cùng cấu trúc với trong thư viện (ý đồ đạo diễn… cách chia ba mức, kết hợp), dòng đầu ghi "Nền: <bộ nào trong thư viện>"
  changes.md     trước khi sửa / sau khi sửa / cái giá (nguyên bảng tổng hợp)
  draw.js        hàm vẽ (trích từ film.js của demo, chữ ký giống _samples: (s) => (t, a, z, B) => void)
  still.jpg      ảnh phong cách
  demo.mp4       phim demo
```

Sau này chỉ cần gọi tên: "Dùng [Cổ phong đêm] của tôi làm một tập về Đình trưởng Ô Giang". Về sau nếu phong cách nền có sửa lỗi thì nhắc một câu, hỏi có muốn đồng bộ không, không tự động sửa.

## Bậc và mô hình

- Tạo mới / sửa lớn phong cách: Opus (high hoặc xhigh).
- Sản xuất hàng loạt bằng phong cách đã chốt lưu: Opus hoặc Sonnet high đều được (tác giả Lemo-Opuscar đã thử thực tế Sonnet 5.5 High cũng ổn định; skill này chưa thử thực tế Sonnet, lần đầu dùng cần xem khung hình mẫu).
- Mỗi bộ phong cách đều làm được bản cơ bản (0 điểm) và bản nâng cao Renoise (STYLE.md có tiền tố).
