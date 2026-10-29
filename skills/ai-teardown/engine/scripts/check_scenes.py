#!/usr/bin/env python3
"""Tự kiểm tra dàn cảnh: mỗi tham chiếu thời gian trong scenes.json (B03 / B03.cue / B03.end, có thể kèm ±giây) phải có nhịp và [[cue]] tương ứng trong narration.json.
Không cần chờ lồng tiếng, viết xong scenes.json là chạy được. Cách dùng: python3 scripts/check_scenes.py <lessonDir>…"""
import json, re, sys
from pathlib import Path

REF = re.compile(r"^(B\d\d)(?:\.([a-z0-9_]+(?:-[a-z][a-z0-9_]*)*))?(?:@[^+-]+)?(?:[+-][\d.]+)?$")

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and (k in ("at", "settle", "hi", "celebrateAt", "titleAt", "questionAt", "eyebrowAt", "peopleOut", "drawnBy", "vsAt", "chatAt", "iconAt", "srcAt", "boxAt", "out") or k.endswith("At")):
                yield f"{path}.{k}", v
            else:
                yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")

ROOT = Path(__file__).resolve().parent.parent
SETS = {}
for f in (ROOT / "assets/iconsets").glob("*.json"):
    j = json.load(open(f)); SETS[j.get("prefix", f.stem)] = set(j["icons"]) | set(j.get("aliases", {}))

def icons(o):
    if isinstance(o, (dict, list)):
        for v in (o.values() if isinstance(o, dict) else o):
            yield from icons(v)
    elif isinstance(o, str) and re.match(r"^[a-z-]+:[a-z0-9-]+$", o): yield o

bad = 0
for d in map(Path, sys.argv[1:]):
    beats = {b["id"]: set(re.findall(r"\[\[([a-z0-9_-]+)\]\]", b["narration"])) for b in json.load(open(d / "narration.json"))["beats"]}
    spec = json.load(open(d / "scenes.json"))
    order = []
    for p, v in walk(spec):
        m = REF.match(v)
        if not m: print(f"{d.name} {p}: không hiểu {v!r}"); bad += 1; continue
        b, cue = m.groups()
        if b not in beats: print(f"{d.name} {p}: không có nhịp này {b}"); bad += 1
        elif cue and cue not in ("end", "cue") and cue not in beats[b]: print(f"{d.name} {p}: {b} không có [[{cue}]] (có: {' '.join(sorted(beats[b]))})"); bad += 1
    for ic in set(icons(spec)):
        pre, name = ic.split(":")
        if pre in SETS and name not in SETS[pre]: print(f"{d.name}: thư viện biểu tượng không có {ic}"); bad += 1
    tj = d / "build" / "timings.json"
    if tj.exists():  # Khi đã có thời gian lồng tiếng, kiểm tra lại: cảnh quá ngắn, khán giả không kịp xem
        TJ = json.load(open(tj)); T = TJ["beats"]; SPD = TJ.get("speed", 1)
        T = T if isinstance(T, dict) else {b["id"]: b for b in T}
        def when(r):
            m = re.match(r"^(B\d\d)(?:\.([a-z0-9_]+(?:-[a-z][a-z0-9_]*)*))?(?:@([^+-]+))?([+-][\d.]+)?$", r)
            b, cue, word, off = m.groups(); B = T[b]
            if word:  # "B03@máy": khoảnh khắc đọc đến từ này (khớp với W() trong lesson.js)
                i = B["text"].find(word)
                base = B["chars"][i] if i >= 0 and B.get("chars") else B["start"]
                if i < 0: print(f"{d.name}: {b} lời dẫn không có '{word}'")
            else:
                base = B["end"] if cue == "end" else B["cues"].get(cue, B["start"]) if cue else B["start"]
            return base + float(off or 0) / SPD
        ts = [when(sc["at"]) for sc in spec["scenes"]] + [max(B["end"] for B in T.values())]
        for k, sc in enumerate(spec["scenes"]):
            if ts[k + 1] - ts[k] < 2.5: print(f"{d.name}: cảnh thứ {k} ({sc['t']} @ {sc['at']}) chỉ có {ts[k+1]-ts[k]:.1f} giây"); bad += 1
            if ts[k + 1] < ts[k]: print(f"{d.name}: cảnh thứ {k + 1} còn sớm hơn cảnh trước"); bad += 1
    starts = [s["at"] for s in spec["scenes"]]
    print(f"{d.name}: {len(spec['scenes'])} cảnh, phủ {len({s.split('.')[0][:3] for s in starts})}/{len(beats)} điểm bắt đầu của nhịp")
sys.exit(1 if bad else 0)
