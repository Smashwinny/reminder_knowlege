# 198账号清单真实实验日志
日期：2026-11-11T01:12:16.929687+08:00（Asia/Shanghai）
真实输入为X Article正文；原文账号计数不是当前账号表现验证。筛选/敏感性/老化样本完全合成，未调用X账号数据接口，不标记真人合格/不合格。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item04
python3 exercise/source_filter_lab.py manifest
```
```text
[
  {
    "file": "source-post.json",
    "bytes": 74602,
    "sha256": "755abbd914aa4f66a4af2c8f7b2b7fab266c9ba29ba2a9278f8e3ee4189c9924"
  },
  {
    "file": "article.txt",
    "bytes": 28387,
    "sha256": "eee3e5513a679383ef04e1868d69d4477c8cfe98b35fe11d0abaa6862a80d828"
  },
  {
    "file": "x-data-dictionary.html",
    "bytes": 684227,
    "sha256": "c4bc0ec5f10ddbda883c8d3db52d505642db36a036a74449761c32d8faf95b80"
  },
  {
    "file": "python-statistics.html",
    "bytes": 151303,
    "sha256": "95a915bafb5f0e5cb730f0ae9fc4dcbc29685d4aae701d4e3d1960aba085695e"
  }
]

```
退出码：0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item04
python3 exercise/source_filter_lab.py audit
```
```text
{
  "top_count": 30,
  "full_count": 168,
  "total": 198,
  "unique_casefold": 198,
  "cross_duplicates": [],
  "new_markers": 140,
  "arithmetic_old": 146,
  "arithmetic_drop_reasons": 45,
  "arithmetic_final": 198,
  "category_sum": 198,
  "real_metric_rows_available": 0
}
{
  "top30": [
    "dotey",
    "Khazix0918",
    "lijigang",
    "op7418",
    "tianyi",
    "yetone",
    "CuiMao",
    "Lakr233",
    "turingou",
    "waylybaye",
    "HiTw93",
    "Saccc_c",
    "Pluvio9yte",
    "oran_ge",
    "xiaohuiyuan",
    "AI_Jasonyu",
    "evilcos",
    "Jackyi_ld",
    "Michael_Liu93",
    "Yuanshan0626",
    "lanhubiji",
    "cymm66",
    "qinbafrank",
    "Svwang1",
    "tychozzz",
    "ooeli_eth",
    "yiren_ai",
    "CrazyKaomei",
    "pengchujin",
    "HiFrey"
  ],
  "full168": [
    "tinyfool",
    "geekbb",
    "tualatrix",
    "xicilion",
    "nihui",
    "lewangx",
    "yanhua1010",
    "skywind3000",
    "LinearUncle",
    "chenchengpro",
    "LawrenceW_Zen",
    "kasong2048",
    "luinlee",
    "RookieRicardoR",
    "hank_zhao",
    "yrmkejun",
    "riba2534",
    "yangyi",
    "gengdaJ",
    "chunxiangai",
    "canghe",
    "shao__meng",
    "MinLiBuilds",
    "yan5xu",
    "xiaomovps",
    "m1ssuo",
    "guansi",
    "liyue_ai",
    "MANISH1027512",
    "Jason23818126",
    "tuturetom",
    "xbanboo",
    "GeekCatX",
    "joshesye",
    "aiwarts",
    "noahduck283",
    "yanliudreamer",
    "AxtonLiu",
    "akokoi1",
    "wangray",
    "Adam38363368936",
    "369Serena",
    "eternityspring",
    "ameliax111",
    "wquguru",
    "alacheng",
    "wey_gu",
    "dingyi",
    "AYi_AInotes",
    "Vincent_AINotes",
    "Hayami_kiraa",
    "randyloop",
    "dov_wo",
    "yaohui12138",
    "Zesee",
    "tangjinzhou",
    "Russell3402",
    "abskoop",
    "vista8",
    "GitHub_Daily",
    "Lonely__MH",
    "goan999999",
    "xiangxiang103",
    "xilo2991",
    "aehyok",
    "alin_zone",
    "lxfater",
    "AlchainHust",
    "gkxspace",
    "liuyi0922",
    "hzlzh",
    "servasyy_ai",
    "SUOHA_AI",
    "kevinma_dev_zh",
    "fkysly",
    "xmmxovo",
    "xiongchun007",
    "beefnoode",
    "guishou_56",
    "xiqingongzi",
    "meepodev",
    "s1ntone",
    "litang0908",
    "ai_xiaomu",
    "jinchenma_ai",
    "XiaohuiAI666",
    "cheery9998",
    "momoai_daily",
    "xiaohu",
    "Gorden_Sun",
    "MaxForAI",
    "Smartpigai",
    "frxiaobei",
    "Valley101_Qian",
    "ai_9684xtpa",
    "KuiGas",
    "xingpt",
    "tmel0211",
    "Crypto77qi",
    "JJayGentleman",
    "_zheergen",
    "Bitwux",
    "Rocky_Bitcoin",
    "Ru7Longcrypto",
    "BTCqzy1",
    "0xZZB",
    "0xduyan",
    "hisevenih",
    "kun66666677",
    "jason_chen998",
    "hexiecs",
    "web4miko",
    "im23pds",
    "DujunX",
    "cryptobraveHQ",
    "0xAA_Science",
    "captain_kent",
    "sanyuanVC",
    "yuexiaoyu",
    "ZhanweiC",
    "joezhoublack",
    "Jhy256",
    "catmangox",
    "wufantouzi",
    "punk2898",
    "lianyanshe",
    "ViewsOfChris",
    "Tsla99T",
    "LZRationalnvest",
    "Dragonhau66",
    "jimmyhuli",
    "LMDFinance",
    "innomad_io",
    "Will_Yang_",
    "xiaomusg",
    "jay30494",
    "michelle_z21331",
    "Web3Lanju",
    "YannisHan77",
    "laowangbj110",
    "yunfan716",
    "168MrZ",
    "mafang71",
    "PandaTalk8",
    "gefei55",
    "yyyole",
    "zhufengme",
    "indiehackercase",
    "sitinme",
    "tonychuhai",
    "yucheng",
    "rionaifantasy",
    "qzhxjhj",
    "stark_nico99",
    "hezhiyan7",
    "santiagoyoungus",
    "daluoseo",
    "sino_go_global",
    "CoderJeffLee",
    "0xEcho99",
    "loki_yan_seo",
    "shenpengwdh",
    "knowledgefxg",
    "sspai_com",
    "CaptainLufei999",
    "Nicole_yang88",
    "Glen92750101",
    "dliphotos"
  ],
  "note": "原文结构核验，不是当前账号有效性/入选标准复核"
}

```
退出码：0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item04
python3 exercise/source_filter_lab.py filtering
```
```text
{
  "synthetic_only": true,
  "fixtures": {
    "boundary": {
      "followers": 5000,
      "days": 14,
      "originals": 8,
      "zh_share": 0.625,
      "median_views": 300,
      "median_likes": 0,
      "promotion": false,
      "excluded_topic": false
    },
    "likes_only": {
      "followers": 100000,
      "days": 14,
      "originals": 8,
      "zh_share": 0.625,
      "median_views": 999,
      "median_likes": 20,
      "promotion": false,
      "excluded_topic": false
    },
    "too_small": {
      "followers": 4999,
      "days": 14,
      "originals": 8,
      "zh_share": 0.625,
      "median_views": 300,
      "median_likes": 0,
      "promotion": false,
      "excluded_topic": false
    },
    "exact_half_zh": {
      "followers": 5000,
      "days": 14,
      "originals": 8,
      "zh_share": 0.5,
      "median_views": 300,
      "median_likes": 0,
      "promotion": false,
      "excluded_topic": false
    },
    "missing_metrics": {
      "followers": 5000,
      "days": 14,
      "originals": 8,
      "zh_share": 0.625,
      "median_views": null,
      "median_likes": null,
      "promotion": false,
      "excluded_topic": false
    },
    "manual_promotion": {
      "followers": 5000,
      "days": 14,
      "originals": 8,
      "zh_share": 0.625,
      "median_views": 300,
      "median_likes": 0,
      "promotion": true,
      "excluded_topic": false
    },
    "high_frequency": {
      "followers": 5000,
      "days": 14,
      "originals": 451,
      "zh_share": 0.625,
      "median_views": 300,
      "median_likes": 0,
      "promotion": false,
      "excluded_topic": false
    },
    "relative_floor_fail": {
      "followers": 100000,
      "days": 14,
      "originals": 8,
      "zh_share": 0.625,
      "median_views": 900,
      "median_likes": 4,
      "promotion": false,
      "excluded_topic": false
    }
  },
  "results": {
    "boundary": {
      "status": "pass",
      "reasons": [],
      "unknown": []
    },
    "likes_only": {
      "status": "pass",
      "reasons": [],
      "unknown": []
    },
    "too_small": {
      "status": "reject",
      "reasons": [
        "followers"
      ],
      "unknown": []
    },
    "exact_half_zh": {
      "status": "reject",
      "reasons": [
        "zh_share"
      ],
      "unknown": []
    },
    "missing_metrics": {
      "status": "unknown",
      "reasons": [],
      "unknown": [
        "interaction"
      ]
    },
    "manual_promotion": {
      "status": "reject",
      "reasons": [
        "promotion"
      ],
      "unknown": []
    },
    "high_frequency": {
      "status": "reject",
      "reasons": [
        "originals"
      ],
      "unknown": []
    },
    "relative_floor_fail": {
      "status": "reject",
      "reasons": [
        "interaction"
      ],
      "unknown": []
    }
  },
  "counts": {
    "pass": 2,
    "reject": 5,
    "unknown": 1
  },
  "policy_note": "450为练习离散化上限，原文约450需人工裁量；中文用严格大于一半"
}

```
退出码：0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item04
python3 exercise/source_filter_lab.py sensitivity
```
```text
{
  "synthetic_views": [
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    10000
  ],
  "mean": 1337.5,
  "median": 100.0,
  "mean_threshold_pass": true,
  "median_threshold_pass": false,
  "floor_sweep": {
    "299": "pass",
    "300": "pass",
    "301": "reject"
  },
  "meaning": "只说明本合成样本及规则敏感性，不推断真人质量"
}

```
退出码：0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item04
python3 exercise/source_filter_lab.py aging
```
```text
{
  "synthetic_only": true,
  "rows": [
    {
      "days_since_snapshot": 0,
      "last_post_age": 7,
      "decision": "pass"
    },
    {
      "days_since_snapshot": 7,
      "last_post_age": 14,
      "decision": "pass"
    },
    {
      "days_since_snapshot": 8,
      "last_post_age": 15,
      "decision": "reject"
    },
    {
      "days_since_snapshot": 180,
      "last_post_age": 187,
      "decision": "reject"
    }
  ],
  "original_claim": "半年约为作者复盘经验，不是经过生存分析证明的通用寿命",
  "scheduled_tasks_created": 0
}

```
退出码：0

## 6
```bash
cd /workspace/reminder-batch/worker-689b81da/item04
python3 exercise/source_filter_lab.py test
```
```text
test_booleans_not_numbers (__main__.Tests.test_booleans_not_numbers) ... ok
test_both_fail (__main__.Tests.test_both_fail) ... ok
test_boundary (__main__.Tests.test_boundary) ... ok
test_half (__main__.Tests.test_half) ... ok
test_high (__main__.Tests.test_high) ... ok
test_like_or (__main__.Tests.test_like_or) ... ok
test_median_even (__main__.Tests.test_median_even) ... ok
test_missing (__main__.Tests.test_missing) ... ok
test_missing_one_other_pass (__main__.Tests.test_missing_one_other_pass) ... ok
test_nan_not_zero (__main__.Tests.test_nan_not_zero) ... ok
test_older (__main__.Tests.test_older) ... ok
test_promotion (__main__.Tests.test_promotion) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.000s

OK

```
退出码：0

官方X数据字典WebFetch返回403；读取同一公开URL的普通HTTP请求成功，已保存HTML/正文。未使用Bearer Token或用户密钥，未照文档样例调用api.x.com。Python3.13官方统计文档已保存；早先WebFetch默认页呈现3.15，本轮计算实际使用Python3.13标准库。

## 计数口径修订与真实重跑
初次统计🆕字面字符140，包含两处图例，不应当作人数。增加“有@handle的标记行”口径，实际重跑：
```bash
python3 exercise/source_filter_lab.py audit
```
```text
{
  "top_count": 30,
  "full_count": 168,
  "total": 198,
  "unique_casefold": 198,
  "cross_duplicates": [],
  "new_markers_literal": 140,
  "marked_account_rows": 138,
  "arithmetic_old": 146,
  "arithmetic_drop_reasons": 45,
  "arithmetic_final": 198,
  "category_sum": 198,
  "real_metric_rows_available": 0
}
{
  "top30": [
    "dotey",
    "Khazix0918",
    "lijigang",
    "op7418",
    "tianyi",
    "yetone",
    "CuiMao",
    "Lakr233",
    "turingou",
    "waylybaye",
    "HiTw93",
    "Saccc_c",
    "Pluvio9yte",
    "oran_ge",
    "xiaohuiyuan",
    "AI_Jasonyu",
    "evilcos",
    "Jackyi_ld",
    "Michael_Liu93",
    "Yuanshan0626",
    "lanhubiji",
    "cymm66",
    "qinbafrank",
    "Svwang1",
    "tychozzz",
    "ooeli_eth",
    "yiren_ai",
    "CrazyKaomei",
    "pengchujin",
    "HiFrey"
  ],
  "full168": [
    "tinyfool",
    "geekbb",
    "tualatrix",
    "xicilion",
    "nihui",
    "lewangx",
    "yanhua1010",
    "skywind3000",
    "LinearUncle",
    "chenchengpro",
    "LawrenceW_Zen",
    "kasong2048",
    "luinlee",
    "RookieRicardoR",
    "hank_zhao",
    "yrmkejun",
    "riba2534",
    "yangyi",
    "gengdaJ",
    "chunxiangai",
    "canghe",
    "shao__meng",
    "MinLiBuilds",
    "yan5xu",
    "xiaomovps",
    "m1ssuo",
    "guansi",
    "liyue_ai",
    "MANISH1027512",
    "Jason23818126",
    "tuturetom",
    "xbanboo",
    "GeekCatX",
    "joshesye",
    "aiwarts",
    "noahduck283",
    "yanliudreamer",
    "AxtonLiu",
    "akokoi1",
    "wangray",
    "Adam38363368936",
    "369Serena",
    "eternityspring",
    "ameliax111",
    "wquguru",
    "alacheng",
    "wey_gu",
    "dingyi",
    "AYi_AInotes",
    "Vincent_AINotes",
    "Hayami_kiraa",
    "randyloop",
    "dov_wo",
    "yaohui12138",
    "Zesee",
    "tangjinzhou",
    "Russell3402",
    "abskoop",
    "vista8",
    "GitHub_Daily",
    "Lonely__MH",
    "goan999999",
    "xiangxiang103",
    "xilo2991",
    "aehyok",
    "alin_zone",
    "lxfater",
    "AlchainHust",
    "gkxspace",
    "liuyi0922",
    "hzlzh",
    "servasyy_ai",
    "SUOHA_AI",
    "kevinma_dev_zh",
    "fkysly",
    "xmmxovo",
    "xiongchun007",
    "beefnoode",
    "guishou_56",
    "xiqingongzi",
    "meepodev",
    "s1ntone",
    "litang0908",
    "ai_xiaomu",
    "jinchenma_ai",
    "XiaohuiAI666",
    "cheery9998",
    "momoai_daily",
    "xiaohu",
    "Gorden_Sun",
    "MaxForAI",
    "Smartpigai",
    "frxiaobei",
    "Valley101_Qian",
    "ai_9684xtpa",
    "KuiGas",
    "xingpt",
    "tmel0211",
    "Crypto77qi",
    "JJayGentleman",
    "_zheergen",
    "Bitwux",
    "Rocky_Bitcoin",
    "Ru7Longcrypto",
    "BTCqzy1",
    "0xZZB",
    "0xduyan",
    "hisevenih",
    "kun66666677",
    "jason_chen998",
    "hexiecs",
    "web4miko",
    "im23pds",
    "DujunX",
    "cryptobraveHQ",
    "0xAA_Science",
    "captain_kent",
    "sanyuanVC",
    "yuexiaoyu",
    "ZhanweiC",
    "joezhoublack",
    "Jhy256",
    "catmangox",
    "wufantouzi",
    "punk2898",
    "lianyanshe",
    "ViewsOfChris",
    "Tsla99T",
    "LZRationalnvest",
    "Dragonhau66",
    "jimmyhuli",
    "LMDFinance",
    "innomad_io",
    "Will_Yang_",
    "xiaomusg",
    "jay30494",
    "michelle_z21331",
    "Web3Lanju",
    "YannisHan77",
    "laowangbj110",
    "yunfan716",
    "168MrZ",
    "mafang71",
    "PandaTalk8",
    "gefei55",
    "yyyole",
    "zhufengme",
    "indiehackercase",
    "sitinme",
    "tonychuhai",
    "yucheng",
    "rionaifantasy",
    "qzhxjhj",
    "stark_nico99",
    "hezhiyan7",
    "santiagoyoungus",
    "daluoseo",
    "sino_go_global",
    "CoderJeffLee",
    "0xEcho99",
    "loki_yan_seo",
    "shenpengwdh",
    "knowledgefxg",
    "sspai_com",
    "CaptainLufei999",
    "Nicole_yang88",
    "Glen92750101",
    "dliphotos"
  ],
  "note": "原文结构核验，不是当前账号有效性/入选标准复核"
}

```
退出码0。名单行138，与正文138一致。前面初次输出保留作为修订轨迹，不是两个版本文章。
