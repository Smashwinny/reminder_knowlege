#!/usr/bin/env python3
"""Summarize the official article and frozen HTTP results; verify invariants."""
from __future__ import annotations
import argparse, json, re, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTICLE = (ROOT / "article_plain.txt").read_text()
STATUS = json.loads((ROOT / "url-status.json").read_text())

def extract():
    tools = re.findall(r"^(\d{1,2})、([^\n]+)", ARTICLE, re.M)
    sections = re.findall(r"^[一二三四五六七]、([^\n]+)", ARTICLE, re.M)
    has_growth = "六、增长获客与渠道分发" in ARTICLE
    has_end = ARTICLE.strip().endswith("祝你项目顺利！！！") or "祝你项目顺利" in ARTICLE[-80:]
    nums = [int(n) for n,_ in tools]
    info = {
        "sections": sections,
        "numbered_entries": len(tools),
        "numbers": nums,
        "missing": [i for i in range(1,57) if i not in nums],
        "duplicate_numbers": sorted({n for n in nums if nums.count(n)>1}),
        "growth_chapter_complete": has_growth and has_end,
        "ends_with_summary": "总结" in ARTICLE and "祝你项目顺利" in ARTICLE,
        "title_in_post": "靠Web出海赚美刀，7大核心方向精选56个宝藏工具，帮你把想法变成收益",
        "sha256_article": hashlib.sha256(ARTICLE.encode()).hexdigest(),
    }
    print(json.dumps(info, ensure_ascii=False, indent=2))
    (ROOT/"article-index.json").write_text(json.dumps(info, ensure_ascii=False, indent=2))
    return info

def status():
    s = STATUS["summary"]
    print(json.dumps(s, ensure_ascii=False, indent=2))
    print("rows", len(STATUS["rows"]))
    return s

def verify():
    info = json.loads((ROOT/"article-index.json").read_text()) if (ROOT/"article-index.json").exists() else extract()
    checks=[]
    def chk(n,ok,d):
        checks.append((n,bool(ok),d)); print(("PASS" if ok else "FAIL"), n, d)
    chk("not_truncated", info["growth_chapter_complete"] and info["ends_with_summary"], "growth+总结 present")
    chk("missing_14", info["missing"]==[14], info["missing"])
    chk("dup_53", info["duplicate_numbers"]==[53], info["duplicate_numbers"])
    chk("56_writeups", info["numbered_entries"]==56, info["numbered_entries"])
    rows=STATUS["rows"]
    chk("has_dated_status", all("checked_at" in r for r in rows), "all dated")
    chk("site_data_not_wrong_domain", not any(r["id"]=="3" and r.get("ok") and "sitedata.io" in (r.get("url") or "") for r in rows), "SiteData not false-positive")
    chk("feedlog_inferred_only", any(r["id"]=="53b" and "inferred" in (r.get("url_source") or "") for r in rows), "Feedlog tagged inferred")
    failed=[c for c in checks if not c[1]]
    print(f"assertions={len(checks)} failed={len(failed)}")
    if failed:
        sys.exit(1)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("cmd", choices=["extract","status","verify","all"], nargs="?", default="all")
    args=ap.parse_args()
    if args.cmd in ("extract","all"): extract()
    if args.cmd in ("status","all"): status()
    if args.cmd in ("verify","all"): verify()
