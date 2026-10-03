---
tags: [概念]
领域: AI Agent / 自我改进
别名: [RRSI, Regularized Recursive Self-Improvement, 正则化递归自改进, harness 自进化]
首次来源: "[[项目笔记/rrsi]]"
---

# RRSI正则化递归自我改进

**一句话定义**：把 agent 的 harness（系统提示词/控制流/工具/记忆/上下文管理）当作可进化对象，让 LLM 在"分析失败→起草候选→泄漏审查→全套评估→闸门筛选"的循环里迭代改写自己的 harness，而防翻车的全部精髓在**正则化**——约束搜索怎么走，不约束 harness 能长什么样（arXiv 2609.24972，Google Cloud AI Research，代码 google-research/rrsi）。

**属于领域**：AI Agent 自我改进 / 评测驱动优化

**通俗理解**：提示词爬山法像一个厨师只调"配方那句话"；RRSI 是连锅、灶台、进货渠道一起换的整厨改造——但不许凭"我觉得好"就换，每换一样要过四道闸门：①**退火预算**（开局可捆绑多处改动，临近收尾每轮只许改一处，公式 `b_t=ceil(b_min+(b_max-b_min)·½(1+cos(πt/T)))`，为的是每处编辑可单独归因）；②**噪声地板**（比历史最高 S* 低 delta 以内的"涨分"当噪声，delta 用 bootstrap 校准出来的评分抖动带）；③**成本规则**（真涨分时 token 成本涨幅 ≤ β₀+β₁·ΔS，带内微涨走整形分 w_s·ΔS−w_c·ΔC+w_n·ν>0，ν=触及从未采纳过的结构组件数只作带内平局打破）；④**Critic 泄漏审查**（见 [[Critic泄漏审查]]）。无正则化的 RSI 会把进化集背下来：进化集最高 +14.1 分、换一套题只剩 +4.7，而 RRSI 在 8 个基准上 OOD 仍正收益且省 30% 策略 token。

**与已有概念的关联**：
- [[提示词爬山法PromptHillClimbing]]：最近的近亲——都调"配方"且只留历史最高分；但爬山只改 prompt 文本+小步转向，RRSI 进化整个 harness 并用四闸门防过拟合（爬山法的 max_steers 小步限流 ≈ 退火预算的朴素版）
- [[AgentHarness智能体挽具]]：进化对象本体——"prompt 只是 harness 里的一个组件"在 RRSI 里被形式化为 9 类可编辑组件集 K
- [[LLM裁判与自动评估]]：进化压力的来源，评估器越可信进化越真
- [[GitWorktree并行隔离]]：每个候选在 evolve/<domain> 分支的独立 worktree 里起草，采纳即 fast-forward，现任 harness 永远是一个 commit
- [[Critic泄漏审查]]：四闸门中最有普遍意义的一道
- [[Agent循环]]：RRSI 是套在 agent 循环外面的"元循环"——内循环干活的 agent，外循环改 agent
- [[质检Gate与自我纠错循环]]：整条选择侧就是一串非补偿性 Gate

**首次接触于**：[[项目笔记/rrsi]]（实验：官方单测 8 passed；真实仓库模块复现退火表+五候选裁决+标签防谎报；toy_rrsi.py 三模式复刻"进化集满分/OOD 归零"过拟合翻车）
