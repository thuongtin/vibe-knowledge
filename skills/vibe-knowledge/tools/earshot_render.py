#!/usr/bin/env python3
"""Dùng thư viện hiệu ứng âm thanh code của earshot (github.com/Leonxlnx/earshot, MIT) để render một loạt hiệu ứng. Do finish.py gọi, cũng có thể chạy riêng.
Phải chạy bằng môi trường riêng của earshot: ~/tools/earshot/.venv/bin/python earshot_render.py <jobs.json> <thư mục xuất>

jobs.json: [{"key": "a1b2c3", "id": "cut_hit/punch", "seed": null, "dur": null, "apex": null, "pitch": null}, …]
  id     mã hiệu ứng earshot <loại>/<thành viên> (danh sách đầy đủ: ~/tools/earshot/.venv/bin/python -m earshot sfx list)
  seed   null = bản lúc phát hành; số nguyên = một take khác của cùng hiệu ứng (hiệu ứng dùng lặp trong cùng một phim thì đổi seed để tránh lặp máy móc)
  dur    thời lượng mục tiêu (giây), sửa theo tham số công thức, không đổi tốc độ
  apex   điểm to nhất của tiếng vút / âm đi lên rơi vào giây thứ mấy (tính từ đầu file)
  pitch  tên nốt hoặc Hz ("E5", "G1", 440), chỉ có hiệu lực với hiệu ứng có cao độ
Đầu ra: <key>.wav (48 kHz dấu phẩy động) và <key>.json (onset_s / peak_s / end_s / dur_s / checks), đã tồn tại thì bỏ qua (bộ nhớ đệm)."""
import json, sys
from pathlib import Path

import numpy as np
import soundfile as sf
from earshot.forge import bank

SR = 48000


def main():
    jobs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    done = 0
    for j in jobs:
        wav, meta_p = out / f"{j['key']}.wav", out / f"{j['key']}.json"
        if wav.exists() and meta_p.exists():
            continue
        kw = {k: j[k] for k in ("seed", "dur", "apex", "pitch") if j.get(k) is not None}
        y, meta = bank.render(j["id"], sr=SR, **kw)
        y = np.asarray(y, np.float32)
        sf.write(str(wav), y, SR, subtype="FLOAT")          # bank.render trả về (n,) hoặc (n, 2), mẫu đứng trước
        keep = {k: meta.get(k) for k in ("id", "seed", "onset_s", "peak_s", "end_s", "dur_s", "peak_db", "lufs_m_max", "edits")}
        c = meta.get("checks")
        keep["checks_ok"] = (c or {}).get("ok", None) if isinstance(c, dict) else None
        meta_p.write_text(json.dumps(keep, ensure_ascii=False, default=str), encoding="utf-8")
        done += 1
    print(f"earshot: render mới {done} cái, tổng {len(jobs)} cái → {out}")


if __name__ == "__main__":
    main()
