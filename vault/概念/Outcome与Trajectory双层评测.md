---
tags: [概念]
领域: AI Agent / 评估工程
别名: [Outcome Eval, Trajectory Eval, 双层评测, 结果与轨迹分层评分]
首次来源: "[[项目笔记/agent-eval]]"
---

# Outcome 与 Trajectory 双层评测

**一句话定义**：Agent 评测必须把**终态（Outcome：目标文件存在吗/引用有效吗/外部系统真变了吗）和执行过程（Trajectory：该用的工具用了吗/参数合法吗/有无循环与越权/失败后恢复了吗）拆成两层分别设计 grader**，因为"报告正确、过程仍可能有问题；轨迹合理、结果仍可能没交付"。

**属于领域**：AI Agent 评估

**通俗理解**：传统 LLM 评测是直线 `Input→Model→Output→Score`；Agent 是 `Goal→Plan→ToolCall→Observation→Re-plan→环境变化→Final Output` 的可变路径。只看终态，会放过"先访问禁用数据源再换回来"和"搜 30 次碰对答案成本失控"；只看轨迹，会漏掉"过程漂亮但最后保存失败"。**对会改状态的 Agent，环境终态比最后回复更可信**——代码 Agent 真跑测试、SQL Agent 真执行查询、退款 Agent 核对退款记录（NVIDIA 把工具使用当一等评分信号）。

**配套三层 Grader**：**Rules**（确定性检查：Schema/字段/URL/参数/次数/禁止工具/终态，便宜稳定易排错，但链接能打开≠支撑结论）+ **LLM Judge**（语义：结论是否被引用支持、冲突是否如实呈现；每 Judge 只评一维，v1/v2 对比用 Pairwise + 顺序随机防位置/长度偏好）+ **Human**（定 Rubric、建 gold label、接高风险与低置信 case、**随机抽查防高置信漏判**）。

**与已有概念的关联**：
- [[LLM裁判与自动评估]]：三层中的 Judge 层正是它；本概念补"Judge 是测量工具不是标准答案，自己也要过 Eval（校准集、分错误类型报告、abstain 能力）"
- [[HardFailure一票否决与发布门禁]]：两层评测的结果如何汇成 gate 决策
- [[证据优先质检ProofOverClaims]]：Outcome 层的哲学根源——查证据不听宣称
- [[质检Gate与自我纠错循环]] / [[护栏模式Guardrails]]：Rules 层的近亲
- [[预执行安全网与执行事件]]：Trajectory 检查在执行前/中的版本

**首次接触于**：[[项目笔记/agent-eval]]
