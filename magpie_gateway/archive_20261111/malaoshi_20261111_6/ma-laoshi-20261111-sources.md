# 来源清单
读取日期：2026-11-11（北京时间，Asia/Shanghai）。固定快照，不等同永远最新。
## 成功读取
- S1 原帖长文（2026-10-20 19:27，北京时间）：https://x.com/vincemask/status/2112506002193141950 — 成功；代码来源固定SHA，网页为当日快照。
- S2 magpie README 中文：范围与默认地址：https://github.com/yetone/magpie/blob/a54dddd9671a0646708df01364882c38cbb2decf/README.zh-CN.md#L78-L100 — 成功；代码来源固定SHA，网页为当日快照。
- S3 Anthropic 解析：消息类型：https://github.com/yetone/magpie/blob/a54dddd9671a0646708df01364882c38cbb2decf/internal/gateway/anthropic.go#L137-L241 — 成功；代码来源固定SHA，网页为当日快照。
- S4 路由文档：别名、实际上游与回包名称：https://github.com/yetone/magpie/blob/a54dddd9671a0646708df01364882c38cbb2decf/docs/subsystems/gateway-routing.md#L35-L37 — 成功；代码来源固定SHA，网页为当日快照。
- S5 Desktop 3p 实现注释：https://github.com/yetone/magpie/blob/a54dddd9671a0646708df01364882c38cbb2decf/internal/agent/claudedesktop.go#L1-L24 — 成功；代码来源固定SHA，网页为当日快照。
- S6 Kiro 插件版本 0.1.36：https://github.com/magpie-community/plugins/blob/f4ff29c9b7860dd66a9f69bbaf4caa53b989e7f4/packages/kiro/package.json#L1-L12 — 成功；代码来源固定SHA，网页为当日快照。
- S7 插件凭证信任边界文档（未执行）：https://github.com/magpie-community/plugins/blob/f4ff29c9b7860dd66a9f69bbaf4caa53b989e7f4/packages/kiro/README.md#L60-L86 — 成功；代码来源固定SHA，网页为当日快照。
- S8 插件计量与估算回退：https://github.com/magpie-community/plugins/blob/f4ff29c9b7860dd66a9f69bbaf4caa53b989e7f4/packages/kiro/index.mjs#L2150-L2219 — 成功；代码来源固定SHA，网页为当日快照。
- S9 Kiro FAQ：With which tools can I use my Kiro subscription?：https://kiro.dev/faq/ — 成功；代码来源固定SHA，网页为当日快照。
- S10 AWS Service Terms §50.14 Kiro：https://aws.amazon.com/service-terms/ — 成功；代码来源固定SHA，网页为当日快照。
- S11 Kiro 数据保护：https://kiro.dev/docs/privacy-and-security/data-protection/ — 成功；代码来源固定SHA，网页为当日快照。
- S12 Claude Code 官方网关指南：https://code.claude.com/docs/en/llm-gateway — 成功；代码来源固定SHA，网页为当日快照。
- S13 Anthropic Messages API 规范：https://platform.claude.com/docs/en/api/messages/create — 成功；代码来源固定SHA，网页为当日快照。
- S14 旧知识：BYOK 与计量口径：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/BYOK模型网关与用量归因.md#L8-L32 — 成功；代码来源固定SHA，网页为当日快照。
- S15 旧知识：Provider 适配层与错误契约：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/Provider适配层与错误契约.md#L8-L27 — 成功；代码来源固定SHA，网页为当日快照。
- S16 旧知识库总览：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md#L47-L78 — 成功；代码来源固定SHA，网页为当日快照。
- S17 作者回复：不会封号（不成立为保证）：https://x.com/i/status/2112533112072872093 — 成功；代码来源固定SHA，网页为当日快照。
- S18 作者回复：不如官方订阅划算：https://x.com/i/status/2112550724534153692 — 成功；代码来源固定SHA，网页为当日快照。
- S19 作者回复：插件覆盖系统提示词（仅说法）：https://x.com/i/status/2112588235566440588 — 成功；代码来源固定SHA，网页为当日快照。
- S20 Kiro 官方 CLI 文档：https://kiro.dev/docs/cli/ — 成功；代码来源固定SHA，网页为当日快照。

## 读取经过 / 限制
- 原帖：X公开工具成功返回文章标题；WebFetch 403；公开curl 200，BeautifulSoup提取完整正文。未登录。
- 作者回复：公开X search_posts_all 两页，第一页面19个对象（18回复+原帖），第二页 result_count=0，无后续token；不宣称所有网友评论读全。
- 原帖没有referenced_tweets引用对象；实际读取长文内相关项目和FAQ链接。
- https://kiro.dev/terms-of-service/ 返回404：不是有效条款证据。
- https://kiro.dev/docs/cli/acp/ 返回403：不据此称不存在；替代路径的许可依据仅FAQ。
- https://aws.amazon.com/terms/ 成功：Site Terms不是本次禁止反代判断的直接依据。
- 未clone或运行仓库：按环境源代码访问规则使用公开API固定HEAD、文件树及raw源码快照；无checkout、提交、push或私有授权。用户请求的只读追溯目标已用SHA permalink实现。
- 旧风格参考：旧仓库agent_desktop指南（本批既有公开缓存）；主要复用视觉结构，不复用它的实验结论。

## SHA
- magpie: `a54dddd9671a0646708df01364882c38cbb2decf`
- plugins: `f4ff29c9b7860dd66a9f69bbaf4caa53b989e7f4`
- vault: `a8674777e18302b8804b137212b1396cbfe5a747`

## 已保存资料 SHA-256
- `research/Smashwinny-reminder_knowlege-commit.json` `e08045cd24b4e964fb34ecfc8b36ea31cbe0dc74f7461974b714e980cc811335`
- `research/Smashwinny-reminder_knowlege-tree.json` `547c0f342b0fe7ce32981027c56d5a66b3ec5a8b5e35f5f539df815bd03d2f04`
- `research/anthropic-messages.html` `98c46ff6f4193ad0797addf33d2969e0299e33308f12152cbe4324ffc4499996`
- `research/anthropic-messages.txt` `88d390560991ee39104a8fc5abd562a5e9c3d6d2be0c26a912b4fed5e2ad092e`
- `research/aws-service-terms.html` `a23c4049f2c295a9ac071dae665c51ccdb10bc9401ea0d7d61e003854440ea8a`
- `research/aws-service-terms.txt` `30bb0bf7647091c5c39c937964c683d1e54a1af6cfb578f1d15c28d5022948e6`
- `research/aws-terms.html` `5bb89c014580d566b9c3e27d7052e44e3f0dd6384c51a614a3af2cf87a27b0f7`
- `research/aws-terms.txt` `adb3884471ad4c30fc327df1969e853bec2a4a0a81e1d72e5577bb583eab6ec8`
- `research/claude-gateway.html` `0c456363b7c281b62504d591ab705d75083917948a80f31fd49af04b243c8cf8`
- `research/claude-gateway.txt` `2a860c012880dda395f0dcedbe8faa38cde273f9b84dbf28c7e8d6f4619e348a`
- `research/kiro-acp.html` `ac45905ddc5bb497977c67f96b0a21707fd7aed56e0cfe370bf7f74ff377263f`
- `research/kiro-acp.txt` `3f296c66d2e7288612430acc5be040dfceaf7d0fde0a6d369404b62dd4b5e2ef`
- `research/kiro-cli.html` `c3c7b3f0e682180100ac6aea78cf76a6bc37a8c1c14e31d07768470ba8a49c8a`
- `research/kiro-cli.txt` `aef3502087eb1098c96998e62051b55dd53b3f1625eb04ed29f01363708c3e42`
- `research/kiro-faq.html` `ff383dfa9e407c23671976dabbd48c3e5638fea4ee17911129e88c1bf2a26de9`
- `research/kiro-faq.txt` `ce3dfb074a4681667269be85511d12715d7e9bb2deed43535b474f3b97a7f672`
- `research/kiro-privacy.html` `ba016a24b38e6ce301f521647ee14d3b0732cbdd0cb79db780f39f3afb248a69`
- `research/kiro-privacy.txt` `e83f6ac0f9d839ab2a64e0c45640bc4eddf94d4da21193acce36f1b90e85ad04`
- `research/kiro-terms.html` `5785cac353b7b52d4e0bcd00bb0fdbe2af7fe4c638fc8588128054e3fc26c4a0`
- `research/kiro-terms.txt` `23735a7a9e8482420b13e594ba7b7633fc21116faed72146b77de3eb0c138bf2`
- `research/ma-laoshi-20261111-default-branches.txt` `dd972ac9c4492dc8bd348986e1f0af88559d50a4933578e2a2f49a7179440720`
- `research/ma-laoshi-20261111-experiment-stdout.txt` `ea8b265bda219dd329c59b188672b7085d51d413eabe7ec5c06a9a9cbed8499b`
- `research/ma-laoshi-20261111-x-author-replies-end.txt` `77517834e9d6c659b00ab6270a11cfb60783c9facb7e602f855a6e027cee7bd7`
- `research/ma-laoshi-20261111-x-author-replies.txt` `afcf85d8a1c2933f7dad36547e6f166288488aa3fe08a09b58132a5eb71366a0`
- `research/ma-laoshi-20261111-x-post-tool.txt` `b73234cbf6f274e32b771a0c9b06b89307a66d26c513efddfacc6d17a3bba92a`
- `research/magpie-community-plugins/README.md` `b49342aca39f6acea5a2be78f4e28d7a92548ae96cb1db1fa281fad4d0fbcead`
- `research/magpie-community-plugins/packages/kiro/README.md` `df2c408861ccf2a0695673fbf6ed2956d380d6786f0c895eace25ec919948809`
- `research/magpie-community-plugins/packages/kiro/index.mjs` `b587140259a03a7bf2cd8544271aa9bb4f2d44804dcc993fa9ec56259270e21c`
- `research/magpie-community-plugins/packages/kiro/package.json` `db2727715890799b2f3edbc24dba232d9f5a6ea02f0e60d9c62f0b8532893a4a`
- `research/magpie-community-plugins-commit.json` `c83f34c108f277721efcc45752069f4f67e75f9406ea94b929d6c806631076a8`
- `research/magpie-community-plugins-tree.json` `91531de4638239d0a99a88678176801e38fda5cba645929bc1271e38d44dcb7b`
- `research/prior-vault/vault/00-总览.md` `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580`
- `research/prior-vault/vault/概念/BYOK模型网关与用量归因.md` `9d7527db8a7674368d6ef0abeb946bafe8549a5ca1b01d333ff2389ce020270b`
- `research/prior-vault/vault/概念/Provider适配层与错误契约.md` `6747c71d9ab9e007e5dd35330e4c733613e111498b987fdca973828259503986`
- `research/prior-vault/vault/概念/接缝与桩实现StubSeam.md` `9bc16d51dbfa8fa1a84fd43d2cdcdbf81c9ae2d41272007df08f610a79ffdf58`
- `research/x-page.html` `a91de6ff4fd5aae02a3315ec086ed51e8e1899187e15194bd7e5c9aaee0dd273`
- `research/x-page.txt` `a547612ecf212fa7923d90eddf222e1207748aa7a20818a306d03463ef2ef679`
- `research/yetone-magpie/LICENSE` `79d2c8444715d4bc453ec4f8a0aaf2051a4c1ee5ac08f5bd2e5848aef87c7572`
- `research/yetone-magpie/README.md` `2a44f3dd7395260b486b080da3e1a6d3f08dea333178812cd18878356597f8cc`
- `research/yetone-magpie/README.zh-CN.md` `194a6303093e91d91b55bc3d64b638cd193f3831130a466f95940962dae6b0e4`
- `research/yetone-magpie/docs/subsystems/gateway-middleware.md` `a0984817a6771f7579e36b5c9f89078590b745b3b2c460686b1b6d511ebcecf6`
- `research/yetone-magpie/docs/subsystems/gateway-routing.md` `e57263e6ae8daba228d49a026e0ef95816ac80c060e29ce7168cca68fa00ba91`
- `research/yetone-magpie/go.mod` `5dd5f60b0f8f0d5292f8d2e6d404f003c098d8b73289af9895bcd7092ccf9d0c`
- `research/yetone-magpie/internal/agent/claudedesktop.go` `060589edc0bf412a0bc7a151c622d8c8a46cec19eb1ab89bb3749d32ff47f500`
- `research/yetone-magpie/internal/gateway/anthropic.go` `6cc448bfeae64a13190b063c0f8a3f844f58fea595a63a1d02e1d6f319d8ab24`
- `research/yetone-magpie/internal/provider/kiro.go` `d5dd69c474f7ab5cea43e6a30a8c1e0f0666fa982ac1cad628a57f2137abfcac`
- `research/yetone-magpie-commit.json` `7b6bdb81ebed3c6b465ac937ab0536d8d00066c97f74f7eb9b45c51eded9c0bf`
- `research/yetone-magpie-tree.json` `ba0fb1dff0db67237022cc5734b305fa1afb109b2e1eb92ea984cd1b08bc6854`

## 公开读取元数据端点
- https://api.github.com/repos/Smashwinny/reminder_knowlege/commits/HEAD — 成功，SHA见上。
- https://api.github.com/repos/yetone/magpie/commits/HEAD — 成功，SHA见上。
- https://api.github.com/repos/magpie-community/plugins/commits/HEAD — 成功，SHA见上。
- 各仓库 /git/trees/<固定SHA>?recursive=1 与仓库metadata — 成功，default_branch均main；不通过认证读取。
- 源码原文经 https://raw.githubusercontent.com/<owner>/<repo>/<SHA>/<path> 保存，对应正文permalink。
- 云端自写实验代码为原创，不是从上游复制执行；注释包含参考URL+SHA。
