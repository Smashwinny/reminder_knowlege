# 真实实验日志

2026-11-11 Asia/Shanghai；Python3.13，标准库；全部自写教学程序、合成输入，无交易。

## 冻结输入
目的：固定seed=20261111生成1200根OHLCV。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/02-technical-analysis
python3 exercise/lab.py generate
```
实际exit=0，stdout原文：
```text
seed=20261111; rows=1200; synthetic=true; regime boundaries=400,800 (教学生成器信息，非策略输入)
```
验证：out/ohlcv.csv共有1200行数据；合成制度三段只供造数，策略不读制度标签。

## 核验数据和因果性
目的：检查OHLC、暖机、未来扰动不影响此前信号和费用单调性。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/02-technical-analysis
python3 exercise/lab.py validate
```
实际exit=0，stdout原文：
```text
PASS 5 checks: OHLC invariant, warmup, future mutation prefix, fee monotonic, lag contract
```
验证：validation.json标记5项自编检查PASS；不是独立审核，也不是所有交易边界覆盖。

## 成本敏感性
目的：同一10/30规则分别以0、5、20基点单边成本回测。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/02-technical-analysis
python3 exercise/lab.py backtest
```
实际exit=0，stdout原文：
```text
{"0": {"return_pct": 1.1254, "max_drawdown_pct": -48.5424, "one_way_turnover": 48, "fee_bps": 0}, "0.0005": {"return_pct": -1.2734, "max_drawdown_pct": -49.4858, "one_way_turnover": 48, "fee_bps": 5.0}, "0.002": {"return_pct": -8.1401, "max_drawdown_pct": -52.2163, "one_way_turnover": 48, "fee_bps": 20.0}}
```
验证：costs.json保留收益、最大回撤、单边换仓；高费率不得优于低费率。

## 冻结参数与反例
目的：只用前800根选参数；后400根验证，并与买入持有和错误未来函数对照。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/02-technical-analysis
python3 exercise/lab.py holdout
```
实际exit=0，stdout原文：
```text
{"training_first_800": {"5/20": 23.2253, "10/30": 23.6727, "20/60": -4.3396}, "frozen_choice": [10, 30], "holdout_400": {"return_pct": -20.171, "max_drawdown_pct": -21.7416, "one_way_turnover": 16, "fee_bps": 5.0}, "invalid_lookahead_example": {"return_pct": -16.3602, "max_drawdown_pct": -19.2239, "one_way_turnover": 16, "fee_bps": 5.0}, "holdout_buy_and_hold_pct": -17.2986, "warning": "合成数据不说明市场预测能力；反例故意读取未来，不可用于策略评价"}
```
验证：holdout.json中frozen_choice=[10,30]；样本外−20.171%，错误反例−16.3602%不得引用为可交易。

## 校验文件与边界
目的：对CSV和JSON写SHA256，声明不接账户、不下单。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/02-technical-analysis
python3 exercise/lab.py audit
```
实际exit=0，stdout原文：
```text
SHA256 {"costs.json": "9edf4f43e6edb989860c6b79106db1cb48529b9a746c2a79db103c9f7c6c9d61", "validation.json": "7084e9b744ce6ef85b713c82304c721cf279ed7bf8a288f1cf007926a6747b44", "holdout.json": "fb94e122dbf573fd95765474fe60e8e826ccd5276aae6d45e7bf3bafc77c3241", "ohlcv.csv": "8129748c79292ef18e71096af0e3995f3ec6f662278d81e5f55a34a6d5b19b47"}
无账户、无下单、无外部API；不是投资建议
```
验证：manifest.json可重新计算；没有交易、账户、付费API或个人私密数据。

补强执行滞后检查：用29根100再6根200的手工序列，断言第29根信号=1但仓位=0、第30根仓位=1；重新执行validate及audit均exit0。原5项计数不增加，替换原重复表达式检查。
