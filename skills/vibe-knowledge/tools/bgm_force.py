#!/usr/bin/env python3
"""BGM bắt buộc của Vibe知识大赏 (người dùng quy định 2026-10-28: video nào cũng phải có vibe-bgm, âm lượng thống nhất, vừa phải).
Được cine/tools/finish.py gọi khi trộn âm (new_film.py / tệp này với --patch sẽ cài hook vào finish.py):
  0. Ngoại lệ duy nhất: người dùng yêu cầu rõ ràng đổi bài → mục nhạc ghi bgm: true + user_request: "nguyên văn lời người dùng", mục này được coi là BGM, vibe-bgm nhường chỗ (âm lượng vẫn được hiệu chỉnh).
  1. prepare(): film.js không đặt BGM (mục có tên tệp src là bgm.wav) → dùng fit_bgm.py cắt một bản build/bgm_auto.wav theo độ dài phim để tự động bổ sung;
     các bản nhạc nền nguyên đoạn khác ≥20 giây (Lyria, thư viện nhạc) đều ngừng dùng, hiệu ứng âm thanh ngắn và âm thanh gốc của cảnh được giữ lại.
  2. calibrate(): bất kể film.js ghi gain lớn bao nhiêu, âm lượng tổng thể của BGM đều được hiệu chỉnh lại theo giọng nói:
     khi có người nói (đã hạ thấp) BGM thấp hơn giọng nói VOICE_GAP dB; gain_curve của film.js chỉ giữ lại "hình dạng" (chỗ nào lên xuống), âm lượng tuyệt đối do đây quyết định.
     Chỗ không có lời nói tự động nâng lên theo logic hạ thấp vốn có của finish.py (khoảng +7 dB), thẻ cuối phim lại được nâng theo gain_curve.
  3. Ghi build/bgm.json (có BGM hay không, tỷ lệ giọng nói trước và sau hiệu chỉnh), qa.py sẽ đọc nó, không có thì báo động.
Cài patch thủ công: python3 bgm_force.py --patch <thư mục series> (ví dụ: ~/Desktop/vibe-knowledge/examples/vk)"""
import json
import subprocess
import sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
BGM_SRC = SK / "assets/music/vibe-bgm.m4a"
VOICE_GAP = 10.0        # Khi có người nói, BGM thấp hơn giọng nói bao nhiêu dB. Người dùng yêu cầu "âm lượng cao hơn một chút" (10-28): 14 → 10; dưới 8 bắt đầu lấn giọng nói, trên 12 thì hơi nhỏ
LONG = 20.0             # Mục nhạc không phải BGM dài hơn mức này được coi là nhạc nền nguyên đoạn, ngừng dùng


def is_bgm(m):
    return Path(str(m.get("src", ""))).name in ("bgm.wav", "bgm_auto.wav")


def is_user_bgm(m):
    # Lối thay đổi duy nhất: người dùng yêu cầu rõ ràng đổi bài trong hội thoại, trong film.js viết như sau —
    # music.push({ src: P("audio/xxx.wav"), …, bgm: true, user_request: "nguyên văn lời người dùng, ví dụ: kỳ này đổi sang xxx.mp3 tôi đưa" })
    return bool(m.get("bgm")) and bool(str(m.get("user_request", "")).strip())


def prepare(info, total, B, py=sys.executable):
    music = info.get("music", [])
    keep, dropped = [], []
    user = [m for m in music if is_user_bgm(m)]
    for m in music:
        if user and is_bgm(m):            # Người dùng yêu cầu đổi bài: vibe-bgm nhường chỗ
            dropped.append(Path(str(m.get("src"))).name); continue
        if is_user_bgm(m):
            m["_bgm"] = True; keep.append(m)
        elif m.get("bgm") and not is_user_bgm(m):
            print("  BGM bắt buộc: có mục đánh dấu bgm: true nhưng không ghi user_request (nguyên văn lời người dùng), không công nhận, vẫn dùng vibe-bgm như thường")
            dropped.append(Path(str(m.get("src"))).name)
        elif is_bgm(m):
            m["_bgm"] = True; keep.append(m)
        elif float(m.get("dur", 0)) >= LONG and not str(m.get("src", "")).startswith("earshot:"):
            dropped.append(Path(str(m.get("src"))).name)
        else:
            keep.append(m)
    auto = False
    if not any(m.get("_bgm") for m in keep):
        out = Path(B) / "bgm_auto.wav"
        subprocess.run([py, str(SK / "tools/fit_bgm.py"), str(out), "--seconds", f"{total:.3f}"], check=True,
                       stdout=subprocess.DEVNULL)
        keep.insert(0, {"src": str(out), "from": 0, "at": 0, "dur": total, "gain": 0, "fade_in": 0.3, "fade_out": 1.8, "_bgm": True})
        auto = True
    if user:
        print(f"  BGM: người dùng yêu cầu thay đổi → {Path(str(user[0].get('src'))).name} ({user[0].get('user_request')})")
    if dropped:
        print(f"  BGM bắt buộc: ngừng dùng nhạc nền nguyên đoạn {', '.join(dropped)} (" + ("người dùng yêu cầu đổi bài" if user else "Vibe知识大赏 thống nhất dùng vibe-bgm") + ")")
    if auto:
        print(f"  BGM bắt buộc: film.js không đặt BGM, đã tự động bổ sung vibe-bgm theo độ dài phim {total:.1f}s")
    info["music"] = keep
    return {"auto": auto, "dropped": dropped, "user_bgm": (Path(str(user[0]["src"])).name, user[0]["user_request"]) if user else None}


def calibrate(bgmt, narr, speech, B, state):
    """bgmt: track BGM đã nhân hình dạng gain_curve và đường bao hạ thấp (n×2); narr: track giọng nói; speech: mặt nạ mẫu của đoạn có lời nói."""
    import numpy as np   # Chỉ cần khi trộn âm; --patch chạy được bằng python3 hệ thống
    rep = {"has_bgm": bool(np.any(bgmt)), "voice_gap_target_db": VOICE_GAP, **state}
    if rep["has_bgm"] and speech.any():
        rv = np.sqrt(np.mean(narr[speech] ** 2)); rb = np.sqrt(np.mean(bgmt[speech] ** 2))
        before = 20 * np.log10(rv / max(rb, 1e-9))
        g = 10 ** ((before - VOICE_GAP) / 20)
        bgmt = bgmt * g
        quiet = ~speech
        rq = np.sqrt(np.mean(bgmt[quiet] ** 2)) if quiet.any() else 0
        rep.update(voice_gap_before_db=round(float(before), 1), gain_applied_db=round(float(20 * np.log10(g)), 1),
                   voice_gap_db=VOICE_GAP, gap_in_pauses_db=round(float(20 * np.log10(rv / max(rq, 1e-9))), 1) if quiet.any() else None)
        print(f"  Hiệu chỉnh BGM: khi có người nói giọng cao hơn BGM {before:.1f} → {VOICE_GAP:.1f} dB (BGM {20 * np.log10(g):+.1f} dB); chỗ không có lời nói giọng cao hơn BGM {rep['gap_in_pauses_db']} dB")
    (Path(B) / "bgm.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return bgmt


# ── Cài hook vào finish.py (idempotent) ──
HOOKS = [
    ("    import hashlib, os\n",
     "    import hashlib, os\n"
     "    sys.path.insert(0, str(Path.home() / \".claude/skills/vibe-knowledge/tools\")); import bgm_force as VKBGM   # BGM bắt buộc của Vibe知识大赏\n"
     "    _bgm_state = VKBGM.prepare(info, total, B)\n"
     "    bgmt = np.zeros((n, 2))\n"),
    ("            clipa[j0:j1] += a[: j1 - j0] * (g * dk)[:, None]\n",
     "            (bgmt if m.get(\"_bgm\") else clipa)[j0:j1] += a[: j1 - j0] * (g * dk)[:, None]\n"),
    ("    mix = narr * 1.0 + bed * duck[:, None] + sfx * 0.9 + clipa\n",
     "    clipa += VKBGM.calibrate(bgmt, narr, env > 0.5, B, _bgm_state)\n"
     "    mix = narr * 1.0 + bed * duck[:, None] + sfx * 0.9 + clipa\n"),
]
MARK = "import bgm_force as VKBGM"


def patch(series):
    p = Path(series).expanduser() / "cine/tools/finish.py"
    s = p.read_text(encoding="utf-8")
    if MARK in s:
        print(f"✓ Đã có hook BGM bắt buộc: {p}"); return
    for a, b in HOOKS:
        if s.count(a) != 1:
            sys.exit(f"{p} không tìm thấy (hoặc có hơn một chỗ): {a.strip()[:60]}... engine cine đã bị sửa, hook cần viết lại")
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")
    print(f"✓ Patch: {p} (bắt buộc vibe-bgm + hiệu chỉnh âm lượng theo giọng nói)")


if __name__ == "__main__":
    if "--patch" in sys.argv:
        patch(sys.argv[sys.argv.index("--patch") + 1])
    else:
        sys.exit(__doc__)
