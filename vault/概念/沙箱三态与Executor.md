---
tags: [概念]
领域: AI Agent / 执行环境
别名: ["Environment 三态", "self-hosted executor", "openai_hosted sandbox", "none 环境"]
首次来源: "[[项目笔记/openai-agents-api]]"
---

# 沙箱三态与Executor

**一句话定义**：托管 harness 的执行环境（Environment）三种形态——`none`（无工位：只问答/调远程工具）、`openai_hosted`（厂商云沙箱：跑代码改文件产 artifacts）、`self_hosted`（**你的机器**起 executor 连上 session，harness 远程下发命令由 executor 执行）——本质是"agent 的手脚放在谁家"的架构决策。

**属于领域**：AI Agent / 执行环境（[[AgentHarness智能体挽具]] 职责 3"正确环境暴露正确工具"的产品化）

**通俗理解**：none 是"咨询顾问只动嘴"；openai_hosted 是"公司给你配好工位电脑"；self_hosted 是"顾问远程操作**你办公室**的电脑"——命令不是你逐条转发，而是 harness 直接下发给你的 executor，你的代码只管 executor 生死（开机/断线重连/关机），适合私有网络、内网数据库、专有软件。注意 none 环境没有 Bash/apply-patch/工作区文件（实测契约校验可拦此类非法配置）。

**实测证据**：openai/codex 沙箱家族 5 个 crate（linux-sandbox / windows-sandbox-rs / windows-sandbox-service / mxc-sandbox / sandboxing）；本地 `codex sandbox python -c ...` 真跑：命令在 Windows restricted token 沙箱内执行成功、写文件被 `PermissionError: [Errno 13]` 拦住且文件确实未落盘——**云上沙箱与本地 CLI 是同一套开源实现**，零费用可学。

**与已有概念的关联**：
- [[AgentHarness智能体挽具]]：最小权限职责的实物形态
- [[工具调用生命周期]] / [[LLM工具调用]]：function 工具永远回调你的代码执行（环境只在 harness 侧时亦然）
- [[提示注入]]：沙箱是注入防线执行侧的物理边界；key 永不进沙箱（官方红线）
- [[Serverless边缘函数]]：同为"环境即租来资源"，一个按容器时长一个按请求计费

**首次接触于**：[[项目笔记/openai-agents-api]]
