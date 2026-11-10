# 真实离线实验日志

执行日期 2026-11-11 01:20:21 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. baseline
```bash
cd /workspace/chen-jiao-batch2-20261111/item08
python3 exercise/lab.py baseline
```
退出码 0
```text
synthetic baseline surplus= 3000 CNY/month; NOT user financial data

```
## 2. runway
```bash
cd /workspace/chen-jiao-batch2-20261111/item08
python3 exercise/lab.py runway
```
退出码 0
```text
zero income, essentials only: runway= 5.0 months; expenses +20% -> 4.167 months; simplified

```
## 3. cost
```bash
cd /workspace/chen-jiao-batch2-20261111/item08
python3 exercise/lab.py cost
```
退出码 0
```text
hypothetical tools 300/month -> surplus= 2700 annual tool cost= 3600 ; no subscriptions purchased

```
## 4. priority
```bash
cd /workspace/chen-jiao-batch2-20261111/item08
python3 exercise/lab.py priority
```
退出码 0
```text
reversible zero-purchase learning actions= ['整理现有笔记', '用现有电脑做CSV工具'] ; arbitrary ranking is not earnings forecast

```

## 逐步目的和验证
- 步骤1 假设现金流基线：目的 先列数字来源，禁止代入真实用户。；验证 虚构结余3000元/月。
- 步骤2 收入中断敏感性：目的 用必要支出测试跑道脆弱性。；验证 5个月，支出+20%后4.167个月。
- 步骤3 工具费用侵蚀：目的 把消费成本从收入故事中分离。；验证 月结余降为2700，年成本3600元。
- 步骤4 零购买行动门：目的 优先可逆且有产物的学习动作。；验证 筛出2个零购买动作，非收益预测。

## 未验证边界
所有收入、支出和储蓄是假设，不是用户财务资料；没有验证任何收益、投资回报或生产率提升。无投资开户、金融交易、订阅购买或个人理财判断。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读4579字符、替换字符0。为本人自查，非独立审核。
