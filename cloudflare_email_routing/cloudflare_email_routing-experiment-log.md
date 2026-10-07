# 实验日志 · Cloudflare Email Routing（cloudflare_email_routing）

- 任务：f1fad58a-1241-48e4-8fd2-498786c6a24c
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 实验位置：`exercise/routing_simulator.py`（纯 Python 标准库）

## 实验设计

Cloudflare Email Routing 是无服务端组件可本地运行的托管服务，真实端到端需要自有域名 + Cloudflare 账户接管 DNS，超出本机条件。因此实验目标改为：<span class="hl">用代码复刻官方文档宣称的路由匹配逻辑，并用断言测试逐条验证</span>——验证"文档行为"本身，如实声明非端到端。

## 依据（全部真实读取，2026-10-07）

- `email-service/configuration/email-routing-addresses/index.md`：destination address 验证流程、三种 action（Send to email / Send to Worker / Drop）、同 pattern 仅列表首条生效、RFC 5233 subaddressing 回退、catch-all 兜底拼错地址、未验证目标→规则禁用。
- `email-service/configuration/domains/index.md`：MX 三条（route1/2/3.mx.cloudflare.net）、SPF `v=spf1 include:_spf.mx.cloudflare.net ~all`、DKIM selector cf2024-1、不能与外部邮件服务器共存、SPF 查询≤10。
- `email-service/platform/limits/index.md`：每域名 200 条路由规则、每账户 200 个 destination、每规则 1 个 action、入站 25 MiB、出站 5 MiB/验证目标 25 MiB、收件人 50、主题 998 字符、头 16 KB。

## 运行记录

`python routing_simulator.py`（exit=0，完整输出 `exercise/run_output.txt`）：

- **13/13 断言通过**，逐条对应文档行为：T1 精确优先于 catch-all；T2 无匹配拒收；T3 catch-all 接拼错 local part；T4 `user+tag@` 回退匹配 `user@`（+tag 保留）；T5 `user+tag@` 有字面规则时字面规则优先；T6 同 pattern 首条生效；T7 未验证目标→规则禁用且拒收；T8 禁用后 catch-all 兜底；T9 drop 优先于 catch-all；T10 26 MiB 拒收；T11 25 MiB 边界放行；T12 Worker 接管；T13 非本域名拒收。
- 演示场景（复刻原帖用法）：5 条规则（support/register 显式转发、billing、hi@ drop、catch-all 归档），5 个测试收件地址判决全部符合预期。
- 边界诚实声明：未验证项 = 真实 DNS 生效时间（官方称 5–15 分钟传播）、Dashboard UI 实际行为、Northwest 促销时效（引用推文作者 8 天实测，属第三方主张）。

## 结论

官方文档的匹配逻辑可被无歧义复刻为 131 行代码并通过全部断言；"无限邮箱"= catch-all + 200 规则上限 + 200 目标上限的免费转发器，不能发信（出站是另一项 Beta 付费能力）。原帖".com 权重高"无可核对证据，按待证主张处理。

## 产物

- `exercise/routing_simulator.py`、`exercise/run_output.txt`
