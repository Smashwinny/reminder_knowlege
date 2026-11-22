---
tags: [项目笔记]
类别: 知识学习类（API 成本工程）
来源项目: gpt6_handbook
完成日期: 2026-11-22
---

# gpt6_handbook：原手册选型思路与提示词缓存官方复核

## 项目是什么

原记录为 @ai_xiaomu 引用《GPT-6 Astra、Sol、Luna 使用手册》的 X 帖。学习保留“按任务选型、锁推理参数、重复前缀分账”的方法，同时以 2026-11-22 官方模型页和 Prompt caching 文档纠正初稿中混合新旧机制的口径。

## 来源核实

- 原帖：https://x.com/ai_xiaomu/status/2104959406840688654
- 缓存：https://developers.openai.com/api/docs/guides/prompt-caching
- 模型索引：https://developers.openai.com/api/docs/models
- 旧/新型号页：`gpt-6-sol`、`gpt-6.1-sol`、`gpt-6.2-sol` 官方模型页。

当前索引列出 6.2 Astra/Sol、6.1 Terra、6 Luna、6 Cyber；6.1 Sol 页面可读但不在当前索引。旧 Sol 支持 `none`，6.1/6.2 Sol 不接收。GPT-5.6+ 不是固定 128 token 断点，命中读价也有 0.1×/0.05× 等型号差异。

## 带来的概念

- [[提示词缓存计费与命中边界]]：前缀、断点、TTL、路由、写价、读价和 usage 分开。
- [[能力地板选型]]：追加“锁具体 model ID 与文档日期”，不另建同义概念。
- [[付费调用回执与预算熔断]]：追加 cached/write token 回执字段，估算不替代账单。
- [[KV缓存与上下文]]：推理侧 KV 与 API 侧缓存相关但不同层。

## 实验做了什么

`exercise/cache_economics.py` 改为仓库相对样本路径和可参数化成本模型。当前总览粗估 65,903 token，每次新增 200 token、共 10 次、普通读价假设 $5/M、写入 1.25×、后续全命中：0.1× 读价成本 $0.7187、省 78.3%；0.05× 成本 $0.5704、省 82.7%；两者均 2 次平衡。两条命令实际复跑正常退出。

## 坑与结论

- 初次 PDF 页序错乱；v2 从修订 HTML 重印，共 12 页，Windows.Data.Pdf 全部逐页渲染检查，页序正确且无裁切/空白页。原 PDF 保留，manifest 指向 v2。
- 原手册发布日期、基准、客户案例、灰度范围未逐项核实。
- 无 API key，未发真实请求；粗分词、全命中假设和公式输出不是实际命中率或账单。
- 指南：`gpt6_handbook/gpt6-handbook-guide.html`；审核版：`gpt6_handbook/GPT-6使用手册-小白指南-v2.pdf`。
