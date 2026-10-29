"""Đọc session.env (KEY=VALUE, dòng bắt đầu bằng # là chú thích, ~ được mở rộng), và tính ra thư mục Claude Code lưu bản ghi phiên."""
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def env():
    e = {}
    for line in (HERE / "session.env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            e[k.strip()] = os.path.expanduser(v.strip())
    return e


def project_logs():
    """*.jsonl dưới <thư mục cấu hình>/projects/<đường dẫn dự án với ký tự không phải chữ cái hay chữ số được đổi thành ->, sắp xếp theo thời gian sửa."""
    e = env()
    root = Path(e.get("SESSION_CONFIG") or "~/.claude").expanduser() / "projects"
    proj = str(Path(e["SESSION_PROJ"]).expanduser().resolve())
    d = root / re.sub(r"[^A-Za-z0-9]", "-", proj)
    if not d.exists():   # Khi đường dẫn có chữ Hán hoặc ký tự tương tự thì quy tắc đặt tên có thể khác: lùi về cái có tên chứa tên thư mục dự án và được sửa gần nhất
        cands = [p for p in root.glob("*") if p.is_dir() and re.sub(r"[^A-Za-z0-9]", "-", Path(proj).name) in p.name]
        d = max(cands, key=lambda p: p.stat().st_mtime) if cands else d
    return sorted(d.glob("*.jsonl"), key=os.path.getmtime)
