# 9.9 到 29.9 的价差：先算亏损，再谈复制 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：冻结教学成本假设
目的：冻结教学成本假设

```bash
cd /workspace/chen-jiao-batch2-20261111/item10
python3 exercise/lab.py prepare
```
真实结果 exit=0：
```text
{'price': '29.9', 'purchase': '9.9', 'shipping': '4', 'packaging': '1', 'fee_rate': '.05', 'return_cost': '5', 'fixed': '900', 'note': 'hypothetical; not a real merchant ledger'}

```
验证：assumptions.json 中每项假设可复核

## 步骤 2：运行基线盈亏平衡
目的：运行基线盈亏平衡

```bash
cd /workspace/chen-jiao-batch2-20261111/item10
python3 exercise/lab.py base
```
真实结果 exit=0：
```text
unit_contribution= 5.1645 break_even_orders= 175 100_orders_net= -383.5500

```
验证：贡献为正才计算订单数，固定成本另扣

## 步骤 3：枚举 16 种成本情景
目的：枚举 16 种成本情景

```bash
cd /workspace/chen-jiao-batch2-20261111/item10
python3 exercise/lab.py sensitivity
```
真实结果 exit=0：
```text
scenarios= 16 negative= 7 worst= -11.5165

```
验证：写出 CSV，数负贡献情景

## 步骤 4：区分百万 GMV 与贡献目标
目的：区分百万 GMV 与贡献目标

```bash
cd /workspace/chen-jiao-batch2-20261111/item10
python3 exercise/lab.py million
```
真实结果 exit=0：
```text
1M gross revenue needs orders= 33445 1M hypothetical contribution-minus-fixed needs= 193804

```
验证：贡献目标订单量必须大于销售额目标

## 未验证边界
待验证：原帖收益、真实订单、平台费率、税费、库存回收、人工成本、需求与合规。未采购、未发布、未创建账号。
