# 第6项来源与阅读范围
2026-11-11 Asia/Shanghai；公开资料，原帖文字及引用已完整实读。
- https://x.com/ai_xiaomu/status/2110570608375497107 ：原帖2026-10-15 11:17:00 Asia/Shanghai，仅推荐。
- https://x.com/CrazyKaomei/status/2110554196953170106 ：引用2026-10-15 10:11:47 Asia/Shanghai，note_tweet完整文字；6天12条近3万粉、40万赞均未独立核验，原视频未观看。
- 保存X MCP响应：research/x-original-and-quotes.txt、x-quote-direct.txt；返回ID核对后的最小原文保存source-post.json。旧同名JSON实际为别帖，已隔离history，不入包。引用没有提供软件/代码，本实验是独立方法验证，不冒称作者模板复刻。

## 去重与实现基线
- https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747 ，本批已读vault/00-总览.md快照；本轮复读React逐帧视频渲染、动效描述词表、ai-video-pipeline三笔记。只补新增知识。
- 本批第4项experiment-log.md与源码；第5项knowledge-proposal.md：不重做已有静音Remotion/Canvas门禁概念。
- https://github.com/remotion-dev/remotion/tree/e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d ，沿用第4项固定源码与4.0.542依赖。本轮读取Sequence文档1–120行及LICENSE全文；没有声称审计整个仓库。固定文件packages/docs/docs/sequence.mdx说明Sequence的局部帧时间；安装包版本由锁文件固定，不把main文档当二进制实测。
- https://ffmpeg.org/ffmpeg.html#Stream-selection ，本轮实读Streamcopy与手动流选择部分，确认-map与-c:v copy语义（2026-11-11）。实际工具行为由ffprobe与流哈希验证。

## 实测环境/许可
Node24.22.1、npm11.21.1、Remotion4.0.542、React19.1.0、TS5.9.3、Chrome=/usr/bin/google-chrome；复用现有依赖，无额外API/密钥或安全设置改变。WeasyPrint70.0（既有item04隔离环境）实际打印PDF。
Remotion采用自己的许可，本次非商业评估；不是MIT。文案/合成器由worker自写，音频为正弦及衰减，无外部录音/歌曲/人声。未给出商业音乐权利保证或人工听感评分。
