# Awesome Muse Connectors · 实验日志（task 11a3d01a-eed7-4af0-bf68-70e5822927e9）

初跑：2026-10-28；审核修订：2026-11-22。
上游固定 commit：`0ffbcc02876c6fc1e3cc25c9f46356c49a7f11bf`。
边界：无 Muse 运行时；本轮不执行任何连接器、不读取凭据、不调用真实 API。

## 初日志问题

1. 159 个 `SKILL.md` 被全部称为连接器，实际包含 `_template`；应为 158 个连接器条目+1 个模板。
2. 初日志把 Cohesivity 的 2026-10-04 init/auth/status/provision 实测记成 fal.ai。固定文件中 Cohesivity 才是 Live-tested，fal.ai 第 47 行仍为 Draft。
3. “Live-tested=工具/已验证”过宽，标签只覆盖条目列出的具体命令和环境，不证明整个连接器、所有参数或当前兼容性。
4. 健康探测三态与维护者成熟度声明被混为一谈，前者是运行观察，后者是目录自述。

## 修订后的静态审计

新增 `audit_catalog.py`，只读取 `repo/connectors/*/SKILL.md` 的五段结构和 Maturity，不复制 Auth 正文、主机、脚本或任何敏感内容。输出 `catalog-audit-v2.json`。

实际命令：

```bash
python -I awesome_muse_connectors/exercise/audit_catalog.py
python -I awesome_muse_connectors/exercise/test_audit_catalog.py
```

结果：

- SKILL.md 159；连接器条目 158；五段结构完整 159。
- Draft 154；Live-tested specific commands 4：Cohesivity、Lodestone、Mushare、Slack。
- `_template` 单独标为 template，不计入连接器。
- 7 项 unittest 全部通过：总数、模板排除、anthropic 五段/Draft、Draft 多数、缺失成熟度、Live 标签范围、记录不复制敏感正文。

初学期 anthropic 实跑曾报需要 Muse 动态凭证助手，保留为“文案不能独立运行”的历史证据；本轮未重复执行。

## 审查框架与边界

Auth / catalog_hosts / Operating Rules / Files / Maturity 五段可用于安装前审查，但结构完整不等于安全或兼容。官方 Meta 自定义连接器不审核声明、目录独立社区定位与初学期来源说明保留；来源历史 commit 6e31fd44 与本次审计 commit 0ffbcc0 分开。

## PDF

修订 HTML 后新增 v2 PDF，共 8 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `38048fb9bda463c12963d87e619c2d514990b88e510384e7d6d39b2e7d0098cd`。
