#!/usr/bin/env python3
"""只读探测官方 URL 是否能解析到 HTTP 状态。不登录、不注册、不付款、不带推荐码。"""
from __future__ import annotations

import argparse
import json
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools.json"
UA = "ReminderLearnBot/1.0 (read-only URL probe; +https://github.com/Smashwinny/reminder_knowlege)"
TZ = ZoneInfo("Asia/Shanghai")
TIMEOUT = 20


def load_catalog() -> dict:
    return json.loads(TOOLS.read_text(encoding="utf-8"))


def assert_no_referral(url: str) -> None:
    lowered = url.lower()
    forbidden = ("mppk02p", "invitecode", "invite_code", "ref=", "referral")
    for token in forbidden:
        if token in lowered:
            raise ValueError(f"拒绝探测带推荐/邀请参数的 URL: {url}")


def probe(url: str) -> dict:
    assert_no_referral(url)
    started = time.perf_counter()
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"})
    result = {
        "requested_url": url,
        "ok": False,
        "status": None,
        "final_url": None,
        "elapsed_ms": None,
        "error": None,
        "redirected": False,
    }
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            result["status"] = int(resp.status)
            result["final_url"] = resp.geturl()
            result["redirected"] = resp.geturl().rstrip("/") != url.rstrip("/")
            result["ok"] = 200 <= int(resp.status) < 400
            # read a tiny bit to complete the request, do not save body
            resp.read(256)
    except urllib.error.HTTPError as e:
        result["status"] = int(e.code)
        result["final_url"] = e.geturl() if hasattr(e, "geturl") else url
        result["error"] = f"HTTPError {e.code} {e.reason}"
        result["ok"] = 200 <= int(e.code) < 400
    except Exception as e:  # noqa: BLE001 — 探测必须把网络失败记下来
        result["error"] = f"{type(e).__name__}: {e}"
    result["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
    return result


def classify(row: dict) -> str:
    if row["official_url"] is None:
        return "原文缺号未探测"
    if row["result"]["ok"]:
        return "可达"
    if row["result"]["status"] in {401, 403}:
        return "被拦截或需登录（站点存在但未放行）"
    if row["result"]["status"] == 404:
        return "404"
    if row["result"]["error"]:
        return "网络或证书失败"
    return "不可达"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", type=float, default=0.15, help="请求间隔，避免过密访问")
    parser.add_argument("--out", default=str(HERE / "url-probe-results.json"))
    args = parser.parse_args()
    catalog = load_catalog()
    checked_at = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S Asia/Shanghai")
    rows = []
    for tool in catalog["tools"]:
        item = {
            "article_no": tool["article_no"],
            "name": tool["name"],
            "chapter": tool["chapter"],
            "confidence": tool["confidence"],
            "official_url": tool["official_url"],
            "url_note": tool.get("url_note") or "",
            "result": None,
            "classification": None,
        }
        if tool["official_url"]:
            item["result"] = probe(tool["official_url"])
            time.sleep(args.sleep)
        else:
            item["result"] = {
                "requested_url": None,
                "ok": False,
                "status": None,
                "final_url": None,
                "elapsed_ms": 0,
                "error": "missing_from_article",
                "redirected": False,
            }
        item["classification"] = classify(item)
        rows.append(item)
        status = item["result"]["status"]
        print(f"{tool['article_no']:>8}  {tool['name']:<28}  {status}  {item['classification']}  {tool['official_url'] or '-'}")

    # also probe the standalone article URL that already 404'd in the API
    article = {
        "article_no": "article-id",
        "name": "X 独立文章链接",
        "chapter": "访问核验",
        "confidence": "api_404",
        "official_url": catalog["meta"]["article_id_url"],
        "url_note": catalog["meta"]["note"],
        "result": probe(catalog["meta"]["article_id_url"]),
        "classification": None,
    }
    article["classification"] = "404" if article["result"]["status"] == 404 else classify(article)
    rows.append(article)
    print(f"{'article':>8}  {'X article link':<28}  {article['result']['status']}  {article['classification']}")

    payload = {
        "checked_at": checked_at,
        "method": "HTTP GET, follow redirects, no auth, no POST, no referral parameters",
        "user_agent": UA,
        "timeout_sec": TIMEOUT,
        "counts": {},
        "rows": rows,
    }
    from collections import Counter
    c = Counter(r["classification"] for r in rows)
    payload["counts"] = dict(c)
    Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print()
    print("checked_at:", checked_at)
    print("counts:", json.dumps(payload["counts"], ensure_ascii=False))
    reachable = sum(1 for r in rows if r["classification"] == "可达" and r["article_no"] != "article-id")
    with_url = sum(1 for r in rows if r["official_url"] and r["article_no"] != "article-id")
    print(f"工具官网可达 {reachable}/{with_url}（不含独立文章链接和缺号项）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
