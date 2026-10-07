---
tags: [项目笔记, 面试, AI工程, 知识库]
created: 2026-10-07
---

# ai-engineering-interview-questions-company-wise

- 仓库：https://github.com/pallavi-shekhar/ai-engineering-interview-questions-company-wise （Apache-2.0，Outcome School 维护，快照 commit b62705c，2026-10-07 克隆实测 1685 stars）
- 来源记录：@程序员鱼皮 推文 https://x.com/yupi996/status/2107147301785338207

## 是什么

把 35 家 AI 公司公开面经里的面试题逐公司整理成一份"考情地图"：单文件 README（2047 行），约 600 道 AI 工程师面试题，常见题标注"Asked at: 哪些公司问过"，能答的题附 Outcome School 博客答案深链。

## 实测数据（本机解析，exercise/quiz_generator.py stats）

- 题目总数 **598**；带答案链接 **232（38.8%）**；有 Asked at 标注 **97 题（16%）**
- 六大分区：Frontier AI Labs 197 / Common Questions 119 / AI-Native 产品公司 114 / Big Tech 82 / AI 基础设施 66 / 前线部署与企业 20
- 公司提及榜 Top5：Anthropic 13 / OpenAI 12 / NVIDIA 11 / Perplexity 11 / Microsoft 11
- 帖子口径注：单题频次榜（KV 缓存 8 家、MoE 6 家、提示词/RAG/微调 6 家）≠ 公司总榜，两者统计单位不同

## 怎么用（效率建议）

1. 按目标公司找它的公司分区（含 roles 与公开报道的面试 loop），再刷公共高频题。
2. 用频次排优先级：Asked at 家数多的题先准备（KV 缓存 > MoE > RAG/微调选型）。
3. 带 Answer 链接的 38.8% 题顺链读博客，形成"题→答→体系"链路；无答案题回到本 vault 的对应概念笔记。

## 关联

- [[KV缓存与上下文]]（最高频考点）、[[MoE混合专家]]、[[RAG架构谱系]]、[[提示词模板]]、[[SFT监督微调]]、[[LoRA低秩适配微调]]、[[本地推理引擎]]、[[量化与GGUF]]
- 品味同源：[[证据优先质检ProofOverClaims]]、[[证据等级与性价比双轴]]（Asked at 是可核对标注，不是押题承诺）
- 概念提案：考情地图与频次证据（见项目目录 knowledge-proposal.md，协调者终审）

## 局限

题目全部来自公开面经自述（非内部真题），Asked at 覆盖仅 16%，题库数字随提交动态变化；面试 loop 随团队/级别/地区变化大，当考情地图看，别当押题脚本。
