# 七渠道学习真实实验日志
2026-11-11（Asia/Shanghai），Python3.13标准库。
原帖全文与7个渠道页面均通过WebFetch实读；另读Arena排名/事实性方法、arXiv about、1706.03762v7原文页面。不宣称复现Transformer训练或榜单测量。
公开HTML下载实际命令：python3 exercise/fetch_public.py；完整真实输出见fetch-output.txt。11URL中5份普通HTTP成功，6份403；这些6页WebFetch成功，已保存有限摘录而非伪造HTML。source-manifest分别记录两种读取与哈希。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item07
python3 exercise/source_flow_lab.py catalog
```
```text
{
  "channels": {
    "ai_news": "聚合发现",
    "the_batch": "编辑解读",
    "hf_papers": "社区发现",
    "alphaxiv": "研究发现与讨论",
    "arxiv_recent": "原始论文",
    "arena_home": "偏好评测入口",
    "aa_method": "性能/价格方法"
  },
  "raw_http_success": 5,
  "raw_http_failures": 6,
  "webfetch_read_excerpts": 6,
  "original_post_sha256": "e7bcea7fb0d9797f023b78368e46f1fb8c7ac0361fcd388c17f5d31dd7c2b4ac",
  "note": "主7渠道都经WebFetch实读；原始HTTP失败保留，与成功WebFetch不能混报"
}

```
exit=0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item07
python3 exercise/source_flow_lab.py dedupe
```
```text
{
  "real_anchor_extraction": {
    "hf_papers": {
      "href_id_occurrences": 92,
      "unique_family_count": 24,
      "unique_families": [
        "2609.05661",
        "2609.12397",
        "2609.16900",
        "2609.17496",
        "2609.17653",
        "2609.18323",
        "2609.18605",
        "2609.19499",
        "2609.19554",
        "2609.19656",
        "2609.19671",
        "2609.19745",
        "2609.19879",
        "2609.19969",
        "2609.20423",
        "2609.20511",
        "2609.20519",
        "2609.20612",
        "2609.20715",
        "2609.20744",
        "2609.20784",
        "2609.20800",
        "2609.20804",
        "2609.20817"
      ]
    },
    "arxiv_recent": {
      "href_id_occurrences": 145,
      "unique_family_count": 50,
      "unique_families": [
        "2611.11825",
        "2611.11840",
        "2611.11846",
        "2611.11848",
        "2611.11896",
        "2611.11898",
        "2611.11907",
        "2611.11913",
        "2611.11929",
        "2611.11965",
        "2611.11975",
        "2611.11995",
        "2611.12013",
        "2611.12014",
        "2611.12048",
        "2611.12060",
        "2611.12092",
        "2611.12095",
        "2611.12109",
        "2611.12114",
        "2611.12118",
        "2611.12120",
        "2611.12122",
        "2611.12128",
        "2611.12164",
        "2611.12167",
        "2611.12200",
        "2611.12222",
        "2611.12232",
        "2611.12291",
        "2611.12293",
        "2611.12300",
        "2611.12307",
        "2611.12333",
        "2611.12334",
        "2611.12356",
        "2611.12374",
        "2611.12377",
        "2611.12379",
        "2611.12393",
        "2611.12478",
        "2611.12552",
        "2611.12635",
        "2611.12640",
        "2611.12675",
        "2611.12762",
        "2611.12775",
        "2611.12816",
        "2611.12825",
        "2611.12865"
      ]
    },
    "paper_v7": {
      "href_id_occurrences": 15,
      "unique_family_count": 1,
      "unique_families": [
        "1706.03762"
      ]
    }
  },
  "synthetic_alias_examples": [
    {
      "family": "1706.03762",
      "version": "v7",
      "canonical": "https://arxiv.org/abs/1706.03762v7"
    },
    {
      "family": "1706.03762",
      "version": "v6",
      "canonical": "https://arxiv.org/abs/1706.03762v6"
    },
    {
      "family": "1706.03762",
      "version": null,
      "canonical": "https://arxiv.org/abs/1706.03762"
    },
    {
      "family": "1706.03762",
      "version": null,
      "canonical": "https://arxiv.org/abs/1706.03762"
    }
  ],
  "example_family_count": 1,
  "example_version_key_count": 3,
  "warning": "链接中论文ID出现/去重不代表全文已读、当日主榜成员或新论文唯一数量"
}

```
exit=0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item07
python3 exercise/source_flow_lab.py evidence
```
```text
{
  "ledger": [
    {
      "claim": "arXiv本身不做同行评审",
      "file": "snapshots/arxiv_about.txt",
      "needle": "not peer-reviewed",
      "matched": true
    },
    {
      "claim": "当前AA混合价格按cache/input/output=7:2:1",
      "file": "snapshots/aa_method.txt",
      "needle": "7:2:1",
      "matched": true
    },
    {
      "claim": "AA输出速率口径包含首token等待",
      "file": "snapshots/aa_method.txt",
      "needle": "includes time to first token",
      "matched": true
    }
  ],
  "scope": "只是已读方法文档的可定位文本证据；不验证榜单/论文结论/真实模型表现"
}

```
exit=0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item07
python3 exercise/source_flow_lab.py ranks
```
```text
{
  "synthetic_only": true,
  "intervals": {
    "A": [
      100,
      120
    ],
    "B": [
      105,
      125
    ],
    "C": [
      70,
      90
    ]
  },
  "rank_spreads": {
    "A": [
      1,
      2
    ],
    "B": [
      1,
      2
    ],
    "C": [
      3,
      3
    ]
  },
  "note": "套用官方排名区间端点公式，不估计Arena原始分数/置信区间或显著性"
}

```
exit=0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item07
python3 exercise/source_flow_lab.py cost
```
```text
{
  "synthetic_only": true,
  "order": [
    "cached",
    "uncached_input",
    "output"
  ],
  "USD_per_million": [
    0.2,
    1.0,
    4.0
  ],
  "tokens_small": [
    700,
    200,
    100
  ],
  "cost_small_USD": 0.00074,
  "tokens_large": [
    700,
    200,
    1000
  ],
  "cost_large_USD": 0.00434,
  "missing_price": null,
  "warning": "自选虚构价格与token，不是任何真实供应商报价或AA复测；缓存token只算一次"
}

```
exit=0

## 6
```bash
cd /workspace/reminder-batch/worker-689b81da/item07
python3 exercise/source_flow_lab.py test
```
```text
test_alias (__main__.Tests.test_alias) ... ok
test_bad_interval (__main__.Tests.test_bad_interval) ... ok
test_channel_count (__main__.Tests.test_channel_count) ... ok
test_cost_unit (__main__.Tests.test_cost_unit) ... ok
test_long_output (__main__.Tests.test_long_output) ... ok
test_missing (__main__.Tests.test_missing) ... ok
test_no_nan (__main__.Tests.test_no_nan) ... ok
test_rank_a (__main__.Tests.test_rank_a) ... ok
test_rank_c (__main__.Tests.test_rank_c) ... ok
test_unknown_host (__main__.Tests.test_unknown_host) ... ok
test_unrelated_path (__main__.Tests.test_unrelated_path) ... ok
test_version (__main__.Tests.test_version) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.001s

OK

```
exit=0

排名CI与价格都是明确合成fixture；没有付费API、模型调用、订阅/关注、定时任务或真实供应商价格复测。method关键字匹配只是可追溯定位，不等于科学结论验证。

归档脚本首次增加快照附件时缩进错误（IndentationError），在执行归档前失败；修正缩进后重跑，不影响上述实验输出或PDF。
