---
tags: [项目]
类别: 知识学习类（Google 论文复现 + 评测驱动提示词进化）
上游仓库: https://github.com/google-research/rrsi（Apache-2.0，HEAD be50316）
完成日期: 2026-10-03
---

# rrsi

**这是什么**（一句话）：Google Cloud AI Research 的 RRSI（arXiv 2609.24972，COLM '26）——让 AI 在评估驱动的进化环里**针对失败的检查重写自己的 harness**（系统提示词/控制流/工具/记忆），用四道正则化闸门防"背题式过拟合"；本任务从一条 X 高赞推文溯源到论文+开源代码，源码精读 + 离线复现。

**它给我什么能力**：
- 读懂 2026 年"自进化 agent"论文系（RRSI/RSI-Master/Recuris）的公共词汇：harness、进化集、OOD、正则化闸门
- 给自己的 prompt/harness 建最小回归体系：固定检查题+留出题+改前改后都跑
- 可拆用的纯函数件：余弦退火预算/噪声地板校准/成本规则/组件打标（Apache-2.0，全部离线可跑）
- 识破"刷榜式 agent 宣传"的三个追问：OOD 留出集？成本账？泄漏审查？

**引入的概念**：
- [[RRSI正则化递归自我改进]] — 主概念：进化环+四闸门（退火预算/噪声地板/成本规则/Critic）
- [[Critic泄漏审查]] — 评估前抓"针对评分集作弊"的六条拒绝规则
- [[图环挽具三层工程]] — 推文引用链第二环（arXiv 2609.00050）：graph/loop/harness 三层

**实验记录**（做了什么、结果、坑）：
- 官方单测 `pytest tests`：**8 passed in 0.11s**（纯方法核、零 API；官方三实例 Terminal-Bench 2.1/Harvey LAB/EngDesign 需 Vertex AI+Docker，本机未跑，已如实标注）
- 实验一 `exercise/rrsi_core_demo.py`（零改动复用真实仓库模块）：退火表 T=10 → 4,4,4,4,3,3,3,2,2,2 收 1；五候选裁决——A 大涨中选、B 带内走整形分支 +2.50、C 触地板拒、D critic_reject、E 超成本预算（ΔC=8.60>8.10）拒；标签防谎报四种全纠正（申报 skill+空 diff→prompt 等）
- 实验二 `exercise/toy_rrsi.py` 迷你进化环三模式：诚实+审查 = 2 轮收敛 S_id/S_ood 双 1.000 成本 36；作弊+审查 = 连续 3 轮被拦 bounded repair 终止；作弊+无审查 = S_id 1.000 但 **S_ood 0.000**、成本 95（2.6×）——论文要防的过拟合一次看全
- 坑：candidate B 的带内分支演示要先算好奖励（[1,0] 均值 0.5 会顶出 delta 边界）；break 放在打印前会让"第 3 次拒绝"无声终止，bounded repair 消息要在打印之后

**后续可深入的方向**：
- 有 Vertex 凭据时跑 `python rrsi.py --domain coding smoke/baseline` 体验真进化
- 把 toy_rrsi.py 的提案者换成真 LLM API，规则库扩到真实项目 prompt
- 对读 RSI-Master / Recuris，比较不同正则化思路
