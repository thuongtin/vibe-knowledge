#!/usr/bin/env python3
"""Đọc các đoạn minh hoạ từ bảng cảnh quay (clips do film.js xuất ra), cắt gọn rồi đặt vào lessons/<số bài>/assets/clips/: <id>.mp4 (chỉ lấy đúng đoạn đó, co về kích thước khung, 60 khung hình) + <id>.jpg (ảnh bìa, dùng cho xem trước và contact sheet).
Cách dùng: python3 cine/tools/clips.py <số bài> [--port 8964]
Mỗi mục của clips: {id, src (đường dẫn tuyệt đối), from (giây bắt đầu của phim gốc), dur, at (xuất hiện ở giây thứ mấy của bài này), x, y, w, h, audio: "full"|"duck"|"mute", gain? (dB), fade? (giây, 0=cắt cứng), poster_at? (giây), seg? (chỉ phát seg giây đầu của phim gốc, phần còn lại giữ nguyên khung hình)}"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from browser import launch

ROOT = Path(__file__).resolve().parent.parent.parent


def film_clips(lesson, port):
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(f"http://127.0.0.1:{port}/cine/index.html?lesson={lesson}&capture")
        pg.wait_for_function("window.__film && window.__film.ready", timeout=180000)
        c = pg.evaluate("__film.clips")
        b.close()
    return c


def main():
    lesson = sys.argv[1]
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8964"
    out = ROOT / "lessons" / lesson / "assets" / "clips"
    out.mkdir(parents=True, exist_ok=True)
    clips = film_clips(lesson, port)
    for c in clips:
        mp4, jpg, sig = out / f"{c['id']}.mp4", out / f"{c['id']}.jpg", out / f"{c['id']}.sig"
        w, h = int(c["w"]) // 2 * 2, int(c["h"]) // 2 * 2
        seg = float(c.get("seg", c["dur"]))                       # seg < dur: phim gốc chỉ phát seg giây, sau đó giữ nguyên ở khung hình cuối
        key = f"{c['src']}|{c['from']}|{c['dur']}|{seg}|{w}x{h}"      # điểm bắt đầu, thời lượng, kích thước khung thay đổi thì cắt lại
        if not mp4.exists() or mp4.stat().st_mtime < Path(c["src"]).stat().st_mtime or not sig.exists() or sig.read_text() != key:
            hold = max(0.0, float(c["dur"]) - seg)
            vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=60" + (f",tpad=stop_mode=clone:stop_duration={hold:.3f}" if hold > 0.01 else "")
            af = ["-af", f"apad=pad_dur={hold:.3f}"] if hold > 0.01 else []
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(c["from"]), "-i", c["src"], "-t", f"{seg:.3f}",
                            "-vf", vf, *af, "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(mp4)], check=True)
            sig.write_text(key)
        # Ảnh bìa: mặc định lấy giây thứ 0.4 của đoạn; poster_at=0 lấy khung hình đầu (trong hình ảnh dùng ảnh bìa làm hiệu ứng bay vào trước, khi vào vị trí thì chuyển liền mạch sang video thật)
        pa = float(c.get("poster_at", min(0.4, c["dur"] / 2)))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{pa:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(jpg)], check=True)
        print(f"✓ {c['id']}  {Path(c['src']).name} {c['from']}s+{c['dur']}s → {w}×{h}")
    print(f"→ {out} ({len(clips)} đoạn)")


if __name__ == "__main__":
    main()
