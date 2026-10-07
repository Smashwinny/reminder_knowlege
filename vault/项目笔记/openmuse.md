---
tags: [项目笔记, 持久任务, 动作审批, 不确定结果]
学习审核日期: 2026-10-05
上游仓库: https://github.com/CopilotKit/openmuse
固定版本: b06caad7005ac5b6d2b451752a3794a6ae1759c1
许可: MIT
验证范围: 真实PGlite与上游核心；合成提供方、同进程Worker、受控重开
---

# OpenMuse：持久任务、精确审批与不确定写入

## 是什么，能学到什么

本项目整理 OpenMuse 固定版本的任务引擎、动作审批和 SQL 存储核心。学习重点是：任务状态如何保存，worker 如何有条件地领取与写回，审批怎样对应具体提案，以及没有可靠外部回执时如何保留未知结果。界面或产品说明不是这些机制已经在完整应用中验收的证据。

可以带走五种工程方法：分别定义任务、运行记录与动作；把审批和内容/连接/版本绑定；检查重复操作键的实际契约；对旧执行者写回设置当前身份条件；把真实数据库与合成外部服务的证据分开。它们有助于设计可恢复流程，但不自动保证所有外部效果只发生一次。

## 与已有知识的合并

- [[人机协同Interrupt]]：追加 LangGraph 节点重执行的既有勘误，以及 OpenMuse 审批绑定具体提案的案例；两种实现不混同
- [[Checkpoint存档与持久执行]]：追加完整快照/节点写入的粒度勘误，再对照 OpenMuse 保存状态、条件写回和宿主存活要求
- [[证据状态机]]：追加 outcome_unknown 与重复决定的处理边界，不将不确定写入强判成功或失败
- [[接缝与桩实现StubSeam]]：追加真实 SQL/PGlite、合成提供方、同进程竞争和受控 close/reopen 的证据划分
- [[AgentHarness智能体挽具]]、[[产物留痕与状态外置]]、[[JSONL事件日志与折叠模型]]：复用任务运行与产物留痕思想，不把数据库记录自动当作 JSONL 折叠或防篡改日志
- [[沙箱与审批正交]]、[[技能路由器与授权硬门]]、[[工具调用三段式流水线]]、[[LLM工具调用]]、[[工具调用生命周期]]、[[程序化工具调用]]、[[控制面与数据面]]：模型提议、可信决定入口、实际执行和环境能力分别核对；工具结果里的“已批准”文字不自行成为批准
- [[多Agent协作乱序竞态]]、[[共享状态与Reducer]]、[[消息队列与异步削峰]]：为并发和异步提供背景；Reducer 合并规则不能代替数据库原子领取，消息入队也不代表外部效果完成
- [[证据优先质检ProofOverClaims]]：以所列实际断言和回执限定结论，不复用作者历史整站测试数作为本次成绩

[[项目笔记/ai_native_handbook]] 的委托/执行分层、[[项目笔记/codex_advanced]] 的契约与运行区别，以及 [[项目笔记/patchright_enhanced]]、[[项目笔记/nce_reading]]、[[项目笔记/route_studio]] 的组件/替身/外部结果边界，都作为相关案例复用。未把旧项目的数量、性能、平台或许可移植为 OpenMuse 事实。本次不新建同义的审批、恢复或证据概念；租约和幂等键细节先保留为本项目实例。

## 已有六组命令与计数

历史学习环境为 Linux、Bash、Node v24.19.0、npm 11.9.0 和 Python 3。核心依赖为 PGlite 0.3.16、pg 8.23.0、zod 4.6.5，含传递依赖共 16 项，其版本和完整性与固定上游锁对应。TypeScript 转换的实验性警告保留；这不是全应用构建或完整类型检查。

原始核心入口顺序执行四组测试；历史独立审核从最终 ZIP 新目录完成六组教材命令：核对版本与材料、安装核心依赖并复核、运行审批组、运行引擎组、运行所选持久化用例、运行四个自写变式并再核对。安装阶段访问官方 npm 仓库；测试路径不需要账号或网络。此次公开整理只复核既有材料，没有重新安装依赖、运行实验或启动服务。

- 21 项选取的原样上游测试通过：12 项 actions、8 项 engine、1 项 persistence；失败为 0
- 4 项另行编写的变式通过；不能称为 25 项上游官方测试，历史独立重跑同一集合也不累加为 50 项覆盖
- 三个上游测试文件共有 22 项定义；持久化选择器只选 fresh nested data directory，另一个 PostgreSQL 池错误用例未选择
- Node 此次 TAP 实际报告 skipped=0；“1 项未选择”不能改写成 skipped=1，更不能写全 22 项通过
- 四组测试退出码为 0，网络守卫记录 attempts=0。15 项上游原件指纹、16 项依赖完整性与测试项数分开计，不相加

被测真实实现为 SQL Store、PGlite、ActionService 与 TaskWorker；提供方 execute/prepare、连接判断、任务处理器和时钟是受控输入。不是纯内存字典模拟数据库，也不是接通真实提供方的端到端实验。

## 核心观察与边界

1. **审批绑定的是具体提案。** propose 把解析后的输入、连接、目标及目标版本纳入内容哈希；decide 按作用域读取，核对 hash、到期及连接状态/身份，再通过数据库领取 awaiting_review。历史反例覆盖拒绝、错误主体、旧 hash、到期、断连和换账号；并发批准时提供方 fixture 只调用一次。哈希不等于签名、认证或任意篡改防护
2. **传递版本不等于真实条件写入。** 实验确认保存的目标版本被交给注入的 execute，不能写成 HTTP If-Match、ETag 或 Google 并发修改冲突已经实测。真实适配器、网络和资源侧拒绝仍未验收
3. **操作键不是新意图校验器。** 同操作键换主题，propose 在重新解析/prepare 之前命中已有记录，返回原提案、原正文和原 hash，动作仍只有一份；换新操作键再改主题，hash 才变化，旧 hash 与错误主体的批准都被拒且 fixture 调用为 0。两种 hash 用途不同，不能将复用键当可靠的修改操作
4. **条件写回阻止旧 worker 覆盖。** TaskWorker 用 compareAndSwap 领取任务，并以当前领取身份和 running 状态约束 checkpoint。guard 核对中止状态、当前身份与任务状态，不直接比较到期时刻；心跳续期失败会中止本地执行。该机制不是外部服务强制执行的单调 fencing token
5. **接管实验使用虚拟时间。** 自写变式推进 60001 毫秒后，新 worker 接管；旧 checkpoint 被拒，旧处理器下一次 guard 阻止效果计数增加。观察为总领取 2 次、新处理器 1 次、旧受守卫效果 0、最终保存新结果。两 worker 在同一进程共享 PGlite，没有真实等待一分钟、跨进程 PostgreSQL 或分布式故障证明
6. **取消只保护实际调用守卫的路径。** 守卫检查与后续外部效果不是同一数据库原子操作，已经派发的请求可能继续完成；跳过 guard 的自定义处理器不能借用取消测试结论。引擎末项只证明写运行记录失败后 stop 能完成且任务标为 failed，没有断言此后所有任务能继续

## 未知结果与持久化，不应混成“安全重试”

执行器显式标记不确定结果的合成错误被保存为 outcome_unknown；恢复函数可将遗留 executing 也转成该状态。再次 decide 遇到非 awaiting_review 时返回已有提案，不自动再次 execute。自写变式中真实 PGlite 正常 close/reopen 后仍保留未知，提供方 fixture 总调用数为 1。

这说明本地控制路径保留不确定性，不说明真实邮件曾发送或提供方已经完成对账。超时可能发生在请求接收前，也可能发生在已接收但回执丢失后；是否补偿、重发或另建动作，需要真实提供方证据和适当决定。本实验没有自动解决所有未知写入，也没有验证 exactly-once。

持久化只测正常关闭后重新打开。没有强杀、断电、崩溃耐久性、跨进程共享、灾难恢复或生产迁移验证。固定 README 说明后台推进仍依赖宿主运行；独立 worker 的共享 PostgreSQL 部署是文档路线，不是这次 PGlite 实验的结果。

## 既有 LangGraph 笔记的窄更正

[[人机协同Interrupt]] 与 [[Checkpoint存档与持久执行]] 追加了原学习材料已经提出的恢复粒度勘误，保留全部旧正文以供追踪。依据分别为官方 Interrupt 文档和固定版本 checkpointers 文档；没有运行 LangGraph，也不把其节点恢复规则套入 OpenMuse 自己的 TaskWorker。

## 未验证范围与材料边界

没有完整应用构建/启动、真实账号/认证、Google 邮件或日历效果、HTTP ETag 条件写入、模型推理、浏览器/桌面操作、Docker/E2B 或 CopilotKit Intelligence 集成；没有多进程数据库、任意处理器安全、生产授权审计、性能或外部效果恰好一次证明。网络守卫只约束本次所审测试路径，不是未知代码的强安全沙箱。

固定 docs/VERIFICATION.md 中作者 2026-09-16 的 154 项测试及浏览器/Docker 描述是历史材料，未作为本次执行成绩。原始介绍网页未成功读取，其宣传不作为本次已验证事实。

上游 LICENSE 为 MIT，练习保留完整 Copyright (c) 2026 OpenMuse contributors 和许可文本。最终原始 ZIP 有 37 个成员，内嵌清单核对另外 36 个成员；包含 15 份原样上游材料，未打包 node_modules、缓存或临时数据库。依赖许可和服务账户权益不能从项目 MIT 许可推导。

原指南是 ReportLab 直接生成的 23 页 PDF，历史审核逐页查看渲染页面；HTML 仅结构核查，没有浏览器视觉或 HTML→PDF 验收。教材示意图不是整站运行截图。本次公开副本审核另见配套日志，材料完成不代表读者已经掌握。

## 最新公开知识读取范围

此次合并基于 GitHub main 快照 3cda5466a6a4c6359a412e596c5934859a9ef9f3。通过连接器取得并核对完整 UTF-8 字节、Git blob SHA 与 SHA-256：MOC、学习方法、仓库说明、两份模板、上方列出的 18 篇概念及 5 篇项目，共 28 份正文。与此前已经读过的正文完全一致者，以精确字节证据复用其阅读；元数据不算正文。

该快照有 306 篇概念和 109 篇项目笔记；其余 288 篇概念、104 篇项目仅做路径/标题筛查，未全文阅读。名称与主题筛查覆盖 OpenMuse、Open Muse、open_muse、open-muse、CopilotKit、持久任务、审批、租约、幂等、不确定结果、Checkpoint 和 Interrupt 等；结论限于当前公开快照及实际已读范围，不能称为全库正文无重复或其他设备副本已核验。

本次新增项目笔记、向四篇既有概念追加案例/勘误并在 MOC 加入口；不新增概念，不改写历史累计计数、原正文或既有项目。原学习的 394 条公开索引元数据、18 篇公开正文、376 篇未读正文是较早阶段的独立范围。

## 六份配套材料

- [彩色 PDF 指南](../../openmuse/delivery/openmuse-guide.pdf)
- [HTML 指南](../../openmuse/delivery/openmuse-guide.html)
- [核心练习包](../../openmuse/delivery/openmuse-core-exercise.zip)
- [历史实验日志](../../openmuse/delivery/openmuse-experiment-log.md)
- [知识笔记](../../openmuse/delivery/openmuse-knowledge-notes.md)
- [发布审核及历史证据复核](../../openmuse/delivery/openmuse-review-log.md)

## 固定来源

- [ActionService](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/actions.ts)、[SQL Store](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/db.ts)、[TaskWorker](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/engine/worker.ts)、[任务服务](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/engine/service.ts)
- [审批测试](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/actions.test.ts)、[引擎测试](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/engine.test.ts)、[持久化测试及排除用例](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/persistence.test.ts)
- [README](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/README.md)、[MIT LICENSE](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/LICENSE)、[作者历史验收](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/docs/VERIFICATION.md)
- [LangGraph Interrupt 官方更正依据](https://docs.langchain.com/oss/python/langgraph/interrupts)、[固定 Checkpointer 文档](https://github.com/langchain-ai/docs/blob/f17ce09ae2fc2b0bb30306b1ce78d874f3c0a77c/src/oss/langgraph/checkpointers.mdx)

返回 [[00-总览|知识库总览]]。
