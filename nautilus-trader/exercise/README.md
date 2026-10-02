# NautilusTrader 动手实验：AUD/USD EMA 双均线交叉回测

本实验用 NautilusTrader 1.231.0（pip 稳定版）+ 仓库自带的真实 tick 数据
（`repo/test_data/truefx/audusd-ticks.csv`，约 10 万条 AUD/USD 报价），
从零写一个 EMA 交叉策略并跑回测，再改参数看结果变化。

## 环境

- Python 3.12–3.14（本机 3.14.7，UTF-8 模式已开）
- `pip install -U nautilus-trader pandas`
- 数据文件来自克隆的上游仓库 `repo/test_data/`，无需联网下载

## 步骤

### 第 1 步：跑默认参数（快 EMA=10，慢 EMA=20）

```bash
cd F:\reminder\nautilus-trader\exercise
python ema_cross_backtest.py
```

- 目的：验证环境 + 理解"数据 → 引擎 → 策略 → 报表"全链路。
- 预期输出（2026-10-02 实测）：

```
            fast: 10
            slow: 20
           ticks: 99821
     first_ts_ns: 1580398089820000000
         signals: 85
           fills: 170
closed_positions: 85
    realized_pnl: -526.82
     commissions: 227.82
   final_balance: 999473.18
```

✅ 检测标准：`final_balance` 接近 100 万 USD，`signals`/`fills` 是正整数。

### 第 2 步：改参数，看"策略频率"的影响

```bash
python ema_cross_backtest.py 5 10    # 更快：5/10
python ema_cross_backtest.py 20 60   # 更慢：20/60
```

实测对比（同一天数据）：

| 参数 | 信号数 | 成交笔数 | 已实现盈亏(USD) | 手续费(USD) | 期末余额(USD) |
|---|---|---|---|---|---|
| 5/10 | 145 | 290 | -883.62 | 388.62 | 999,116.38 |
| 10/20 | 85 | 170 | -526.82 | 227.82 | 999,473.18 |
| 20/60 | 32 | 64 | -326.76 | 85.76 | 999,673.24 |

- 规律：**均线周期越短，信号越频繁，手续费越高，亏损越大**——典型的"鞭打（whipsaw）"现象。
- 这个教学策略本身没有赚钱优势（`EMACross` 官方也明说 "has no edge"），
  它的价值是让你看清成本结构。

### 第 3 步（可选）：读代码理解全链路

- `load_ticks()`：CSV → pandas → `QuoteTickDataWrangler` → `list[QuoteTick]`（纳秒时间戳）
- `run()`：建引擎 → 加模拟交易所（SIM，净额结算、保证金账户、maker/taker 手续费 0.00002）→ 加数据 → 加策略 → `engine.run()`
- `EMACross.on_bar()`：K线收盘后比较快/慢 EMA，金叉买、死叉卖，信号来先平仓

## 踩坑记录（1.231.0 稳定版 vs 仓库 develop 分支）

| 坑 | 解决 |
|---|---|
| 仓库示例 `from nautilus_trader.backtest import BacktestEngine` 在 pip 版不存在 | 用 `from nautilus_trader.backtest.engine import BacktestEngine` |
| `from nautilus_trader.testkit...` 不存在 | pip 版是 `nautilus_trader.test_kit.providers` |
| 策略没有 `buy()/sell()` 便捷方法 | 用 `self.order_factory.market(...)` + `self.submit_order(...)` |
| 报表不在引擎上 | 在 `engine.trader.generate_*_report()` |
| 报表 Money 列是 `"123.45 USD"` 字符串 | 正则提取数字再求和 |
| truefx CSV 有重复时间戳 | `df[~df["timestamp"].duplicated(keep="first")]` |
| pandas 3.0 解析混合时间格式 | `pd.to_datetime(..., format="mixed", utc=True)` |
