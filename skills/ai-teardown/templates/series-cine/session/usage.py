#!/usr/bin/env python3
"""Tổng hợp mức sử dụng của phiên thật: số lượt, lệnh gọi công cụ, token, quy đổi theo giá API Opus 5.5 ($4 đầu vào / $20 đầu ra / $0.20 đọc cache / $8 ghi cache, mỗi triệu token).
Claude Code dùng cache 1 giờ, ghi cache tính gấp 2 lần giá đầu vào (khớp với total_cost_usd do chính nó báo). Khi cùng một phản hồi bị tách thành nhiều dòng bản ghi thì chỉ tính một lần theo message id.
Cách dùng: python3 session/usage.py > session/usage.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import project_logs
fs = [str(p) for p in project_logs()]
if not fs: sys.exit("Chưa có bản ghi phiên")
u = dict(input_tokens=0, output_tokens=0, cache_read_input_tokens=0, cache_creation_input_tokens=0); msgs = tools = 0; ts = []; models = set()
seen = set()
for f in fs:
    for line in open(f):
        d = json.loads(line)
        if "timestamp" in d: ts.append(d["timestamp"])
        m = d.get("message") or {}
        if m.get("role") != "assistant": continue
        mid = m.get("id")
        models.add(m.get("model"))
        for c in m.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use": tools += 1
        if mid in seen: continue          # cùng một phản hồi bị tách thành nhiều dòng bản ghi thì chỉ tính một lần
        seen.add(mid); msgs += 1
        for k in u: u[k] += (m.get("usage") or {}).get(k, 0) or 0
cost = u["input_tokens"] * 4e-6 + u["output_tokens"] * 20e-6 + u["cache_read_input_tokens"] * 0.2e-6 + u["cache_creation_input_tokens"] * 8e-6
print(json.dumps({"files": [os.path.basename(f) for f in fs], "models": sorted(x for x in models if x), "assistant_msgs": msgs, "tool_calls": tools,
                  "first": ts[0] if ts else None, "last": ts[-1] if ts else None, **u, "api_equiv_usd": round(cost, 2)}, ensure_ascii=False, indent=1))
