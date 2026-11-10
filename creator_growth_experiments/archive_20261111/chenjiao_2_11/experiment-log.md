# 涨粉复盘：把成功故事改写成可检验假设 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：创建合成人群数据
目的：创建合成人群数据

```bash
cd /workspace/chen-jiao-batch2-20261111/item11
python3 exercise/lab.py prepare
```
真实结果 exit=0：
```text
synthetic cohorts= [['A', 'warm', 80, 100], ['A', 'cold', 10, 100], ['B', 'warm', 9, 10], ['B', 'cold', 120, 1000]] NOT author analytics

```
验证：文件明示 synthetic，不能误标作者后台

## 步骤 2：计算两组 Wilson 区间
目的：计算两组 Wilson 区间

```bash
cd /workspace/chen-jiao-batch2-20261111/item11
python3 exercise/lab.py interval
```
真实结果 exit=0：
```text
8/100 CI95= (0.04109296948581091, 0.14998266879403072) 12/100 CI95= (0.06999337365267776, 0.19812268002908368)

```
验证：验证区间重叠且上下界合法

## 步骤 3：复现分层与聚合方向反转
目的：复现分层与聚合方向反转

```bash
cd /workspace/chen-jiao-batch2-20261111/item11
python3 exercise/lab.py confounding
```
真实结果 exit=0：
```text
aggregate A= 0.45 B= 0.12772277227722773 within warm B .90 > A .80; cold B .12 > A .10

```
验证：B 分层优于 A，但总量比例较低

## 步骤 4：计算每关注人工成本
目的：计算每关注人工成本

```bash
cd /workspace/chen-jiao-batch2-20261111/item11
python3 exercise/lab.py cost
```
真实结果 exit=0：
```text
hours= 2 follows= 8 labor_cost_per_follow= 12.5
hours= 4 follows= 12 labor_cost_per_follow= 16.666666666666668
pre-register: same audience, fixed 14 posts, no optional stopping, no automatic publishing

```
验证：以假设时薪计算，不推导收益

## 未验证边界
待验证：作者历史链接中的原始后台、增长/收入、因果归因和真实内容实验。没有发帖、联系博主或采集私密数据。
