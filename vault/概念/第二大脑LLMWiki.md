---
tags: [概念]
领域: 知识管理 × AI Agent
别名: ["LLM-Wiki", "第二大脑", "Second Brain", "活的 wiki"]
首次来源: "[[项目笔记/karpathy_second_brain]]"
---

# 第二大脑LLMWiki

**一句话定义**：把原始素材（文章/转录/PDF）丢进只读的 raw/ 文件夹，让 LLM agent 增量构建并持续维护一个原子页 + 双链的 Markdown wiki——知识被"编译"一次并保持更新，而不是每次查询现检索。

**属于领域**：知识管理 × AI Agent（Karpathy 2026-04 gist《llm-wiki》命名，推文级传播千万浏览）

**通俗理解**（比喻/例子，讲完落回术语）：传统笔记是自己养的花，浇水全靠自己，出差两周就枯；第二大脑是雇了不会累、不会忘、一次能改 15 个文件的园丁（LLM），人只管扔种子（raw 源）和提问。落回术语：三层架构——**raw/ 人写只读（审计线）、wiki/ LLM 全权维护、CLAUDE.md schema 与人共同进化**；三大操作 **Ingest（摄入：一源触及 10~15 页）/ Query（先读 index.md 再钻页，答案回填成新页）/ Lint（体检：断链/孤儿页/矛盾/过时论断）**。金句："Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

**与已有概念的关联**：
- raw 只读 + log.md 只追加 = [[JSONL事件日志与折叠模型]] 的"事实层不可变、派生层可重建"同款哲学
- schema（CLAUDE.md）与 [[AgentSkills技能包]]（SKILL.md）同物种；结构化槽位即 [[PromptAsCode提示词即代码]]；Lint 即 [[质检Gate与自我纠错循环]] 的客观检查站
- 与 [[RAG检索增强生成]] 是范式对照：RAG 每查询现检索零积累；wiki 是增量编译复利资产；规模大了用 qmd（BM25+向量，即 [[HNSW近似最近邻索引]] 那套）补混合检索
- raw→wiki→schema 逐层压缩可回溯，同构 [[三层记忆]]
- wiki 只是 .md 的 git 仓库，应用仅是视图 = [[本地优先与文件监听]]；Obsidian 的 graph view/反链/Web Clipper 是免费增值件
- 隐私与最小授权约束 LLM 只写 wiki/ 不碰 raw/ = [[提示注入]] 防御思想
- **F:\reminder 本仓库就是实例**：拾遗队列=raw 层，vault\=wiki 层，learn-project SKILL=schema，入库查重=Lint（见 [[项目笔记/karpathy_second_brain]] 映射表）

**首次接触于**：[[项目笔记/karpathy_second_brain]]
