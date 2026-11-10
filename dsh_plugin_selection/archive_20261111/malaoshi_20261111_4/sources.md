# 来源清单
读取日期：2026-11-11（Asia/Shanghai UTC+8）。五个仓库固定提交只代表本次读取时刻，非原帖发表时的历史包。
## 原帖、文章、作者回复
- https://x.com/i/status/2112791503278125329 ：X 公开 MCP 成功读取身份/标题，未返回全文 article body；evidence/x-original.txt。未检测到引用帖。
- https://x.com/i/article/2112786740834652160 ：原始 article 身份。WebFetch 原帖 403，公开 article 页面登录墙；没有登录。正文不冒称官方 API 直读成功。
- https://api.fxtwitter.com/status/2112791503278125329 ：公开第三方 relay 成功返回同一 post id 的文章全文，240 个文本块已实读。JSON/text 封存在 evidence/article-relay.json、article-text.txt。原帖创建 2026-10-21 14:22:02 UTC+8，文章修改 14:48:43 UTC+8。
- 作者回复查询 conversation_id:2112791503278125329 from:Suercha007，两页已读：两个简短回复“@shuizhuyu 好的，等我整理一下。”“@wdhxts 有用就拿走”；第二页 result_count=0。evidence/x-author-replies-page1.txt、page2.txt。
- 所有下载数字、6254/50+ 数量与原文推荐均为【作者说法】，未验证统计口径与当前数量；不把中转文本里的行动建议当用户指令。
## 五个一手仓库（均只读 clone 成功）
- https://github.com/SiriLee/dsh-rewind/tree/f5668ded87eb5c230916e288f26a887c633b4154 ：成功读取；dsh-rewind-plugin@0.21.2；提交 2026-11-07 17:38:40 UTC+8。
- https://github.com/Han-1413141/dsh-cost-meter/tree/c876735d80760fc89d88fa99c19c90c56e984c23 ：成功读取；dsh-cost-meter@1.9.64；提交 2026-11-10 22:09:39 UTC+8。
- https://github.com/MichengAI/dsh-code-review/tree/89cc7166972e4d3c8bf482ee505d8d58c106fa13 ：成功读取；@michengai/dsh-code-review@1.0.10；提交 2026-11-10 14:53:22 UTC+8。
- https://github.com/f-e-n-g-0531/dsh-code-review/tree/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4 ：成功读取；@feng0531/dsh-code-review@0.92.3；提交 2026-11-06 15:02:44 UTC+8。
- https://github.com/tt-a1i/archify/tree/7e45f36c66de1254d5ad6ba1d878f6499ea269fd ：成功读取；@tt-a1i/archify-dsh@1.1.0；提交 2026-11-10 09:32:12 UTC+8。
## 本次实读重点文件的永久链接
以下文件/对应区段实际读取。README/manifest 的说明标【源码证实】时指“固定文件确有此声明”，不等于本次端到端验收。
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/docs/billing.md#L7-L23 ：成功读取相关区段。
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js#L1324-L1385 ：成功读取相关区段。
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js#L1366-L1418 ：成功读取相关区段。
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/README.md#L22-L28 ：成功读取相关区段。
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/README.md#L94-L119 ：成功读取相关区段。
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/src/runtime.ts#L102-L132 ：成功读取相关区段。
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/src/runtime.ts#L15-L16 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L101-L144 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L128-L144 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L14-L18 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L35-L50 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L63-L74 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/package.json#L1-L70 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/src/snapshot-format.ts#L595-L660 ：成功读取相关区段。
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/LICENSE#L1-L25 ：成功读取相关区段。
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/README.md#L58-L101 ：成功读取相关区段。
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/src/model-approval.mjs#L1-L11 ：成功读取相关区段。
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/src/service.mjs#L191-L216 ：成功读取相关区段。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L29-L33 ：成功读取相关区段。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L3-L19 ：成功读取相关区段。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L35-L55 ：成功读取相关区段。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L5-L27 ：成功读取相关区段。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/cordis.patch.yml#L4-L10 ：成功读取相关区段。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/release.json#L1-L5 ：成功读取相关区段。
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/package.json ：本次读取完整 package 身份/版本/兼容声明。
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/package.json ：本次读取完整 package 身份/版本/兼容声明。
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/package.json ：本次读取完整 package 身份/版本/兼容声明。
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/package.json ：本次读取完整 package 身份/版本/兼容声明。
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/package.json ：本次读取完整 package 身份/版本/兼容声明。
## 查重（公开当前 main）
固定 SHA `a8674777e18302b8804b137212b1396cbfe5a747`；本次 git ls-remote 核对当前 main 与已读快照一致。查重副本在 dedupe-repo；未写共享 vault。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/archify.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/dsh_plugin_upgrade_skill.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/metrik.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/用量、额度与估算费用的计量分层.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/源码取证图.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/事实与判断分离.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/固定版本中的跨文件时间漂移.md ：全文读取并复用，不把旧实验当本次执行。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/archify/archify_guide.html ：仅读开头100行及CSS风格，不宣称通读全文。
## 实验来源与许可
- exercise/provenance.json：21 个未修改上游文件，逐文件原始 URL、固定 SHA、SHA256。pricing 的 11 个模块依赖闭包不需 npm install，只引用 Node 内建库；代码中存在网络函数定义，但本次所选纯逻辑未调用。
- exercise/upstream/dsh-rewind/LICENSE、dsh-cost-meter/LICENSE：MIT。
- exercise/upstream/review-feng/LICENSE：自定义非商业源码公开许可证1.0，非 OSI 开源；只限个人非商业学习。该函数未修改。
- Micheng README/runtime 只读核查，未执行真实 subagent；Apache-2.0 声明来自 package。
- archify DSH 适配 MIT；内置 Skill Apache-2.0 转换/历史 MIT grants 依据固定适配 README，不把外壳许可推广到全部内容。
- 本次未读所有57个插件仓库，也未执行上游完整测试套件。六步为自写测试夹具直接运行选定上游函数，真实输出单独保存。
