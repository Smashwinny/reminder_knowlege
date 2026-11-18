# ChatSEO 六技能 · 实验日志（task 2b6b9a2f-5da4-4d5c-b0cb-cbe3930453ce）

实验日期：2026-10-27
性质：方法论学习 + 核心机制本地复刻。未接入 ChatSEO（Pro €49/月起）、未连接 Search Console、未编辑真实页面。
全部练习使用明确标注的示例数据。

## 实验设计

原文（@NicholasDulait《My chief of SEO, claude code opus 5.5》）给出一套 SEO Agent 工作流：
Claude Code 当"SEO 主管"，ChatSEO MCP 当情报层，人审批一切上线操作。
实验回答：①ChatSEO 接入的真实门槛是什么？②六技能里最有复用价值的核心机制是什么？
③能否不花钱在本地验证该机制？

## 步骤与真实输出

### 步骤 1：ChatSEO MCP 接入条件核实（chatseo.app/mcp 直读）

- 端点：`https://api.chatseo.app/mcp`，Streamable HTTP，**OAuth 2.1 + RFC 9728 保护资源元数据**（免贴 Key 自动引导登录）
- 38 个工具：Search Console 读取 / 审核 / 简报 / Shopify 文章发布等
- **门槛：Pro 及以上，€49/月起**；页面无免费试用说明
→ 结论：文章"免费给技能文件"，但**数据服务不免费**；技能规则可学，数据层要另算账。

### 步骤 2：六技能规则提取（FxTwitter 长文镜像逐段读取）

| 技能 | 核心规则 | 本指南关注点 |
|---|---|---|
| money-keywords | 只要商业意图词；top3 是落地页才留；**没量的写 n/a 不编** | 未知数据留空纪律 |
| page-brief | 有 URL 已在获点击→停，改旧页别新建 | 先查已有资产防重建 |
| ship-page | **DIFF GATE**：发布前列出旧版有新版丢的全部元素，草稿/分支先行，人审批 | 核心可复用机制 |
| geo-rankings | "best X 2026"类查询的 AI 引用规划 | 新搜索范式 |
| pattern-drip | 一次一页；只换城市名的页不发 | 反垃圾内容纪律 |
| weekly-seo | 28 天环比；60 天内动过的页不碰；输出 5 个按业务价值排序的动作 | 观察期纪律 |

### 步骤 3：DIFF GATE 本地复刻（核心实验）

作者坦白 DIFF GATE 的由来：**Claude 曾把线上页面的排名表格静默删掉**。这正是
[[证据优先质检ProofOverClaims]] 的 SEO 版——"编译过不算数，上线前 diff 才算数"。

自建示例页面模拟该事故：
- old-page.html：含 `<table id="pricing">` / 表单 / 图片 / 3 个链接
- new-page.html：改写版，**表格被静默删除**（模拟 Agent 翻车）
- `exercise/diff_gate.py`：零依赖复刻闸门规则

实测三轮（全部真实执行）：
```
① python diff_gate.py old-page.html new-page.html
→ ❌ DIFF GATE 拦截：- 表格 pricing   exit=7 ✅ 抓住丢失
② python diff_gate.py old-page.html old-page.html
→ ✅ 通过   exit=0 ✅ 无误报
③ 把表格补回 new-fixed.html 再跑
→ ✅ 通过   exit=0 ✅ 修复后放行
```

### 步骤 4：合规边界核对（Google 搜索垃圾政策）

购买链接、排名交换、无用户价值的大规模生成内容均属垃圾行为；
"每天只发一页"不构成质量或合规保证。pattern-drip 的"只换城市不发"规则与之一致。

## 结论

- 六技能的真实价值在**纪律**不在工具：未知写 n/a、先查旧页、diff 后发布、一次一页、观察期不动——全是确定性规则；
- DIFF GATE 已本地复刻并验证（3/3 符合预期），可平移到任何"AI 改写线上内容"场景；
- ChatSEO 数据层 €49/月起，技能文件免费≠数据免费；
- 未验证：真实排名提升（需站点+数据+观察期，非本实验范围）。

## 产物

- `exercise/diff_gate.py` — DIFF GATE 本地复刻（零依赖）
- `exercise/old-page.html` / `new-page.html` / `new-fixed.html` — 示例页面
- `exercise/experiment-log.md`（本文件）
