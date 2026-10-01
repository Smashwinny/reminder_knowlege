---
tags: [概念]
领域: AI / 大模型应用
别名: [RAG, Retrieval-Augmented Generation, 检索增强生成]
首次来源: "[[项目笔记/vector_database_qdrant]]"
---

# RAG检索增强生成

**一句话定义**：回答问题前先去外部知识库检索相关资料，把资料塞进提示词再让大模型生成答案——"开卷考试"代替"闭卷硬编"。

**属于领域**：大模型应用架构

**通俗理解**：五步流水线：用户提问 → 问题向量化（[[向量与Embedding]]）→ [[向量数据库]] 语义检索 Top-k 相关片段 → 检索结果 + 问题拼成提示词 → LLM 生成有据可依的回答。没有 RAG 时模型对私有文档一问三不知或幻觉瞎编；RAG 让"模型不知道"变成"现查现用"，且知识更新只需改库、不用重训模型。

**与已有概念的关联**：
- 检索环节就是 [[向量数据库]] 的核心应用场景（Qdrant 官方有 langchain-qdrant 集成包）
- 问题向量化用 [[向量与Embedding]]
- 产业链位置：ollama 跑模型 → langchain/langgraph 编排流程 → Qdrant 存知识，三者拼成完整私有知识库
- 与 [[Agent循环]] 结合 = **Agentic RAG**：检索器成为一件工具，LLM 自己决定查不查、查不到转网搜、自查检索质量重查（纠错式 RAG/CRAG）；awesome-llm-apps 的 rag_tutorials 区 24 个教程是这条链的渐进升级（本地、混合检索、多模态、知识图谱+引用）

**首次接触于**：[[项目笔记/vector_database_qdrant]]（另见 [[项目笔记/langchain]]、[[项目笔记/awesome-llm-apps]]）
