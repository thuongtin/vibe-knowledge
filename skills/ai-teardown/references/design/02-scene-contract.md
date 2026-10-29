# 02 · Hợp đồng cảnh và runtime

## Cốt lõi: sân khấu chỉ nhận thời gian t

```
          lesson.json + timings.json
                    │ biên dịch (compile)
                    ▼
   Stage ──► cảnh[] ──► nguyên thủy.create(container, params, ctx) → instance
     │                      instance.render(localT, env)   hàm thuần
     │                      instance.beats                 điểm từng bước
     │                      instance.hotspots(localT)      bấm vào hình để xem xuất xứ
     ▼
  stage.seek(t)  ◄── Hyperframes: sự kiện window 'hf-seek' (từng khung hình)
                 ◄── Remotion: useCurrentFrame / fps (từng khung hình)
                 ◄── Bài giảng tương tác: <audio>.currentTime, thanh tiến độ, "bước tiếp"
```

Cả ba host đều chỉ gọi `stage.seek(t)`. Spike đo thực tế: cùng một file đóng gói (`spike/build/app.js`, 73 KB) chạy ở ba nơi ra cùng một hình ảnh, thành phẩm Hyperframes và Remotion có SSIM từng khung hình ≥ 0,990.

## Giao diện nguyên thủy

```js
export default {
  name: "Loop",
  create(root, params, ctx) {        // chỉ dựng DOM, không làm hoạt ảnh
    // ctx = { stage, id, at: {x, y, scale}, theme, aspect, css(id, text) }
    return {
      beats: [{ t, id, label }],      // giây cục bộ; dùng cho "từng bước" của bài giảng và vạch chương
      render(t, env) { … },           // giây cục bộ; env = { t, stage, cam, aspect, toScreen }
      hotspots(t) { return [{ el, facts: ["F012"], label }] },
      geometry?(t),                   // tùy chọn: để ống kính làm zoom-to-fit (Morph có)
    };
  },
};
```

## Quy tắc tất định (vi phạm bất kỳ điều nào, render từng khung hình sẽ nhấp nháy hoặc lệch vị trí)

1. Giá trị hoạt ảnh chỉ có thể là hàm của `t`: `spring.js` (lò xo dạng đóng, đổi mục tiêu nhiều lần = cộng các đáp ứng bước) hoặc `ease.js`.
2. Không dùng CSS `transition` / `animation` (style cơ bản của sân khấu đã vô hiệu hóa toàn cục), `setTimeout`, `requestAnimationFrame`, `Date.now()`, `Math.random()` không có seed (dùng `hash01(i, seed)`).
3. Không mang trạng thái giữa các khung hình: mỗi lần `render` đều ghi lại toàn bộ thuộc tính mà nó phụ trách (`setStyle/setAttr/setText` chỉ ghi DOM khi giá trị thay đổi, rất rẻ).
4. **Không thêm `will-change` cho phần tử bị ống kính phóng to**: chữ sẽ bị phóng to từ bitmap đã cache nên bị nhòe. Spike đo thực tế khi không thêm thì đẩy gần 7,6 lần chữ vẫn rõ nét.
5. **SVG marker không dùng `context-stroke`**: Chrome cache nét vẽ của marker, màu giữa các khung hình trước sau bị lẫn. Đổi thành chuyển giữa vài marker màu cố định theo trạng thái.
6. Phông chữ dùng file cục bộ (`assets/fonts`), trước khi xuất phim `document.fonts.load` toàn bộ độ đậm.
7. Chữ chuyển đổi trong container phải có cửa sổ vào ra riêng (`swap(t, tin, tout)`: mờ vào 0,18 giây, mờ ra 0,1 giây), chữ mới và cũ không chồng lên nhau.

Nghiệm thu tính tất định chia hai lớp: **snapshot DOM phải khớp tuyệt đối** (cùng một t, bất kể seek tới từ hướng nào); **so sánh pixel có dung sai** (rasterize của Chrome vào khoảnh khắc làm mờ, đổi chữ có chút nhiễu rất nhỏ: Spike đo thực tế 18 thời điểm × 4 thứ tự seek, DOM đều khớp, chênh lệch pixel ≤ 0,006% số pixel). Muốn khớp từng byte thì render bằng `--docker` của Hyperframes.

## Tọa độ và ống kính

- **Tọa độ thế giới**: gốc = tâm khung hình (khi ống kính ở (0,0), tỉ lệ 1). Cảnh dùng `stage.add(prim, {x, y, scale})` để đặt vào thế giới.
- **Phóng to từng lớp**: nội dung lớp kế tiếp đặt vào bên trong nút của lớp trước theo `scale` (ví dụ 0,16), ống kính đẩy gần khoảng `1/scale` lần thì "chui vào" nút. Nút dùng `open` / `close` để nhường chỗ (nhãn và màu nền mờ đi, hiện lại).
- **Ống kính**: `stage.camera([{t, x, y, z, cfg?}])`, tỉ lệ chạy lò xo trong không gian logarit, đẩy từ 1× đến 6× cảm giác tốc độ đều.
- **Lớp màn hình**: con trỏ, phụ đề, nhãn góc không phóng to theo ống kính; con trỏ định vị bằng tọa độ thế giới, mỗi khung hình đổi bằng `toScreen`.

## Thích ứng host

| Host | Cách làm | Lưu ý |
|---|---|---|
| Hyperframes | `window.addEventListener("hf-seek", e => stage.seek(e.detail.time))`; trước khi dựng sân khấu bất đồng bộ đặt `window.__hfTimelinesBuilding = true`, dựng xong đặt false và phát `hf-timelines-built` | lint yêu cầu đăng ký `window.__timelines[id]`: đăng ký một timeline GSAP rỗng chỉ khai báo thời lượng; lớp thế giới mang `data-layout-allow-overflow` (ống kính đẩy kéo ra ngoài khung hình là có chủ ý) |
| Remotion | dựng sân khấu một lần trong `useLayoutEffect` (`delayRender` chờ phông chữ), mỗi khung hình `stage.seek(frame / fps)` | Phông chữ dùng `staticFile` + `@font-face`; phiên bản `@remotion/*` phải khớp với `remotion` |
| Bài giảng tương tác | `<audio>` là đồng hồ chính, khi phát thì `requestAnimationFrame` đọc `currentTime` → `seek` | rAF chỉ điều khiển phát tương tác, không tham gia xuất phim |

## 16:9 và 9:16

`FRAMES` cho kích thước và vùng an toàn của hai khung hình (đường trên của dải phụ đề: 16:9 là 890, 9:16 là 1500). Nguyên thủy đọc `ctx.aspect` khi `create`, tự mang hai bộ bố cục; 9:16 không phải là cắt. V1 giao 16:9 trước, 9:16 bổ sung ở M2 (bố cục dọc của Morph là thiếu sót đã biết).
