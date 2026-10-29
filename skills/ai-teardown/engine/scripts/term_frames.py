#!/usr/bin/env python3
"""Phát lại .cast do term_record.py ghi thành các khung hình, để primitives/terminal.js phát.

Cách dùng: python3 scripts/term_frames.py <in.cast> <out.json> [--fps 15] [--max-gap 1.2] [--speed 1]
- Dùng pyte phát lại từng sự kiện, lấy mẫu theo fps, chỉ lưu những dòng có thay đổi (vi phân).
- --max-gap: những đoạn "màn hình không động" dài hơn số giây này đều bị nén xuống đúng bằng ngần ấy (thời gian chờ trống khi agent suy nghĩ, chạy lệnh không cần phát hết).
- --speed: tăng tốc toàn bộ thêm nữa.
- Các mark đánh dấu lúc ghi sẽ được quy đổi theo trục thời gian mới, ghi vào marks, khi ghép lời dẫn có thể căn chỉnh.
Đầu ra: {cols, rows, duration, marks:{tên: giây}, frames:[{t, d:{số dòng: [[chữ, màu chữ, màu nền, cờ], ...]}, c:[cột, dòng, có hiện con trỏ hay không]}]}
Bit cờ: 1 in đậm 2 in nghiêng 4 gạch chân 8 đảo màu.
"""
import argparse, json, re
from pathlib import Path

import pyte

# Mã điều khiển giao thức bàn phím mà pyte không nhận ra (giao thức bàn phím kitty, modifyOtherKeys), nếu không lọc sẽ lộ ra những chữ như "1u" trên màn hình
KITTY = re.compile(r"\x1b\[[<>=?]\d*(?:;\d+)*u|\x1b\[>\d*(?:;\d+)*m")


def row_runs(line, cols):
    runs, cur = [], None
    for x in range(cols):
        ch = line[x]
        if ch.data == "":  # nửa sau của ô ký tự rộng
            continue
        flags = (1 if ch.bold else 0) | (2 if ch.italics else 0) | (4 if ch.underscore else 0) | (8 if ch.reverse else 0)
        key = (ch.fg, ch.bg, flags)
        if cur and cur[1:] == list(key):
            cur[0] += ch.data
        else:
            cur = [ch.data, *key]
            runs.append(cur)
    # Bỏ khoảng trắng kiểu mặc định ở cuối dòng để giảm dung lượng
    while runs and runs[-1][1] == "default" and runs[-1][2] == "default" and runs[-1][3] == 0 and runs[-1][0].strip() == "":
        runs.pop()
    if runs and runs[-1][1] == "default" and runs[-1][2] == "default" and runs[-1][3] == 0:
        runs[-1][0] = runs[-1][0].rstrip()
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cast"); ap.add_argument("out")
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--max-gap", type=float, default=1.2)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--drop", default="", help="nội dung cần xoá cả dòng (regex), ví dụ tên dịch vụ MCP riêng tư")
    ap.add_argument("--clip", action="append", default=[], help="cắt đoạn: tên:mark điểm đầu:mark điểm cuối (có thể bỏ điểm cuối = đến hết); mỗi đoạn xuất riêng <thư mục đầu ra>/<tên>.frames.json")
    a = ap.parse_args()

    lines = Path(a.cast).read_text(encoding="utf-8").splitlines()
    head = json.loads(lines[0])
    ev = [json.loads(l) for l in lines[1:]]
    cols, rows = head["width"], head["height"]
    screen = pyte.Screen(cols, rows)
    stream = pyte.Stream(screen)

    # 1) Ánh xạ lại trục thời gian: khoảng trống giữa các sự kiện đầu ra vượt quá max-gap thì nén ngắn lại
    remap, prev_raw, prev_new = [], 0.0, 0.0
    for e in ev:
        gap = e[0] - prev_raw
        new = prev_new + min(gap, a.max_gap)
        remap.append(new / a.speed)
        prev_raw, prev_new = e[0], new

    # 2) Phát lại + lấy mẫu theo khung hình
    frames, last_rows, marks = [], [None] * rows, {}
    step = 1 / a.fps
    next_t = 0.0

    # Che mờ: email, API key, token đều thay bằng dấu chấm tròn (thay từng ô, bố cục không đổi)
    SECRET = re.compile(r"[\w.+-]+@(?!example\.com)[\w-]+\.[\w.-]+|(?<![A-Za-z])sk-[A-Za-z0-9_-]{16,}|eyJ[A-Za-z0-9_-]{10,}")   # example.com là địa chỉ ví dụ, không che mờ

    def screen_text():
        # Ghép cả màn hình thành một chuỗi theo thứ tự đọc: đầu ra dài bị ngắt cứng ở cuối dòng, ghép lại là nối liền, nên tên người dùng, khoá, tên dịch vụ nằm vắt qua nhiều dòng cũng bắt được
        cells = [(y, x) for y in range(rows) for x in range(cols)]
        return cells, "".join(screen.buffer[y][x].data or " " for y, x in cells)

    def redact():
        cells, txt = screen_text()
        for m in SECRET.finditer(txt):
            for i in range(m.start(), m.end()):
                y, x = cells[i]; screen.buffer[y][x] = screen.buffer[y][x]._replace(data="•")
        # Tên người dùng của máy này (khi đầu ra bị cắt thành nhiều khối, việc thay thế trong luồng sẽ bị sót; khung hình mà đầu ra stream đến giữa chừng chỉ lộ ra "/Users/andy" cũng phải thay)
        for m in re.finditer(r"andyhu|(?<=/Users/)a(?:n(?:d(?:y(?:h)?)?)?)?$|(?<=/Users/)a(?:n(?:d(?:y(?:h)?)?)?)?(?=\s)", txt):
            for k, i in enumerate(range(m.start(), m.end())):
                y, x = cells[i]; screen.buffer[y][x] = screen.buffer[y][x]._replace(data="myname"[k])

    # Trạng thái tài khoản cá nhân (nhắc hạn mức, cảnh báo cấu hình máy) không cho khán giả xem: xoá cả dòng thành trống
    DROP = re.compile(r"weekly limit|usage limit|% left|warnings · f2|(?i:memmy)|^hook: |ERROR codex_core|failed to load skill|Starting MCP servers" + (f"|{a.drop}" if a.drop else ""))

    def drop():
        hit = {y for y in range(rows) if DROP.search("".join(screen.buffer[y][x].data for x in range(cols)))}
        cells, txt = screen_text()
        for m in DROP.finditer(txt):   # Trường hợp bị ngắt xuống hai dòng cũng tính: mỗi dòng liên quan đều xoá
            hit.update(cells[i][0] for i in range(m.start(), m.end()))
        for y in hit:
            for x in range(cols):
                screen.buffer[y][x] = screen.default_char

    def snap(t):
        drop()
        redact()
        d = {}
        for y in range(rows):
            r = row_runs(screen.buffer[y], cols)
            if r != last_rows[y]:
                d[str(y)] = r
                last_rows[y] = r
        c = [screen.cursor.x, screen.cursor.y, 0 if screen.cursor.hidden else 1]
        if d or not frames or frames[-1]["c"] != c:
            frames.append({"t": round(t, 3), "d": d, "c": c})

    for e, t in zip(ev, remap):
        while next_t < t:
            snap(next_t)
            next_t += step
        if e[1] == "o":
            data = KITTY.sub("", e[2]).replace("\ufeff", "").replace("\ufffd\ufffd", "• ")   # dấu đầu dòng bị tách hỏng trong bản quay màn hình cũ.replace("andyhu", "myname")   # tên người dùng máy này đổi thành chỗ giữ chỗ cùng độ dài, bố cục không đổi
            stream.feed(data)
        elif e[1] == "m":
            marks[e[2]] = round(t, 3)
    snap(next_t)
    duration = round(next_t + 1.0, 3)
    Path(a.out).write_text(json.dumps({"cols": cols, "rows": rows, "duration": duration, "marks": marks, "frames": frames},
                                      ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    # Cắt đoạn: khung hình đầu mỗi đoạn ghi trạng thái toàn màn hình, sau đó vi phân như cũ; thời gian tính từ 0, các mark trong đoạn cũng được quy đổi cùng
    for spec in a.clip:
        name, m0, *rest = spec.split(":")
        t0 = marks[m0] if m0 else 0.0
        t1 = marks[rest[0]] if rest and rest[0] else duration
        state, cur_c, out_frames = [[] for _ in range(rows)], [0, 0, 1], []
        for f in frames:
            if f["t"] <= t0:
                for k, v in f["d"].items():
                    state[int(k)] = v
                cur_c = f["c"]
                continue
            if f["t"] > t1:
                break
            out_frames.append({"t": round(f["t"] - t0, 3), "d": f["d"], "c": f["c"]})
        out_frames.insert(0, {"t": 0.0, "d": {str(y): state[y] for y in range(rows)}, "c": cur_c})
        # Mark trong đoạn: "tên đoạn.mark" được khôi phục thành tên chuẩn (như r5.submit → submit), tiện viết mark:submit trong cảnh
        sub = {(k.split(".", 1)[1] if k.startswith(name + ".") else k): round(v - t0, 3) for k, v in marks.items() if t0 <= v <= t1}
        dst = Path(a.out).parent / f"{name}.frames.json"
        dst.write_text(json.dumps({"cols": cols, "rows": rows, "duration": round(t1 - t0 + 0.5, 3), "marks": sub, "frames": out_frames},
                                  ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"  Đã cắt {dst.name}: {t1 - t0:.1f} giây, {len(out_frames)} khung hình, mark {sub}")
    raw = ev[-1][0] if ev else 0
    print(f"{Path(a.out).name}: {len(frames)} khung hình, gốc {raw:.1f} giây → phát lại {duration:.1f} giây, mark {marks}")


if __name__ == "__main__":
    main()
