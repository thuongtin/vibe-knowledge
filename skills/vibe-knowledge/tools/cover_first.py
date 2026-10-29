#!/usr/bin/env python3
"""Nối ảnh bìa vào đầu phim thành phẩm, làm khung đầu (nền tảng mặc định lấy khung đầu làm ảnh bìa).
python3 cover_first.py <phim thành phẩm.mp4> <ảnh bìa.jpg> <đầu ra.mp4> [--hold 0.5]
Ảnh bìa dừng hold giây rồi cắt cứng vào chính phim; âm thanh đẩy lùi toàn bộ hold giây, phía trước bù im lặng. Khổ hình, tốc độ khung giống phim thành phẩm, ảnh bìa phủ đầy khổ hình và cắt căn giữa."""
import json
import subprocess
import sys


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    a, b = s["r_frame_rate"].split("/")
    return s["width"], s["height"], round(int(a) / int(b))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        sys.exit(__doc__)
    src, cover, out = args
    hold = float(sys.argv[sys.argv.index("--hold") + 1]) if "--hold" in sys.argv else 0.5
    w, h, fps = probe(src)
    ms = round(hold * 1000)
    fc = (f"[1:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps},format=yuv420p,trim=duration={hold}[c];"
          f"[0:v]setsar=1,format=yuv420p[m];[c][m]concat=n=2:v=1:a=0[v];"
          f"[0:a]adelay={ms}:all=1,alimiter=limit=0.79:level=false[a]")   # mã hoá lại AAC sẽ nâng đỉnh 0.5–1 dB, nên giới hạn trước ở khoảng -2 dBFS, sau mã hoá true peak ≤ -1
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-loop", "1", "-framerate", str(fps), "-t", str(hold), "-i", cover,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print(f"→ {out} (ảnh bìa {hold:g} giây + phim chính)")


if __name__ == "__main__":
    main()
