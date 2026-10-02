---
tags: [项目]
类别: 知识学习类（方法论）
上游仓库: https://github.com/Aquinas-Protocol/second-brain（社区 starter kit 实例，已克隆 repo\）
完成日期: 2026-10-02
---

# karpathy_second_brain（Karpathy 第二大脑 / LLM-Wiki）

**这是什么**（一句话）：Karpathy 在 gist《llm-wiki》提出的个人知识库玩法——不让 LLM 每次查询现检索（RAG），而是让它增量构建并持续维护一个 Markdown wiki；社区 starter kit（second-brain）把它落成 raw/ + wiki/ + CLAUDE.md + 四条斜杠命令 + 夜间定时任务。

**它给我什么能力**：收藏夹变知识资产 / 读书伴生 wiki / 科研渐进综合 / 团队知识库无人值守维护 / 直接优化 F:\reminder 本仓库的 vault 流程 / 问答成果回填 wiki。

**引入的概念**：
- [[第二大脑LLMWiki]] — 三层架构（raw 只读 / wiki LLM 维护 / schema 共同进化）+ Ingest/Query/Lint 三操作
- [[原子笔记与双链]] — wiki 层的语言：一页一概念 + `[[双链]]` + 来源标注

**实验记录**（做了什么、结果、坑）：
- exercise\mini-wiki\：8 页迷你 wiki + 三个零依赖 Python 工具（mini_ingest / wiki_lint / wiki_query），把 LLM 的簿记动作写成确定性脚本演示。10 步全流程真实跑通：ingest 前 lint 报"log.md 不存在"→ ingest 两源生成 2 源摘要页+6 概念页+index+log → lint 全绿（8 页 24 双链）→ 埋断链被 lint 抓出 3 问题（断链/孤儿页/index 未收录）→ query "wiki" 命中排序正确（14.5 分源摘要页居首）→ `grep "^## \[" log.md` 成功解析时间线。
- 坑：Edge 无头打印后 PDF 需等几秒才落盘；grep 中文 heading 生成的概念页文件名含中文，Windows 下 OK 但跨平台脚本要注意编码（脚本全部显式 encoding="utf-8"）。

**后续可深入的方向**：
- 给 F:\reminder\vault\ 写一个 wiki_lint 脚本（查断链/孤儿概念/未收录进 00-总览 的页）
- 试用 qmd（本地 BM25+向量混合检索，CLI + MCP server 双形态）对 vault 做检索增强
- 把本项目的"答案回填"原则用于日常 vault 使用：好答案存成新概念页
