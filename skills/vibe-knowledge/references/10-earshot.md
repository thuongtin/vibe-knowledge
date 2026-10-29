# 10 · Hiệu ứng âm thanh bằng code earshot (dùng chung hai bậc, 0 điểm)

Nguồn: github.com/Leonxlnx/earshot (MIT, 2963★). Toàn bộ 252 hiệu ứng âm thanh được lưu dưới dạng "mã công thức", render trong vài giây theo số thứ tự, không cần mạng, không cần mô hình; cùng một hiệu ứng đổi seed là có một take mới. Ngoài ra còn có kiểm tra chất lượng thính giác (timeline / sheet / critique), phần đó phải tải mô hình khoảng 1,1 GB, cài khi cần.

## Cài đặt (máy này đã cài: ~/tools/earshot, 2026-10-27)

```bash
git clone --depth 1 https://github.com/Leonxlnx/earshot ~/tools/earshot && cd ~/tools/earshot
/usr/local/bin/python3.12 -m venv --system-site-packages .venv          # tái dùng numpy/scipy/librosa/soundfile có sẵn của 3.12
CERT=$(/usr/local/bin/python3.12 -c "import certifi;print(certifi.where())")   # pip bản python.org trên máy này có vấn đề về chứng chỉ
.venv/bin/python -m pip install --cert "$CERT" pyloudnorm && .venv/bin/python -m pip install --cert "$CERT" --no-deps -e .
PYTHONPATH= .venv/bin/python -m earshot sfx list          # 252 sounds in the bank
```
Thư viện âm thanh chỉ phụ thuộc numpy / scipy; chưa cài torch và mô hình, nên describe / match / timeline / critique tạm thời chưa dùng được.

## Dùng trong phim

1. Khi `new_film.py` tạo series sẽ vá finish.py bằng `patch_earshot.py` (series đã có: `python3 tools/patch_earshot.py <thư mục series>`).
2. film.js:
```js
import { earshot, earshotRun } from "../../cine/engine/know.js";
const ES = earshot(music);
ES("cut_hit/punch", T("B06.nolie"));                          // điểm khởi âm rơi vào at
ES("whoosh_fast/tight", T("B06.one"), { align: "peak" });      // điểm to nhất rơi vào at
ES("pro_sub_drop/low", T("B10.die"), { gain: -6, pitch: "G1" });
earshotRun(ES, "pro_typing_key/soft", t0, t1, 90);            // tiếng gõ phím cho văn cổ hiện từng chữ
```
3. Khi render, finish.py tự động gọi môi trường earshot để render, cache ở `lessons/<bài>/build/esfx/`, trong log mỗi mục in ra "căn tới giây thứ mấy, sớm bao nhiêu mili giây".
4. **Đừng viết thêm sfx tích hợp sẵn của cine (bộ âm tổng hợp slam / impact / chime)**, sẽ chồng thành hai lớp; earshot đã bao phủ các vai trò này.

## Vai trò trong phim kiến thức → hiệu ứng đề xuất

| Vai trò (khoảnh khắc trong phim của chúng ta) | Số hiệu đề xuất | Căn chỉnh | Gain | Ghi chú |
|---|---|---|---|---|
| Con dấu đóng xuống / từ khóa slam | `cut_hit/punch`, `pro_pop_in/deep` | onset | −8 | cả phim ≤4 lần |
| Công bố lớn / tên phim chốt | `pro_impact/short`, `impact/punch` (dur 1.5) | onset | −8 | thêm `pro_sub_drop/soft` làm nền tần số thấp |
| Số chốt xuống | `pro_pop/thup`, `ui_pop/soft` | onset | −10 | |
| Số cuộn | chuỗi `pro_hover_tick/soft` | onset | −16 | khoảng cách earshotRun ≥66 ms |
| Văn cổ hiện từng chữ / gõ chữ | chuỗi `pro_typing_key/soft`, hoặc `pro_typing_run/soft` cả một đoạn | onset | −16 | khoảng cách ≥87 ms |
| Thẻ điều khoản / phần tử bật vào | `pro_pop_in/round`, `ui_pop/step` | onset | −12 | bật vào liên tiếp thì mỗi lần đổi seed |
| Cáo thị / lật trang / thẻ trượt vào | `swipe/paper`, `swipe/cloth` | onset | −12 | |
| Bút dạ quang gạch điểm chính | `swish/flick` | onset | −14 | điều tra thị giác |
| Vẽ vòng đỏ | `pro_zip/arc` | onset | −14 | điều tra thị giác |
| Đẩy gần đóng băng / chụp màn hình | `shutter/film`, `shutter/snap` | onset | −10 | |
| Chuyển cảnh / bay vào nhanh | `whoosh_fast/tight`, `whoosh_fast/crisp` | **peak**, rơi sau điểm cắt khoảng +37 ms | −12 | |
| Hít vào trước cú đảo chiều | `reverse_swell/cymbal`, `reverse_swell/short` | **peak**, sau điểm cắt khoảng +42 ms | −10 | **cả phim tối đa 1 lần** |
| Dồn nén căng thẳng | `riser/dark`, `pro_riser/air_gate` | điểm kết thúc khớp với lúc công bố | −14 | |
| Sụp đổ / bi kịch / kết cục | `pro_sub_drop/low`, `downlifter/sub_sink` | onset | −6 | tần số thấp, chú ý độ lớn |
| Xung đột / biến chất (tin → sợ) | `cut_hit/rumble` | onset | −8 | |
| Phần thưởng / đồng xu / thực hiện lời hứa | `mallet/glock`, `mallet/flourish`, `pro_notify/ding_2045` | onset | −10 | có thể dùng pitch để khớp âm điệu nhạc nền |
| Nút lựa chọn khó xử xuất hiện / được chọn | `toggle/on`, `toggle/latch` | onset | −12 | |
| Gõ cửa / gỗ / thẻ tre | `knock/wood`, `knock/double`, `fit/hit/bamboo_tok` | onset (sớm 40 ms) | −10 | |
| Bác bỏ tin đồn đảo chiều / lỗi | `glitch/burst`, `pro_glitch/standard` | điểm kết thúc khớp điểm cắt | −12 | |
| Mở đầu series | `logo_sting/soft_bloom`, `pro_logo_sting/swell_sting` | onset | −8 | |
| Chớp sáng cuối phim | `shimmer/m3`, `pro_shimmer/m1` | onset | −14 | |

Kinh nghiệm về thời điểm (trung vị đo thực tế với preset launch của earshot): chạm nhẹ sớm hơn điểm cắt hình 60 ms, gõ sớm 40 ms, nhấp sớm 11 ms, bật vào muộn 30 ms, điểm to nhất của tiếng vút muộn 37 ms, điểm to nhất của chũm chọe ngược muộn 42 ms.

## Kiểm tra chất lượng thính giác (phải cài mô hình, tùy chọn)

`earshot timeline thanh-pham.mp4 --video thanh-pham.mp4`: "bản chép nghe" của cả phim (thời điểm, độ lớn, nhãn của từng sự kiện âm thanh, độ lệch đồng bộ âm hình);
`earshot sheet thanh-pham.mp4 -o sheet.png`: ảnh chú thích kèm khung hình video, phổ tần, độ lớn; `earshot critique thanh-pham.mp4`: chấm điểm so với phim phát hành chuyên nghiệp và đưa ra đề xuất sửa kèm mốc thời gian.
Cách cài: `.venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu && .venv/bin/python -m pip install -e ".[mcp]" && .venv/bin/python -m earshot doctor --fetch` (khoảng 1,1 GB).
