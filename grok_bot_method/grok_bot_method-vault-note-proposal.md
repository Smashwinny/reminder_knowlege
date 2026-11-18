# Grok Bot 方法论 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：310d587b-b014-4ab0-8c33-59f25a733f27 ｜ 项目目录：F:\reminder\grok_bot_method

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 岗位契约四件套
- 一句话定义：把常驻 Agent 当员工管的四个文件化要素——契约（≤3 条可验收职责+红线+失败定义）、试用期（小样本试运行）、转正条件（连续 N 次通过才放权、红线触发即回退）、交接（岗位上下文落盘 ROLE.md）。
- 领域：AI Agent / 治理
- 已有概念关联：[[Agent指令文件AgentMd]]（守则的雇佣版）；[[AgentHarness智能体挽具]]（契约与最小权限两职责的落地）；[[代码管边界提示词管判断]]（红线归机制）
- 来源项目：grok_bot_method（样例契约 6/6 通过官方安全对照）

### 2. 共享环境非隔离原则
- 一句话定义：多 Agent 共用一台机器/一个账户时，"各自的屏幕/会话视图"不构成安全边界；敏感文件不放共享盘；分信任级别要分账户/分机器；回收权限要"移出+撤销会话"双动作（terminate≠收权）。
- 领域：AI Agent / 安全
- 已有概念关联：[[沙箱与审批正交]]（能力≠默认姿态）；[[最小权限]] 思想；[[共享状态与Reducer]] 的风险面
- 来源项目：grok_bot_method（官方 FAQ 原文 "Do not use separate Bots as a security boundary"；Computers 文档 terminate 语义）

## 二、项目笔记（建议新建 vault\项目笔记\grok_bot_method.md）
- 项目是什么：X 长文《Grok Bot: How to Hire Your First AI Employee》+ xAI 官方 FAQ/Computers 文档——常驻 AI 员工的雇佣方法论（Grok Bot 为载体）
- 带来的概念：[[岗位契约四件套]]、[[共享环境非隔离原则]]
- 实验做了什么：官方两份文档直读核验（共享电脑/computer takeover/terminate 语义/30 天自动终止）；契约样例产出与六项安全对照（6/6）
- 坑与结论：skill 须真任务试跑再变 routine（官方）；三次试运行/五次通过是作者经验非官方保证；视频业绩官方不背书

## 三、合并建议（不新建，增补已有笔记）
- [[AgentHarness智能体挽具]]：增补"契约+最小权限"的雇佣式落地
- [[沙箱与审批正交]]：增补 Grok Bot Auto-review + computer takeover 为产品化实例
- [[人机协同Interrupt]]：增补 computer takeover 为产品化形态

## 四、MOC 更新建议
"AI Agent / Harness 工程"分区增补两条新概念；项目索引加 grok_bot_method。
