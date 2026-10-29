#!/usr/bin/env python3
"""Chỉnh từng lượt của phiên thật (turnN.jsonl, stream-json) thành turnN.json dùng cho hình ảnh bài học:
câu lệnh, từng lần gọi công cụ (tên + giải thích một câu + số giây tương đối), văn bản nó viết, thời gian dùng của lượt này và chi phí quy đổi.
Tên người dùng máy trong đường dẫn luôn đổi thành ~ (quy tắc che khi quay màn hình).
Cách dùng: python3 session/export.py [lượt…] (mặc định tất cả)"""
import glob
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from common import env, project_logs

HERE = Path(__file__).resolve().parent
HOME = os.path.expanduser("~")


def scrub(s):
    cfg = env().get("SESSION_CONFIG", "")
    if cfg and cfg != os.path.expanduser("~/.claude"):
        s = s.replace(cfg + "/skills/", "~/.claude/skills/")   # symlink skill trong ví dụ khoá học, hiển thị cho học viên thành vị trí chuẩn
    s = s.replace(HOME, "~")
    return re.sub(r"/Users/[A-Za-z0-9._-]+", "~", s)


def short(tool, inp):
    if tool == "Bash":
        return inp.get("description") or inp.get("command", "")[:90]
    if tool in ("Read", "Write", "Edit"):
        return Path(inp.get("file_path", "")).name
    if tool == "Skill":
        return inp.get("skill", "")
    if tool in ("Glob", "Grep"):
        return inp.get("pattern", "")
    return json.dumps(inp, ensure_ascii=False)[:80]


def ts(d):
    t = d.get("timestamp")
    return datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp() if t else None


def export(n):
    src = HERE / f"turn{n}.jsonl"
    if not src.exists():
        return None
    t0 = float((HERE / f"turn{n}.start").read_text().strip())
    events, texts, result = [], [], {}
    for line in src.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "assistant":
            for c in d["message"].get("content", []):
                if c.get("type") == "tool_use":
                    events.append({"kind": "tool", "tool": c["name"], "what": scrub(short(c["name"], c.get("input", {}))),
                                   "cmd": scrub(c.get("input", {}).get("command", ""))[:400] if c["name"] == "Bash" else ""})
                elif c.get("type") == "text" and c["text"].strip():
                    events.append({"kind": "text", "text": scrub(c["text"])})
                    texts.append(scrub(c["text"]))
        elif d.get("type") == "result":
            result = {k: d.get(k) for k in ("duration_ms", "num_turns", "total_cost_usd", "is_error", "subtype")}
    # Thời gian tương đối: stream-json không có dấu thời gian từng mục, dùng thời gian trong bản ghi phiên (jsonl dưới config/projects) để bổ sung
    proj = [str(p) for p in project_logs()]
    stamps = []
    if proj:
        for line in open(proj[-1], encoding="utf-8"):
            d = json.loads(line)
            m = d.get("message") or {}
            if m.get("role") == "assistant" and ts(d) and ts(d) >= t0 - 1:
                for c in m.get("content") or []:
                    if isinstance(c, dict) and c.get("type") in ("tool_use", "text") and (c.get("type") == "tool_use" or c.get("text", "").strip()):
                        stamps.append(round(ts(d) - t0, 1))
    for i, e in enumerate(events):
        e["t"] = stamps[i] if i < len(stamps) else None
    # Khi dùng --continue, total_cost_usd trong result mỗi lượt là giá trị luỹ kế của cả phiên: chi phí lượt này = luỹ kế lượt này − luỹ kế lượt trước
    prev = HERE / f"turn{n - 1}.jsonl"
    if result.get("total_cost_usd") is not None:
        result["cum_cost_usd"] = result["total_cost_usd"]
        pc = 0.0
        if prev.exists():
            for line in prev.read_text(encoding="utf-8").splitlines():
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if d.get("type") == "result":
                    pc = d.get("total_cost_usd") or 0.0
        result["total_cost_usd"] = round(result["cum_cost_usd"] - pc, 4)
    out = {"turn": n, "prompt": (HERE / f"turn{n}.prompt.txt").read_text(encoding="utf-8").strip(),
           "start": datetime.fromtimestamp(t0).strftime("%Y-%m-%d %H:%M"), "events": events, "final": texts[-1] if texts else "", **result}
    (HERE / f"turn{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or sorted(int(re.findall(r"\d+", p.name)[0]) for p in HERE.glob("turn*.jsonl"))
    for n in ns:
        o = export(n)
        if o:
            print(f"turn{n}: {len(o['events'])} sự kiện, mất {o.get('duration_ms', 0) / 1000:.0f}s, quy đổi ${o.get('total_cost_usd') or 0:.2f}")
