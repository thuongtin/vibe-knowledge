#!/usr/bin/env python3
"""Đề xuất độ dài theo độ phức tạp của chủ đề (quy tắc xem references/13-duration.md).
python3 duration.py --scores khainiem,kienthuc,nhanqua,bangchung,baidong [--template A-F] [--pick tên bậc hoặc số giây] [--json]
Năm mục, mỗi mục 0–2 điểm. In ra độ phức tạp, bậc đề xuất, bốn lựa chọn độ dài (bậc đề xuất xếp đầu, có thể đưa thẳng vào AskUserQuestion).
--pick truyền bậc người dùng chọn (Lướt nhanh/Giảng sâu/Tiêu chuẩn/Đào sâu, vẫn nhận 速览/精讲/标准/深挖) hoặc số giây, kiểm tra có lệch quá nhiều so với độ phức tạp không, lệch từ hai bậc trở lên sẽ in nhắc nhở."""
import json
import sys

DIMS = ["Số khái niệm", "Kiến thức nền", "Chuỗi nhân quả", "Mật độ bằng chứng", "Bất đồng/đảo ngược"]
TIERS = [
    {"name": "Lướt nhanh", "range": "45–60 giây", "sec": (45, 60), "beats": "5–7", "dots": "●○○○",
     "can": "một móc câu + một kết luận + một ví dụ + câu hỏi ngược", "cut": "tiền đề, triển khai nguồn, nhóm đối chứng, đảo ngược nhiều nhất một câu"},
    {"name": "Giảng sâu", "range": "1:30–2:00", "sec": (90, 120), "beats": "7–9", "dots": "●●○○",
     "can": "kể xong mạch chính + 1 bằng chứng then chốt + 1 lần đảo ngược", "cut": "bằng chứng thứ hai, đối chiếu lịch sử, uốn nắn hiểu lầm"},
    {"name": "Tiêu chuẩn", "range": "2:30–3:00", "sec": (150, 180), "beats": "10–12", "dots": "●●●○",
     "can": "mạch chính + 2–3 bằng chứng + 1 lần đảo ngược + nhóm đối chứng + câu hỏi ngược", "cut": "các khâu thứ yếu trong chuỗi nhân quả, hai thuyết song song chỉ giữ một chỗ"},
    {"name": "Đào sâu", "range": "3:30–5:00", "sec": (210, 300), "beats": "14–20", "dots": "●●●●",
     "can": "chuỗi nhân quả đầy đủ (mỗi bước một bằng chứng hình ảnh) + hai thuyết song song + uốn nắn hiểu lầm + mở rộng", "cut": "về cơ bản không cắt, mỗi chương một cảnh bom tấn để chống mệt mỏi"},
]
HABIT = {"A": "thông lệ phim khái niệm đoán đố 3:30–4:30", "B": "thông lệ series phim lưỡng nan khoảng 2:55", "C": "thông lệ phim nỗi đau + nguyên lý 2:00–2:30",
         "D": "thông lệ phim một mạch chính khoảng 3:00", "E": "thông lệ phim vượt ải 4–6 phút", "F": "thông lệ phim sáu mặt xoay vòng 45–60 giây"}
CPS = 5.5  # chữ/giây của phim thành phẩm (giới hạn dưới), giới hạn trên là 6


def words(t):
    a, b = t["sec"]
    return f"{round(a * CPS / 10) * 10}–{round(b * 6 / 10) * 10}"


def level(score):
    return (0, "đơn giản") if score <= 3 else (1, "trung bình") if score <= 6 else (2, "phức tạp")


def recommend(score, evid):
    lv = level(score)[0]
    if lv == 0:
        return 0 if evid == 0 else 1
    return 2 if lv == 1 else 3


def tier_of(pick):
    ALIAS = {"速览": 0, "精讲": 1, "标准": 2, "深挖": 3}
    if pick in ALIAS:
        return ALIAS[pick]
    for i, t in enumerate(TIERS):
        if pick.lower() == t["name"].lower():
            return i
    s = float(pick)
    return min(range(4), key=lambda i: 0 if TIERS[i]["sec"][0] <= s <= TIERS[i]["sec"][1] else min(abs(s - x) for x in TIERS[i]["sec"]))


def main():
    a = sys.argv
    if "--scores" not in a:
        sys.exit(__doc__)
    sc = [int(x) for x in a[a.index("--scores") + 1].split(",")]
    if len(sc) != 5 or any(x not in (0, 1, 2) for x in sc):
        sys.exit("--scores cần 5 số nguyên 0–2, thứ tự: " + ", ".join(DIMS))
    tpl = a[a.index("--template") + 1].upper() if "--template" in a else None
    total = sum(sc); lv, lname = level(total); rec = recommend(total, sc[3])
    order = [rec] + [i for i in range(4) if i != rec]
    opts = []
    for i in order:
        t = TIERS[i]
        desc = f"khoảng {words(t)} chữ · {t['beats']} nhịp · độ tỉ mỉ {t['dots']} | nói được đến: {t['can']} | phải cắt: {t['cut']}"
        if i == rec and tpl in HABIT:
            desc += f" | {HABIT[tpl]}"
        if i == rec and lv == 2:
            desc += " | cũng có thể tách thành hai kỳ, mỗi kỳ bậc Tiêu chuẩn"
        if abs(i - rec) >= 2:
            desc += " | ⚠ lệch khá xa so với độ phức tạp"
        opts.append({"label": f"{t['name']} {t['range']}" + (" (đề xuất)" if i == rec else ""), "description": desc})
    out = {"score": total, "level": lname, "detail": dict(zip(DIMS, sc)),
           "question": f"Chủ đề này thiên về {lname} ({total}/10), muốn làm dài bao nhiêu?", "recommend": TIERS[rec]["name"], "options": opts}
    if "--pick" in a:
        p = tier_of(a[a.index("--pick") + 1]); want = rec
        if abs(p - want) >= 2:
            out["warning"] = ("Chỉ nói được đến kết luận, phần \"tại sao\" gần như không nói tới, phần bình luận dễ xuất hiện \"không hiểu\"." if p < want else
                              "Nội dung không đủ lấp đầy độ dài này, sẽ xuất hiện lặp lại và hình ảnh tĩnh lâu; nên giảm xuống một bậc, hoặc thêm một chủ đề con liên quan.")
    if "--json" in a:
        print(json.dumps(out, ensure_ascii=False, indent=1)); return
    print(f"Độ phức tạp {total}/10 · {lname} (" + ", ".join(f"{k} {v}" for k, v in out["detail"].items()) + ")")
    print(f"Đề xuất: {out['recommend']}\nCâu hỏi: {out['question']}")
    for o in opts:
        print(f"- {o['label']}\n    {o['description']}")
    if "warning" in out:
        print(f"⚠ Nhắc nhở: {out['warning']}")


if __name__ == "__main__":
    main()
