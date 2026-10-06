---
tags: [概念]
领域: AI / Agent 编排
别名: [interrupt, Human-in-the-Loop, HITL, 人工审批]
首次来源: "[[项目笔记/langgraph]]"
---

# 人机协同 Interrupt

**一句话定义**：在图的关键节点调用 `interrupt(问题)`，任务在此冻结并把问题抛给外部的人；人通过 `Command(resume=答案)` 唤醒，图从冻结的那一行原样继续，答案成为 interrupt() 的返回值。

**属于领域**：AI Agent 编排 / 人机交互

**通俗理解**：像餐厅出菜前的"经理试菜"——菜（任务）停在第 9 步等经理点头，经理可能 5 分钟后回来也可能第二天才回来；厨房（进程）不用干等，直接下班，菜谱和火候都写在存档里。关键认知：**不是"程序挂起等人"，而是"任务等待人"**——进程正常退出、不占资源，恢复是"带答案再 invoke 一次"。典型场景：Agent 要执行退款、发邮件等敏感操作前先 interrupt 要审批。

**实现前提**：必须挂 Checkpointer（冻结点要落盘），且用同一 thread_id 唤醒。

**与已有概念的关联**：
- 属于：[[LangGraph与Agent编排]]
- 依赖：[[Checkpoint存档与持久执行]]
- 对比：[[质检Gate与自我纠错循环]]（Gate 是机器自动裁判放行；Interrupt 是留给人裁判的口子——两者常串联：Gate 先自动筛，最后一步人拍板）

**首次接触于**：[[项目笔记/langgraph]]

## OpenMuse 对照：恢复位置勘误与提案绑定（2026-10-06）

[[项目笔记/openmuse]] 的既有学习材料指出，上文“从冻结的那一行原样继续”过度概括。LangGraph 官方说明是从被中断节点的开头重新执行，interrupt 之前的代码会再次运行；恢复值成为相应 interrupt 的返回值。前置副作用须考虑幂等，或放在合适的审批后/独立节点边界。旧文原样保留以便追踪，不能继续把它当逐代码行恢复保证；此处只核对官方说明，没有运行 LangGraph。

OpenMuse 使用自己的 ActionService。固定实现把输入、连接、目标与目标版本纳入提案内容 hash；决定时核对当前记录、hash、时效与连接，再原子领取待审状态。历史真实 PGlite 测试中，错误主体、旧 hash、断连、换账号等被拒；并发批准只调用一次合成提供方。其可信决定入口和存储是前提，hash 本身不是身份认证、签名或任意篡改防护。

目标版本交给 fixture 只证明传参，没有测试真实 Google/HTTP ETag 冲突。动作准备的幂等键与内容 hash 也不同：同键改输入返回原提案，换新键改输入才生成变化的 hash。这些是本项目契约，不能合成“批准后任意内容均可执行”，关联 [[工具调用三段式流水线]]、[[沙箱与审批正交]]。

来源：[LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[固定 ActionService](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/actions.ts)、[原始审批测试](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/actions.test.ts)；[历史实验日志](../../openmuse/delivery/openmuse-experiment-log.md)。
