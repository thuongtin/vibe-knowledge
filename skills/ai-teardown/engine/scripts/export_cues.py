#!/usr/bin/env python3
"""Xuất stage.sfx (cue hiệu ứng âm thanh) và stage.videos (bảng đăng ký sticker video) từ trang ra JSON: python3 scripts/export_cues.py <page.html> <out.json>"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EXE = Path.home() / "Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell"
page, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(EXE) if EXE.exists() else None)
    pg = b.new_page()
    pg.goto(page.as_uri())
    pg.wait_for_function("window.__stage !== undefined", timeout=30000)
    data = pg.evaluate("({ sfx: window.__stage.sfx || [], duration: window.__stage.duration, videos: window.__stage.videos || [] })")
    b.close()
out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(data['sfx'])} cue hiệu ứng âm thanh → {out}")
