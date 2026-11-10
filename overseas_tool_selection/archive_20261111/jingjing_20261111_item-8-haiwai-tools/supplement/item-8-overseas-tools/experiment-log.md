# 出海工具清单：完整长文、编号与可达性 · 真实实验日志

执行时间：2026-11-11 01:20:18 CST（UTC+8）

只读公共研究＋云端隔离实验。自编程序不是上游实现，除明确标出的官方构建。

## 从官方长文提取目录
目的：清点章节、编号、是否写到总结

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-overseas-tools
python3 exercise/summarize.py extract
```

真实输出（exit=0）：
```text
{
  "sections": [
    "市场机会与竞品调研",
    "SEO 与内容资产",
    "产品设计、AI 能力与演示",
    "建站、本地化与基础设施",
    "支付、跨境资金与合规",
    "增长获客与渠道分发",
    "数据分析与用户反馈"
  ],
  "numbered_entries": 56,
  "numbers": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    15,
    16,
    53,
    54,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    55,
    56
  ],
  "missing": [
    14
  ],
  "duplicate_numbers": [
    53
  ],
  "growth_chapter_complete": true,
  "ends_with_summary": true,
  "title_in_post": "靠Web出海赚美刀，7大核心方向精选56个宝藏工具，帮你把想法变成收益",
  "sha256_article": "a7dbcfa98840cdeccb8f5eb557a457cfca264a1a608d5edba7e7b98f980eecbb"
}

```
验证：growth_chapter_complete 与 ends_with_summary 为 true

## 读取已执行的HTTP结果
目的：汇报带时间戳的可达性统计和事后更正

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-overseas-tools
python3 exercise/summarize.py status
```

真实输出（exit=0）：
```text
{
  "checked_at": "2026-11-11 01:15:38 CST（UTC+8）",
  "named_entries": 58,
  "reachable_2xx_3xx": 53,
  "failed_or_blocked": 3,
  "skipped_missing": 2,
  "article_claimed_tools": 56,
  "numbering_notes": "原文缺14；53出现两次（Fiverr与Feedlog）；增长章在官方article.plain_text中是完整的，不是截断。",
  "followup_at": "2026-11-11 01:17:29 CST（UTC+8）",
  "correction": "已撤回误把 sitedata.io（信贷评分）当作SEO工具；Feedlog改记 feedlog.ai 并标明仍是推断；Similarweb/Fiverr 的403/404在换UA后复检为200；Midjourney/Toolify/TAAFT仍403。"
}
rows 58

```
验证：输出含 checked_at 与 correction

## 核验编号与更正规则
目的：确认未把截断写错、未把错误域名标成成功

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-overseas-tools
python3 exercise/summarize.py verify
```

真实输出（exit=0）：
```text
PASS not_truncated growth+总结 present
PASS missing_14 [14]
PASS dup_53 [53]
PASS 56_writeups 56
PASS has_dated_status all dated
PASS site_data_not_wrong_domain SiteData not false-positive
PASS feedlog_inferred_only Feedlog tagged inferred
assertions=7 failed=0

```
验证：退出码0；site_data_not_wrong_domain PASS

## 留下清单指纹
目的：锁定长文摘录与状态表

```bash
cd /workspace/reminder-batch-2026-11-11/item-8-overseas-tools
sha256sum exercise/article_plain.txt exercise/url-status.json exercise/article-index.json
```

真实输出（exit=0）：
```text
a7dbcfa98840cdeccb8f5eb557a457cfca264a1a608d5edba7e7b98f980eecbb  exercise/article_plain.txt
a5566d8ad0b822da09f3fff49d74ba8cc2896f33a6436a75b8eda8ba503d31d3  exercise/url-status.json
debe4ea08ac4d81bea634a8e87724933c54ce81ee6cc90321ae1e0c9805bd6cd  exercise/article-index.json

```
验证：article-index 中的 sha256_article 可复算


## 未验证边界
未注册、未付款、未接入任何支付或广告账户。SiteData 官方域名仍未确认。部分站点在本环境返回 403，只说明被拦截。作者「56个经过实战验证」的说法未经本实验复现。未核对每个工具的当前定价与服务条款。
