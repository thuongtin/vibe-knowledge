"""Dùng chung cho công cụ cine: tìm trình duyệt headless (xuất hình bằng Metal).
Biến môi trường CINE_CHROME được ưu tiên; nếu không thì dùng chromium_headless_shell mới nhất trong bộ nhớ đệm Playwright; không có cái nào thì giao cho mặc định của Playwright."""
import os
from pathlib import Path

GPU = ["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"]


def chrome():
    if os.environ.get("CINE_CHROME"):
        return os.environ["CINE_CHROME"]
    found = sorted(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-*/chrome-headless-shell"),
                   key=lambda p: int(p.parts[-3].rsplit("-", 1)[-1]))
    return str(found[-1]) if found else None


def launch(p):
    exe = chrome()
    return p.chromium.launch(executable_path=exe, args=GPU) if exe else p.chromium.launch(args=GPU)
