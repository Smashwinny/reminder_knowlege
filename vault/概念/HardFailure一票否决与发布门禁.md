---
tags: [概念]
领域: AI Agent / 评估工程
别名: [Hard Failure, Release Gate, 发布门禁, 一票否决指标]
首次来源: "[[项目笔记/agent-eval]]"
---

# Hard Failure 一票否决与发布门禁

**一句话定义**：把"绝不能发生的错误"（编造来源/越权写入/工具失败仍宣称完成）设为 **Hard Failure 直接判死、绝不进平均分**，评测指标据此变成**实验前预注册的 Release Gate**（primary 提升量 + non-inferiority 不退步 + safety 硬门禁 + reliability + cost per **successful** task），门禁过了也不直接切流量，先 shadow 再 canary。

**属于领域**：AI Agent 评估 / 发布工程

**通俗理解**：报告完整度 95 分 + 语言 90 分 + 编造一条关键来源——算术平均可能还好看，但业务不会接受。所以指标分两种：**gate**（安全/权限/关键事实，决定能不能放行）与 **optimization metric**（成本/延迟/语言质量，在可用版本之间继续优化）。Gate 必须**在实验前写死**——看到结果再定标准，人会本能地给喜欢的版本找解释。

**三个反直觉点（实测验证，agent-eval 实验 2/3）**：
1. **cost per successful task ≠ 单次 API 费**——便宜但老失败的 Agent 重跑三次+人工返工更贵；实测 v2 成功率 29/30>v1 的 27/30，但成本 ×2.92 超门禁照样否决；
2. **全过门禁也不切 100% 流量**——shadow（收真实请求不影响用户）→ canary（小流量+可回滚）→ 逐步扩大；
3. **Eval 的终点是一项可解释、可回滚的发布决定**，不是一屏好看的图表。

**与已有概念的关联**：
- [[质检Gate与自我纠错循环]]：Gate 思想同源，本概念把它推到发布决策层
- [[LLM裁判与自动评估]] / [[Outcome与Trajectory双层评测]]：给 Gate 供数的两层
- [[评分契约与护栏]]：guardrail 拦截与 gate 一票否决同族
- [[事实与判断分离]]：硬门禁（事实层）与优化指标（偏好层）分开处理
- [[零信任与最小权限]] 类安全概念：越权类 Hard Failure 的防线

**首次接触于**：[[项目笔记/agent-eval]]
