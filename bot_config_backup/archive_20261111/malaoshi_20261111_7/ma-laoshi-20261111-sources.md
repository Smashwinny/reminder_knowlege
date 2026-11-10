# 来源账本

读取日期2026-11-11（北京时间 UTC+8）；公开材料，不读真实用户记录。

## S1 原帖
https://x.com/xiangxiang103/status/2110638131720700149

X公开工具成功读到note_tweet；原帖时间2026-10-15 15:45:19（北京时间）；WebFetch返回403。无引用帖字段。

## S2 完整作者提示词
https://x.com/i/status/2110638135642313069

成功读note_tweet；作者回复搜索10条，下一页0条；API搜索不保证覆盖已删/不可见内容。

## S2b 跨账号回复
https://x.com/i/status/2110713635358322803

公开回复成功读取；仅作者说法，未测试。

## S3 GitHub token
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

官方文档成功读取；动态文档按读取日期固定，未取得文档仓库SHA。

## S4 GitHub push protection
https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection

官方文档成功读取；不能假设私有仓库默认受保护。

## S5 GitHub secret scanning
https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning

官方文档成功读取；历史扫描、先轮换与可用计划说明。

## S6 Git官方bare语义
https://github.com/git/git/blob/a52a24e03c8c711f1d5e252fba78f9276908129b/Documentation/git-init.txt#L17-L47

固定Git 2.47.3 peeled commit；ls-remote与raw文档成功。releases/tag/v2.47.3返回404，不作为缺失源码证据。

## S7 查重总览
https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md#L47-L57

当前main通过公开commits页面核实；复用已下载公开快照（不做本地clone，遵循source-control技能），读总览并搜索备份主题，无同题专项笔记。

## S8 复用安全概念
https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/只读闸门三原则.md#L8-L22

成功读取；复用白名单/最小权限/可审计分层思路，不重做原数据库实验。

## S9 复用页面风格
https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/agent_desktop/agent_desktop-小白指南.html

已读公开reference版HTML；复用卡片、鲜艳配色、SVG、问答递进风格；不复用其运行结论。

知识库固定SHA：a8674777e18302b8804b137212b1396cbfe5a747（提交时间2026-11-04 17:42:58 北京时间）。Git v2.47.3源码固定SHA：a52a24e03c8c711f1d5e252fba78f9276908129b。GitHub docs为动态页面，未取得文档仓库SHA，按本次读取日期引用。

证据文件对应：post、author-prompt、author-replies、replies-last-page；X作者回复搜索下一页0条，不保证不可见或被删内容。未读图片附件（结论仅据文字）。
