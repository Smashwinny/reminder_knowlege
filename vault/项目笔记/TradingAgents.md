---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/TauricResearch/TradingAgents
完成日期: 2026-10-03
---

# TradingAgents

**这是什么**（一句话）：把一次股票交易决策拆成一家"虚拟交易公司"里 12 个 LLM 角色的流水线协作——4 分析师并行调研 → 多空研究员辩论 → 交易员提案 → 三方风险辩论 → 组合经理拍板（arXiv 2412.20138，109,521★，v0.5.2）。

## 带来的新概念
- [[私有子图输出隔离]] — 并行分析师各跑私有子图，只回传报告键，wrap_up 兜底防工具死循环
- [[对抗辩论式决策架构]] — 条件边路由器 + 计数器实现多空/风险两段辩论环
- [[决策记忆结算反思闭环]] — append-only markdown 日志：决策→结算(alpha)→反思教训回注，幂等+原子写+point-in-time

## 实验做了什么（全部离线零 API key）
- **E1** 官方端到端测试 11/11 过（ScriptedModel 假 LLM + 假数据供应商全离线）；坑：pytest 需 `--basetemp` 本地目录
- **E2** 导出图拓扑：16 节点 / 29 边，mermaid 存 `exercise/graph_topology.mmd`
- **E3** 主实验：`propagate("NVDA")` 全管线跑通，signal=Overweight，15 次 LLM 调用，3 线程并行分析师，12 个数据路由方法全命中
- **E4** 辩论路由实测：多空 Bull→Bear→Bull→RM；风险 Conservative→Neutral→PM（计数起点从 1 起算的坑）
- **E5** 记忆日志：写 2 次幂等成 1 条；结算后 `[+3.1% | +1.2% | 5d]` + REFLECTION 原子写入；API 是 `update_with_outcome` 非 settle_decision

## 坑与结论
- LLM 决策解析走 Pydantic 结构化输出 + 五档 Rating 硬解析双保险，signal/final_rating/日志三处一致性有断言
- backtest.py 明确 scope=决策质量评估，无仓位/现金账本，**不是组合模拟器**——严肃回测要接 [[事件驱动回测]]（NautilusTrader）做执行层
- 数据 7 家全免费（yfinance/SEC EDGAR/FRED/StockTwits/Reddit/Polymarket/AlphaVantage），跑通只需一个 LLM key
- ⚠️ 研究框架，不构成投资建议，不能直接实盘

## 产出
- PDF：`F:\reminder\tradingagents\TradingAgents-小白指南.pdf`（14 问 + 5 实验）
- 实验：`F:\reminder\tradingagents\exercise\`（e2_graph_topology.py / e3_run_offline.py / e4_e5_router_memory.py）
