---
tags: [概念]
领域: AI Agent / 编排模式
别名: [Parallelization, 并行化, Sectioning, Voting投票, Governing总裁]
首次来源: "[[项目笔记/agentic_design_patterns]]"
---

# 并行化编排 Parallelization

**一句话定义**：把相互独立的 LLM 调用同时执行以换时间或换可靠性——《Agentic Design Patterns》模式 3，三种形态：Sectioning 切片 / Voting 投票 / Governing 总裁。

**属于领域**：AI Agent 编排

**通俗理解**：
- **Sectioning（切片）**：教材分章多人同写，各自独立互不干扰，最后装订；
- **Voting（投票）**：同一题让三个评委独立作答取多数——本质是**花 3 倍 token 买确定性**，用冗余对冲温度带来的随机性（[[LLM采样与温度]]）；
- **Governing（总裁）**：事实核查员、文风编辑、安全审查员同时给意见，总裁一次合成——多视角分工但只有一个出口。

**最轻量实现**：Governing 不需要完整多 Agent 框架，一个 `ThreadPoolExecutor` + 三个 prompt 就够（实验模式 3 实测）；要状态管理再升级 [[多智能体协作]]。

**与已有概念的关联**：
- [[多智能体协作]]：并行化的重量级后继；CrewAI 的并行 Task 即 Voting/Sectioning
- [[共享状态与Reducer]]：并行写回合并的机制
- [[工单任务图与前沿调度]]：入度为零的任务天然可并行

**首次接触于**：[[项目笔记/agentic_design_patterns]]
