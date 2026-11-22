---
tags: [项目笔记]
类别: 开源项目类（交易所技能包审计）
来源项目: cue_okx_skills
完成日期: 2026-11-22
---

# cue_okx_skills：固定预检文档与合成资金安全模型

## 项目是什么

审计 okx/agent-skills 在 Cue 类 Agent 中的授权、确认、回读与红线纪律；学习对象是交易所 Earn/资金/交易账户，不是链上钱包。未连接账户或执行资金操作。

## 来源核实

- 上游：https://github.com/okx/agent-skills
- 固定 commit：https://github.com/okx/agent-skills/commit/0ea4378645dfc212e9d58df9fc4ca4446398c9e3
- 原帖：https://x.com/AYi_AInotes/status/2105250949706977401

固定文档确认 Step 0、未登录 site 占位、API key 优先、OAuth 默认 live、写参数/USDT 模式与红线不自动处置。提示词和文档 guard 不等于底层机制已验证。

## 带来的概念

- [[资金操作四步纪律]]：授权/确认/回读/红线。
- [[默认姿态审计]]：默认实盘与占位符需先查清。
- [[技能路由器与授权硬门]]：文档要求与机制硬门分层。

## 实验做了什么

新增合成 `audit_preflight.py`：未登录 global 不算选择，API key 优先，OAuth 默认 live，pending 不新登录，写参数与 USDT 模式 fail-closed。9 项 unittest 全部通过，未用真实凭据。

## 坑与结论

- 未验证 CLI 硬门、fills、链路原子性、真实成交或盈利。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`cue_okx_skills/cue-okx-guide.html`；审核版：`cue_okx_skills/Cue-OKX-Skills-小白指南-v2.pdf`。
