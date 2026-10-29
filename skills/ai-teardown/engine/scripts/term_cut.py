#!/usr/bin/env python3
"""Cắt bỏ một đoạn chờ trống trong các khung quay màn hình (ví dụ vòng xoay dài trước khi hộp phê duyệt hiện ra): python3 scripts/term_cut.py x.frames.json <điểm-đầu> <điểm-cuối>
Điểm đầu/điểm cuối viết dạng "dấu±giây", như submit+12 approve1-6. Các thay đổi hình ảnh của đoạn bị cắt sẽ gộp thành một khung, các dấu và tổng độ dài cùng dịch lên trước."""
import json, re, sys
p = sys.argv[1]; d = json.load(open(p)); m = d["marks"]
def at(x):
    k, sgn, v = re.match(r"(\w+)([+-])([\d.]+)", x).groups(); return m[k] + (float(v) if sgn == "+" else -float(v))
a0, a1 = at(sys.argv[2]), at(sys.argv[3]); gap = a1 - a0 - 0.8
state, out, cur = {}, [], None
for f in d["frames"]:
    if f["t"] <= a0: out.append(f); continue
    if f["t"] < a1:
        state.update(f["d"]); cur = f["c"]; continue
    if state: out.append({"t": round(a0 + 0.8, 3), "d": state, "c": cur}); state = {}
    out.append({**f, "t": round(f["t"] - gap, 3)})
d["frames"] = out; d["marks"] = {k: (v if v <= a0 else round(v - gap, 3)) for k, v in m.items()}; d["duration"] = round(d["duration"] - gap, 3)
json.dump(d, open(p, "w"), ensure_ascii=False, separators=(",", ":"))
print(f"{p}: đã cắt {gap:.1f} giây, các dấu {d['marks']}")
