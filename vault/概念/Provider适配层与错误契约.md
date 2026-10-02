---
tags: [概念]
领域: AI Agent / LLM 接入架构
别名: ["API×Provider 两维拆分", "永不 reject 错误契约", "错误契约", "11 API 38 provider"]
首次来源: "[[项目笔记/agent-kernel]]"
---

# Provider 适配层与错误契约

**一句话定义**：多模型接入的两维拆分——**API（协议格式，pi 用 11 个实现服务 38 家 provider，其中 openai-completions 一个实现覆盖 20 家）× Provider（服务商，每家只是 15~30 行纯配置）**——配套一条类型级错误契约：stream 函数同步返回 EventStream 而非 Promise，**永不 throw 也不 reject**，所有失败编码成流内 error 事件，上层循环才敢用 stopReason 分支、一行 try/catch 不写。

**属于领域**：AI Agent / LLM 接入架构（[[ChatModel与消息类型]] 讲统一接口的"是什么"，本笔记讲支撑它的"怎么组织"和"错误怎么流动"）

**通俗理解**（比喻/例子，讲完落回术语）：API×Provider 像**插座标准 × 电器厂商**——协议是插座标准（国标/美标共 11 种），厂商是电器（38 家），新厂商只需声明"我用国标"（15 行配置），不用重新发明电。错误契约像**快递柜而非上门送件**：调用方把请求放进柜子（EventStream）就返回，一切后续（成功/失败/断流）都以柜内事件呈现——调用方无处 await，也就无处 try/catch，**契约不靠文档约定，靠类型系统强制**。

**两条方向相反的规则**（判断错误该"吞"还是该"抛"）：调模型的函数**永不抛异常**（读者是程序，程序处理不了网络故障，降级成 stopReason 优雅退出）；工具函数**必须抛异常**（读者是模型，模型读懂"文件不存在"会自己 ls 排查重试，内核 catch 成 isError:true 结果回喂）。一句话：**先问错误的读者是程序还是模型**。配套设计：setup 失败（鉴权/动态 import）用 lazyStream 包成流内 error 事件；失败路径补发完整事件序列（message_start/end、turn_end、agent_end），保证订阅者看到的事件序列在任何路径下闭合——UI 和持久化才能写得极简。

**实战印证**（agent-kernel 实验）：本机仅有 z.ai 的 Anthropic 协议端点、mini-agent 只会说 OpenAI chat/completions——自写 130 行零依赖 shim 做 OpenAI→Anthropic 双向转换（含工具 schema 映射、tool_result 合并、SSE 合成、429 自动重试），两个 agent 真跑通。这正是"协议格式与服务商解耦"思想的应用：**写一次适配层，所有 OpenAI 兼容客户端都能跑在任意后端上**。

**与已有概念的关联**：
- [[ChatModel与消息类型]]：统一接口的对外形态；本笔记是其内部架构
- [[Agent循环]]：错误契约是循环敢用 stopReason 分支的前提
- [[工具调用三段式流水线]]："工具必须抛异常"这条规则的归属地
- [[MCP协议]] / [[M×N集成问题]]：同一"标准收敛"经济学在工具侧的版本
- [[零依赖编程]]：shim 实验的实现方式

**首次接触于**：[[项目笔记/agent-kernel]]（note 02《38 家大模型，11 个实现就够了》）
