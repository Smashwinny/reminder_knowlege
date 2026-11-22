# 资金操作四步纪律（练习交付物）

> 源自 okx/agent-skills SKILL.md 静态审计（2026-10-28）。适用于一切 agent 触达资金的场景。

## ① 授权模式二选一，绝不混用
- OAuth：隐式 profile，**无 demo 字段；省略 --demo = 实盘（默认！）**
- API Key：显式 profile，demo/simulated 在创建时选死
- 先 `config show --json` + `auth status --json` 亲查，不采信上游结论

## ② 写操作逐项确认（确认矩阵）
- 下单前确认：instId/side/ordType/sz(+下单模式 quote_ccy vs margin)
- 合约先核 ctVal 面值，报"X 张 ≈ $Y"再确认
- 改杠杆前报对现有仓位的影响

## ③ 执行后回读对账
- 读命令（orders/positions/fills）立即执行不受限
- 回执 ≠ 成交：看 fills 与账单，不只看出单回执

## ④ 红线不自动处置
- 需要撤单/停机/平仓才能继续时：呈报发现，人决定
- agent 的默认姿态=呈现选项，不是替你做主

## 审计留痕三问（每个资金动作后自问）
① 当时处于实盘还是模拟？② 谁确认了写参数（记录原文）？③ 回读数据与预期差多少？

## 2026-11-22 审核增补

固定 commit `0ea4378`。`audit_preflight.py` 用合成 config/auth status 验证：未登录 site=global 是占位、API key 优先、OAuth 默认 live、`--demo` 才 demo；9 项测试通过。没有连接账户、运行 CLI 或执行任何资金操作。提示词中的 guard 描述不等于底层机制已通过审计。
