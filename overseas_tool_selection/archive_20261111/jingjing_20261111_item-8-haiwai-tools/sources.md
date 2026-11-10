# 第8项来源清单

读取与实验日期：2026-11-11 Asia/Shanghai（UTC+8）
知识库查重基线：https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
main SHA：`a8674777e18302b8804b137212b1396cbfe5a747`
该提交时间：2026-11-04 17:42:58 Asia/Shanghai（GitHub 原文 `2026-11-04T09:42:58Z`）
查重范围：`vault/00-总览.md` 全文检索（关键词含出海、SEO、本地化、支付、增长工具、Shopify、Stripe 等），以及文件树路径筛查。未声称逐字读完全库。总览没有本帖或「56 个出海工具」的专门项目笔记。`[[付费调用回执与预算熔断]]` 讲模型调用账单，不是支付平台选型。建议互链 `[[证据优先质检ProofOverClaims]]`。

## 一手来源（已实读）

- S1 夏林果帖子 https://x.com/momo_peggy/status/2110301714876346822
  - 作者：夏林果的出海日记 @momo_peggy（用户 id `1952680595332460544`）
  - 发布时间：2026-10-14 17:28:30 Asia/Shanghai（API `2026-10-14T09:28:30.000Z`）
  - 读取方式：X MCP `get_posts_by_ids`（2026-11-11）。短帖 69 字，完整工具清单在 `article.plain_text`，9776 字。文章标题：`靠Web出海赚美刀，7大核心方向精选56个宝藏工具，帮你把想法变成收益`。快照见 `sources/article-plain.txt`。
  - 读取时公开互动：赞 405、回复 82、转帖 48、引用 55、书签 731、展示 75384（之后会变）。
- S2 独立文章链接 https://x.com/i/article/2110257071849603072
  - 出现在 S1 的 entities 中，字段 `status=404`，`unwound_url` 即此地址。
  - 用同一 id 调用 `get_posts_by_ids` 返回 Not Found Error。
  - 2026-11-11 01:22:18 Asia/Shanghai 对同一 URL 做只读 GET：HTTP 状态 200，但最终跳转到 `https://x.com/i/jf/onboarding/web?redirect_after_login=...` 登录引导页。因此不能把这次 200 写成「文章页可匿名打开」。正文仍以 S1 的 `article.plain_text` 为准。
- S3 各工具官方站点（只读探测，不是对产品本身的审核）
  - 探测清单与结果见 `exercise/tools.json`、`exercise/url-probe-results.json`。探测时间：2026-11-11 01:22:18 Asia/Shanghai。
  - 已填官网 57 个地址（Discord 与 Disboard 拆开；原文缺号 14 未探测）。其中 52 个返回成功状态，5 个返回 403（Fiverr、Midjourney、Product Hunt、Toolify、There's An AI For That），按「站点可能存在但本环境被拦截」记录，不写成网站不存在。
  - Customer 的网址按功能推断为 https://customer.io/ ，SiteData 按检索对应 https://sitedata.dev/ ，均已在目录中标明。

## 实际读到的文本边界（以本次 plain_text 为准）

- 七个章节和文末「总结」都完整读到。第 6 章「增长获客与渠道分发」从 Product Hunt（38）读到 Loops（48），并进入第 7 章，不是中途截断。
- 任务摘要里「增长章节中途截断」与本次读到的 9776 字正文不一致，故不采用该摘要作为事实。
- 实际缺陷是编号：缺 14；53（Fiverr）和 54（Adsy）出现在第 2 章 SEO 末尾；第 7 章再次使用 53（Feedlog）并跳到 55（Crisp），没有第二次出现 54。编号条目仍是 56 条，但不是 1 到 56 的干净序列。
- 原文在 Starryblu 条末尾写了推荐码。本批只记录其存在，探测时只用官网根路径，不使用该码，不注册。

## 访问与失败

- S1 正文可读，没有因不可读跳项。S2 不能作为独立可读文章页。
- 没有登录任何工具、没有付款、没有采购外链、没有上传私密记录。
- 封面图等 article.cover_media 未做视觉鉴定。
