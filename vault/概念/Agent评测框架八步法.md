---
tags: [概念]
领域: AI Agent / 评估工程
别名: [Agent Eval Framework, Evaluation Framework, 评测八步法, Eval Charter]
首次来源: "[[项目笔记/agent-eval]]"
---

# Agent 评测框架八步法

**一句话定义**：把"Agent 能不能上线"变成可证明的工程流程——**明确发布决策 → 定义成功与 Hard Failure → 建数据集 → 记结果与轨迹 → 配 Rules/Judge/Human → 重复运行 → 设 Release Gate → 线上失败回流**（X @ClorisSignal 长文）。

**属于领域**：AI Agent 评估 / 质量工程

**通俗理解**：Traditional 软件测试证明"程序没崩"；Agent 评测要证明"它做对了"——因为 Agent 最危险的失败是**做错了还显示"已完成"**（静默失败）。八步法的第一步不是选框架买平台，而是写 **Eval Charter**：为什么评、评谁（system_under_test 要写全模型+Prompt+检索+工具+环境，否则无法复现）、拿什么比、什么错误绝不能发生（OpenAI 称这一阶段 Specify）。**写完 Charter 时一次模型都还没跑，但最重要的决定已钉死。**

**数据集要点**：第一版 30 条够跑通（12 常见/6 边界/4 冲突/4 工具失败/2 历史事故/2 对抗），做门禁前扩到 100–300；切成 dev/holdout/regression/challenge 四份**分别报告**（混在一起 challenge 拉低总分，只看流量则低频安全风险被淹没）；**每次线上事故必变成新 regression case**；模型生成的题不能直接当金标准（出题与答题共享偏差）。

**与已有概念的关联**：
- [[LLM裁判与自动评估]]：八步法中"配 Judge"一步的展开；本文补 Judge 校准（calibration set 100–500 条、分错误类型单独报告、高置信错误更要抽检）
- [[质检Gate与自我纠错循环]]：Release Gate 是质检 Gate 在发布决策层的版本
- [[规格书先行SpecDriven]]：Charter 先行 = "把规格写成合同再动工"的评测版
- [[证据优先质检ProofOverClaims]]：Outcome 查环境终态（文件/退款记录/测试真跑）而非听 Agent 说"完成"
- [[Compaction上下文压缩算法]] 同属 Agent 工程化配套；[[AgentHarness智能体挽具]] 是执行侧、八步法是证明侧

**首次接触于**：[[项目笔记/agent-eval]]
