# 知识入库提案 · kronos_kline_model

- 任务：c5310fbd-13d8-4972-8870-41104ab1e877
- worker：kimi-pool-20261007-w1（2026-10-07）
- 查重范围：`vault/概念/`、`vault/项目笔记/`（Kronos/K线/金融大模型 grep 仅命中 daily-stock-analysis、nautilus_trader、事件驱动回测，无重复）

## 提案 1：新建项目笔记（worker 已按裁定直接新建）

`vault/项目笔记/kronos_kline_model.md` —— 已写入：两阶段框架、模型家族表（mini/small/base 开源 large 未放出）、本机回归测试 4/4 实证、宣称逐项核实表、与量化工具链的互补关系、祛魅边界。

## 提案 2：新建概念（请协调者终审合并）

**文件名**：`vault/概念/时序分词与行情基础模型.md`

**一句话**：把连续 OHLCV 行情经专用 tokenizer 量化成分层离散 token，就能用"词表+自回归 Transformer"的 NLP 范式做金融时序基础模型——Kronos 是该路线的首个开源实现（AAAI 2026）。

**正文要点**：
- 两阶段：专用 tokenizer（连续多维→分层离散 token）→ decoder-only 自回归预训练；分层捕捉多尺度行情结构。
- 可信边界：回归测试可证"行为可复现"，论文指标 ≠ 交易 edge；"最佳数字在未开源的 large 上"是读论文的必备警惕。
- 反模式：把预测曲线当策略直接下单；忽略 512 上下文截断；假设训练数据可独立复核（未发布）。
- 链接：`[[项目笔记/kronos_kline_model]]`、`[[交易成本与鞭打效应]]`、`[[事件驱动回测]]`、`[[证据优先质检ProofOverClaims]]`、`[[技术指标MA与MACD与RSI]]`

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 kronos_kline_model（worker 不动总览）。
