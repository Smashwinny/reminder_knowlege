---
tags: [项目]
类别: 开源项目类（AI 交易终端，纯技术研究，零真实交易）
上游仓库: https://github.com/alsk1992/CloddsBot
完成日期: 2026-10-03
---

# cloddsbot（alsk1992/CloddsBot）

**这是什么**：Claude 驱动的本地 AI 交易终端（"Claude+Odds"），TypeScript/MIT/v1.9.1，2888 星（2026-10-03 查证，推文时 899）。聊天对话驱动，接 10 个预测市场 + 7 个永续交易所 + 21 个消息平台，121 个 SKILL.md 技能包。拾遗推文"23 岁小伙睡一觉赚 280 美元"的主角仓库——**故事不可核实且带返佣推广，但仓库本身真实、代码中上质量，当"AI+交易"工程蓝图学**。

**它给我什么能力**：
1. AI 交易终端六层参考架构（网关/渠道适配/Agent/工具/风控/执行），可搬到任何"AI+危险操作"系统
2. 负风险套利检测器完整思路（Jaccard 配对 + 比价 + 打分 + 过滤），300 行 Python 可复刻
3. 净边际过滤公式 + 多跳负环检测（−log 边权 + Bellman-Ford）
4. 10 道盘前风控清单 + 动态 Kelly（风控测试黄金模板，tests/trading 可直接读）
5. "开源+币+返佣"鉴伪流程（fxtwitter 取证 → GitHub API 验仓 → 跑测试验代码）

**引入的概念**：
- [[预测市场与二元合约]]
- [[负风险套利]]
- [[净边际与多跳套利环]]
- [[风控链与Kelly仓位]]
- [[AI交易终端]]

**实验记录**（exercise\，全部真实运行，Python 3.14.7 纯标准库 + Node v24.21.0，全程零真实交易零 API 费，含投资免责声明）：
- **ex1 负风险套利扫描**（主实验）：Polymarket gamma-api + CLOB 公开订单簿（免钥只读），40 热门市场全二元，12 个取到双边最优卖价，合计成本全部 1.001~1.010，0 个套利机会——市场有效，1.001 地板 = tick size。坑：gamma 的 clobTokenIds 是 JSON 字符串须二次 parse，否则 40 个市场全被滤成 0。
- **ex2 跨所净边际**：OKX vs Kraken 真实行情，毛价差 0.0007%~0.011% vs 双 taker 费 0.36%，净边际 −0.36% 两方向全拒。坑：Binance 公共 API 地域限制（restricted location）。
- **ex3 多跳负环检测**：OKX 三元组真实中间价，−log(rate×(1−fee)) 边权，两方向环边权和 +0.0030/+0.0030 无套利（乘数 0.997）。大坑：环方向汇率语义写反会"负环满地"报 71 亿倍乘数——套利检测器最危险 bug 是把必亏报成暴富。
- **ex4 跑通上游**：npm install 834 包（坑：helius-laserstream@0.1.8 仅 darwin/linux，Windows 需 --force 绕平台检查）；typecheck 0 错误；tests/trading 11/11 全绿，含"风控减仓可超上限但 kill switch 拦得住"的活标本测试。

**坑与结论**：Binance 地域限制 / clobTokenIds 字符串 / helius-laserstream 不支持 win32 / 环方向汇率反=假暴富，四坑全实测。结论：仓库当蓝图学（风控分层+技能包生态+检测算法），盈利叙事当营销听（tick 地板+手续费两连实测证明热门市场无缝隙）。

**后续可深入的方向**：把 ex1 扫描器加 WebSocket 实时化、扩 Kalshi 做真跨平台配对；读 repo 的 `src/feeds/` 学 10 个市场适配器如何统一 schema（对照 [[双数据源适配器隔离]]）。

**产出**：`cloddsbot\CloddsBot-小白指南-AI交易机器人拆解.pdf`（14 问，含投资免责声明）
