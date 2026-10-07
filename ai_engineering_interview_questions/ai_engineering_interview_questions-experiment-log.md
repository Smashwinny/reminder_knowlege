# 实验日志 · AI 工程面试题库（ai_engineering_interview_questions）

- 任务：66fb1030-debe-42c6-bd19-7ad61b6e8c1d
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 实验位置：`exercise/quiz_generator.py`（纯 Python 标准库，无第三方依赖）

## 实验设计

仓库本体是单文件 README.md（2047 行）的题库，无代码可运行。实验目标：把"README 到底装了多少题、结构如何、谁被问得最多"从宣传数字变成可复现的解析统计，并做一个按主题抽题生成自测卷的小工具。

## 运行记录（全部真实执行）

### 运行 1：`python quiz_generator.py stats`

对 `repo/README.md` 全量解析（`##` 大类 / `###` 主题 / `- ` 题目 / 缩进的 `Asked at:` 与 `Answer:` 行），真实输出（完整见 `exercise/run_output.txt`）：

```
题目总数：598
带答案链接：232（38.8%）
被标注'哪些公司问过'的题目：97

按大类题目分布：
  Frontier AI Labs                                    197 题
  Common Questions Asked Across Companies             119 题
  AI-Native Product Companies                         114 题
  Big Tech AI Organizations                            82 题
  AI Infrastructure and Platform Companies            66 题
  Forward-Deployed and Enterprise AI                  20 题

公司提及榜 Top 5：Anthropic 13 / OpenAI 12 / NVIDIA 11 / Perplexity 11 / Microsoft 11
```

- 598 与帖子宣称"约 600 道"吻合；35 家公司在各主题分区标题与公司专属分区中体现。
- 发现：帖子说"KV 缓存 8 家最多"，而 README 的 Asked at 标注中 Anthropic（13）/OpenAI（12）最高——KV 缓存的"8 家"是指**该题**被 8 家公司问过，两者口径不同（公司榜 vs 单题频次），指南中已注明。

### 运行 2：`python quiz_generator.py quiz --topic "RAG" --count 5 --seed 42`

- 匹配到 "RAG and Retrieval" 主题共 12 题，种子 42 下抽出 5 题（BM25 vs 稠密检索、chunking 策略、HyDE、RAG 评估等）。
- 生成 `quiz_RAG.md` + `quiz_RAG.html`（彩色表格卷面）。

### 运行 3：`python quiz_generator.py quiz --topic "KV Cache" --count 4 --seed 7`

- **失败（真实记录）**：主题 "KV Cache" 无匹配。脚本按子串匹配主题分区名，README 中 KV 缓存题在 "Inference, Serving and GPU Performance" 与 "LLM Internals and Architecture" 分区，没有名为 KV Cache 的主题。脚本打印了全部 48 个可选主题并以 exit=1 退出。

### 运行 4：`python quiz_generator.py quiz --topic "Inference" --count 4 --seed 7`

- 改主题后成功：匹配 15 题，抽出 FP16/BF16/FP8/INT4 量化对比、PagedAttention 与 KV-cache 碎片、五种并行策略对比、vLLM/SGLang/TensorRT-LLM 选型 4 题——正好覆盖帖子点名的 KV 缓存高频考点。
- 生成 `quiz_Inference.md` + `quiz_Inference.html`。
- 验证种子可复现：同命令重复执行输出一致。

## 结论

- 仓库规模、答案覆盖率（38.8%）、公司榜均经独立解析核实，宣传数字基本属实。
- 单文件 Markdown 结构规整，标准库正则即可全量解析，适合作为"数据化复习优先级"的素材。
- 限制：Asked at 标注仅 97 题（16%）有，公司榜样本有限；"约 600 题"为动态数字，随提交变化。

## 产物

- `exercise/quiz_generator.py`、`exercise/run_output.txt`
- `exercise/quiz_RAG.md/.html`、`exercise/quiz_Inference.md/.html`
