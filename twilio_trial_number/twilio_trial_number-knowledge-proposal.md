# 知识入库提案 · twilio_trial_number

- 任务：df222942-997b-4ebc-be4a-952cc5535c79
- worker：kimi-pool-20261007-w1（2026-10-07）
- 查重范围：`vault/概念/`、`vault/项目笔记/`（grep 邮件路由/ Twilio / 试用号 / CPaaS 无同义条目；[[项目笔记/cloudflare_email_routing]] 为本系列姊妹篇）

## 提案 1：新建项目笔记（worker 已按裁定直接新建）

`vault/项目笔记/twilio_trial_number.md` —— 已写入：机制（额度/试用号分配/验证 recipient/模板/地理/30 天）、实测（9/9 断言）、五条隐藏条款、耗材思维、与 cloudflare_email_routing 的接收端组合。

## 提案 2：新建概念（请协调者终审合并）

**文件名**：`vault/概念/免费层额度墙设计.md`

**一句话**：SaaS 免费试用层的额度墙通常同时卡在五个维度——数量（各产品固定量）、对象（已验证 recipient 上限）、内容（仅官方模板）、地理（限注册国）、时间（30 天过期）——Twilio 试用号是五维齐全的标准样本。

**正文要点**：
- 五维额度墙拆解（Twilio 实例数字）；防滥用核心机制 = 验证 recipient 列表；CPaaS 四层模型（号码/额度/模板/合规）。
- 反模式：把试用号当长期资产绑定重要账户；只看"免费额度"数字不看维度；用试用号做营销发送（直接撞 A2P 合规墙）。
- 链接：`[[项目笔记/twilio_trial_number]]`、`[[项目笔记/cloudflare_email_routing]]`、`[[证据优先质检ProofOverClaims]]`

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 twilio_trial_number（worker 不动总览）。
