# 来源清单
读取日期：2026-11-11（北京时间 Asia/Shanghai）；全部为公开资料。

- 官方远端HEAD与本地clone SHA：b30d54b8aebe6408e02d1473446d25f8083da68f，提交北京时间2026-11-11 00:38。https://github.com/earendil-works/pi/commit/b30d54b8aebe6408e02d1473446d25f8083da68f
- 查重main：a8674777e18302b8804b137212b1396cbfe5a747，已读取vault/00-总览.md、概念/Checkpoint存档与持久执行.md、概念/Compaction上下文压缩算法.md；已查看fast-jev-compaction/fast_jev_guide.html风格。https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
- 原帖全文（成功，note_tweet）：https://x.com/i/status/2112456455123022031 ，北京时间2026-10-20 16:10:41。raw/ma-laoshi-20261111-2112456455123022031.json
- 引用长文（成功，plain_text）：https://x.com/i/status/2109089837097853220 ，北京时间2026-10-11 09:12:56，文中版本1.1.0。raw/ma-laoshi-20261111-2109089837097853220.json
- 原帖回复检索两页成功，末页无结果，无next_token；两条非作者回复，未见作者回复：raw/ma-laoshi-20261111-replies-page*.txt。搜索不等于所有被删/不可见回复均可读。
- 视频未下载观看，长文全部延伸内链未展开，不据此声称读完整个知识网络。
- 旧CLI发布commit：914cf1472e715297caa30db4b9535d534a9eb718；git show读取其package.json，git ls-tree packages/durable为空；既有架构核查报告作为定位线索，结论由依赖声明复核。

## 固定源码链接（均成功实读）
- [包与依赖](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/package.json#L157-L168)
- [核心概念](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/README.md#L92-L104)
- [恢复与提交去重](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/README.md#L115-L138)
- [持久睡眠 / 宿主唤醒](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/README.md#L140-L199)
- [表与索引前缀实现](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/src/storage/sqlite/schema.ts#L47-L61)
- [Node前缀验证](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/src/storage/sqlite/node.ts#L14-L21)
- [baseline选择与前置](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/src/harness/context.ts#L239-L279)
- [当前进度默认值](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/src/harness/agent.ts#L33-L40)
- [close提交延迟状态](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/src/session/session.ts#L779-L810)
- [1.3.0更新](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/CHANGELOG.md#L252-L265)
- [1.4.0睡眠与迁移](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/CHANGELOG.md#L211-L248)
- [1.5.0延迟持久化](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/CHANGELOG.md#L65-L75)
- [1.0.3进度间隔](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/CHANGELOG.md#L351-L366)
- [真实压缩回归断言](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/test/harness-compaction.test.ts#L380-L431)
- [进度丢失与恢复测试](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/test/harness-deferred-progress.test.ts#L99-L219)
- [只注册faux模型](https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/test/chat-support.ts#L41-L75)
- [0.84.2依赖声明](https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/package.json#L42-L83)

## 查重笔记固定链接
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/Checkpoint存档与持久执行.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/Compaction上下文压缩算法.md
