# Cue × OKX Skills · 实验日志（task 7d734b42-782c-4281-a4a3-907c378a7c04）

初跑：2026-10-28；审核修订：2026-11-22。
上游固定 commit：`0ea4378645dfc212e9d58df9fc4ca4446398c9e3`。
边界：未安装/运行 OKX CLI，未连接账户，未下单、撤单、停机或执行任何资金操作。

## 固定文档审计

- `okx-cex-auth/SKILL.md`：Step 0 强制，未登录时 site=global 是默认占位符；登录前必须由用户明确选站点。
- `_shared/preflight.md`：config show 与 auth status 必须合并；API key 优先且不回落 OAuth；OAuth 无 demo 字段，省略 `--demo` 即 live（默认），显式 `--demo` 才模拟。
- 写操作确认矩阵、USDT 的 quote_ccy/margin 区分、合约 ctVal 面值和红线不自动处置按原静态审计保留。
- 文档提到部分 CLI guard，但本轮未审计 CLI 实现；不能把提示词纪律或文档引用的 guard 当已验证机制硬门，也不证明跨账户链原子性。

## 修订后的合成实验

新增 `audit_preflight.py`，把文档决策表实现为独立函数：

- `selected_site`：只有 profile 非空 site，或 logged_in/pending 的 auth site 才算选择；not_logged_in 的 global 返回 None。
- `detect_auth`：任何非空 API key 优先，禁止再开 OAuth；logged_in 用 OAuth，pending 等待，未登录加载 auth skill。
- `oauth_trading_mode`：默认 live，demo=True 才 demo。
- `validate_order`：核心参数与 USDT 的 quote_ccy/margin 必须显式确认。

实际命令：

```bash
python -I cue_okx_skills/exercise/audit_preflight.py
python -I cue_okx_skills/exercise/test_audit_preflight.py
```

主程序断言通过，新增 `preflight-audit-v2.json`；9 项 unittest 全部通过。所有输入为合成，未使用真实凭据或资金数据。

## 边界修订

初稿“全部纪律只在提示词层”“最佳商业实现”等过强表述已改为固定文档与待验证机制分层。成交、盈利、最优路径和十秒成交均不当作已核实事实。

## PDF

修订 HTML 后新增 v2 PDF，共 8 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `f0abd1c45d5cdcd4ab8ccc7829d8993cd53d23cad7ade126d39a8dd9e33f39f1`。
