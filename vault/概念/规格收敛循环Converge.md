---
tags: [概念]
领域: 软件工程 / AI 协作
别名: [converge, 收敛对账, Converged 报告]
首次来源: "[[项目笔记/speckit]]"
---

# 规格收敛循环Converge

**一句话定义**：AI 施工完一轮后，**拿代码对照 spec/plan/tasks 逐项对账，把"宣称建了但没建/建漏"的部分追加为新任务继续施工，循环直到对账报告给出 "Converged"（已收敛）**——给"AI 说做完了"上一道验收锁。

**属于领域**：AI 协作工程 / 规格驱动开发（github/spec-kit 2026 新增环节）

**通俗理解**：装修队说"完工了"，你不能光听——拿图纸一间屋一间屋点验：少装的开关写进新的工单再派回去，点验到"全部对上"才收房。spec-kit 里 implement 负责干活、converge 负责点验补单，两者组成 `implement → converge → implement → …` 的循环，直到 converge 主动报告 Converged。它治的正是 vibe coding 最典型的翻车：**上下文漂移导致 AI 最后一轮"自我感觉良好"**。

**与已有概念的关联**：
- 与 [[质检Gate与自我纠错循环]] 同族：都是"检错→补活"循环，但 converge 的判据是**规格工件清单**（spec/plan/tasks 逐项勾稽），不是泛泛的自查
- 是 [[规格书先行SpecDriven]] 的验收侧闭环：spec 是合同，converge 是按合同逐条验收
- 补 [[工单任务图与前沿调度]] 的短板：那边假设工单全按图完工，converge 处理"完工后重新对账发现漏项"的现实
- 配套确定性脚本 check-prerequisites 保证对账前工件齐全，同 [[源码即Prompt]] 的机械活不交给模型原则

**首次接触于**：[[项目笔记/speckit]]（specify init 实测生成 speckit-converge SKILL.md，Next Steps 面板明确"repeat implement→converge until Converged"）
