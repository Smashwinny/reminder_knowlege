---
tags: [概念]
领域: AI 工具生态 / 编程智能体
别名: ["Harness Engineering", "挽具工程", "智能体挽具", "agent harness"]
首次来源: "[[项目笔记/agent-harness]]"
---

# AgentHarness智能体挽具

**一句话定义**：模型之外的一切运行环境——决定 agent 能看什么、能碰什么、什么能跨会话存活、什么算证据、什么时候必须停；**模型是推理引擎，harness 是让推理可靠落地的那套"挽具"**。

**属于领域**：AI 工具生态 / 编程智能体

**通俗理解**：同一匹马（模型），套上不同的挽具（缰绳+车+车道），能干的活完全不同。放进聊天框它只能答题；放进带终端、测试、浏览器工具、项目记忆和审查循环的代码仓库里，它就能交付软件。**权重没变，harness 变了**。Dario Amodei 解释 Claude Code 诞生时原话："Of course, you need an interface, you need a harness to use them"；OpenAI 在《Harness engineering: leveraging Codex in an agent-first world》里同样把 agent 反复失败归因于"环境欠规格"而非模型不行。

**生产级 harness 的七个职责**（来自 ECC 生态与 Harness Engineering 方法论）：
1. **请求→契约**：动手前把需求固化成有边界对象，防止 agent 悄悄换了活儿还宣告成功
2. **给 agent 一张地图**：小的根指南告诉它去哪找，详细知识贴在代码旁边按需加载（见 [[分层按需加载]]）
3. **正确环境暴露正确工具**：最小权限，写权限只给该给的目录（无头模式默认拒绝写文件，必须显式授权）
4. **验证与证据**：模型说 DONE 不算数，产出物必须真实存在且合格（[[证据优先质检ProofOverClaims]]、[[质检Gate与自我纠错循环]]）
5. **上下文工程**：预算、压缩、模型分级路由（[[上下文预算与战略压缩]]）
6. **失败廉价**：重试死掉的沙箱、从日志重放上下文，而不是从头再来（[[Checkpoint存档与持久执行]]）
7. **停止条件**：明确什么算完成、什么必须停，防死循环

**与已有概念的关联**：
- [[Agent循环]] 是 harness 的心脏；[[Agent中间件]] 是把各职责挂到循环上的挂点
- prompt 只是 harness 里的一个组件：**Prompt engineering 改进指令本身，harness engineering 改进指令被执行的条件**（[[源码即Prompt]]、[[PromptAsCode]]）
- ECC（affaan-m/ECC，27万 star）是"把 harness 当操作系统来做"的样本：293 skills / 68 agents / hooks / rules
- 工具暴露过多的反面教材见 [[工具目录膨胀]]

**首次接触于**：[[项目笔记/agent-harness]]
