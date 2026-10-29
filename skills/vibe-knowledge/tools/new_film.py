#!/usr/bin/env python3
"""Tạo một kỳ phim ngắn tri thức mới (xây trên engine cine của ai-teardown).

Cách dùng:
  python3 ~/.claude/skills/vibe-knowledge/tools/new_film.py <số kỳ> --template A --title "Định luật Benford" [--ws ~/Desktop/vibe-knowledge] [--series vk]
         [--voice-ref <bản ghi 10–30 giây của bạn.wav>] [--ratio 16:9]

Việc làm:
1. Nếu không gian làm việc / series chưa tồn tại thì gọi new_series.py --style cine của ai-teardown để tạo (engine, phông chữ, công cụ render).
2. Cài kit/know.js vào <series>/cine/engine/, vá cine/tools/record.py, stills.py: sau mỗi lần seek thì await window.__vk.wait() (chờ ảnh, khung video giải mã xong rồi mới chụp).
3. Sao chép mẫu tham chiếu giọng nhân bản vào <series>/voice/host-ref.wav (mặc định assets/voice/default-voice-ref.wav: giọng AI do MiMo thiết kế giọng tạo ra, không phải người thật).
4. lessons/<số kỳ>/: narration.json (khung lời dẫn của khuôn), film.js (khung hình ảnh), facts.md (danh sách sự kiện), assets.json (danh sách tài nguyên Renoise), assets/{img,clips,audio}/.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
AT = Path.home() / ".claude/skills/ai-teardown"
DEFAULT_REF = Path(os.environ.get("VK_VOICE_REF") or Path(__file__).resolve().parents[1] / "assets/voice/default-voice-ref.wav")   # Mặc định: "giọng nam trầm ổn của blogger công nghệ" do AI thiết kế; muốn dùng giọng nhân bản của mình thì truyền --voice-ref hoặc đặt VK_VOICE_REF

SEEK = 'pg.evaluate("(t) => window.__film.seek(t)", t)'
PATCHED = SEEK + '; pg.evaluate("() => window.__vk ? window.__vk.wait() : null")'


def patch_tools(sd: Path):
    for name in ("record.py", "stills.py"):
        p = sd / "cine/tools" / name
        s = p.read_text(encoding="utf-8")
        if "__vk" in s:
            continue
        if SEEK not in s:
            sys.exit(f"{p} không tìm thấy lệnh gọi seek, engine cine đã bị sửa, phải viết lại bản vá")
        p.write_text(s.replace(SEEK, PATCHED), encoding="utf-8")
        print(f"✓ Bản vá: {p.relative_to(sd)}")


FIN_OLD = '"-i", str(m["src"]),'
FIN_NEW = '"-i", str(m["src"] if Path(m["src"]).is_absolute() else ROOT / m["src"]),'


def patch_finish(sd: Path):
    p = sd / "cine/tools/finish.py"
    s = p.read_text(encoding="utf-8")
    if FIN_NEW in s:
        return
    if FIN_OLD not in s:
        sys.exit(f"{p} không tìm thấy cách viết music src, engine cine đã bị sửa, phải viết lại bản vá")
    p.write_text(s.replace(FIN_OLD, FIN_NEW), encoding="utf-8")
    print(f"✓ Bản vá: {p.relative_to(sd)} (src của music có thể ghi đường dẫn tương đối so với thư mục series)")


def patch_bgm(sd: Path):
    # BGM bắt buộc của Vibe Knowledge Showcase (người dùng quy định): khi trộn âm finish.py thấy chưa đặt vibe-bgm thì tự bổ sung, âm lượng hiệu chỉnh theo giọng người
    subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "bgm_force.py"), "--patch", str(sd)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--template", required=True, choices=list("ABCDEF"))
    ap.add_argument("--title", required=True)
    ap.add_argument("--ws", default=str(Path.home() / "Desktop/vibe-knowledge"))
    ap.add_argument("--series", default="vk")
    ap.add_argument("--voice-ref", default=str(DEFAULT_REF))
    a = ap.parse_args()

    ws = Path(a.ws).expanduser().resolve()
    sd = ws / "examples" / a.series
    if not (sd / "cine/engine/core.js").exists():
        subprocess.run([sys.executable, str(AT / "engine/scripts/new_series.py"), str(ws), a.series, "--style", "cine", "--title", "Vibe Knowledge Showcase"], check=True)
        shutil.copytree(AT / "templates/series-cine/tools", sd / "tools", dirs_exist_ok=True)
    shutil.copy(SKILL / "kit/know.js", sd / "cine/engine/know.js")
    patch_tools(sd)
    patch_finish(sd)
    patch_bgm(sd)
    sys.path.insert(0, str(SKILL / "tools")); import patch_earshot; patch_earshot.patch(sd)   # hiệu ứng âm thanh code earshot

    ref = sd / "voice/host-ref.wav"
    src = Path(a.voice_ref).expanduser()
    if not ref.exists() or src.resolve() != ref.resolve():
        if not src.exists():
            sys.exit(f"Không tìm thấy mẫu tham chiếu giọng: {src}")
        ref.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, ref)
        print(f"✓ Mẫu tham chiếu giọng: {src} → {ref.relative_to(ws)}")

    L = sd / "lessons" / a.id
    if L.exists():
        sys.exit(f"Kỳ này đã tồn tại: {L}")
    for d in ("assets/img", "assets/clips", "assets/audio", "build", "stills"):
        (L / d).mkdir(parents=True)
    T = SKILL / "templates"
    narr = (T / f"narration/{a.template}.json").read_text(encoding="utf-8")
    (L / "narration.json").write_text(narr, encoding="utf-8")
    film = (T / "film.skeleton.js").read_text(encoding="utf-8").replace("__TITLE__", a.title).replace("__ID__", a.id).replace("__TPL__", a.template)
    (L / "film.js").write_text(film, encoding="utf-8")
    shutil.copy(T / "facts.md", L / "facts.md")
    shutil.copy(T / "assets.json", L / "assets.json")
    print(f"✓ Kỳ mới: {L}\n  Khuôn {a.template} · {a.title}\n  Bước tiếp: viết facts.md → narration.json → assets.json (báo giá xác nhận) → lồng tiếng → film.js")


if __name__ == "__main__":
    main()
