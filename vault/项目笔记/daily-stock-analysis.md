---
tags: [项目]
类别: 开源项目类（LLM 金融数据聚合分析）
上游仓库: https://github.com/ZhuLinsen/daily_stock_analysis
完成日期: 2026-10-02
---

# daily-stock-analysis（DSA 股票智能分析系统）

**这是什么**（一句话）：LLM 驱动的多市场（A股/港股/美股/日/韩/台）自选股每日自动分析系统——聚合行情/新闻/基本面 → 规则指标打分 → LLM 综合研判出"决策仪表盘"（评分/买卖点/风险/催化）→ 推送到企微/飞书/TG/Discord/Slack/邮箱，另有 Web 工作台与 15 种策略问股。MIT，Python 3.10+，实测版本 be148f3。

**它给我什么能力**：
- 多源不稳定 API 聚合的完整工程模板（19 fetcher 降级链 + 限速 + 子进程超时隔离 + 列名归一化）
- pandas 技术指标参考实现（MA/MACD/RSI，口径有 1e-10 级测试锁定）
- "确定性代码打底 + LLM 提炼"的报告流水线范式 + 评分契约/护栏/可后验资产三件套
- 策略即 YAML（提示词说明书 + 工具清单 + 别名路由）的可扩展专家人格包
- GitHub Actions 零成本定时跑批 + 多渠道推送的部署范式

**引入的概念**：
- [[数据源降级链]]
- [[事实与判断分离]]
- [[评分契约与护栏]]
- [[技术指标MA与MACD与RSI]]

**实验记录**（做了什么、结果、坑）：
- 环境：exercise\venv（Python 3.14.7，pandas 3.0.6/numpy 2.5.3/pydantic/pytest 等，按 import 报错迭代补装最小集；完整 requirements 的 akshare/mini-racer 等未装）
- 实验1：仓库自带 test_stock_analyzer_rsi.py + test_stock_analyzer_bias.py → 12 passed + 11 subtests（0.61s），RSI_6 期望值精确到 69.01902761094098
- 实验2（exercise/exp1_indicators.py，全部真实运行）：A 三段合成K线形态区分 PASS（bull→强势多头/78分/买入；bear→空头排列；top→强烈卖出/38分）；B 独立参考实现 vs repo MA5/DIF/DEA/BAR/RSI12 |差|=0.00e+00 全 PASS；C decision-scale-v1 五档映射逐档验证一致；D ma_golden_cross.yaml 契约解析成功，strategies 共 15 个 YAML
- 坑：① import src.stock_analyzer 会级联拉起 src.config→data_provider→efinance_fetcher 等一长串依赖（requests/tenacity/fake_useragent 逐个补）；② Python 3.14 下 pandas 3.0.6 兼容良好；③ 中文 Windows 跑 Python 前 PYTHONUTF8=1

**后续可深入的方向**：
- src/agent/ 的多轮策略问股 Agent 循环与 litellm 路由细节
- Fork + GitHub Actions Secrets 完整部署一次，体验零成本定时推送
- DecisionSignal 资产库与 evals/ 的 Agent 轨迹评估
- 与 nautilus-trader（回测/实盘框架）的衔接：DSA 出结构化信号 → 回测框架验证
- ⚠️ 该工具仅供学习研究程序技术，AI 输出不构成投资建议
