# 第8项真实实验日志：出海工具清单与官网探测

执行时间：2026-11-11 01:22:18 Asia/Shanghai（UTC+8）
工作目录：/workspace/reminder-batch-2026-11-11/item-8-haiwai-tools/exercise
Python：3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]
只读公开研究：解析已保存的 article.plain_text，并对公开 URL 做 GET。没有注册、登录、付款、采购外链或使用推荐码。

## 步骤 1 · 从原文快照审计编号与章节
目的：固定本次实际读到的 article.plain_text：字数、七个章节、总结、编号缺号与错位，而不是沿用「增长章节中途截断」的任务摘要。

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-haiwai-tools/exercise
python3 - <<'PY'
from pathlib import Path
import re, json
t=Path('../sources/article-plain.txt').read_text()
print('plain_text 字符数:', len(t))
print('含总结:', '总结' in t)
chs=re.findall(r'(?m)^([一二三四五六七]、[^\n]+)', t)
print('章节:', chs)
items=re.findall(r'(?m)^\s*(\d{1,2})、\s*([^\n：:]+)', t)
nums=[int(a) for a,b in items]
print('编号条目数:', len(items))
print('序列:', nums)
print('1-56 缺号:', [i for i in range(1,57) if i not in nums])
from collections import Counter
print('重复编号:', {k:v for k,v in Counter(nums).items() if v>1})
print('第 6 章是否完整读到 Loops:', '48、Loops' in t or '48、Loops' in t.replace(' ',''))
print('第 6 章标题存在:', any(c.startswith('六') for c in chs))
PY
```

真实结果：退出码 0，输出 446 字符。

```text
plain_text 字符数: 9776
含总结: True
章节: ['一、市场机会与竞品调研', '二、SEO 与内容资产', '三、产品设计、AI 能力与演示', '四、建站、本地化与基础设施', '五、支付、跨境资金与合规', '六、增长获客与渠道分发', '七、数据分析与用户反馈']
编号条目数: 56
序列: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 53, 54, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 56]
1-56 缺号: [14]
重复编号: {53: 2}
第 6 章是否完整读到 Loops: True
第 6 章标题存在: True
```

验证：退出码 0；七章都在；缺号仅 14；53 重复；总结存在。
本步验证：通过

## 步骤 2 · 按阶段打印选型清单
目的：把原文工具按七个业务环节编成「先用 / 按需再加」清单，明确不必一次采购全部，并标出编号错位、推断网址和作者自有产品。

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-haiwai-tools/exercise
python3 checklist.py
```

真实结果：退出码 0，输出 2124 字符。

```text
选型清单（默认少量组合，不必一次采购或接入全部）
依据：已读长文用法 + 编号缺陷记录。不是使用效果测评。

## 一、市场机会与竞品调研
原文提到： 沉浸式翻译、AITDK、SiteData、Similarweb、Wayback Machine、Wappalyzer、Google Trends、Exploding Topics
  先用: 沉浸式翻译、Wayback Machine、Google Trends、Wappalyzer、AITDK
  按需再加: SiteData、Similarweb、Exploding Topics
  原则: 先免费或低成本看原文、历史快照、趋势和技术栈；趋势曲线不能当成需求已经验证。

## 二、SEO 与内容资产
原文提到： Screaming Frog SEO Spider、SEO Minion、Semrush、Moz Link Explorer、Ahrefs、（原文缺号）、Linkhouse、Collaborator、Fiverr、Adsy
  先用: Screaming Frog SEO Spider、SEO Minion
  按需再加（二选一）: Semrush、Ahrefs
  外链相关需人工审页: Moz Link Explorer、Linkhouse、Collaborator、Fiverr、Adsy
  原则: 先修自己站点的技术问题。关键词套件作者说 Semrush 和 Ahrefs 选一个即可。外链采购只看相关性、真实流量和页面质量，不批量堆链接。Fiverr 与 Adsy 在原文里编号错位置于本章。

## 三、产品设计、AI 能力与演示
原文提到： Figma、Framer、IconPark、OpenRouter、Dify、Replicate、n8n、Midjourney、Ideogram、Loom、Screen Studio
  先用: Figma、OpenRouter
  按需再加: Framer、Dify、n8n、Replicate、IconPark、Midjourney、Ideogram、Loom、Screen Studio
  原则: 先把五个关键页面连成可点击流程，再用真实任务比较模型成本和质量。Framer 不适合复杂大型 SaaS。带文字的生图必须人工校对。

## 四、建站、本地化与基础设施
原文提到： Cloudflare、Vercel、DeepL、Weglot、Lokalise
  先用: Cloudflare、Vercel、DeepL
  按需再加: Weglot、Lokalise
  原则: 先保证访问和部署，再测一个语言市场；DeepL 只能出第一版，关键页要人工润色。

## 五、支付、跨境资金与合规
原文提到： Stripe、Paddle、Lemon Squeezy、Starryblu、Termly
  先用（先验证愿付）: Lemon Squeezy、Paddle
  需要自控订阅数据时: Stripe
  资金账户与政策草稿: Starryblu、Termly
  原则: 作者建议用测试支付走完付款、退款、升级、取消和失败重试。本批只做官网可达探测，不发起任何真实或测试支付，不注册账户，不使用原文推荐码。Termly 生成的文本不是法律意见。

## 六、增长获客与渠道分发
原文提到： Product Hunt、Uneed、Microlaunch、BetaList、Discord、Disboard、Toolify、There's An AI For That、Typefully、Beehiiv、Customer、Loops
  先用: Product Hunt、Typefully、Beehiiv、Loops
  按需再加: Uneed、Microlaunch、BetaList、Discord、Disboard、Toolify、There's An AI For That、Customer
  原则: 提交到导航站不等于产品验证成功。社群先参与讨论。Customer 在原文只有简称，对应官网是推断。

## 七、数据分析与用户反馈
原文提到： Google Search Console、Google Analytics 4、PostHog、Microsoft Clarity、Feedlog、Crisp、Cursorful
  先用: Google Search Console、Google Analytics 4、PostHog
  按需再加: Microsoft Clarity、Crisp、Cursorful、Feedlog
  原则: 注册了却没有第一份结果时，先改首次使用，不要继续投放。Feedlog 是作者自述的自己的产品，选型时单独标注利益关系。

全局纪律：
  1. 不要把「作者整理了 56 个实战工具」理解成精确、无缺号的官方目录。
  2. 官网能打开 ≠ 工具适合你，更不是付费计划或效果已经验证。
  3. 不注册、不采购外链、不接入支付、不使用推荐码。
```

验证：退出码 0；七章都有先用建议；写出不注册、不采购、不用推荐码。
本步验证：通过

## 步骤 3 · 对官方 URL 做只读 HTTP GET 探测
目的：在 2026-11-11 Asia/Shanghai 记录每个已填写官网的 HTTP 状态和最终 URL。不登录、不付款、不带推荐码。独立文章链接一并探测。

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-haiwai-tools/exercise
python3 check_urls.py --sleep 0.2
```

真实结果：退出码 0，输出 4543 字符。

```text
       1  沉浸式翻译                         200  可达  https://immersivetranslate.com/
       2  AITDK                         200  可达  https://aitdk.com/
       3  SiteData                      200  可达  https://sitedata.dev/
       4  Similarweb                    200  可达  https://www.similarweb.com/
       5  Wayback Machine               200  可达  https://web.archive.org/
       6  Wappalyzer                    200  可达  https://www.wappalyzer.com/
       7  Google Trends                 200  可达  https://trends.google.com/
       8  Exploding Topics              200  可达  https://explodingtopics.com/
       9  Screaming Frog SEO Spider     200  可达  https://www.screamingfrog.co.uk/seo-spider/
      10  SEO Minion                    200  可达  https://seominion.com/
      11  Semrush                       200  可达  https://www.semrush.com/
      12  Moz Link Explorer             200  可达  https://moz.com/link-explorer
      13  Ahrefs                        200  可达  https://ahrefs.com/
      14  （原文缺号）                        None  原文缺号未探测  -
      15  Linkhouse                     200  可达  https://linkhouse.net/
      16  Collaborator                  200  可达  https://collaborator.pro/
53-early  Fiverr                        403  被拦截或需登录（站点存在但未放行）  https://www.fiverr.com/
54-early  Adsy                          200  可达  https://www.adsy.com/
      17  Figma                         202  可达  https://www.figma.com/
      18  Framer                        200  可达  https://www.framer.com/
      19  IconPark                      200  可达  https://iconpark.oceanengine.com/
      20  OpenRouter                    200  可达  https://openrouter.ai/
      21  Dify                          200  可达  https://dify.ai/
      22  Replicate                     200  可达  https://replicate.com/
      23  n8n                           200  可达  https://n8n.io/
      24  Midjourney                    403  被拦截或需登录（站点存在但未放行）  https://www.midjourney.com/
      25  Ideogram                      200  可达  https://ideogram.ai/
      26  Loom                          200  可达  https://www.loom.com/
      27  Screen Studio                 200  可达  https://screen.studio/
      28  Cloudflare                    200  可达  https://www.cloudflare.com/
      29  Vercel                        200  可达  https://vercel.com/
      30  DeepL                         200  可达  https://www.deepl.com/
      31  Weglot                        200  可达  https://www.weglot.com/
      32  Lokalise                      200  可达  https://lokalise.com/
      33  Stripe                        200  可达  https://stripe.com/
      34  Paddle                        200  可达  https://www.paddle.com/
      35  Lemon Squeezy                 200  可达  https://www.lemonsqueezy.com/
      36  Starryblu                     200  可达  https://www.starryblu.com/
      37  Termly                        200  可达  https://termly.io/
      38  Product Hunt                  403  被拦截或需登录（站点存在但未放行）  https://www.producthunt.com/
      39  Uneed                         200  可达  https://www.uneed.best/
      40  Microlaunch                   200  可达  https://microlaunch.net/
      41  BetaList                      200  可达  https://betalist.com/
     42a  Discord                       200  可达  https://discord.com/
     42b  Disboard                      200  可达  https://disboard.org/
      43  Toolify                       403  被拦截或需登录（站点存在但未放行）  https://www.toolify.ai/
      44  There's An AI For That        403  被拦截或需登录（站点存在但未放行）  https://theresanaiforthat.com/
      45  Typefully                     200  可达  https://typefully.com/
      46  Beehiiv                       200  可达  https://www.beehiiv.com/
      47  Customer                      200  可达  https://customer.io/
      48  Loops                         200  可达  https://loops.so/
      49  Google Search Console         200  可达  https://search.google.com/search-console/about
      50  Google Analytics 4            200  可达  https://marketingplatform.google.com/about/analytics/
      51  PostHog                       200  可达  https://posthog.com/
      52  Microsoft Clarity             200  可达  https://clarity.microsoft.com/
      53  Feedlog                       200  可达  https://feedlog.ai/
      55  Crisp                         200  可达  https://crisp.chat/
      56  Cursorful                     200  可达  https://cursorful.com/
 article  X article link                200  可达

checked_at: 2026-11-11 01:22:18 Asia/Shanghai
counts: {"可达": 53, "原文缺号未探测": 1, "被拦截或需登录（站点存在但未放行）": 5}
工具官网可达 52/57（不含独立文章链接和缺号项）
```

验证：退出码 0；生成 url-probe-results.json；含 checked_at 时区标签；缺号项不探测。
本步验证：通过

## 步骤 4 · 汇总探测结果并区分可达、拦截、失败
目的：把探测结果按可达、拦截、失败和缺号分类打印，避免把 403 写成网站不存在，也避免把 200 写成工具已验证。

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-haiwai-tools/exercise
python3 - <<'PY'
import json
from collections import Counter
p=json.load(open('url-probe-results.json'))
print('checked_at:', p['checked_at'])
print('method:', p['method'])
print('counts:', json.dumps(p['counts'], ensure_ascii=False))
rows=[r for r in p['rows'] if r['article_no']!='article-id']
with_url=[r for r in rows if r['official_url']]
print('已填官网数:', len(with_url))
for label in ['可达','被拦截或需登录（站点存在但未放行）','404','网络或证书失败','原文缺号未探测']:
    items=[r for r in p['rows'] if r['classification']==label]
    print(f'--- {label} ({len(items)}) ---')
    for r in items:
        st=r['result'].get('status')
        err=r['result'].get('error') or ''
        final=r['result'].get('final_url') or ''
        print(f"  {r['article_no']} {r['name']}: status={st} final={final} err={err[:120]}")
inferred=[r for r in rows if r['confidence']=='inferred']
print('推断网址探测结果:')
for r in inferred:
    print(' ', r['name'], r['classification'], r['result'].get('status'))
art=next(r for r in p['rows'] if r['article_no']=='article-id')
print('独立文章链接:', art['classification'], art['result'])
PY
```

真实结果：退出码 0，输出 4569 字符。

```text
checked_at: 2026-11-11 01:22:18 Asia/Shanghai
method: HTTP GET, follow redirects, no auth, no POST, no referral parameters
counts: {"可达": 53, "原文缺号未探测": 1, "被拦截或需登录（站点存在但未放行）": 5}
已填官网数: 57
--- 可达 (53) ---
  1 沉浸式翻译: status=200 final=https://immersivetranslate.com/en/ err=
  2 AITDK: status=200 final=https://aitdk.com/ err=
  3 SiteData: status=200 final=https://sitedata.dev/ err=
  4 Similarweb: status=200 final=https://www.similarweb.com/ err=
  5 Wayback Machine: status=200 final=https://web.archive.org/ err=
  6 Wappalyzer: status=200 final=https://www.wappalyzer.com/ err=
  7 Google Trends: status=200 final=https://trends.google.com/trends/ err=
  8 Exploding Topics: status=200 final=https://explodingtopics.com/ err=
  9 Screaming Frog SEO Spider: status=200 final=https://www.screamingfrog.co.uk/seo-spider/ err=
  10 SEO Minion: status=200 final=https://keywordseverywhere.com/seominion/ err=
  11 Semrush: status=200 final=https://www.semrush.com/ err=
  12 Moz Link Explorer: status=200 final=https://moz.com/link-explorer err=
  13 Ahrefs: status=200 final=https://ahrefs.com/ err=
  15 Linkhouse: status=200 final=https://linkhouse.net/ err=
  16 Collaborator: status=200 final=https://collaborator.pro/ err=
  54-early Adsy: status=200 final=https://adsy.com/ err=
  17 Figma: status=202 final=https://www.figma.com/ err=
  18 Framer: status=200 final=https://www.framer.com/ err=
  19 IconPark: status=200 final=https://iconpark.oceanengine.com/ err=
  20 OpenRouter: status=200 final=https://openrouter.ai/ err=
  21 Dify: status=200 final=https://dify.ai/ err=
  22 Replicate: status=200 final=https://replicate.com/ err=
  23 n8n: status=200 final=https://n8n.io/ err=
  25 Ideogram: status=200 final=https://ideogram.ai/ err=
  26 Loom: status=200 final=https://www.loom.com/ err=
  27 Screen Studio: status=200 final=https://screen.studio/ err=
  28 Cloudflare: status=200 final=https://www.cloudflare.com/ err=
  29 Vercel: status=200 final=https://vercel.com/ err=
  30 DeepL: status=200 final=https://www.deepl.com/en err=
  31 Weglot: status=200 final=https://www.weglot.com/ err=
  32 Lokalise: status=200 final=https://lokalise.com/ err=
  33 Stripe: status=200 final=https://stripe.com/ err=
  34 Paddle: status=200 final=https://www.paddle.com/ err=
  35 Lemon Squeezy: status=200 final=https://www.lemonsqueezy.com/ err=
  36 Starryblu: status=200 final=https://www.starryblu.com/ err=
  37 Termly: status=200 final=https://termly.io/ err=
  39 Uneed: status=200 final=https://www.uneed.best/ err=
  40 Microlaunch: status=200 final=https://microlaunch.net/ err=
  41 BetaList: status=200 final=https://betalist.com/ err=
  42a Discord: status=200 final=https://discord.com/ err=
  42b Disboard: status=200 final=https://disboard.org/ err=
  45 Typefully: status=200 final=https://typefully.com/ err=
  46 Beehiiv: status=200 final=https://www.beehiiv.com/ err=
  47 Customer: status=200 final=https://customer.io/ err=
  48 Loops: status=200 final=https://loops.so/ err=
  49 Google Search Console: status=200 final=https://search.google.com/search-console/about err=
  50 Google Analytics 4: status=200 final=https://marketingplatform.google.com/about/analytics/ err=
  51 PostHog: status=200 final=https://posthog.com/ err=
  52 Microsoft Clarity: status=200 final=https://clarity.microsoft.com/ err=
  53 Feedlog: status=200 final=https://feedlog.ai/ err=
  55 Crisp: status=200 final=https://crisp.chat/en/ err=
  56 Cursorful: status=200 final=https://cursorful.com/ err=
  article-id X 独立文章链接: status=200 final=https://x.com/i/jf/onboarding/web?redirect_after_login=%2Fi%2Farticle%2F2110257071849603072&mode=login err=
--- 被拦截或需登录（站点存在但未放行） (5) ---
  53-early Fiverr: status=403 final=https://www.fiverr.com/ err=HTTPError 403 Forbidden
  24 Midjourney: status=403 final=https://www.midjourney.com/ err=HTTPError 403 Forbidden
  38 Product Hunt: status=403 final=https://www.producthunt.com/ err=HTTPError 403 Forbidden
  43 Toolify: status=403 final=https://www.toolify.ai/ err=HTTPError 403 Forbidden
  44 There's An AI For That: status=403 final=https://theresanaiforthat.com/ err=HTTPError 403 Forbidden
--- 404 (0) ---
--- 网络或证书失败 (0) ---
--- 原文缺号未探测 (1) ---
  14 （原文缺号）: status=None final= err=missing_from_article
推断网址探测结果:
  Customer 可达 200
独立文章链接: 可达 {'requested_url': 'https://x.com/i/article/2110257071849603072', 'ok': True, 'status': 200, 'final_url': 'https://x.com/i/jf/onboarding/web?redirect_after_login=%2Fi%2Farticle%2F2110257071849603072&mode=login', 'elapsed_ms': 230, 'error': None, 'redirected': True}
```

验证：退出码 0；独立文章链接结果被单独列出；推断项 Customer 被单独列出。
本步验证：通过

## 步骤 5 · 目录纪律单元测试
目的：锁定缺号 14、编号 53 对应两个不同工具、Adsy 错位于第 2 章、Customer 为推断、探测 URL 不含推荐码。

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-haiwai-tools/exercise
python3 -m unittest test_catalog.py -v
```

真实结果：退出码 0，输出 686 字符。

```text
test_adsy_is_in_chapter_two (test_catalog.TestCatalog.test_adsy_is_in_chapter_two) ... ok
test_customer_is_inferred (test_catalog.TestCatalog.test_customer_is_inferred) ... ok
test_missing_number_fourteen (test_catalog.TestCatalog.test_missing_number_fourteen) ... ok
test_no_referral_in_probe_urls (test_catalog.TestCatalog.test_no_referral_in_probe_urls) ... ok
test_number_53_appears_twice_as_different_tools (test_catalog.TestCatalog.test_number_53_appears_twice_as_different_tools) ... ok
test_probe_results_if_present (test_catalog.TestCatalog.test_probe_results_if_present) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
```

验证：退出码 0，测试全部 OK。
本步验证：通过

## 未验证边界

- 官网 HTTP 状态只说明地址能否打开，不证明功能、定价、作者用法或「经过实战验证」。
- Customer 的官网是根据功能描述推断的 Customer.io，即使该站可达也不能证明作者指的就是它。
- SiteData 按检索对应到 sitedata.dev，名称有歧义。
- 没有做支付测试、外链采购、账号注册或工具深度试用。
- 原文推荐码未使用。独立文章链接若 404，正文仍以母帖 article.plain_text 为准。
- 本日志不是第三方独立审核。

汇总：全部步骤退出码为 0。各步：[{'i': 1, 'returncode': 0, 'ok': True, 'chars': 446}, {'i': 2, 'returncode': 0, 'ok': True, 'chars': 2124}, {'i': 3, 'returncode': 0, 'ok': True, 'chars': 4543}, {'i': 4, 'returncode': 0, 'ok': True, 'chars': 4569}, {'i': 5, 'returncode': 0, 'ok': True, 'chars': 686}]
