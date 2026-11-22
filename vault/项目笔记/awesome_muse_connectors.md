---
tags: [项目笔记]
类别: 开源项目类（工具目录审计）
来源项目: awesome_muse_connectors
完成日期: 2026-11-22
---

# awesome_muse_connectors：固定目录五段静态审计

## 项目是什么

Anil-matcha/awesome-muse-connectors 是独立社区 Muse 连接器目录，不是 Meta 审核商店。固定 commit 0ffbcc0 全量扫描结构与成熟度，未执行连接器。

## 来源核实

- 固定目录：https://github.com/Anil-matcha/awesome-muse-connectors/commit/0ffbcc02876c6fc1e3cc25c9f46356c49a7f11bf
- Meta 自定义连接器说明：https://www.meta.com/help/artificial-intelligence/1687253048996149/
- 原帖：https://x.com/0xlangeai

159 个 SKILL.md 含 `_template`，实际 158 个连接器+1 模板；154 Draft、4 个特定命令 Live-tested。Cohesivity 才是 2026-10-04 实测例，初日志误记 fal.ai 已纠正；fal.ai 当前固定文件仍为 Draft。

## 带来的概念

- [[连接器五段审查法]]：Auth/Hosts/Rules/Files/Maturity；结构完整不等于安全或可运行。
- [[四级验证编目法]]：成熟度声明与独立复跑分层。
- [[健康探测三态]]：运行探测与维护者声明互补，不互相替代。

## 实验做了什么

新增 `audit_catalog.py` 输出 `catalog-audit-v2.json`，7 项 unittest 通过。初学期 anthropic 实跑需 Muse 运行时保留为历史证据；本轮不读取凭据或调用 API。

## 坑与结论

- Live-tested 只覆盖所列命令与环境，不证明整个工具。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`awesome_muse_connectors/awesome-muse-connectors-guide.html`；审核版：`awesome_muse_connectors/Awesome-Muse-Connectors-小白指南-v2.pdf`。
