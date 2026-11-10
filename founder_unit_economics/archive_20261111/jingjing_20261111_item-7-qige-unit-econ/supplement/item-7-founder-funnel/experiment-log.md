# 先销售再交付：自述路径与单位经济 · 真实实验日志

执行时间：2026-11-11 01:20:16 CST（UTC+8）

只读公共研究＋云端隔离实验。自编程序不是上游实现，除明确标出的官方构建。

## 运行带标签的漏斗模型
目的：用作者自述与教学假设生成派生指标和27组敏感度

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-founder-funnel
python3 exercise/funnel.py
```

真实输出（exit=0）：
```text
derived {
  "avg_order_if_100": 5000.0,
  "service_delivery_cost": 200000.0,
  "service_contribution": 300000.0,
  "ad_orders": 20.0,
  "cac": 1000.0,
  "contrib_per_order": 3000.0,
  "ad_profit_under_assumptions": 40000.0,
  "net_course_revenue_per_seat": 2682.0,
  "seats_to_match_claimed_gmv": 186.4,
  "photo_listing_is_not_a_profit_model": true,
  "investment_excluded_from_profit": true
}
wrote /workspace/reminder-batch-2026-11-11/item-7-founder-funnel/exercise/results.json /workspace/reminder-batch-2026-11-11/item-7-founder-funnel/exercise/sensitivity.csv rows 27
PASS inputs_tagged all inputs tagged
PASS claims_not_measured no input marked measured
PASS investment_not_in_profit investment excluded
PASS photo_flag 5 yuan is process test
PASS avg_order 5000.0
PASS contrib 3000.0
PASS sensitivity_27 27
PASS sensitivity_direction (10000.0, 40000.0)
PASS stress_negative -30000.0
assertions=9 failed=0

```
验证：退出码0；assertions=9 failed=0；没有任何输入被标成measured

## 查看敏感度表
目的：直接读取表格，确认基准与高压组合的利润方向

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-founder-funnel
python3 -c "import csv; rows=list(csv.DictReader(open('exercise/sensitivity.csv'))); print('rows',len(rows)); base=next(r for r in rows if r['is_base']=='True'); bad=next(r for r in rows if r['close_rate']=='0.05' and r['delivery_cost_ratio']=='0.6' and r['ad_spend']=='50000'); print('base',base['profit'],'stress',bad['profit'])"
```

真实输出（exit=0）：
```text
rows 27
base 40000.0 stress -30000.0

```
验证：高压利润低于基准且为负

## 确认融资未进入利润
目的：防止把千万投资误写成营业收入

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-founder-funnel
python3 -c "import json; d=json.load(open('exercise/results.json')); print(d['derived']['investment_excluded_from_profit']); print(d['inputs']['investment']['source']); print(d['disclaimer'])"
```

真实输出（exit=0）：
```text
{'value': True, 'source': 'derived', 'note': '融资不是营业收入，模型利润不含投资额'}
author_claim
作者融资、GMV、课程收入和场地均为自述，本模型只做带标签的算术敏感度，不是财务审计。

```
验证：输出含 True 与 author_claim

## 留下模型指纹
目的：锁定模型与结果

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-founder-funnel
sha256sum exercise/funnel.py exercise/results.json exercise/sensitivity.csv
```

真实输出（exit=0）：
```text
4a71aa28ad0cd8b14915fcf82e809996797b3a2001f4be85c2f5a65e54cf788f  exercise/funnel.py
41d17549644e16a6fc19ca7aed023dd388c89d27a6db348680931256189bc1c4  exercise/results.json
0d4a366547634939f01c8bdd0f5e3e4fe0b74b79fb1c10ec79b677ffbb7f3bd3  exercise/sensitivity.csv

```
验证：文件存在且哈希可复算


## 未验证边界
未核验闲鱼后台、广告账单、课程销量、退款率、投资协议或办公租赁。模型中的转化率、交付成本、广告花费均为教学假设。不打电话、不注册、不投流、不推广课程。
