---
tags: [项目笔记, 开源项目, 量化, 金融AI, 时序模型]
created: 2026-10-07
---

# Kronos：K 线基础模型

- 仓库：https://github.com/shiyu-coder/Kronos（MIT，快照 67b630e，2026-10-07 克隆实测 40102 stars；HF 权重 NeoQuasar/*）
- 来源：@Gk 推文 https://x.com/0xGky/status/2106826437453861101；论文 arXiv 2508.02739，AAAI 2026 接收（2025-11-10 官宣）

## 是什么

首个开源的 K 线专用基础模型：两阶段框架——①专用 tokenizer 把连续 OHLCV 量化成**分层离散 token**（2k 词表）；②decoder-only 自回归 Transformer 在 45+ 全球交易所数据上预训练。一个模型服务预测/补全/生成等量化任务。用法：KronosTokenizer + Kronos.from_pretrained + KronosPredictor.predict(df, x_ts, y_ts) 三步。

## 模型家族（核实自 README Model Zoo）

| 模型 | 上下文 | 参数 | 开源 |
|---|---|---|---|
| mini | 2048 | 4.1M | ✅ |
| small | 512 | 24.7M | ✅（本机实测） |
| base | 512 | 102.3M | ✅ |
| large | 512 | 499.2M | ❌（论文最优成绩尺寸） |

## 本机实证

官方回归测试 4/4 通过（95.87s，CPU）：HF 固定版本 Kronos-small 在真实行情回归数据上推理，输出与官方期望逐点一致（rel 1e-5），MSE 回归 0.008979/0.003741（±1e-6）。证据边界：证明"模型行为可复现"，不证明"预测可赚钱"。

## 与量化工具链的关系

互补：[[daily-stock-analysis]]（数据）、[[nautilus_trader]]/[[事件驱动回测]]（回测验证）、[[技术指标MA与MACD与RSI]]（人工特征）。正确姿势：Kronos 输出作为策略特征之一进回测框架验证，不直接照预测下单。

## 边界与祛魅

- 高噪声金融序列"预测形状"≠交易边际，中间隔着回测、[[交易成本与鞭打效应]]、非平稳漂移。
- 训练数据集未随仓库发布，"45 家交易所"无法独立复核；最佳指标在未开源的 large 上。
- 微调：finetune/ 与 finetune_csv/ 官方脚本，可用自己的 OHLCV 数据适配。

## 关联

- [[daily-stock-analysis]]、[[nautilus_trader]]、[[事件驱动回测]]、[[预测市场与二元合约]]
- 概念提案：时序分词与行情基础模型（见项目目录 knowledge-proposal.md，协调者终审）
