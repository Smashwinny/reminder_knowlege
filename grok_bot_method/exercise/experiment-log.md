# Grok Bot 方法 · 实验日志（task 310d587b-b014-4ab0-8c33-59f25a733f27）

实验日期：2026-10-27
性质：方法论学习 + 官方文档核验 + 契约样例产出。未创建 Bot、未验证账号资格。

## 步骤与真实输出

### 步骤 1：官方文档直读核验（docs.x.ai，本 session 实时抓取）

**FAQ（docs.x.ai/grok-bot/faq）确认的产品机制：**
- 云电脑**按用户分配不按 Bot**：同账户所有 Bot 共享一台机器——文件、浏览器会话、登录全共享；原文警告 **"Do not use separate Bots as a security boundary"**；
- 后台运行：关掉 App/电脑不中断 background turn 与 routine；
- 协作：多 Bot 可并行，每 Bot 一屏，但"一个 Bot 同时只跑一个 computer-use 任务"；
- **skill vs routine**：skill 是做事方法；routine 是把工作流绑定某 Bot 并定时/事件触发；官方建议"先把 skill 在真实一次性任务上试跑再变 routine"；
- 权限：按工具/动作风险/Auto-review 规则分级审批；密码/2FA/验证码走 computer takeover；
- 模板分享 Bot：暴露配置但不暴露电脑/登录/历史。

**Computers（docs.x.ai/grok-bot/computers）确认：**
- 每个成员一台托管电脑，属于其所有团队；重建/终止影响所有团队；
- 持久盘保留 Bot/文件/登录，自建软件在重建时清除（Team Setup Scripts 恢复的会还原）；
- 企业管理（Enterprise）：Recreate / Terminate / Delete VMs and Data / Delete All Grok Bot Data（输 DELETE 确认、审计日志、每团队同时一个操作）；
- 30 天无使用自动终止休眠机（默认关闭、无宽限）；
- 终止 ≠ 移除访问权限：还需 Manage Group Access + IdP 撤销会话。

### 步骤 2：方法提炼（@distortgeekin 长文，分类阶段已读全文 163 段）

核心方法四件套：① 岗位契约（职责/验收/红线）② 三次试运行 ③ 五次通过才扩大自主 ④ 权限分层 + 交接规则。

### 步骤 3：契约样例产出与符合性检查

为虚构岗位"每日行业情报员"编写完整契约（`exercise/sample-job-contract.md`），
并对照官方文档做 6 项安全符合性检查：全部通过（不以 Bot 为安全边界 / 先问规则覆盖
send-publish-delete-purchase / 登录走接管 / routine 前试跑 / 重大决策查当前来源 / 屏幕≠隔离）。

## 结论

- "雇 AI 员工"的关键不是配置而是**契约化**：职责三条可验收、红线明确、失败定义具体；
- 最重要的安全认知（官方原文）：**同账户 Bot 共享一台云电脑，屏幕不是隔离边界**；
- skill→routine 的"先真任务试跑"与三次试运行+五次通过，是同一纪律的两个尺度（官方建议 + 作者经验）；
- 视频里"某工程师六个 Bot"的效果是作者陈述，官方文档不能为其业绩背书。

## 产物

- `exercise/sample-job-contract.md` — 岗位契约样例 + 安全符合性检查表
- `exercise/experiment-log.md`（本文件）
