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
- [[RRSI正则化递归自我改进]]：让 harness 自己变强的元循环——把本条的"七职责"整体当可进化对象，四闸门保证"变强"不退化为"背题"；[[图环挽具三层工程]] 把 harness 定位为系统三层之一
- [[Agent循环]] 是 harness 的心脏；[[Agent中间件]] 是把各职责挂到循环上的挂点
- prompt 只是 harness 里的一个组件：**Prompt engineering 改进指令本身，harness engineering 改进指令被执行的条件**（[[源码即Prompt]]、[[PromptAsCode]]）
- ECC（affaan-m/ECC，27万 star）是"把 harness 当操作系统来做"的样本：293 skills / 68 agents / hooks / rules
- 工具暴露过多的反面教材见 [[工具目录膨胀]]

**首次接触于**：[[项目笔记/agent-harness]]

## AI Native 手册：任务委托在每一跳收缩（2026-10-05）

[[项目笔记/ai_native_handbook]] 给“最小权限工具”补充任务级视角：用户有权做某事，不会自动使任意 Agent 获得同样权限。一次动作必须同时满足用户权限、Agent 能力上限、平台策略、当前委托与运行约束；子委托只能在父委托允许的范围内进一步收窄，不能因角色名称或工具菜单而扩大。

自编教学程序用可信夹具登记根委托，子委托只取资源子集、动作子集及不晚于父委托的到期时间。已有实验观察到：附录读取被允许而其他资源被拒；扩资源、扩动作和延长有效期三类子委托申请都被拒。请求中的任务或运行实例不匹配也会拒绝。这里的主体和运行实例只是虚构字符串，没有实现真实身份认证、运行环境存活检查或密码学委托证明。

这补充了 [[多智能体协作]] 与 [[子智能体咨询]] 的分工机制，不把分工本身当作授权；执行边界仍需 [[沙箱与审批正交]] 和 [[代码管边界提示词管判断]]。教学程序仅演示上述有限约束，没有建成手册所述全部企业权限体系，也不是阿里巴巴提供的实现。

来源：[手册印刷 p53 / PDF 58](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=58)；[六步实验日志](../../ai_native_handbook/delivery/ai_native_handbook-experiment-log.md)。
