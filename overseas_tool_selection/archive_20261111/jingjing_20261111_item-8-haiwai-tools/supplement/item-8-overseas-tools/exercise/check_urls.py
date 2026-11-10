#!/usr/bin/env python3
"""Read-only HTTP status check of official (or best-known official) URLs.

No sign-up, no purchase, no form submit. A 200 does not mean the product is
usable, correctly identified, or 'verified in production' as the author claimed.
"""
from __future__ import annotations
import json, ssl, time, csv, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parent

# url_source: official_wellknown | inferred_from_common_domain | article_did_not_give_url
TOOLS = [
    {"id":"1","name":"沉浸式翻译","section":"市场调研","url":"https://immersivetranslate.com/","url_source":"official_wellknown"},
    {"id":"2","name":"AITDK","section":"市场调研","url":"https://aitdk.com/","url_source":"official_wellknown"},
    {"id":"3","name":"SiteData","section":"市场调研","url":"https://www.sitedata.io/","url_source":"inferred_from_common_domain","note":"原文未给域名，先探测 sitedata.io"},
    {"id":"4","name":"Similarweb","section":"市场调研","url":"https://www.similarweb.com/","url_source":"official_wellknown"},
    {"id":"5","name":"Wayback Machine","section":"市场调研","url":"https://web.archive.org/","url_source":"official_wellknown"},
    {"id":"6","name":"Wappalyzer","section":"市场调研","url":"https://www.wappalyzer.com/","url_source":"official_wellknown"},
    {"id":"7","name":"Google Trends","section":"市场调研","url":"https://trends.google.com/","url_source":"official_wellknown"},
    {"id":"8","name":"Exploding Topics","section":"市场调研","url":"https://explodingtopics.com/","url_source":"official_wellknown"},
    {"id":"9","name":"Screaming Frog SEO Spider","section":"SEO","url":"https://www.screamingfrog.co.uk/seo-spider/","url_source":"official_wellknown"},
    {"id":"10","name":"SEO Minion","section":"SEO","url":"https://seominion.com/","url_source":"inferred_from_common_domain"},
    {"id":"11","name":"Semrush","section":"SEO","url":"https://www.semrush.com/","url_source":"official_wellknown"},
    {"id":"12","name":"Moz Link Explorer","section":"SEO","url":"https://moz.com/link-explorer","url_source":"official_wellknown"},
    {"id":"13","name":"Ahrefs","section":"SEO","url":"https://ahrefs.com/","url_source":"official_wellknown"},
    {"id":"14","name":"（原文缺号）","section":"SEO","url":None,"url_source":"missing_in_article","note":"官方长文从13跳到15，没有第14项"},
    {"id":"15","name":"Linkhouse","section":"SEO","url":"https://linkhouse.net/","url_source":"inferred_from_common_domain"},
    {"id":"16","name":"Collaborator","section":"SEO","url":"https://collaborator.pro/","url_source":"inferred_from_common_domain"},
    {"id":"53a","name":"Fiverr","section":"SEO","url":"https://www.fiverr.com/","url_source":"official_wellknown","note":"原文编号写成53，与后文Feedlog冲突"},
    {"id":"54","name":"Adsy","section":"SEO","url":"https://www.adsy.com/","url_source":"inferred_from_common_domain"},
    {"id":"17","name":"Figma","section":"设计AI演示","url":"https://www.figma.com/","url_source":"official_wellknown"},
    {"id":"18","name":"Framer","section":"设计AI演示","url":"https://www.framer.com/","url_source":"official_wellknown"},
    {"id":"19","name":"IconPark","section":"设计AI演示","url":"https://iconpark.oceanengine.com/official","url_source":"official_wellknown"},
    {"id":"20","name":"OpenRouter","section":"设计AI演示","url":"https://openrouter.ai/","url_source":"official_wellknown"},
    {"id":"21","name":"Dify","section":"设计AI演示","url":"https://dify.ai/","url_source":"official_wellknown"},
    {"id":"22","name":"Replicate","section":"设计AI演示","url":"https://replicate.com/","url_source":"official_wellknown"},
    {"id":"23","name":"n8n","section":"设计AI演示","url":"https://n8n.io/","url_source":"official_wellknown"},
    {"id":"24","name":"Midjourney","section":"设计AI演示","url":"https://www.midjourney.com/","url_source":"official_wellknown"},
    {"id":"25","name":"Ideogram","section":"设计AI演示","url":"https://ideogram.ai/","url_source":"official_wellknown"},
    {"id":"26","name":"Loom","section":"设计AI演示","url":"https://www.loom.com/","url_source":"official_wellknown"},
    {"id":"27","name":"Screen Studio","section":"设计AI演示","url":"https://www.screen.studio/","url_source":"official_wellknown"},
    {"id":"28","name":"Cloudflare","section":"建站本地化","url":"https://www.cloudflare.com/","url_source":"official_wellknown"},
    {"id":"29","name":"Vercel","section":"建站本地化","url":"https://vercel.com/","url_source":"official_wellknown"},
    {"id":"30","name":"DeepL","section":"建站本地化","url":"https://www.deepl.com/","url_source":"official_wellknown"},
    {"id":"31","name":"Weglot","section":"建站本地化","url":"https://www.weglot.com/","url_source":"official_wellknown"},
    {"id":"32","name":"Lokalise","section":"建站本地化","url":"https://lokalise.com/","url_source":"official_wellknown"},
    {"id":"33","name":"Stripe","section":"支付合规","url":"https://stripe.com/","url_source":"official_wellknown"},
    {"id":"34","name":"Paddle","section":"支付合规","url":"https://www.paddle.com/","url_source":"official_wellknown"},
    {"id":"35","name":"Lemon Squeezy","section":"支付合规","url":"https://www.lemonsqueezy.com/","url_source":"official_wellknown"},
    {"id":"36","name":"Starryblu","section":"支付合规","url":"https://www.starryblu.com/","url_source":"inferred_from_common_domain","note":"原文含推荐码，本实验不使用、不推广该码"},
    {"id":"37","name":"Termly","section":"支付合规","url":"https://termly.io/","url_source":"official_wellknown"},
    {"id":"38","name":"Product Hunt","section":"增长获客","url":"https://www.producthunt.com/","url_source":"official_wellknown"},
    {"id":"39","name":"Uneed","section":"增长获客","url":"https://www.uneed.best/","url_source":"inferred_from_common_domain"},
    {"id":"40","name":"Microlaunch","section":"增长获客","url":"https://microlaunch.net/","url_source":"inferred_from_common_domain"},
    {"id":"41","name":"BetaList","section":"增长获客","url":"https://betalist.com/","url_source":"official_wellknown"},
    {"id":"42a","name":"Discord","section":"增长获客","url":"https://discord.com/","url_source":"official_wellknown"},
    {"id":"42b","name":"Disboard","section":"增长获客","url":"https://disboard.org/","url_source":"official_wellknown"},
    {"id":"43","name":"Toolify","section":"增长获客","url":"https://www.toolify.ai/","url_source":"official_wellknown"},
    {"id":"44","name":"There's An AI For That","section":"增长获客","url":"https://theresanaiforthat.com/","url_source":"official_wellknown"},
    {"id":"45","name":"Typefully","section":"增长获客","url":"https://typefully.com/","url_source":"official_wellknown"},
    {"id":"46","name":"Beehiiv","section":"增长获客","url":"https://www.beehiiv.com/","url_source":"official_wellknown"},
    {"id":"47","name":"Customer","section":"增长获客","url":"https://customer.io/","url_source":"inferred_from_common_domain","note":"原文只写Customer，按功能描述推断为 Customer.io，未在原文确认域名"},
    {"id":"48","name":"Loops","section":"增长获客","url":"https://loops.so/","url_source":"official_wellknown"},
    {"id":"49","name":"Google Search Console","section":"数据分析","url":"https://search.google.com/search-console","url_source":"official_wellknown"},
    {"id":"50","name":"Google Analytics 4","section":"数据分析","url":"https://marketingplatform.google.com/about/analytics/","url_source":"official_wellknown"},
    {"id":"51","name":"PostHog","section":"数据分析","url":"https://posthog.com/","url_source":"official_wellknown"},
    {"id":"52","name":"Microsoft Clarity","section":"数据分析","url":"https://clarity.microsoft.com/","url_source":"official_wellknown"},
    {"id":"53b","name":"Feedlog","section":"数据分析","url":"https://feedlog.com/","url_source":"inferred_from_common_domain","note":"作者自述为自有产品；原文未给域名，先探测 feedlog.com"},
    {"id":"55","name":"Crisp","section":"数据分析","url":"https://crisp.chat/","url_source":"official_wellknown"},
    {"id":"56","name":"Cursorful","section":"数据分析","url":"https://cursorful.com/","url_source":"inferred_from_common_domain"},
]

def probe(url: str):
    ctx = ssl.create_default_context()
    headers = {"User-Agent": "ReminderLearningBot/1.0 (read-only research; HTTP status only)"}
    last = None
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, method=method, headers=headers)
            t0 = time.time()
            with urlopen(req, context=ctx, timeout=20) as r:
                return {"status": r.status, "final_url": r.geturl(), "method": method, "content_type": r.headers.get("Content-Type"), "elapsed_s": round(time.time()-t0, 3), "error": None}
        except HTTPError as e:
            last = {"status": e.code, "final_url": getattr(e, "url", url), "method": method, "content_type": e.headers.get("Content-Type") if e.headers else None, "elapsed_s": None, "error": f"HTTPError {e.code}"}
            if method == "HEAD" and e.code in {403, 405, 501}:
                continue
            return last
        except Exception as e:
            last = {"status": None, "final_url": url, "method": method, "content_type": None, "elapsed_s": None, "error": f"{type(e).__name__}: {e}"}
            if method == "HEAD":
                continue
            return last
    return last

def main():
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S CST（UTC+8）")
    rows = []
    to_check = [t for t in TOOLS if t.get("url")]
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(probe, t["url"]): t for t in to_check}
        results = {id(t): f.result() for f,t in [(fut, futs[fut]) for fut in as_completed(futs)]}
    # as_completed dict by id of tool might be messy; redo mapping
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(probe, t["url"]): t["id"] for t in to_check}
        for fut in as_completed(futs):
            results[futs[fut]] = fut.result()
    for t in TOOLS:
        rec = dict(t)
        rec["checked_at"] = now
        if not t.get("url"):
            rec.update({"status": "skipped", "final_url": None, "method": None, "ok": False, "error": rec.get("note")})
        else:
            r = results[t["id"]]
            rec.update(r)
            rec["ok"] = isinstance(r.get("status"), int) and 200 <= r["status"] < 400
        rec["reachable_is_not_endorsement"] = True
        rows.append(rec)
    ok = sum(1 for r in rows if r.get("ok"))
    skipped = sum(1 for r in rows if r.get("status")=="skipped")
    failed = len(rows) - ok - skipped
    summary = {"checked_at": now, "named_entries": len(rows), "reachable_2xx_3xx": ok, "failed_or_blocked": failed, "skipped_missing": skipped, "article_claimed_tools": 56, "numbering_notes": "原文缺14；53出现两次（Fiverr与Feedlog）；增长章在官方article.plain_text中是完整的，不是截断。"}
    (ROOT/"url-status.json").write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2))
    with (ROOT/"url-status.csv").open("w", newline="") as f:
        fields = ["id","name","section","url","url_source","status","final_url","method","ok","error","note","checked_at"]
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for r in rows:
        print(f"{r['id']:>4} {r['name']:<24} {str(r.get('status')):<12} {r.get('ok')} {r.get('error') or ''}")
    # verification: we recorded a dated status for every named entry; missing #14 is skipped not faked
    assert any(r["id"]=="14" and r["status"]=="skipped" for r in rows)
    assert any(r["id"]=="53a" for r in rows) and any(r["id"]=="53b" for r in rows)
    assert all("checked_at" in r for r in rows)
    print("CHECKLIST+HTTP PASS (reachability only)")

if __name__ == "__main__":
    main()
