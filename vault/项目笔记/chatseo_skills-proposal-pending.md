# ChatSEO 六技能 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：2b6b9a2f-5da4-4d5c-b0cb-cbe3930453ce ｜ 项目目录：F:\reminder\chatseo_skills

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 上线前差异闸门（DIFF GATE）
- 一句话定义：AI 改写线上内容前，先机械列出"旧版有而新版丢失的元素清单"（表格/表单/图片/链接/H1），清单必须经人工逐项确认后才允许发布；fail-closed，有丢失即退出非零。
- 领域：AI 工具生态 / 内容安全
- 已有概念关联：[[证据优先质检ProofOverClaims]]（"改写完成"宣称不算证据，diff 清单才算）；[[质检Gate与自我纠错循环]]（Gate 的发布域特化）
- 来源项目：chatseo_skills（本地复刻 diff_gate.py 三轮实测 3/3：抓丢失/无误报/修复放行）

### 2. 政策到纪律翻译
- 一句话定义：把平台政策（如 Google 垃圾政策"无用户价值的大规模内容"）翻译成 Agent 可执行的具体纪律（"只换城市名的页不发""一次一页"）——合规不靠模型自觉靠规则前置。
- 领域：AI 工具生态 / 合规
- 已有概念关联：[[护栏模式Guardrails]]（确定性护栏包住 LLM）；[[Agent指令文件AgentMd]]（行为契约）
- 来源项目：chatseo_skills（pattern-drip 规则 vs Google spam policies 对照）

## 二、项目笔记（建议新建 vault\项目笔记\chatseo_skills.md）
- 项目是什么：X 长文《My chief of SEO, claude code opus 5.5》所述六技能 SEO Agent 工作流（Claude Code 主管 + ChatSEO MCP 情报层 + 人审批）
- 带来的概念：[[上线前差异闸门（DIFF GATE）]]、[[政策到纪律翻译]]
- 实验做了什么：ChatSEO MCP 接入条件核实（Pro €49/月起、OAuth2.1+RFC9728）、六技能规则提取、DIFF GATE 本地复刻三轮实测
- 坑与结论：技能文件免费≠数据服务免费；新域名无权重照样排名 40；"60 天内动过的页不碰"的观察期纪律

## 三、合并建议（不新建，增补已有笔记）
- [[证据优先质检ProofOverClaims]]：增补 DIFF GATE 为"改写域"机械化实例
- [[OAuth资源发现]]：增补 ChatSEO MCP 为 RFC 9728 实战实例
- [[技能路由器与授权硬门]]：增补"人审批上线"为授权硬门实例

## 四、MOC 更新建议
"AI 工具生态"分区增补两条新概念；项目索引加 chatseo_skills。
