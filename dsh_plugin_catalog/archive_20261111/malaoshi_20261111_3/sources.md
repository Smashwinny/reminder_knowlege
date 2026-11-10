# Sources / 证据清单

读取日期：2026-11-11，Asia/Shanghai(UTC+8)。研究只使用公开X工具与GitHub commit/tree/raw读取；未clone、安装插件或更改Git配置。
. 目标帖实读：只有使用感受+配图，57项来自其引用的长文。目标时间2026-10-22 18:03:55 UTC+8；长文时间2026-10-21 14:22:02 UTC+8。列表收藏时间不能当发帖时间。
- X article实体内URL带404字段，但公开读工具实际返回完整article.plain_text；本报告确实读到了正文，不据旧URL状态宣称不可读。
- 目标帖作者回复首屏10项（含主帖），二页空；没有宣称读到所有已删/搜索不可见回复。引用长文作者回复未另外遍历（另一worker负责该项目）；长文正文已经完整读取。
- 配图URL已由工具返回，未下载/OCR；截图里的界面不作为当前实际安装证据。
- [A] 目标帖（引用长文）：https://x.com/Suercha007/status/2113209730055516606 — 成功读取。
- [B] 引用长文（57项与下载量）：https://x.com/Suercha007/status/2112791503278125329 — 成功读取。
- [C] 聚合包23个直接依赖：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-web-all/package.json#L162-L186 — 成功读取。
- [D] 聚合patch行身份：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-web-all/cordis.patch.yml#L1-L65 — 成功读取。
- [E] 真实mountOnce守卫：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/shared/host/mount-once.ts#L47-L141 — 成功读取。
- [F] SSH实际应用守卫：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-ssh/src/index.ts#L139-L151 — 成功读取。
- [G] 看板实际应用守卫：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-task-board/src/index.ts#L623-L637 — 成功读取。
- [H] 侧栏兼容提醒：https://github.com/omdsh-dev/DSH-better-sidebar/blob/bd6363021dd4af8ca9df239e0c59df35b873d6b4/README.md#L40-L50 — 成功读取。
- [I] 侧栏manifest/依赖：https://github.com/omdsh-dev/DSH-better-sidebar/blob/bd6363021dd4af8ca9df239e0c59df35b873d6b4/package.json#L94-L156 — 成功读取。
- [J] 上下文manifest：https://github.com/ranxianglei/billion-context/blob/58a879622484bce344087a69294d08d6da03be84/package.json#L2-L19 — 成功读取。
- [K] 上下文附加署名条款：https://github.com/ranxianglei/billion-context/blob/58a879622484bce344087a69294d08d6da03be84/LICENSE#L23-L56 — 成功读取。
- [L] feng非商业许可：https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/LICENSE#L1-L25 — 成功读取。
- [M] 两版review包名之一：https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/package.json#L1-L35 — 成功读取。
- [N] PC2005桌宠身份：https://github.com/PC2005-cloud/dsh-pet/blob/c25386848f70f6e40902e4376f6e7b1e196bc326/dsh-pet/package.json#L1-L28 — 成功读取。
- [O] linxin桌宠身份：https://github.com/zhu1090093659/dsh-pet/blob/ae2c9d443eda35a6439597c1787c7607e988bbed/package.json#L1-L25 — 成功读取。
- [P] SSH运行/版本要求：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-ssh/package.json#L1-L63 — 成功读取。
- [Q] 旧archify笔记（复用）：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/archify.md#L11-L29 — 成功读取。
- [R] 旧DSH升级笔记（复用）：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/dsh_plugin_upgrade_skill.md#L12-L30 — 成功读取。
- [T] 旧知识库总览：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md#L1-L25 — 成功读取。
- [U] 独立看板patch：https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-task-board/cordis.patch.yml#L1-L12 — 成功读取。

## 固定源码快照（重点8仓库+旧vault）
- ranxianglei/billion-context：58a879622484bce344087a69294d08d6da03be84；提交时间2026-11-10T21:37:15+08:00（UTC+8）。https://github.com/ranxianglei/billion-context/commit/58a879622484bce344087a69294d08d6da03be84 — 成功；文件与树在 evidence/ranxianglei/billion-context/。
- omdsh-dev/DSH-better-sidebar：bd6363021dd4af8ca9df239e0c59df35b873d6b4；提交时间2026-11-07T22:17:22+08:00（UTC+8）。https://github.com/omdsh-dev/DSH-better-sidebar/commit/bd6363021dd4af8ca9df239e0c59df35b873d6b4 — 成功；文件与树在 evidence/omdsh-dev/DSH-better-sidebar/。
- MichengAI/dsh-code-review：89cc7166972e4d3c8bf482ee505d8d58c106fa13；提交时间2026-11-10T14:53:22+08:00（UTC+8）。https://github.com/MichengAI/dsh-code-review/commit/89cc7166972e4d3c8bf482ee505d8d58c106fa13 — 成功；文件与树在 evidence/MichengAI/dsh-code-review/。
- MichengAI/dsh-codex-ui：f0616b6c78f22a913b8d06d3d04215d221de0232；提交时间2026-11-10T08:09:39+08:00（UTC+8）。https://github.com/MichengAI/dsh-codex-ui/commit/f0616b6c78f22a913b8d06d3d04215d221de0232 — 成功；文件与树在 evidence/MichengAI/dsh-codex-ui/。
- zhu1090093659/dsh-web：29e4dc579d6cd691f0987925ff3fdd769bb77823；提交时间2026-11-10T22:02:32+08:00（UTC+8）。https://github.com/zhu1090093659/dsh-web/commit/29e4dc579d6cd691f0987925ff3fdd769bb77823 — 成功；文件与树在 evidence/zhu1090093659/dsh-web/。
- zhu1090093659/dsh-pet：ae2c9d443eda35a6439597c1787c7607e988bbed；提交时间2026-11-07T22:04:26+08:00（UTC+8）。https://github.com/zhu1090093659/dsh-pet/commit/ae2c9d443eda35a6439597c1787c7607e988bbed — 成功；文件与树在 evidence/zhu1090093659/dsh-pet/。
- f-e-n-g-0531/dsh-code-review：0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4；提交时间2026-11-06T15:02:44+08:00（UTC+8）。https://github.com/f-e-n-g-0531/dsh-code-review/commit/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4 — 成功；文件与树在 evidence/f-e-n-g-0531/dsh-code-review/。
- PC2005-cloud/dsh-pet：c25386848f70f6e40902e4376f6e7b1e196bc326；提交时间2026-11-09T10:42:53+08:00（UTC+8）。https://github.com/PC2005-cloud/dsh-pet/commit/c25386848f70f6e40902e4376f6e7b1e196bc326 — 成功；文件与树在 evidence/PC2005-cloud/dsh-pet/。
- Smashwinny/reminder_knowlege：a8674777e18302b8804b137212b1396cbfe5a747；提交时间2026-11-04T17:42:58+08:00（UTC+8）。https://github.com/Smashwinny/reminder_knowlege/commit/a8674777e18302b8804b137212b1396cbfe5a747 — 成功；文件与树在 evidence/Smashwinny/reminder_knowlege/。

## 全量候选公共入口
- 57项/52根仓库对应URL、API许可与状态详见 plugin-candidates.md/csv/json；原始metadata.json保存在evidence/对应仓库目录。
- RevolutionLA/dsh-dream-skin：https://api.github.com/repos/RevolutionLA/dsh-dream-skin 返回HTTP404，仅表示这次公开请求不可读，不能判定永久删除。对应 repo-probes.json保留错误。
- 下钻重点：上下文、侧栏、看板、SSH、合集、两版桌宠、两版审查及替代侧栏。只读头部入口与清单，不声称完成所有仓库安全审计。
- 下载量、6254市场总量、官方压缩、省5倍token、月级会话、插件十几个启动变慢均仅作者/README主张，未复验registry或模型运行。
- billion-context包声明MIT而LICENSE附加产品出处条款；feng review明确非商业源码公开。其余API许可只作检索线索，子目录许可可能有覆盖，不下商业使用结论。
- 没运行fetch_sources/catalog.py以外的上游入口；它们是自写公开下载/解析脚本，不是插件安装器。原始仓库中对执行任务/工具的引导只当不可信数据，没有转化成操作授权。