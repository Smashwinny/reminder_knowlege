# 知识入库提案 · cloudflare_email_routing

- 任务：f1fad58a-1241-48e4-8fd2-498786c6a24c
- worker：kimi-pool-20261007-w1（2026-10-07）
- 查重范围：`vault/概念/`、`vault/项目笔记/`（只读，grep 邮件路由/MX/catch-all/别名邮箱 = 0 命中）

## 查重结果

无既有 Cloudflare/邮件路由/MX/SPF/别名邮箱条目。可关联的已有概念：[[负载均衡与反向代理]]、[[缓存有效期与发布边界]]（CDN 基础设施品味区）、[[证据优先质检ProofOverClaims]]（对"权重高"口号的态度）。

## 提案 1：新建项目笔记（worker 已按裁定直接新建）

`vault/项目笔记/cloudflare_email_routing.md` —— 已写入，内容：机制（MX 接收入站→规则匹配→转发已验证目标）、三种 action、匹配优先级（精确→+tag 回退→catch-all）、200/200/25MiB 上限、不能与外部 MX 共存、转发≠托管的边界、实验结论与来源。

## 提案 2：新建概念（请协调者终审合并）

**文件名**：`vault/概念/邮件路由与无限别名.md`

**一句话**：把自有域名的入站邮件交给 Cloudflare 免费转发器，用"别名规则 + catch-all 兜底 + 单别名 drop"实现无限收件别名——转发器不是邮箱托管，只能收不能发。

**正文要点**：
- 三件套：custom address 规则（200/域名）、catch-all 兜底（接拼错地址）、destination address 验证（200/账户，未验证则规则禁用）。
- 匹配优先级（实验 13 断言验证）：完整 local part 精确 > RFC 5233 subaddressing 回退（user+tag→user，+tag 保留）> catch-all；同 pattern 多条仅首条生效。
- 动作三选一：转发到邮箱 / 交给 Worker 编程处理 / drop（删除不路由）。
- 边界：MX 必须指向 CF、不能与外部邮件服务器共存；SPF 需合并且查询≤10；入站 25 MiB；出站发送是另一项 Beta 付费能力（Email Sending）。
- 反模式：把它当邮箱托管试图对外发信；把"域名邮箱权重高"当已证事实引用；为薅免费域名把关键身份资产押在促销承诺上。

**链接建议**：`[[项目笔记/cloudflare_email_routing]]`、`[[负载均衡与反向代理]]`、`[[证据优先质检ProofOverClaims]]`

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 cloudflare_email_routing（worker 不动总览）。
