#!/usr/bin/env python3
"""Đề xuất phong cách theo chủ đề: python3 recommend.py "商鞅立木为什么能让人相信新法" [--top 3] [--json]

Chấm điểm: mỗi từ khóa phong cách (keywords trong catalog.json) trúng trong chủ đề được +2 + số chữ (càng cụ thể càng cao, “trà sữa” thắng “trà”), trúng từ chỉ tông điệu +1; phong cách của chính người dùng (~/vibe-knowledge-styles/*/style.json) cũng tham gia và được +1 thêm.
Khi không có từ nào trúng thì bổ sung theo thứ tự FILL (xen kẽ sáng tối, khác họ): Điểm sáng sao trời / Chữ hoa tổng nghệ / Tin tức phụ đề / Bảng phấn …
Kết quả đề xuất bảo đảm ba bộ khác biệt rõ về hình ảnh (cùng một họ fam tối đa 2 bộ, phong cách bản nâng cao được đánh dấu “cần tạo ảnh”), mỗi bộ kèm: lý do (trúng những từ nào), bản gốc đề xuất, bản mẫu, đường dẫn ảnh phong cách.
Sau khi nhận kết quả, Claude dùng AskUserQuestion để hỏi người dùng: mục đề xuất số một xếp đầu và ghi “(khuyến nghị)”, preview của mỗi lựa chọn đặt đường dẫn ảnh phong cách và một câu mô tả hình ảnh."""
import json, sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
CAT = json.loads((SK / "styles/catalog.json").read_text(encoding="utf-8"))
MINE = Path.home() / "vibe-knowledge-styles"


def load_styles():
    out = []
    for s in CAT["styles"]:
        out.append({**s, "still": str(SK / "styles" / s["key"] / "still.jpg"), "mine": False})
    if MINE.exists():
        for d in sorted(MINE.iterdir()):
            f = d / "style.json"
            if f.exists():
                s = json.loads(f.read_text(encoding="utf-8"))
                out.append({**s, "key": d.name, "still": str(d / "still.jpg"), "mine": True})
    return out


def recommend(topic, top=3):
    styles = load_styles()
    scored = []
    for s in styles:
        hits = [k for k in s.get("keywords", []) if len(k) >= 2 and k.lower() in topic.lower()]   # Từ đơn chữ quá dễ trúng nhầm (“thông minh” ≠ nhà Minh), trong catalog luôn viết từ từ hai chữ trở lên
        tone = [k for k in s.get("tone", []) if k in topic]
        score = sum(2 + len(k) for k in hits) + len(tone) + (1 if s["mine"] else 0)
        scored.append((score, s, hits + tone))
    scored.sort(key=lambda x: (-x[0], x[1].get("no", 99)))
    picks, per_cat = [], {}
    for sc, s, hits in scored:                      # Đặt trước những bộ có từ trúng (cùng một loại tối đa 2 bộ)
        if sc <= 0 or len(picks) >= top:
            continue
        fam = s.get("fam", s.get("cat"))
        if per_cat.get(fam, 0) >= 2:
            continue
        picks.append((sc, s, hits)); per_cat[fam] = per_cat.get(fam, 0) + 1
    FILL = ["starfield", "variety", "caption-news", "chalk", "darkgold", "swiss", "titles", "investigation", "journal", "collage", "paper", "isometric", "neon", "minimal", "metro", "darkmath", "memphis", "blueprint", "riso", "ransom", "desktop", "isotype", "keynote", "editorial", "rpg", "silent", "aurora", "vapor", "constructivist", "cards", "gufeng", "pixel", "woodcut", "qinghua", "dunhuang", "scroll", "copper", "farm", "tvnews", "clay", "poster", "deco", "lighttable", "sketch"]
    for k in FILL:   # Rồi bổ sung theo “khác biệt lớn nhất”: xen kẽ sáng tối, không trùng họ
        if len(picks) >= top:
            break
        if k not in {x["key"] for x in styles}:
            continue
        fam = next(x for x in styles if x["key"] == k).get("fam")
        if picks and fam in {p[1].get("fam") for p in picks}:
            continue
        if len(picks) >= top:
            break
        if all(p[1]["key"] != k for p in picks):
            picks.append((0, next(x for x in styles if x["key"] == k), []))
    res = []
    for i, (sc, s, hits) in enumerate(picks[:top]):
        tpl = s.get("templates", ["A"])[0]
        why = f"Chủ đề có “{', '.join(hits[:4])}”, đúng với “{s['fit']}”" if hits else f"Chủ đề không chỉ rõ hướng nào, bộ này phù hợp với “{s['fit']}”, làm phương án dự phòng tạo khác biệt"
        res.append({"rank": i + 1, "key": s["key"], "name": s["name"], "en": s.get("en", ""), "mine": s["mine"], "score": sc,
                    "one": s["one"], "why": why, "template": tpl, "template_name": CAT["templates"].get(tpl, ""),
                    "sample": s.get("sample", ""), "still": s["still"], "fam": s.get("fam", ""), "tier": s.get("tier", "Cơ bản")})
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 3
    if "--top" in sys.argv:
        args = [a for a in args if a != str(top)]
    topic = " ".join(args)
    r = recommend(topic, top)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1)); sys.exit()
    print(f"Chủ đề: {topic}\n")
    for x in r:
        tag = " (khuyến nghị)" if x["rank"] == 1 else ""
        print(f"{x['rank']}. {x['name']}{tag}{' · Phong cách của tôi' if x['mine'] else ''}({x['fam']} · {'bản nâng cao, cần tạo ảnh' if x['tier'] == 'Nâng cao' else '0 điểm'}) — {x['one']}")
        print(f"   Vì sao: {x['why']}")
        print(f"   Bản gốc đi kèm: {x['template']} {x['template_name']}")
        print(f"   Bản mẫu: {x['sample']}  Ảnh phong cách: {x['still']}\n")
