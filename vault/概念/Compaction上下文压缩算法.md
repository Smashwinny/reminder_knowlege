---
tags: [概念]
领域: AI Agent / 上下文工程
别名: ["context compaction", "上下文压缩", "切割点压缩", "结构化摘要压缩"]
首次来源: "[[项目笔记/agent-kernel]]"
---

# Compaction 上下文压缩算法

**一句话定义**：agent 内部自动压缩对话历史的完整算法——token 记账（优先用 provider 真实 usage，仅对新增消息估算）→ 双路径触发（阈值：用到 `window − reserveTokens`；溢出：约 25 种正则匹配各家 provider 的溢出报错并排除限流误判）→ 切割点（保留最近 keepRecentTokens 原文、更早进结构化摘要）→ 摘要生成（固定模板 + 增量更新 + 文件操作清单）。

**属于领域**：AI Agent / 上下文工程（[[上下文预算与战略压缩]] 讲用户侧"什么时候主动压缩"，本笔记讲实现者侧"内核怎么自动压"；[[KV缓存与上下文]] 讲缓存经济账）

**通俗理解**（比喻/例子，讲完落回术语）：像**会议纪要制度**——最近几小时的发言保留逐字稿（原文），更早的整理成带固定栏目的纪要（Goal / Progress(Done/In Progress/Blocked) / Key Decisions / Next Steps）。三个容易忽略的细节：①**切割点只落在整轮边界**——切在工具调用序列中间会让模型看到"半轮对话"，pi 的做法是 split-turn 两段摘要再拼接；②**文件操作清单从 tool_calls 参数里程序化提取**（读过/改过哪些文件），不靠模型在摘要里"记得"；③**迭代压缩带旧摘要增量更新**（PRESERVE/ADD/UPDATE），不是每次从零重总结。实测（agent-kernel demo-compaction）：800 窗口阈值 680，19 条消息 799 tok 触发，切割点第 7 条，799→594 tok 释放 205。

**溢出触发的隐藏坑**：各家 provider 的"上下文满了"报错文案五花八门（Anthropic/OpenAI/Google/国产各有格式），还有**静默溢出**（stop=stop 但 usage.input>窗口，z.ai 风格）和**截断溢出**（stop=length+output=0，小米 MiMo 风格）；必须用 NON_OVERFLOW_PATTERNS 排除限流误判。溢出恢复只允许一次（`_overflowRecoveryAttempted` 标志防无限循环），compact 后仍溢出就放弃并提示换大窗口模型。

**与已有概念的关联**：
- [[上下文预算与战略压缩]]：用户侧预算观（何时主动压/千万别压）；本笔记是内核自动化的实现版
- [[Agent循环]]：压缩挂在 agent_end 之后和 prompt 之前两个时机
- [[KV缓存与上下文]]：压缩必然丢 KV 缓存，早压省 token vs 缓存重建的权衡
- [[Checkpoint存档与持久执行]]：压缩状态也要可存档可恢复
- [[项目笔记/cmu-agents]]：CMU 11-768 作业里的工作记忆压缩是同一问题的教学版实现（实测 2816→409 tok）

**首次接触于**：[[项目笔记/agent-kernel]]（note 04《pi 上下文压缩的那些事》；pi compaction.ts 880 行）
