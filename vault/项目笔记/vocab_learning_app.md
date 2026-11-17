---
tags: [项目笔记]
领域: AI 辅助教育 / 英语词汇学习
来源项目: vocab_learning_app
上游版本: 0.1.11
上游提交: 638ae84f97a04474cb63c6098eacfc6c83b813af
---

# vocab_learning_app：词汇星图与可核验复习排程

## 项目是什么

原 X 帖本次读取返回 HTTP 402，未把网站摘要冒充正文。线索仓库 `HytidelLegend/htd-ai-augmented-education` 已重定向到真实公开仓库 [HytidelLegend/ai-aug-edu](https://github.com/HytidelLegend/ai-aug-edu)。本次固定 `VERSION=0.1.11`、commit `638ae84f97a04474cb63c6098eacfc6c83b813af`，聚焦其中“词汇星图”应用，以及直接相关的 `build-word-entry`、`schedule-ebbinghaus-plan`。

词汇星图是本机单用户 React 19 + Vite 6 前端与 Python 回环 API：唯一 JSONL 总词库存完整词条，项目只引用 `wordId` 并独立保存熟悉度，多个艾宾浩斯/葫芦计划保存各自日程、轮次和通过记录，收藏跨项目共享。考试词表文本不等于完整释义词库；未建词保持占位，不猜释义。

## 带来的概念

- [[词汇关系图谱]]：同族词用分组聚拢而不画 family 边；同义、近义、反义、拼写相似用不同类型和核验状态的边表达；首屏最多 500 个词条与占位节点。
- [[LCS拼写相似度]]：`2 × LCS(a,b) / (len(a)+len(b)) >= 0.75`，源码以 `8 × LCS >= 3 × 总长` 做整数判定；别名、屈折词形和已确认同族/派生词排除。
- [[固定间隔重复排程]]：每日最多引入一个新批次，默认在 +1/+2/+4/+7/+15 天复习；这是项目约定，不是唯一科学时间表，也不是按表现动态调整的 FSRS。
- [[分页掌握门槛]]：葫芦法只排首次学习，每页至少 80% 通过才可前进；5 词页须通过 4 词，乱序只改稳定展示顺序，不改计划日程。
- 词条证据与核验分层：来源引用、`ai_generated + confidence + pending`、脚本 `automatic_passed`、Agent `agent_passed` 分开记录；Schema 合法不等于语义正确。

## 与已有知识的关联

- [[确定性脚本]]：排程、LCS 和稳定乱序由代码确定；复习计划不交给 LLM 逐日心算。
- [[证据优先质检ProofOverClaims]]：本次将独立参考测试、静态源码核验、上游运行时验收分开报告，不能把 15 项自写检查扩写为 UI/API 全栈通过。
- [[本地优先与文件监听]]：相同点是用户数据落本地开放 JSON/JSONL；本项目未见 vault_watch 式文件监听，不能把它写成双向同步实现。
- [[原子笔记与双链]]：词汇星图与 Obsidian 图谱都可关联笔记，但词汇边还带关系类型、来源和核验状态，不能仅凭视觉相似推断语义。

## 实验做了什么

1. 真实克隆并固定版本；`npm ci` 退出码 0，安装 70 个前端包，同时 npm 报告 2 个 high 漏洞，未改锁文件。
2. 上游 Python 隔离环境创建/依赖安装被权限分类器拒绝；`npm run build` 也被拒绝。按规则未绕过，未运行上游 smoke、真实 API/UI、外站采集或音频。
3. 在 `exercise/verify_learning_model.py` 写独立标准库参考模型，实际以 Python 3.14.7 `-I` 运行：15 项通过、0 失败。8 词/每日 3 词得到 3 批、40 个复习事件、排至 D18；葫芦 4/5 过而 3/5 不过；quiet/quite=0.8，cat/cut=0.666667；并核对上游对应源码契约。
4. 原始日志 `exercise/experiment-log.txt` SHA-256：`5241525b78dcc71a339df507b22068403acdeaa2a4b4a19d19144bf7fddb1293`；机器结果在 `exercise/experiment-results.json`。
5. Edge 无头打印生成 13 页、882121 字节 PDF，文件头/EOF 完整；本机 Read 缺少 `pdftoppm`，所以只完成结构检查，未声称逐页视觉审核。

## 坑与结论

- 旧仓库名仍出现在 README 安装指令，真实页面已经重定向；引用功能时必须同时钉 commit。
- 固定间隔不是自适应记忆算法；计划通过记录不会自动调整未来间隔。
- 图谱“看起来相连”不等于专家确认；待核验候选必须保留虚线与 pending 状态。
- revision/409、原子写入、状态机和回环 Origin 检查增强本地单用户可靠性，但不构成多用户认证或完整安全证明。
- 指南：`vocab_learning_app/guide.html`、`vocab_learning_app/vocab_learning_app-小白指南.pdf`。
