#!/usr/bin/env python3
"""HTTP-check the official demo and encode a 4-frame placeholder GIF.

The GIF uses system CJK fonts as stand-ins. It is NOT the project's Seal/Orac
glyphs and must not be presented as paleography.
"""
from __future__ import annotations
import json, ssl, urllib.request, time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
URL = "https://ivan666jjj.github.io/yigezi/"
REPO = "https://api.github.com/repos/Ivan666jjj/yigezi"

def fetch(url: str):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "ReminderLearningBot/1.0 (read-only research)"})
    ctx = ssl.create_default_context()
    t0 = time.time()
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        body = r.read(2048)
        info = {
            "url": url,
            "final_url": r.geturl(),
            "status": r.status,
            "content_type": r.headers.get("Content-Type"),
            "bytes_preview": len(body),
            "elapsed_s": round(time.time()-t0, 3),
        }
        return info, body

def main():
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S CST（UTC+8）")
    demo, body = fetch(URL)
    demo["contains_title"] = "一个字的一生" in body.decode("utf-8", "replace")
    repo, rbody = fetch(REPO)
    repo_json = json.loads(rbody.decode() + urllib.request.urlopen(urllib.request.Request(REPO, headers={"User-Agent": "ReminderLearningBot/1.0 (read-only research)"}), timeout=30).read().decode()) if False else json.loads(urllib.request.urlopen(urllib.request.Request(REPO, headers={"User-Agent": "ReminderLearningBot/1.0 (read-only research)"}), timeout=30).read())
    # redo repo fetch cleanly
    req = urllib.request.Request(REPO, headers={"User-Agent": "ReminderLearningBot/1.0 (read-only research)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        repo_json = json.loads(r.read().decode())
        repo = {"url": REPO, "status": r.status, "full_name": repo_json.get("full_name"), "sha_pushed_at": repo_json.get("pushed_at"), "stargazers": repo_json.get("stargazers_count"), "default_branch": repo_json.get("default_branch"), "homepage": repo_json.get("homepage"), "license": (repo_json.get("license") or {}).get("spdx_id")}
    # placeholder GIF
    font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 72, index=0)
    small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 18, index=0)
    frames = []
    labels = [("甲骨文（占位）", "商代"), ("小篆（占位）", "秦"), ("繁体", "汉以后"), ("简体", "现代")]
    char = "水"
    for lab, era in labels:
        im = Image.new("RGB", (360, 280), (250, 247, 240))
        d = ImageDraw.Draw(im)
        d.rectangle([16, 16, 344, 264], outline=(168, 50, 42), width=2)
        d.text((24, 24), lab, font=small, fill=(154, 138, 118))
        d.text((24, 48), era, font=small, fill=(154, 138, 118))
        d.text((140, 100), char, font=font, fill=(35, 31, 26))
        d.text((24, 240), "系统字体占位，非官方篆/甲字形", font=small, fill=(168, 50, 42))
        frames.append(im)
    gif = ROOT / "placeholder-evolution.gif"
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=700, loop=0)
    out = {"checked_at": now, "demo": demo, "repo": repo, "gif": {"path": str(gif), "bytes": gif.stat().st_size, "note": "system-font placeholder, not official glyphs"}}
    (ROOT / "live.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    assert demo["status"] == 200 and demo["contains_title"]
    assert repo["status"] == 200
    assert gif.stat().st_size > 100
    print("LIVE+GIF PASS")

if __name__ == "__main__":
    main()
