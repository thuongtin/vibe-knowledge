#!/usr/bin/env python3
"""Render lesson.json thành dàn ý và phân cảnh để con người xác nhận (dùng cho CP1): python3 scripts/outline.py examples/codex
Xuất <chủ đề>/lesson/outline.md. Mọi nội dung đều đọc từ file dữ liệu, muốn sửa dàn ý thì sửa lesson.json rồi tạo lại."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check import spoken_len  # noqa: E402

MOVE = {"hook": "Móc câu", "ask": "Hỏi", "show": "Diễn", "name": "Gọi tên", "place": "Quy vị", "compare": "So sánh",
        "recap": "Thu lại", "quiz": "Kiểm tra nhỏ", "transition": "Chuyển tiếp", "end": "Cuối phim"}
CUE_RE = re.compile(r"\[\[([a-z][a-z0-9_-]*)\]\]")


def visual_desc(v):
    p = v.get("params", {})
    bits = [v["primitive"]]
    if v.get("ui_mock"):
        bits.append("Giao diện minh hoạ")
    if v.get("honesty", "official") != "official":
        bits.append({"inferred": "Suy đoán", "undisclosed": "Chưa công bố"}[v["honesty"]])
    if v["primitive"] == "Morph":
        bits.append(" → ".join(s["kind"] for s in p.get("states", [])))
    elif p.get("chips"):
        bits.append(", ".join(p["chips"]))
    elif p.get("gates"):
        bits.append("Cổng: " + ", ".join(g["label"] for g in p["gates"]))
    elif p.get("steps"):
        bits.append(" → ".join(p["steps"]))
    if v.get("camera"):
        bits.append(f"Ống kính {v['camera'].get('focus', '')} ×{v['camera'].get('zoom', '')}")
    return ": ".join([bits[0], " · ".join(bits[1:])]) if len(bits) > 1 else bits[0]


def main():
    base = Path(sys.argv[1]).resolve()
    L = json.loads((base / "lesson/lesson.json").read_text(encoding="utf-8"))
    C = json.loads((base / "lesson/concepts.json").read_text(encoding="utf-8"))
    F = {f["id"]: f for f in json.loads((base / "research/facts.json").read_text(encoding="utf-8"))["facts"]}
    S = {s["id"]: s for s in json.loads((base / "research/sources.json").read_text(encoding="utf-8"))["sources"]}
    pace = L["meta"].get("pace_cps", 3.5)
    beats = {b["id"]: b for b in L["beats"]}
    total = sum(spoken_len(b["narration"]) / pace + 0.35 for b in L["beats"])
    cons = {c["id"]: c for c in C["concepts"]}

    out = [f"# {L['meta']['title']} · Dàn ý và phân cảnh", "",
           f"Thông tin tính đến {L['meta']['as_of']} · {L['meta']['aspect']} · dự kiến {total:.0f} giây · {len(L['beats'])} nhịp · {len(L['chapters'])} chương · lồng tiếng {L['meta']['voice']}",
           "", "> Do `scripts/outline.py` tạo từ `lesson.json`, dùng để xác nhận CP1. ⟨tên⟩ trong lời dẫn là vị trí căn hành động hình ảnh.", ""]
    t = 0.0
    for ch in L["chapters"]:
        secs = sum(spoken_len(beats[i]["narration"]) / pace + 0.35 for i in ch["beats"])
        out += [f"## {ch['id']} {ch['title']}({ch['level']}, khoảng {secs:.0f} giây)", "",
                "| Nhịp | Bắt đầu | Thủ pháp | Lời dẫn | Hình ảnh | Khái niệm mới | Nguồn |", "|---|---|---|---|---|---|---|"]
        for i in ch["beats"]:
            b = beats[i]
            nar = CUE_RE.sub(lambda m: f"⟨{m.group(1)}⟩", b["narration"]).replace("|", "/")
            con = cons[b["concept"]]["term"] if b.get("concept") else ""
            out.append(f"| {b['id']} | {int(t // 60)}:{int(t % 60):02d} | {MOVE[b['move']]} | {nar} | {visual_desc(b['visual'])} | {con} | {' '.join(b['facts']) or '—'} |")
            t += spoken_len(b["narration"]) / pace + 0.35
        out.append("")
    out += ["## Khái niệm và điều kiện tiên quyết", "", "| Khái niệm | Tầng | Một câu dễ hiểu | Tiên quyết |", "|---|---|---|---|"]
    out += [f"| {c['id']} {c['term']} | {c['level']} | {c['plain']} | {' '.join(c['prereqs']) or '—'} |" for c in C["concepts"]]
    out += ["", "## Hiểu lầm thường gặp", ""]
    out += [f"- **{m['myth']}** → {m['truth']} ({' '.join(m['facts'])})" for m in C.get("misconceptions", [])]
    out += ["", "## Mục tiêu học tập (câu hỏi kiểm tra mù khi đọc lạnh)", ""]
    out += [f"{i + 1}. {q['question']}  \n   Đáp án tham khảo: {q['answer']}" for i, q in enumerate(C["objectives"])]
    used = sorted({f for b in L["beats"] for f in b["facts"]})
    out += ["", f"## Các sự kiện được trích dẫn ({len(used)} mục)", "", "| Sự kiện | Nội dung | Nguồn |", "|---|---|---|"]
    for fid in used:
        f = F[fid]
        src = "; ".join(f"{S[e['source']]['publisher']} · {S[e['source']]['title']}" for e in f["evidence"])
        out.append(f"| {fid} | {f['claim']} | {src} |")
    (base / "lesson/outline.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"→ {base / 'lesson/outline.md'} (dự kiến {total:.0f} giây)")


if __name__ == "__main__":
    main()
