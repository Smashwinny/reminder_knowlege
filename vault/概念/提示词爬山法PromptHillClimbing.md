---
tags: [概念]
领域: AI Agent / 质量模式
别名: [PromptHillClimbing, 自改进循环, self-improving loop, generate-score-steer 循环, 提示词爬山]
首次来源: "[[项目笔记/assbench]]"
---

# 提示词爬山法 PromptHillClimbing

**一句话定义**：把 prompt 本身当优化对象——generate 按当前 prompt 生成 → 确定性 rubric 打分 → 把最低分维度翻译成修正注释回灌 prompt → 循环并只保留历史最高分（best），像登山者只记最高营地一样让"生成配方"逐轮变强。

**属于领域**：AI Agent 质量工程 / 提示工程

**通俗理解**：反思模式改"这一份产出"，爬山法调"生成配方"——配方是可复用资产，调好了每一炉都好。Ass Bench（Dev Ed 恶搞 benchmark）把这条 40 行的循环开源了：generate/score/steer 三个槽位 + best 单变量 + runs/ 全量日志。

**四个工程铁律**（每条都有实测坑背书）：
- **评分器必须确定性**：上游 scorer 用 Python `hash()` 占位，跨进程盐随机 → 同一 prompt 两遍跑分 0.6450 vs 0.6350，爬坡曲线全是噪声（[[确定性脚本]]）
- **转向要小步**：每圈只对至多 2 个最低分维度转向（max_steers 限流），"steers small and few per round is what keeps the loop from drifting"（[[修改与约束分离]] 同源）
- **prompt 要去重**：steer 只追加不去重 → 同一句注释重复 4 次、prompt 单调膨胀吃掉 [[上下文预算与战略压缩]]；修法 = 幂等去重 + 达标停注（维度 ≥0.95 不再为其转向）
- **注释要正交**：幂等去重 × 参数耦合 = 隐蔽死锁——注释已在 prompt 却不生效，且永远无法再被引导（实验实测卡 0.4550）；每个 steer 注释必须独立生效

**与已有概念的关联**：
- [[RRSI正则化递归自我改进]]：直系后代——爬山调 prompt 配方、RRSI 进化整个 harness，且加了四道正则化闸门（退火预算/噪声地板/成本规则/[[Critic泄漏审查]]）专防"进化集背题"；本条的小步限流（max_steers）是退火预算的朴素版
- [[反思模式Reflection]]：同族不同向——反思改产出（双停止条件），爬山调配方（轮数上限 + 人肉转向）；两者都依赖 [[LLM裁判与自动评估]] 的可信裁判
- [[质检Gate与自我纠错循环]]：score 步就是一个 Gate，评语（notes）即修改素材
- [[纯函数游戏引擎与种子复放]]：best + 全量 JSON 日志 = 循环可复放可审计

**首次接触于**：[[项目笔记/assbench]]（实验：文字版真收敛循环 0.3161→0.6359→1.0000 三轮收敛、逐位可复现）
