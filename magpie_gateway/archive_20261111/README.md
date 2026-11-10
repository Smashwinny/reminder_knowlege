# Magpie 网关：协议统一不等于权限统一：2026-11-11 收尾归档

本页汇总机器人停止学习前已经产出的材料。归档检查不等于重新完成真实服务、硬件或生产环境验证；请以各项限制及原始实验日志为准。

原始交付包已在本地保留；公开目录仅收录经筛选的教材、原创练习、来源说明和必要结果。第三方完整源码、抓取全文及重复压缩包不随本次提交发布。

## 陈娇 · Magpie 网关：协议统一不等于权限统一

- 来源：[https://x.com/i/status/2106599213379309749](https://x.com/i/status/2106599213379309749)
- 归档状态：**待验证（离线实验材料）**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 部分练习读取被排除的上游/来源快照；仅归档自写代码与日志，复跑需按sources和原README另取固定版本依赖，未声称清理版可直接完整复跑。
- ## 未验证边界 待验证：Magpie 编译、运行、订阅/模型、协议转换、流式、真实预算和 Web 权限。没有启动 Magpie、读取凭据、改 Agent 配置或改收费/安全设置。 
- 公开清理版的依赖恢复范围详见 ARCHIVE_DEPENDENCIES.md；原版 README 对自带源码/快照的说明仅适用于本机保留的原包。

阅读与实验入口：

- [experiment-log.md](chenjiao_2_13/experiment-log.md)
- [guide.html](chenjiao_2_13/guide.html)
- [guide.pdf](chenjiao_2_13/guide.pdf)
- [knowledge-proposal.md](chenjiao_2_13/knowledge-proposal.md)
- [sources.md](chenjiao_2_13/sources.md)

其余原创练习文件见 [chenjiao_2_13](chenjiao_2_13/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 马老师 · magpie 本地网关 学转接与验证，不碰订阅反代

- 来源：[https://x.com/vincemask/status/2112506002193141950](https://x.com/vincemask/status/2112506002193141950)
- 归档状态：**离线/组件实验已交付，真实集成待验证**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 部分练习读取被排除的上游/来源快照；仅归档自写代码与日志，复跑需按sources和原README另取固定版本依赖，未声称清理版可直接完整复跑。
- 旧STATUS.md为初次限额时状态，最终带前缀STATUS及实验日志覆盖；统一归档说明必须记录该修订。
- ## 研究阶段失败记录 - 首次使用 `python` 提取网页：`python: command not found`，退出127；使用 `python3`重跑成功。 - WebFetch原帖403，随后普通公开curl200，正文实际可读。 - Kiro /terms-of-service/ 404；/docs/cli/acp/ 403，未作为已读政策证据。 - 上述为工具返回的真实失败，不是额度耗尽提示；本worker没有收到可引用的“配额耗尽”原文。 
- ## 验证边界 这是真HTTP往返，但不是模型推理。没有运行SSE/工具、多模态、缓存、产品GUI、真实账户端点或性能评测。安全边界是本练习的固定回环地址与不读凭证设计，不是操作系统级网络隔离或完整生产安全保证。 
- ## 读取经过 / 限制 - 原帖：X公开工具成功返回文章标题；WebFetch 403；公开curl 200，BeautifulSoup提取完整正文。未登录。 - 作者回复：公开X search_posts_all 两页，第一页面19个对象（18回复+原帖），第二页 result_count=0，无后续token；不宣称所有网友评论读全。 - 原帖没有referenced_tweets引用对象；实际读取长文内相关项目和FAQ链接。 - https://kiro.dev/terms-of-service/ 返回404：不是有效条款证据。 - https://kiro.dev/docs/cli/acp/ 返回403：不据此称不存在；替代路径的许可依据仅FAQ。 - https://aws.amazon.com/terms/ 成功：Site Terms不是本次禁止反代判断的直接依据。 - 未clone或运行仓库：按环境源代码访问规则使用公开API固定HEAD、文件树及raw源码快照；无checkout、提交、push或私有授权。用户请求的只读追溯目标已用SHA permalink实现。 - 旧风格参考：旧仓库agent_desktop指南（本批既有公开缓存）；主要复用视觉结构，不复用它的实验结论。 
- 真实完成：公开研究与离线mock范围；HTML、9页A4 PDF逐页检查、exercise.zip、真实日志、knowledge-proposal、sources及delivery.zip齐全。待验证：真实magpie/Kiro/Claude集成、模型效果、SSE/工具/多模态/实际额度（本次明确不执行）。
- 公开清理版的依赖恢复范围详见 ARCHIVE_DEPENDENCIES.md；原版 README 对自带源码/快照的说明仅适用于本机保留的原包。

阅读与实验入口：

- [ma-laoshi-20261111-experiment-log.md](malaoshi_20261111_6/ma-laoshi-20261111-experiment-log.md)
- [ma-laoshi-20261111-index.html](malaoshi_20261111_6/ma-laoshi-20261111-index.html)
- [ma-laoshi-20261111-knowledge-proposal.md](malaoshi_20261111_6/ma-laoshi-20261111-knowledge-proposal.md)
- [ma-laoshi-20261111-magpie-gateway.pdf](malaoshi_20261111_6/ma-laoshi-20261111-magpie-gateway.pdf)
- [ma-laoshi-20261111-sources.md](malaoshi_20261111_6/ma-laoshi-20261111-sources.md)

其余原创练习文件见 [malaoshi_20261111_6](malaoshi_20261111_6/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 整理说明

同一项目的不同机器人材料按子目录保留，来源与状态逐项记录；内容相近并不等于证据相同。需要原始网页快照或固定版本上游依赖的练习，在取得公开来源后才能重跑，本轮没有为补齐归档启动实验。
