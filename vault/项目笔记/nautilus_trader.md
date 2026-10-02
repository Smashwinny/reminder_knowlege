---
tags: [项目]
类别: 开源项目类
上游仓库: github.com/nautechsystems/nautilus_trader（~28.6K stars，LGPL-3.0）
完成日期: 2026-10-02
---

# nautilus_trader

**这是什么**：开源机构级量化交易平台——Rust 核心（纳秒时间戳、事件总线、Rusty 撮合）+ Python 策略层，回测与实盘共用同一套策略代码；自带数百种金融工具适配器（Interactive Brokers、dYdX、币安等）。热点来源：X 推荐帖（[推文](https://x.com/huoshan007/status/2091709343007977618)）。

**它给我什么能力**：事件驱动回测（tick 级精度）/ 同一策略回测→模拟盘→实盘无缝迁移 / 真实撮合模拟（maker/taker 手续费、保证金、净额结算）/ 多资产多 venue / 策略报表（订单、成交、持仓）。

**引入的概念**：
- [[事件驱动回测]] — tick 级事件循环重放历史，杜绝未来函数；`add_venue/add_data/add_strategy/run` 四步
- [[交易成本与鞭打效应]] — 信号频率 vs 手续费/滑点侵蚀；实测均线越快亏损越大

**实验记录**（F:\reminder\nautilus-trader\exercise\，全部真实运行）：
1. `ema_cross_backtest.py` — **主实验**：仓库自带 truefx AUD/USD 9.98 万条 tick → QuoteTickDataWrangler → 1分钟K线，EMA 交叉策略三参数对比（pip 版 1.231.0）✅ 真实输出：
   - 5/10 → 145 信号 / 290 成交 / 亏 883.62 USD / 手续费 388.62
   - 10/20 → 85 / 170 / -526.82 / 227.82
   - 20/60 → 32 / 64 / -326.76 / 85.76
   - 结论：均线越快，鞭打越狠，成本越高（[[交易成本与鞭打效应]]）

**坑与结论**：
- pip 稳定版 1.231.0 与 repo develop 分支 API 不同：`BacktestEngine` 在 `backtest.engine` 而非 `backtest`；testkit 是 `test_kit.providers`；策略无 `buy()/sell()`，要 `order_factory.market()` + `submit_order()`；报表在 `engine.trader.generate_*_report()` 而非引擎属性
- 报表 Money 列是 `"123.45 USD"` 字符串，需正则提取再求和
- truefx CSV 有重复时间戳，需 `duplicated(keep="first")` 去重；pandas 3.0 解析混合时间格式要 `format="mixed", utc=True`

**后续可深入的方向**：接 IBKR paper trading 实盘；多策略 Portfolio；Rust 核心源码（事件总线/撮合）；Parquet Catalog 数据湖；用真实点差/滑点模型替代固定费率。
