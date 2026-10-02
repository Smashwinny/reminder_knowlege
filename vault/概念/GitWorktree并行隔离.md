---
tags: [概念]
领域: 软件工程 / AI 协作
别名: [worktree 隔离, 并行施工隔离]
首次来源: "[[项目笔记/ai-website-cloner]]"
---

# GitWorktree并行隔离

**一句话定义**：`git worktree` 让同一个仓库同时检出多个独立工作目录（各带独立分支），使多个 builder agent 能并行施工而互不覆盖文件。

**属于领域**：软件工程 / AI 多智能体协作

**通俗理解**：就像给每个施工队分一整层楼，而不是让大家挤在同一层抢工具——各队在自己楼层干活，完工后由工头逐层验收、合并回主楼。在 ai-website-cloner-template 里，主 agent 为每个区块的 builder 开一个 worktree，builder 改崩了也不污染主线；每次 merge 回 main 后立即跑 `npm run build` 验证（[[质检Gate与自我纠错循环]]）。

**与已有概念的关联**：
- 相关：[[多智能体协作]]（worktree 是其"物理隔离"实现手段）、[[构建流水线与Pass]]（并行 Pass 的隔离层）、[[质检Gate与自我纠错循环]]（每次合并后的编译 Gate）

**首次接触于**：[[项目笔记/ai-website-cloner]]
