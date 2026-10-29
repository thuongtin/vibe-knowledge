#!/usr/bin/env python3
"""Tạo mới một series bài giảng: không gian làm việc (bản sao engine) + khung thư mục series.

Cách dùng:
  python3 new_series.py <thư mục workspace> <tên series> [--style sketch|lesson|cine] [--title tên khóa học]

- Khi workspace chưa tồn tại, sao chép nguyên engine/ đi kèm skill (scripts runtime primitives schemas assets) sang đó.
  make_lesson yêu cầu thư mục bài nằm trong workspace (khi đóng gói tính đường dẫn tương đối theo workspace), nên series luôn đặt ở <workspace>/examples/<tên series>/.
- Đã có workspace (ví dụ ~/Desktop/ai-teardown) thì tạo series ngay trong đó, không ghi đè engine.
- sketch: Notion tối giản + engine vẽ tay + nhân vật giảng giải pixel (bộ của khóa nhập môn WorkBuddy); lesson: trình biên dịch mẫu của mùa một và hai (chủ đề macaron / bạc hà / ban đêm, quay màn hình terminal);
  cine: engine làm phim bằng code (bộ của khóa điều phối Opus 5.5, khóa thực chiến phim quảng bá: một bài = seek(t), Three.js/hạt/đoạn phim thật, xem references/10-cine.md).
"""
import argparse
import json
import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]          # ~/.claude/skills/ai-teardown
ENGINE = SKILL / "engine"
PRESETS = SKILL / "presets"
TEMPLATES = SKILL / "templates"


def new_cine(sd, title):
    """Sao chép engine làm phim bằng code vào thư mục series (tools tìm file theo vị trí tương đối <series>/cine, <series>/lessons), font lấy từ engine/assets/fonts."""
    shutil.copytree(ENGINE / "cine", sd / "cine", ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    (sd / "cine/fonts").mkdir(exist_ok=True)
    for f in ["Geist-VF.ttf", "GeistMono-VF.ttf", "NotoSansSC-VF.ttf"]:
        shutil.copy(ENGINE / "assets/fonts" / f, sd / "cine/fonts" / f)
    (sd / "cine/queue.txt").touch()
    (sd / "cine/deliver.env").write_text(f'# Nơi đến của deliver.sh (cú pháp zsh)\nD="$HOME/Desktop/{title}_视频"\nWEB=publish/course\nSTRIP=""\n', encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("name")
    ap.add_argument("--style", choices=["sketch", "lesson", "cine"], default="sketch")
    ap.add_argument("--title", default="")
    a = ap.parse_args()

    ws = Path(a.workspace).expanduser().resolve()
    if not (ws / "scripts/make_lesson.py").exists():
        ws.mkdir(parents=True, exist_ok=True)
        for d in ["scripts", "runtime", "primitives", "schemas", "assets"]:
            shutil.copytree(ENGINE / d, ws / d, dirs_exist_ok=True)
        print(f"✓ Đã tạo workspace: {ws}")
    else:
        print(f"· Dùng workspace có sẵn: {ws}")

    sd = ws / "examples" / a.name
    if sd.exists():
        raise SystemExit(f"Thư mục series đã tồn tại: {sd}")
    (sd / "lessons").mkdir(parents=True)
    (sd / "voice").mkdir()
    (sd / "publish/course").mkdir(parents=True)
    if a.style == "cine":
        new_cine(sd, a.title or a.name)
    else:
        (sd / "assets/img").mkdir(parents=True)
        (sd / "render.queue").touch()

    tpl = TEMPLATES / {"sketch": "series-sketch", "lesson": "series-lesson", "cine": "series-cine"}[a.style]
    for f in ["BRIEF.md", "SCENES_GUIDE.md", "DECISIONS.md"]:
        if (tpl / f).exists():
            shutil.copy(tpl / f, sd / f)
    if a.style == "cine":
        for d in ["examples-lessons", "examples-briefs", "tools", "session"]:
            shutil.copytree(tpl / d, sd / d)
    else:
        shutil.copytree(tpl / "lessons", sd / "examples-lessons")   # bài hoàn chỉnh để tham chiếu, xem trước khi viết bài mới

    # Nhân vật giảng giải (avatar pixel 10 động tác × 8 khung) + sổ ảnh
    images = []
    if a.style == "cine":
        pass
    elif a.style == "sketch" and (PRESETS / "presenter/images.presenter.json").exists():   # hình tượng nhân vật giảng giải tự chuẩn bị (bản mã nguồn mở không kèm hình tượng của tác giả), xem presets/README.md
        for p in (PRESETS / "presenter").glob("*.png"):
            shutil.copy(p, sd / "assets/img" / p.name)
        images = json.loads((PRESETS / "presenter/images.presenter.json").read_text(encoding="utf-8"))["images"]
    if a.style != "cine":
        (sd / "assets/img/images.json").write_text(json.dumps({"images": images}, ensure_ascii=False, indent=1), encoding="utf-8")

    # Tham chiếu giọng nhân bản đã khóa (trong narration.json, voice.clone ghi "../../voice/host-ref.wav")
    if (PRESETS / "voice/host-ref.wav").exists():
        shutil.copy(PRESETS / "voice/host-ref.wav", sd / "voice/host-ref.wav")

    series = {
        "title": a.title or a.name, "author": "@Berryxia", "status": "draft", "status_label": "Đại cương chờ xác nhận",
        "tagline": "", "facts": [], "lessons_sub": "", "footer": "", "lessons": [],
    }
    (sd / "series.json").write_text(json.dumps(series, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ Khung series: {sd}")
    if a.style == "cine":
        print("Bước tiếp theo: điền đại cương trong series.json → viết lessons/NN/narration.json + film.js theo BRIEF.md → make_lesson voice + speed.py → xem bảng tiếp xúc bằng cine/tools/stills.py → cine/queue.txt + queue.sh (xem references/10-cine.md)")
    else:
        print("Bước tiếp theo: điền đại cương trong series.json → viết lessons/NN/narration.json theo BRIEF.md → make_lesson voice/build/final")


if __name__ == "__main__":
    main()
