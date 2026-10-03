---
tags: [概念]
领域: AI Agent / 上下文工程
别名: ["handoff", "交接简报", "Compact & Resume", "跨会话续跑"]
首次来源: "[[项目笔记/chat-on-steroids]]"
---

# Handoff交接简报续跑

**一句话定义**：对话快爆上下文时，让当前对话把"做到哪了"写成一份简报存到本地，再开新对话把简报（附任务计划快照）灌回去继续干——**跨会话**的上下文续命机制。

**属于领域**：AI Agent / 上下文工程（[[Compaction上下文压缩算法]] 是同会话内压缩，本笔记是跨会话交接）

**通俗理解**（比喻/例子，讲完落回术语）：像**夜班交接班记录**——快下班的人写下"做到哪、剩什么、注意什么"，接班的人照单继续。与 Compaction 的三点区别：① 跨度——压缩发生在同一会话内替换历史，handoff 是旧对话→本地文件→新对话；② 作者——压缩由系统执行，handoff 的简报由**模型自己作为最终回答写出**；③ 防伪造——chat-on-steroids 的 handoff id 由本地 `randomUUID` 生成，**绝不让模型自造 id**（注释原话：模型编的 id 会撞真 id、覆盖别人的简报、或给下个会话一个解析到别人简报的 id）。交接时附带任务计划并诚实标注"这是 reported progress, not verification evidence"（汇报的进度不是验证过的证据）——连措辞都在防假完成。

**与已有概念的关联**：
- [[Compaction上下文压缩算法]]：同会话压缩 vs 跨会话交接，互补而非替代
- [[Checkpoint存档与持久执行]]：handoff 简报本质是一种 checkpoint，id 生成权在宿主是防篡改关键
- [[上下文预算与战略压缩]]：用户侧何时该交接
- [[AI味模式库与信号非证据]]："reported ≠ verified" 的措辞自律是同一思想

**首次接触于**：[[项目笔记/chat-on-steroids]]（src/main/session/handoff.ts、handoff-prompt.ts）
