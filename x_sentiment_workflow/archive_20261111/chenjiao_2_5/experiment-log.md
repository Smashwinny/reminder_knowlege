# 真实离线实验日志

执行日期 2026-11-11 01:20:20 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. fixture
```bash
cd /workspace/chen-jiao-batch2-20261111/item05
python3 exercise/lab.py fixture
```
退出码 0
```text
synthetic fixture rows= 4 (not real engagement)

```
## 2. filter
```bash
cd /workspace/chen-jiao-batch2-20261111/item05
python3 exercise/lab.py filter
```
退出码 0
```text
selected= [{'id': 'a', 'ratio': 12.0}] ; missing metrics remain unknown; duplicate/private excluded

```
## 3. injection
```bash
cd /workspace/chen-jiao-batch2-20261111/item05
python3 exercise/lab.py injection
```
退出码 0
```text
untrusted string retained as data; actions=0; structural fixture, not LLM robustness benchmark

```
## 4. dedupe
```bash
cd /workspace/chen-jiao-batch2-20261111/item05
python3 exercise/lab.py dedupe
```
退出码 0
```text
persistent unique IDs= 1 for 2 inputs; no routine created

```

## 逐步目的和验证
- 步骤1 创建合成指标样本：目的 安排重复、空值、注入、隐私用例。；验证 4行，所有互动数字为虚构。
- 步骤2 确定性筛选：目的 只按明确指标计算异常倍数。；验证 a=12倍且只选一条；缺失保持未知。
- 步骤3 外部文本不执行：目的 从结构上不把帖子送给动作分派。；验证 actions=0；不是LLM对抗评估。
- 步骤4 SQLite持久ID去重：目的 证明跨导入可保留唯一ID。；验证 两次输入只保留一行，没有定时任务。

## 未验证边界
没有连续监控、检索历史基线、私信、对外上报或定时任务。注入测试是结构性规则夹具，不是大模型抗注入基准；所有互动数为显式合成。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读4530字符、替换字符0。为本人自查，非独立审核。
