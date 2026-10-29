#!/usr/bin/env python3
"""ai-teardown kiểm tra hợp đồng dữ liệu: schema + nhất quán giữa các file + cổng sự thật + cấu trúc sư phạm.

Cách dùng:
    python3 scripts/check.py examples/codex          # kiểm tra các file đã có trong một thư mục chủ đề
    python3 scripts/check.py examples/codex --only facts

Quy ước thư mục (thiếu cái nào thì bỏ qua cái đó):
    brief.json
    research/sources.json   research/facts.json   research/snapshots/
    lesson/concepts.json    lesson/lesson.json

Mã thoát: có ERROR thì là 1, ngược lại 0. WARN không chặn.
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover
    sys.exit("Thiếu jsonschema: python3 -m pip install --break-system-packages jsonschema")

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
CUE_RE = re.compile(r"\[\[([a-z][a-z0-9_-]*)\]\]")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
CUE_REQUIRED_PRIMS = {"Terminal", "ChatUI", "CodeDiff", "Morph"}
FACT_MOVES = {"show", "name", "place", "compare", "recap"}
INFER_WORDS = ("推断", "可能", "据推测", "大概率", "看起来")
UNDISCLOSED_WORDS = ("未公开", "未披露", "没有公开", "没公开", "不公开", "官方没说")


class Report:
    def __init__(self):
        self.errors, self.warns = [], []

    def err(self, where, msg):
        self.errors.append(f"ERROR {where}: {msg}")

    def warn(self, where, msg):
        self.warns.append(f"WARN  {where}: {msg}")

    def dump(self):
        for line in self.errors + self.warns:
            print(line)
        print(f"\n{len(self.errors)} ERROR, {len(self.warns)} WARN")
        return 1 if self.errors else 0


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def schema_check(rep, name, data):
    schema = load(SCHEMAS / f"{name}.schema.json")
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    for e in sorted(v.iter_errors(data), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in e.path) or "(gốc)"
        rep.err(f"{name}.json {loc}", e.message)


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def quote_found(quote, text):
    q, t = norm(quote), norm(text)
    if q in t:
        return True
    if len(q) > 160:  # trích dẫn dài: đầu và cuối mỗi bên 70 ký tự đều có mặt là đạt
        return q[:70] in t and q[-70:] in t
    return False


def ids(items, key="id"):
    return [it[key] for it in items]


def dupes(values):
    seen, out = set(), set()
    for v in values:
        (out if v in seen else seen).add(v)
    return sorted(out)


LATIN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+#_-]*")


def spoken_len(text):
    """Ước tính độ dài đọc (quy đổi theo chữ): chữ Hán tính 1, từ tiếng Anh hoặc chuỗi số tính 1,5 (đo thực tế với edge-tts)."""
    text = CUE_RE.sub("", text)
    latin = LATIN_RE.findall(text)
    text = LATIN_RE.sub("", text)
    return sum(1 for ch in text if not unicodedata.category(ch).startswith(("P", "Z", "S"))) + 1.5 * len(latin)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    base = Path(args[0]).resolve()
    only = args[args.index("--only") + 1] if "--only" in args else None
    rep = Report()

    files = {
        "brief": base / "brief.json",
        "sources": base / "research" / "sources.json",
        "facts": base / "research" / "facts.json",
        "concepts": base / "lesson" / "concepts.json",
        "lesson": base / "lesson" / "lesson.json",
    }
    data = {}
    for name, path in files.items():
        if only and name != only:
            continue
        if path.exists():
            try:
                data[name] = load(path)
            except json.JSONDecodeError as e:
                rep.err(path.name, f"Phân tích JSON thất bại: {e}")
                continue
            schema_check(rep, name, data[name])
    if not data:
        sys.exit(f"{base} không có file nào để kiểm tra")

    # ---------- sources ----------
    src_by_id = {}
    if "sources" in data:
        srcs = data["sources"]["sources"]
        for d in dupes(ids(srcs)):
            rep.err("sources", f"id trùng {d}")
        for s in srcs:
            src_by_id[s["id"]] = s
            snap = base / "research" / s["snapshot"]
            if not snap.exists():
                rep.err(f"sources {s['id']}", f"Snapshot không tồn tại: {s['snapshot']}")
                continue
            if "sha256" in s:
                h = hashlib.sha256(snap.read_bytes()).hexdigest()
                if h != s["sha256"]:
                    rep.warn(f"sources {s['id']}", "Hash snapshot không khớp, nguồn có thể đã bị thu thập lại")
            if s["tier"] == "T1" and s["kind"] in ("social", "media"):
                rep.warn(f"sources {s['id']}", f"kind={s['kind']} được gắn T1, hãy xác nhận là tài khoản hoặc kênh chính thức")

    # ---------- facts ----------
    fact_by_id = {}
    if "facts" in data:
        facts = data["facts"]["facts"]
        for d in dupes(ids(facts)):
            rep.err("facts", f"id trùng {d}")
        snap_text = {}
        for f in facts:
            fact_by_id[f["id"]] = f
            where = f"facts {f['id']}"
            tiers = []
            for ev in f.get("evidence", []):
                s = src_by_id.get(ev["source"])
                if not s:
                    if src_by_id:
                        rep.err(where, f"tham chiếu tới nguồn không tồn tại {ev['source']}")
                    continue
                tiers.append(s["tier"])
                if s["id"] not in snap_text:
                    p = base / "research" / s["snapshot"]
                    snap_text[s["id"]] = p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""
                if snap_text[s["id"]] and not quote_found(ev["quote"], snap_text[s["id"]]):
                    rep.err(where, f"Trích dẫn không tìm thấy trong snapshot {s['id']}: {ev['quote'][:40]}…")
            st = f["status"]
            if src_by_id:
                if st == "verified" and "T1" not in tiers and tiers.count("T2") < 2:
                    rep.err(where, "verified cần ít nhất một T1, hoặc hai T2")
                if f["category"] == "how" and st in ("verified", "single-source") and "T1" not in tiers:
                    rep.err(where, "Nói về cơ chế (how) bắt buộc phải có T1; nếu không có thì gắn inferred hoặc undisclosed")
                if tiers and set(tiers) == {"T3"} and st != "inferred":
                    rep.warn(where, "Chỉ có nguồn T3, chỉ dùng làm bằng chứng phụ")
            if st in ("conflict", "inferred", "undisclosed") and not f.get("notes"):
                rep.err(where, f"status={st} bắt buộc phải ghi giải thích trong notes")
            if f["category"] == "number" and not f.get("numbers"):
                rep.err(where, "category=number bắt buộc phải điền numbers")
            if f.get("supersedes") and f["supersedes"] not in {x["id"] for x in facts}:
                rep.warn(where, f"supersedes trỏ tới mục không tồn tại {f['supersedes']}")

    # ---------- concepts ----------
    concept_by_id, node_ids = {}, set()
    if "concepts" in data:
        c = data["concepts"]
        nodes = c["master_map"]["nodes"]
        node_ids = set(ids(nodes))
        for d in dupes(ids(nodes)):
            rep.err("concepts", f"id nút sơ đồ tổng trùng {d}")
        for n in nodes:
            if n.get("parent") and n["parent"] not in node_ids:
                rep.err(f"concepts nút {n['id']}", f"parent {n['parent']} không tồn tại")
        for e in c["master_map"]["edges"]:
            for end in ("from", "to"):
                if e[end] not in node_ids:
                    rep.err("concepts đường nối", f"{e['from']}→{e['to']} {end} không tồn tại")
        concepts = c["concepts"]
        for d in dupes(ids(concepts)):
            rep.err("concepts", f"id khái niệm trùng {d}")
        concept_by_id = {x["id"]: x for x in concepts}
        for x in concepts:
            for p in x["prereqs"]:
                if p not in concept_by_id:
                    rep.err(f"concepts {x['id']}", f"tiên quyết {p} không tồn tại")
            if x.get("node") and x["node"] not in node_ids:
                rep.err(f"concepts {x['id']}", f"node {x['node']} không có trong sơ đồ tổng")
        # phát hiện vòng
        state = {}

        def visit(cid, stack):
            state[cid] = 1
            for p in concept_by_id.get(cid, {}).get("prereqs", []):
                if state.get(p) == 1:
                    rep.err("concepts", f"Quan hệ tiên quyết tạo thành vòng: {' → '.join(stack + [p])}")
                elif p in concept_by_id and not state.get(p):
                    visit(p, stack + [p])
            state[cid] = 2

        for cid in concept_by_id:
            if not state.get(cid):
                visit(cid, [cid])
        for q in c["objectives"]:
            for cid in q["concepts"]:
                if cid not in concept_by_id:
                    rep.err(f"concepts {q['id']}", f"Mục tiêu học tập tham chiếu tới khái niệm không tồn tại {cid}")
        refs = [(f"concepts nút {n['id']}", n.get("facts", [])) for n in nodes]
        refs += [(f"concepts {x['id']}", x["facts"]) for x in concepts]
        refs += [(f"concepts {m['id']}", m["facts"]) for m in c.get("misconceptions", [])]
        if fact_by_id:
            for where, fl in refs:
                for fid in fl:
                    if fid not in fact_by_id:
                        rep.err(where, f"tham chiếu tới sự thật không tồn tại {fid}")

    # ---------- lesson ----------
    if "lesson" in data:
        L = data["lesson"]
        beats, chapters = L["beats"], L["chapters"]
        for d in dupes(ids(beats)):
            rep.err("lesson", f"beat id trùng {d}")
        for d in dupes(ids(chapters)):
            rep.err("lesson", f"id chương trùng {d}")
        order = ids(beats)
        listed = [b for ch in chapters for b in ch["beats"]]
        if listed != order:
            rep.err("lesson", "chapters[].beats nối lại phải có thứ tự hoàn toàn giống beats")
        ch_of = {b: ch["id"] for ch in chapters for b in ch["beats"]}
        introduced = {}
        total_chars = 0
        pace = L["meta"].get("pace_cps", 3.5)
        for i, b in enumerate(beats):
            where = f"lesson {b['id']}"
            if ch_of.get(b["id"]) != b["chapter"]:
                rep.err(where, f"trường chapter là {b['chapter']}, nhưng nó được liệt kê trong {ch_of.get(b['id'])}")
            names = CUE_RE.findall(b["narration"])
            declared = [c["name"] for c in b.get("cues", [])]
            for n in set(names) - set(declared):
                rep.err(where, f"[[{n}]] trong lời dẫn không có cue tương ứng")
            for n in set(declared) - set(names):
                rep.err(where, f"cue {n} không được đánh dấu trong lời dẫn")
            total_chars += spoken_len(b["narration"])
            prim = b["visual"]["primitive"]
            if prim in CUE_REQUIRED_PRIMS and not b["visual"].get("ui_mock"):
                rep.warn(where, f"{prim} tái hiện giao diện, visual.ui_mock phải là true")
            if b["move"] in FACT_MOVES and not b["facts"]:
                rep.err(where, f"move={b['move']} bắt buộc phải gắn sự thật")
            # thứ tự khái niệm
            cid = b.get("concept")
            if cid:
                if concept_by_id and cid not in concept_by_id:
                    rep.err(where, f"khái niệm {cid} không có trong concepts.json")
                elif cid in introduced:
                    rep.warn(where, f"khái niệm {cid} đã được giới thiệu ở {introduced[cid]}")
                else:
                    for p in concept_by_id.get(cid, {}).get("prereqs", []):
                        if p not in introduced:
                            rep.err(where, f"Trước khi giới thiệu {cid}, khái niệm tiên quyết {p} chưa được giảng")
                    introduced[cid] = b["id"]
            # cổng sự thật
            ref_text = ""
            for fid in b["facts"]:
                f = fact_by_id.get(fid)
                if not f:
                    if fact_by_id:
                        rep.err(where, f"tham chiếu tới sự thật không tồn tại {fid}")
                    continue
                ref_text += f["claim"] + " " + " ".join(n["value"] for n in f.get("numbers", [])) + " "
                hon = b["visual"].get("honesty", "official")
                if f["status"] == "inferred" and hon != "inferred" and not any(w in b["narration"] for w in INFER_WORDS):
                    rep.err(where, f"{fid} là suy đoán, hình ảnh phải gắn inferred hoặc lời dẫn phải nói rõ là suy đoán")
                if f["status"] == "undisclosed" and hon != "undisclosed" and not any(w in b["narration"] for w in UNDISCLOSED_WORDS):
                    rep.err(where, f"{fid} là chưa được công bố, hình ảnh phải gắn undisclosed hoặc lời dẫn phải nói rõ")
            if fact_by_id:
                spoken = CUE_RE.sub("", b["narration"])
                as_of = L["meta"].get("as_of", "")
                allowed = set(as_of.split("-")) | {p.lstrip("0") for p in as_of.split("-")}
                for num in NUM_RE.findall(spoken):
                    if num not in ref_text and num not in allowed:
                        rep.err(where, f"Số {num} trong lời dẫn không tìm thấy trong các sự thật được tham chiếu")
        if concept_by_id:
            ceiling = data.get("brief", {}).get("depth_ceiling", "L5")
            for cid, x in concept_by_id.items():
                if cid not in introduced and x["level"] <= ceiling:
                    rep.warn("lesson", f"khái niệm {cid} ({x['term']}) nằm trong giới hạn độ sâu {ceiling}, nhưng không có beat nào giới thiệu nó")
        est = total_chars / pace
        target = data.get("brief", {}).get("duration_s")
        print(f"Bản thuyết minh khoảng {total_chars:.0f} đơn vị chữ, với {pace} chữ/giây thì khoảng {est:.0f} giây" + (f"(mục tiêu {target} giây)" if target else ""))
        if target and abs(est - target) / target > 0.15:
            rep.warn("lesson", f"Thời lượng dự kiến {est:.0f} giây, lệch khỏi mục tiêu {target} giây quá 15%")

    sys.exit(rep.dump())


if __name__ == "__main__":
    main()
