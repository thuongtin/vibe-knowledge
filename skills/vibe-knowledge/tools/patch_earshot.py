#!/usr/bin/env python3
"""Vá finish.py của cine để thêm "hiệu ứng âm thanh bằng mã earshot" (new_film.py tự gọi khi tạo series; cũng có thể chạy riêng: python3 patch_earshot.py <thư mục series>).

Sau khi vá, mục music của film.js có thể viết:
  { src: "earshot:cut_hit/punch", at: 12.3, align: "peak", gain: -8, es: { seed: 2, dur: 0.4, apex: null, pitch: "G1" } }
- finish.py trước tiên giao tất cả mục earshot cho ~/.claude/skills/vibe-knowledge/tools/earshot_render.py (chạy bằng venv riêng của earshot),
  kết quả kết xuất được lưu đệm theo băm tham số trong lessons/<bài>/build/esfx/;
- align: "onset" (mặc định, điểm khởi âm rơi vào at) hoặc "peak" (điểm to nhất rơi vào at: tiếng vút, chũm chọe ngược, âm đi lên dùng cái này);
- Mặc định không bị hạ nhỏ theo lời dẫn (duck: false), muốn hạ thì viết duck: true.
Biến môi trường: EARSHOT_PY (python của venv earshot, mặc định ~/tools/earshot/.venv/bin/python), EARSHOT_TOOL (đường dẫn kịch bản kết xuất)."""
import sys
from pathlib import Path

MARK = "# earshot code sfx (vibe-knowledge patch_earshot)"
# Dấu cũ (bản tiếng Trung) để nhận ra finish.py đã được vá từ trước
OLD_MARK = "# earshot \u4ee3\u7801\u97f3\u6548\uff08vibe-knowledge patch_earshot\uff09"

OLD_LOOP = """    for m in info.get("music", []):
        tmp = B / "_music.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{float(m.get('from', 0)):.3f}", "-t", f"{float(m['dur']):.3f}", "-i", str(m["src"] if Path(m["src"]).is_absolute() else ROOT / m["src"]),"""
NEW_LOOP = """    """ + MARK + """: các mục có src viết "earshot:<id>" được kết xuất trước (lưu đệm theo băm tham số), rồi căn theo onset / peak vào at
    import hashlib, os
    es_jobs = []
    for m in info.get("music", []):
        if str(m.get("src", "")).startswith("earshot:"):
            o = m.get("es") or {}
            j = {"id": str(m["src"])[8:], "seed": o.get("seed"), "dur": o.get("dur"), "apex": o.get("apex"), "pitch": o.get("pitch")}
            j["key"] = hashlib.md5(json.dumps(j, sort_keys=True).encode()).hexdigest()[:12]
            m["_es"] = j
            if j not in es_jobs:
                es_jobs.append(j)
    if es_jobs:
        esd = B / "esfx"; esd.mkdir(exist_ok=True)
        (esd / "jobs.json").write_text(json.dumps(es_jobs, ensure_ascii=False), encoding="utf-8")
        py = os.environ.get("EARSHOT_PY", str(Path.home() / "tools/earshot/.venv/bin/python"))
        tool = os.environ.get("EARSHOT_TOOL", str(Path.home() / ".claude/skills/vibe-knowledge/tools/earshot_render.py"))
        subprocess.run([py, tool, str(esd / "jobs.json"), str(esd)], check=True, env={**os.environ, "PYTHONPATH": ""})
        for m in info.get("music", []):
            if "_es" in m:
                meta = json.loads((esd / f"{m['_es']['key']}.json").read_text(encoding="utf-8"))
                lead = float(meta.get("peak_s" if m.get("align") == "peak" else "onset_s") or 0)
                m["src"] = str(esd / f"{m['_es']['key']}.wav")
                m["dur"] = float(meta.get("dur_s") or m.get("dur", 3))
                m["from"] = max(0.0, lead - float(m["at"]))          # khi at quá sớm thì cắt từ giữa tệp
                m["at"] = max(0.0, float(m["at"]) - lead)
                m.setdefault("fade_in", 0.0); m.setdefault("fade_out", 0.02)
                print(f"  earshot {meta.get('id')} → {m['at']:.3f}s({m.get('align', 'onset')} căn, sớm {lead * 1000:.0f} ms)")
    for m in info.get("music", []):
        tmp = B / "_music.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{float(m.get('from', 0)):.3f}", "-t", f"{float(m['dur']):.3f}", "-i", str(m["src"] if Path(m["src"]).is_absolute() else ROOT / m["src"]),"""

OLD_ADD = """            clipa[j0:j1] += a[: j1 - j0] * (g * duck[j0:j1])[:, None]"""
NEW_ADD = """            dk = duck[j0:j1] if m.get("duck", "_es" not in m) else 1.0   # âm thanh earshot mặc định không hạ nhỏ
            clipa[j0:j1] += a[: j1 - j0] * (g * dk)[:, None]"""


def patch(series_dir):
    p = Path(series_dir) / "cine/tools/finish.py"
    s = p.read_text(encoding="utf-8")
    if MARK in s or OLD_MARK in s:
        return False
    if OLD_LOOP not in s or OLD_ADD not in s:
        sys.exit(f"{p}: không tìm thấy vòng lặp nhạc nền cần thay, finish.py đã bị sửa, patch_earshot.py phải sửa theo (trước hết xác nhận đã vá đường dẫn tương đối music src)")
    p.write_text(s.replace(OLD_LOOP, NEW_LOOP, 1).replace(OLD_ADD, NEW_ADD, 1), encoding="utf-8")
    print(f"✓ Bản vá: {p} (hiệu ứng âm thanh bằng mã earshot)")
    return True


if __name__ == "__main__":
    patch(sys.argv[1])
