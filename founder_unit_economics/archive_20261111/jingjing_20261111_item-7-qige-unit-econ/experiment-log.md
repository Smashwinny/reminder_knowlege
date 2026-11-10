# 第7项真实实验日志：单位经济 / 漏斗模型

执行时间：2026-11-11 01:13:18 Asia/Shanghai（UTC+8）
工作目录：/workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
Python：3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]
环境：云端隔离目录；只读公开资料 + 离线数值实验。没有打电话、没有投放、没有改计费、没有使用用户密钥、没有把作者营收当实测。

## 步骤 1 · 列出全部假设并核验来源标签
目的：先把每条输入的数值和 source 标签打印出来，确认模型拒绝无标签入账，并区分作者自述与教学假设。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 unit_econ.py assumptions
```

真实结果：退出码 0，输出 1681 字符。

```text
货币: CNY
说明: 教学用单位经济与漏斗模型。所有数字都是模型输入，不是本批实测成交、也不是经审计的财务报表。
标签定义:
  [author_claim] 来自原帖或引用长文的作者自述原文，未经独立核实，禁止当作实测。
  [author_claim_derived] 由一条或多条自述粗略推算得到，推算过程透明，结论仍未核实。
  [teaching_assumption] 为了让模型能跑而设定的教学假设，不是作者数据，也不是市场调查结果。

=== funnel_teaching ===
  impressions: 20000  [teaching_assumption]
  ctr: 0.03  [teaching_assumption]
  inquiry_rate: 0.08  [teaching_assumption]
  close_rate_custom: 0.15  [teaching_assumption]
  close_rate_course: 0.04  [teaching_assumption]
  cpc: 1.5  [teaching_assumption]  作者只说「秘诀就是投流」，未给出 CPC、CPM 或 CAC。
=== economics ===
  test_sku_price: 5  [author_claim]  原文：「上架了一个5块钱帮别人用AI修图的商品」
  platform_fee_rate: 0.06  [teaching_assumption]  闲鱼等平台费率因类目而异，此处仅为教学占位，待验证。
  payment_fee_rate: 0.006  [teaching_assumption]  教学占位。
  custom_aov_teaching: 3000  [teaching_assumption]
  custom_aov_from_claim: 5000  [author_claim_derived]  由自述「上百单、GMV大概50万」按订单数=100 粗除得到；「上百」不是精确计数。
  delivery_cost_ratio_solo: 0.25  [teaching_assumption]  含自己时间的机会成本占位，不是作者工时记录。
  delivery_cost_ratio_outsourced: 0.55  [teaching_assumption]  教学占位。作者提到找朋友和团队合作，但未披露分成。
  refund_rate_custom: 0.05  [teaching_assumption]
  course_price: 2980  [author_claim]  原文：「第一个知识付费的产品定价是2980」
  course_fulfillment_cost: 200  [teaching_assumption]  平台、答疑、工具与退款准备的占位成本。
  course_refund_rate: 0.08  [teaching_assumption]
  claimed_year_orders: 100  [author_claim_derived]  原文：「25年一整年做了上百单」 取「上百」的下沿 100，仍是自述。
  claimed_year_gmv: 500000  [author_claim]  原文：「GMV大概50万」
  claimed_video_course_revenue: 100000  [author_claim_derived]  原文：「直接给我带来了十几万的课程收入」 「十几万」取下沿 10 万做演示，仍是自述。
  claimed_investment: 10000000  [author_claim]  原文：「拿到了千万投资」 未给出轮次、估值、到账与稀释，不能纳入经营单位经济。

校验：每条输入都带 source，模型拒绝无标签数值直接入账。
```

验证：退出码为 0；每条 funnel_teaching / economics 字段都打印了 source；出现 author_claim、author_claim_derived、teaching_assumption 三类标签说明。
本步验证：通过

## 步骤 2 · 教学保守情景：定制单与课程单位经济
目的：用全部教学假设跑通漏斗和贡献利润；定制单比较独自交付与外包交付；课程轨道只用自述标价 2980，成本和转化仍是教学假设。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 unit_econ.py base
```

真实结果：退出码 0，输出 2117 字符。

```text
【教学保守情景】定制商单漏斗（全部关键成本为 teaching_assumption，客单价也是教学假设，不是自述 GMV）
漏斗：展示 20000 → 点击 600.00 → 咨询 48.00 → 成交 7.2000
流量成本 = 点击 × CPC = 600.00 × ¥1.50 = ¥900.00
## 定制商单 · 独自交付假设
输入标签：
  - impressions: teaching_assumption
  - ctr: teaching_assumption
  - inquiry_rate: teaching_assumption
  - close_rate_custom: teaching_assumption
  - cpc: teaching_assumption
  - custom_aov_teaching: teaching_assumption
  - refund_rate_custom: teaching_assumption
  - fees: teaching_assumption+teaching_assumption
  - delivery_cost_ratio_solo: teaching_assumption
  成交单数: 7.2000
  客单价: ¥3,000.00
  收入: ¥21,600.00
  退款: ¥1,080.00
  净收入: ¥20,520.00
  平台/支付手续费: ¥1,354.32
  交付成本: ¥5,130.00
  履约成本: ¥0.00
  流量成本: ¥900.00
  贡献利润: ¥13,135.68
  CAC（流量成本/成交单数）: ¥125.00
  单笔贡献利润: ¥1,824.40
  贡献利润率: 60.81%

## 定制商单 · 外包交付假设（同一漏斗，只改交付成本占比）
输入标签：
  - impressions: teaching_assumption
  - ctr: teaching_assumption
  - inquiry_rate: teaching_assumption
  - close_rate_custom: teaching_assumption
  - cpc: teaching_assumption
  - custom_aov_teaching: teaching_assumption
  - refund_rate_custom: teaching_assumption
  - fees: teaching_assumption+teaching_assumption
  - delivery_cost_ratio_outsourced: teaching_assumption
  成交单数: 7.2000
  客单价: ¥3,000.00
  收入: ¥21,600.00
  退款: ¥1,080.00
  净收入: ¥20,520.00
  平台/支付手续费: ¥1,354.32
  交付成本: ¥11,286.00
  履约成本: ¥0.00
  流量成本: ¥900.00
  贡献利润: ¥6,979.68
  CAC（流量成本/成交单数）: ¥125.00
  单笔贡献利润: ¥969.40
  贡献利润率: 32.31%

课程漏斗：展示 20000 → 点击 600.00 → 咨询 48.00 → 成交 1.9200
## 课程（标价来自作者自述 2980，其余成本与转化为教学假设）
输入标签：
  - impressions: teaching_assumption
  - ctr: teaching_assumption
  - inquiry_rate: teaching_assumption
  - close_rate_course: teaching_assumption
  - cpc: teaching_assumption
  - course_price: author_claim
  - course_refund_rate: teaching_assumption
  - fees: teaching_assumption+teaching_assumption
  - course_fulfillment_cost: teaching_assumption
  成交单数: 1.9200
  客单价: ¥2,980.00
  收入: ¥5,721.60
  退款: ¥457.73
  净收入: ¥5,263.87
  平台/支付手续费: ¥347.42
  交付成本: ¥0.00
  履约成本: ¥353.28
  流量成本: ¥900.00
  贡献利润: ¥3,663.18
  CAC（流量成本/成交单数）: ¥468.75
  单笔贡献利润: ¥1,907.90
  贡献利润率: 64.02%

结论边界：以上贡献利润只在给定假设下成立，不能证明原帖收入或融资。
```

验证：退出码为 0；打印展示→点击→咨询→成交的人数、流量成本和贡献利润；明确写了不能证明原帖收入或融资。
本步验证：通过

## 步骤 3 · 单因子敏感分析与龙卷风排序
目的：在教学保守/独自交付基准上，对价格、退款率、费率、交付占比、流量成本、成交单数分别做 ±10%、±30% 扰动，按贡献利润振幅排序。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 unit_econ.py sensitivity
```

真实结果：退出码 0，输出 1698 字符。

```text
基准贡献利润（教学保守 / 独自交付）: ¥13,135.68
factor	delta	new_value	contribution	change	margin
price	-30%	2100.000000	8924.98	-4210.70	59.03%
price	-10%	2700.000000	11732.11	-1403.57	60.35%
price	+10%	3300.000000	14539.25	1403.57	61.19%
price	+30%	3900.000000	17346.38	4210.70	61.77%
refund_rate	-30%	0.035000	13357.30	221.62	61.84%
refund_rate	-10%	0.045000	13209.55	73.87	61.16%
refund_rate	+10%	0.055000	13061.81	-73.87	60.47%
refund_rate	+30%	0.065000	12914.06	-221.62	59.79%
fee_rate	-30%	0.046200	13541.98	406.30	62.69%
fee_rate	-10%	0.059400	13271.11	135.43	61.44%
fee_rate	+10%	0.072600	13000.25	-135.43	60.19%
fee_rate	+30%	0.085800	12729.38	-406.30	58.93%
delivery_cost_ratio	-30%	0.175000	14674.68	1539.00	67.94%
delivery_cost_ratio	-10%	0.225000	13648.68	513.00	63.19%
delivery_cost_ratio	+10%	0.275000	12622.68	-513.00	58.44%
delivery_cost_ratio	+30%	0.325000	11596.68	-1539.00	53.69%
traffic_cost	-30%	630.000000	13405.68	270.00	62.06%
traffic_cost	-10%	810.000000	13225.68	90.00	61.23%
traffic_cost	+10%	990.000000	13045.68	-90.00	60.40%
traffic_cost	+30%	1170.000000	12865.68	-270.00	59.56%
n_paid	-30%	5.040000	8924.98	-4210.70	59.03%
n_paid	-10%	6.480000	11732.11	-1403.57	60.35%
n_paid	+10%	7.920000	14539.25	1403.57	61.19%
n_paid	+30%	9.360000	17346.38	4210.70	61.77%

龙卷风（按贡献利润变化振幅降序）：
  price: 最小变化 -¥4,210.70, 最大变化 ¥4,210.70, 振幅 ¥4,210.70
  n_paid: 最小变化 -¥4,210.70, 最大变化 ¥4,210.70, 振幅 ¥4,210.70
  delivery_cost_ratio: 最小变化 -¥1,539.00, 最大变化 ¥1,539.00, 振幅 ¥1,539.00
  fee_rate: 最小变化 -¥406.30, 最大变化 ¥406.30, 振幅 ¥406.30
  traffic_cost: 最小变化 -¥270.00, 最大变化 ¥270.00, 振幅 ¥270.00
  refund_rate: 最小变化 -¥221.62, 最大变化 ¥221.62, 振幅 ¥221.62
说明：本表把各因子当作其余冻结的自变量。现实中成交单数与流量成本往往联动，振幅排序只用于找出最危险的假设，不是因果证明。
```

验证：退出码为 0；每个因子 4 个扰动行；给出振幅降序；说明其余冻结口径不是因果证明。
本步验证：通过

## 步骤 4 · 盈亏平衡：最大 CAC 与最小成交率
目的：计算使贡献利润为零的最大流量成本/CAC，以及使贡献利润非负的最小成交率；课程轨道单独计算。融资不进入平衡式。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 unit_econ.py breakeven
```

真实结果：退出码 0，输出 279 字符。

```text
【教学保守 / 独自交付】
  使贡献利润=0 的最大流量成本: ¥14,035.68
  对应最大 CAC: ¥1,949.40
  当前流量成本: ¥900.00，当前 CAC: ¥125.00
  使贡献利润>=0 的最小成交率: 0.9618%
  当前教学成交率: 15.0000%

【课程轨道】标价来自自述 2980，成本和转化仍是教学假设
  最大流量成本: ¥4,563.18
  最大 CAC: ¥2,376.65
  最小成交率: 0.7889%
融资额、办公面积和「一条视频值几十万」不进入盈亏平衡，因为它们不是单笔经营的单位经济。
```

验证：退出码为 0；同时给出当前值与临界值；文中写明融资额和办公面积不进入盈亏平衡。
本步验证：通过

## 步骤 5 · 自述情景对照（全部未核实）
目的：把作者自述的 GMV、订单下沿、粗除客单价、课程收入下沿和融资金额单独列出；现场复核 500000/100；演示若把自述客单价代入教学漏斗会发生什么，并写明不能据此证实 50 万 GMV。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 unit_econ.py narrative
```

真实结果：退出码 0，输出 1402 字符。

```text
【自述情景对照】以下全部标记为未核实，不是本批实测。
  2025 GMV: ¥500,000.00  [author_claim] 原文：「GMV大概50万」
  订单数下沿: 100  [author_claim_derived] 原文：「25年一整年做了上百单」
  粗除客单价: ¥5,000.00  [author_claim_derived]  由自述「上百单、GMV大概50万」按订单数=100 粗除得到；「上百」不是精确计数。
  现场复核 500000/100 = ¥5,000.00 （与 JSON 中 custom_aov_from_claim 一致: True）
  课程标价: ¥2,980.00  [author_claim]
  单条视频课程收入下沿: ¥100,000.00  [author_claim_derived] 原文：「直接给我带来了十几万的课程收入」  「十几万」取下沿 10 万做演示，仍是自述。
  若把「10万课程收入」按 2980 反推销量 ≈ 33.56 份（ demonstrative only）
  融资: ¥10,000,000.00  [author_claim] 原文：「拿到了千万投资」  未给出轮次、估值、到账与稀释，不能纳入经营单位经济。

## 把自述粗除客单价代入教学漏斗——仍然不是对 50 万 GMV 的证实
输入标签：
  - impressions: teaching_assumption
  - ctr: teaching_assumption
  - inquiry_rate: teaching_assumption
  - close_rate_custom: teaching_assumption
  - cpc: teaching_assumption
  - custom_aov_teaching: teaching_assumption
  - refund_rate_custom: teaching_assumption
  - fees: teaching_assumption+teaching_assumption
  - delivery_cost_ratio_solo: teaching_assumption
  - price: author_claim_derived（仅替换客单价，成本和转化仍是教学假设）
  成交单数: 7.2000
  客单价: ¥5,000.00
  收入: ¥36,000.00
  退款: ¥1,800.00
  净收入: ¥34,200.00
  平台/支付手续费: ¥2,257.20
  交付成本: ¥8,550.00
  履约成本: ¥0.00
  流量成本: ¥900.00
  贡献利润: ¥22,492.80
  CAC（流量成本/成交单数）: ¥125.00
  单笔贡献利润: ¥3,124.00
  贡献利润率: 62.48%

为什么不能把 50 万 GMV 写成「已验证收入」：
  1. 没有订单流水、平台账单或税务记录；
  2. GMV 不是贡献利润，未扣退款、投流、交付分成和自己的时间；
  3. 「上百单」不是精确计数，客单价只是下沿粗除；
  4. 融资是资本项，不能加进贡献利润，更不能用来证明获客效率。
```

验证：退出码为 0；500000/100 与 JSON 中 custom_aov_from_claim 一致为 True；融资被明确排除在单位经济之外。
本步验证：通过

## 步骤 6 · 故障注入：交付成本与退款率恶化
目的：在教学基准上把交付占比和退款率推到恶化甚至成本超过净收入，观察贡献利润何时变负，说明未测成本前不能按自述 GMV 扩张。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 unit_econ.py stress
```

真实结果：退出码 0，输出 355 字符。

```text
基准（教学保守 / 独自交付）贡献利润: ¥13,135.68
fault	delivery_ratio	refund_rate	contribution	margin	status
交付占比升到 0.80	0.80	0.05	1849.68	8.56%	仍为正（仅在本假设下）
退款率升到 0.30	0.25	0.30	9442.08	43.71%	仍为正（仅在本假设下）
交付 0.80 且退款 0.30	0.80	0.30	1126.08	5.21%	仍为正（仅在本假设下）
交付占比 1.10（成本超过净收入）	1.10	0.05	-4306.32	-19.94%	亏损

故障注入结果：1/4 组贡献利润为负。
这证明单位经济对交付成本和退款率敏感；不能在未测成本前按自述 GMV 扩张外包或投放。
```

验证：退出码为 0；至少有一组贡献利润为负；交付占比 1.10 的一组必须亏损。
本步验证：通过

## 步骤 7 · 公式与标签纪律单元测试
目的：用固定合成输入核对漏斗乘法、贡献利润手算、流量成本线性、盈亏平衡、负值拒绝、假设标签、自述客单价除法和融资参数隔离。

```bash
cd /workspace/reminder-batch-2026-11-11/item-7-qige-unit-econ/exercise
python3 -m unittest test_unit_econ.py -v
```

真实结果：退出码 0，输出 1272 字符。

```text
test_assumptions_all_tagged (test_unit_econ.TestFormulas.test_assumptions_all_tagged) ... ok
test_break_even_close_rate_non_negative (test_unit_econ.TestFormulas.test_break_even_close_rate_non_negative) ... ok
test_break_even_traffic_equals_zero_traffic_contribution (test_unit_econ.TestFormulas.test_break_even_traffic_equals_zero_traffic_contribution) ... ok
test_claimed_aov_matches_division (test_unit_econ.TestFormulas.test_claimed_aov_matches_division) ... ok
test_contribution_linear_in_traffic (test_unit_econ.TestFormulas.test_contribution_linear_in_traffic) ... ok
test_funnel_counts (test_unit_econ.TestFormulas.test_funnel_counts) ... ok
test_impossible_close_rate_is_inf (test_unit_econ.TestFormulas.test_impossible_close_rate_is_inf) ... ok
test_investment_not_in_unit_econ_signature (test_unit_econ.TestFormulas.test_investment_not_in_unit_econ_signature) ... ok
test_rejects_negative (test_unit_econ.TestFormulas.test_rejects_negative) ... ok
test_sensitivity_identity_at_zero_delta (test_unit_econ.TestFormulas.test_sensitivity_identity_at_zero_delta) ... ok
test_unit_economics_hand_calc (test_unit_econ.TestFormulas.test_unit_economics_hand_calc) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.001s

OK
```

验证：退出码为 0；全部测试 OK。
本步验证：通过

## 未验证边界

- 原帖与引用长文中的 GMV、投流效果、课程收入、爆款、融资、办公面积、FDE 人数和「发一条爆一条」全部是作者自述，本实验未核实。
- 教学假设中的点击率、成交率、CPC、扣点、交付成本和退款率不是市场调查，也不是作者披露。
- 没有访问闲鱼店铺、视频号、广告后台或工商/融资文件。
- 引用帖所附 3 张图片未做视觉鉴定，不把图片内容当作已核实事实。
- 本日志由同一批次实验脚本写入，不是第三方独立审核。

汇总：全部 7 步退出码为 0 且附加校验通过。
各步：[{'i': 1, 'returncode': 0, 'ok': True, 'chars': 1681}, {'i': 2, 'returncode': 0, 'ok': True, 'chars': 2117}, {'i': 3, 'returncode': 0, 'ok': True, 'chars': 1698}, {'i': 4, 'returncode': 0, 'ok': True, 'chars': 279}, {'i': 5, 'returncode': 0, 'ok': True, 'chars': 1402}, {'i': 6, 'returncode': 0, 'ok': True, 'chars': 355}, {'i': 7, 'returncode': 0, 'ok': True, 'chars': 1272}]
