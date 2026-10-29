#!/usr/bin/env python3
"""Ghi terminal thật: chạy một lệnh trong pseudo-terminal có kích thước cố định, theo kịch bản "chờ gợi ý → gõ chữ → Enter", ghi lại đầu ra thô kèm dấu thời gian.
Thứ ghi ra là .cast kiểu asciinema v2 (dòng đầu là thông tin đầu file, các dòng sau là [giây, "o"|"i"|"m", dữ liệu]), rồi giao cho term_frames.py phát lại thành hình ảnh.

Cách dùng: python3 scripts/term_record.py <kịch-bản.json> <đầu-ra.cast>
kịch-bản.json:
{
  "cmd": ["codex"], "cwd": "~/Desktop/codex-demo", "cols": 110, "rows": 32,
  "env": {"FOO": "1"},
  "steps": [
    {"wait": "regex, xuất hiện trên màn hình mới đi tiếp", "timeout": 60},
    {"type": "chữ cần gõ", "cps": 14},          # gõ từng chữ như người thật
    {"key": "enter"},                          # enter / esc / tab / up / down / ctrl-c / y / n ……
    {"sleep": 1.5},
    {"mark": "submit"},                        # đánh dấu thời gian, dùng khi ghép lời dẫn
    {"wait_idle": 4, "timeout": 600},          # màn hình liên tục N giây không đổi mới đi tiếp (chờ tác tử làm xong)
    {"exit": true}                             # kết thúc ghi (gửi ctrl-c trước, rồi chờ tiến trình thoát)
  ]
}
Trạng thái màn hình được mô phỏng thời gian thực bằng pyte, nên thứ wait nhìn thấy chính là hình ảnh khán giả sẽ thấy.
"""
import json, os, pty, re, select, signal, struct, sys, termios, fcntl, time
from pathlib import Path

import pyte

KEYS = {"enter": "\r", "esc": "\x1b", "tab": "\t", "up": "\x1b[A", "down": "\x1b[B", "left": "\x1b[D", "right": "\x1b[C",
        "shift-tab": "\x1b[Z", "ctrl-c": "\x03", "ctrl-d": "\x04", "backspace": "\x7f", "space": " "}


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    cols, rows = spec.get("cols", 110), spec.get("rows", 32)
    cwd = os.path.expanduser(spec.get("cwd", "."))
    env = {**os.environ, "TERM": "xterm-256color", "COLORTERM": "truecolor", "COLUMNS": str(cols), "LINES": str(rows), **spec.get("env", {})}

    screen = pyte.Screen(cols, rows)
    stream = pyte.ByteStream(screen)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(cwd)
        os.execvpe(spec["cmd"][0], spec["cmd"], env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))

    t0 = time.monotonic()
    import codecs
    dec = codecs.getincrementaldecoder("utf-8")("replace")   # byte của một chữ Hán có thể bị tách ra hai lần đọc, không được giải mã độc lập từng khối
    events = []
    last_change = [time.monotonic()]
    alive = [True]

    def now():
        return round(time.monotonic() - t0, 4)

    def pump(timeout=0.05):
        if not alive[0]:
            return
        r, _, _ = select.select([fd], [], [], timeout)
        if fd in r:
            try:
                data = os.read(fd, 65536)
            except OSError:
                alive[0] = False
                return
            if not data:
                alive[0] = False
                return
            txt = dec.decode(data)
            if txt:
                events.append([now(), "o", txt])
            stream.feed(data)
            last_change[0] = time.monotonic()

    def text():
        # Không dùng screen.display của pyte: khi nửa ô sau của ký tự rộng là chuỗi rỗng thì nó sẽ báo lỗi
        return "\n".join("".join(screen.buffer[y][x].data for x in range(cols)) for y in range(rows))

    # Ghi màn hình hiện tại vào <đầu-ra>.screen.txt theo thời gian thực (mỗi 2 giây), khi ghi bị kẹt thì thấy được đang dừng ở hình nào
    shot_path, last_shot = out.with_suffix(".screen.txt"), [0.0]
    _pump = pump

    def pump(timeout=0.05):
        _pump(timeout)
        if time.monotonic() - last_shot[0] > 2:
            last_shot[0] = time.monotonic()
            try:
                shot_path.write_text(f"[{now()}s]\n" + text(), encoding="utf-8")
            except OSError:
                pass

    def send(s):
        events.append([now(), "i", s])
        os.write(fd, s.encode("utf-8"))

    try:
        run_steps(spec, pump, text, send, now, events, last_change, alive)
    finally:
        finish(pid, fd, pump, alive, events, out, cols, rows, spec, cwd, now, text)


def run_steps(spec, pump, text, send, now, events, last_change, alive):
    for st in spec["steps"]:
        if "wait" in st:
            pat, deadline = re.compile(st["wait"]), time.monotonic() + st.get("timeout", 60)
            while not pat.search(text()):
                if time.monotonic() > deadline or not alive[0]:
                    sys.exit(f"Chờ không thấy \"{st['wait']}\". Màn hình hiện tại:\n{text()}")
                pump()
        elif "wait_idle" in st:
            deadline = time.monotonic() + st.get("timeout", 600)
            while time.monotonic() - last_change[0] < st["wait_idle"]:
                if time.monotonic() > deadline or not alive[0]:
                    break
                pump()
        elif "work" in st:
            # Chờ tác tử làm xong: màn hình liên tục work giây không động là xong; nếu giữa chừng xuất hiện gợi ý phê duyệt thì bấm approve_key để duyệt một lần và ghi hình lúc đó vào nhật ký
            appr = re.compile(st.get("approve_re", r"(?i)(allow|approve|run this command|proceed)\?|Yes, (and )?(proceed|allow)"))
            deadline, n = time.monotonic() + st.get("timeout", 600), 0
            while time.monotonic() < deadline and alive[0]:
                pump()
                if time.monotonic() - last_change[0] >= 1.2 and appr.search(text()) and n < st.get("max_approvals", 3):
                    n += 1
                    events.append([now(), "m", f"approve{n}"])
                    print(f"—— Lần phê duyệt thứ {n}, màn hình lúc đó ——\n{text()}\n", file=sys.stderr)
                    end = time.monotonic() + st.get("approve_delay", 1.5)
                    while time.monotonic() < end:
                        pump(0.05)
                    send(KEYS.get(st.get("approve_key", "enter"), st.get("approve_key", "enter")))
                    continue
                # until_file: phải chờ đến khi thư mục làm việc xuất hiện file này (như renders/*.mp4) mới tính là xong, dừng lại suy nghĩ giữa chừng không tính
                done = not st.get("until_file") or any(Path(os.path.expanduser(spec.get("cwd", "."))).glob(st["until_file"]))
                if time.monotonic() - last_change[0] >= st["work"] and done:
                    break
        elif "select" in st:
            # Trong menu dùng phím mũi tên di chuyển tới mục đích (dòng của mục hiện tại bắt đầu bằng › hoặc >) rồi Enter
            pat = re.compile(st["select"])
            for _ in range(st.get("max", 10)):
                end = time.monotonic() + 0.6
                while time.monotonic() < end:
                    pump(0.05)
                cur = [l for l in text().split("\n") if re.match(r"^\s*[›>❯]\s*\S", l)]
                if cur and pat.search(cur[-1]):
                    break
                send(KEYS[st.get("dir", "down")])
            else:
                sys.exit(f"Không tìm thấy \"{st['select']}\" trong menu. Màn hình hiện tại:\n{text()}")
            end = time.monotonic() + st.get("pause", 1.0)
            while time.monotonic() < end:
                pump(0.05)
            k = st.get("confirm", "enter")   # Ví dụ trong /model bấm s chỉ có hiệu lực với phiên này, không đổi cấu hình mặc định
            send(KEYS.get(k, k))
        elif "shell" in st:
            # Chạy một lệnh ngoài khung hình (ví dụ sao lưu file của phiên bản trung gian), sẽ không xuất hiện trong bản quay màn hình
            import subprocess
            subprocess.run(st["shell"], shell=True, executable="/bin/zsh")
        elif "type" in st:
            gap = 1 / st.get("cps", 14)
            for ch in st["type"]:
                send(ch)
                end = time.monotonic() + gap
                while time.monotonic() < end:
                    pump(end - time.monotonic())
        elif "key" in st:
            send(KEYS.get(st["key"], st["key"]))
        elif "sleep" in st:
            end = time.monotonic() + st["sleep"]
            while time.monotonic() < end:
                pump(max(0.0, end - time.monotonic()))
        elif "mark" in st:
            events.append([now(), "m", st["mark"]])
        elif st.get("exit"):
            break
        pump(0.01)


def finish(pid, fd, pump, alive, events, out, cols, rows, spec, cwd, now, text):
    # Kết thúc: cho chương trình chút thời gian làm mới, rồi mới kết thúc
    end = time.monotonic() + 1.0
    while time.monotonic() < end and alive[0]:
        pump(0.1)
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGKILL):   # shell tương tác sẽ bỏ qua hai tín hiệu đầu
        try:
            if os.waitpid(pid, os.WNOHANG)[0]:
                break
            os.kill(pid, sig)
        except (ProcessLookupError, ChildProcessError):
            break
        time.sleep(0.5)
    os.close(fd)   # macOS: nếu không đóng đầu chính, tiến trình con bị giết sẽ kẹt khi xả đầu ra terminal, waitpid sẽ chờ mãi không được
    try:
        os.waitpid(pid, 0)
    except ChildProcessError:
        pass

    head = {"version": 2, "width": cols, "height": rows, "timestamp": int(time.time()), "cmd": spec["cmd"], "cwd": cwd}
    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(head, ensure_ascii=False) + "\n")
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"Đã ghi xong: {out} ({now():.1f} giây, {len(events)} sự kiện)")
    print(text())


if __name__ == "__main__":
    main()
