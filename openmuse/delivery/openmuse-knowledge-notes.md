# OpenMuse 持久任务精确审批与不确定写入知识笔记

日期：2026-10-05 UTC。项目固定为 [CopilotKit/openmuse@b06caad7005ac5b6d2b451752a3794a6ae1759c1](https://github.com/CopilotKit/openmuse/tree/b06caad7005ac5b6d2b451752a3794a6ae1759c1)。本文保留历史固定来源、公开知识关联、实验结果和未测范围。本次公开整理未重跑实验或安装依赖。

## 1. 查重范围与证据等级

公开知识索引固定于 Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352；相关公开笔记正文固定于 1043e9d6080bff7af9724162e2c44559fab63e40。

公开索引共 394 条元数据，本轮全文读取并按索引字节数与 SHA-256 核验 18 篇相关概念，其余 376 篇只有元数据检索。

名称查重覆盖 OpenMuse、Open Muse、open_muse、open-muse、CopilotKit/openmuse，在历史公开索引元数据和 18 篇已读公开正文中未命中。这个结论不覆盖其他版本或 376 篇未读正文，不能写成“全库无重复”或“从未学过”。笔记存在不代表读者已掌握。

历史知识笔记的产品版本、性能数字、默认配置和旧实验数量没有在本轮逐项重验。哈希一致证明读到同一份文本，不证明其中每项断言正确。下面 OpenMuse 实现描述属于固定源码观察；本轮实际执行结果须与同包实验日志分开阅读，不能把作者历史验收替换成本轮成绩。

## 2. 优先复用的知识，不重新讲一遍

- [[AgentHarness智能体挽具]] 已覆盖模型之外的工具、状态、权限和验收。OpenMuse 是这套思想的具体应用案例，不是新模型，也不因界面相似就等同于其他个人助手
- [[Checkpoint存档与持久执行]]、[[产物留痕与状态外置]] 已解释状态外置和恢复。这里补“恢复哪一层、哪些动作可以重放”，并修正旧笔记的过度承诺
- [[人机协同Interrupt]]、[[沙箱与审批正交]]、[[技能路由器与授权硬门]] 已解释人工决定、执行环境和行动授权。这里补审批对象如何绑定到具体内容与版本，不重建一个同义“人工审批”条目
- [[多Agent协作乱序竞态]]、[[共享状态与Reducer]]、[[消息队列与异步削峰]] 已涉及并发与异步。OpenMuse 的 SQL 原子领取与旧租约写回拒绝，需要独立解释；Reducer 合并规则不能代替数据库互斥
- [[LLM工具调用]]、[[工具调用生命周期]]、[[工具调用三段式流水线]] 已解释模型提议和执行器真正行动。工具结果中的“批准”文字仍不是可信审批入口
- [[接缝与桩实现StubSeam]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]] 已充分覆盖替身与真实服务、声明与证据的区别。只增加本项目的具体测试边界

当前 AI Native 知识已经提出委派范围收缩、发现/批准/执行分层及权限撤销；MCP Toolbox 已有“注解不等于强制边界”；NCE 已有过期异步响应与代次检查；Codex 和 Qwen 已有解析/契约/运行结果分层；Patchright 和 RouteStudio 已有调用发出与外部效果分开。这些均应复用，不重复建立同义原则。

## 3. 必须修正：Interrupt 不是从原代码行无条件续跑

固定 [[人机协同Interrupt]] 正文说恢复时从冻结的那一行原样继续，这会误导副作用设计。LangGraph 官方说明明确：恢复会从被中断节点的开头重新执行，interrupt 前面的代码也会再跑；恢复答案按既定 interrupt 调用顺序匹配。副作用应有幂等设计，或放到适当的审批后/独立节点边界。这里没有运行 LangGraph，不把官方说明写成自测。

来源：[LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)，尤其 Rules of interrupts 与 Side effects called before interrupt must be idempotent。

固定 [[Checkpoint存档与持久执行]] 的“每个节点结束都保存整块快照、已完成节点一概不重跑”也应细化：LangGraph 的完整快照位于 super-step 边界；同一 super-step 内还可持久保存已完成任务的写入，用于失败恢复。这不意味着保存了每一行程序位置，也不能单靠 checkpoint 保证外部副作用只发生一次。

来源：[LangChain 官方 checkpointers 文档源码](https://github.com/langchain-ai/docs/blob/f17ce09ae2fc2b0bb30306b1ce78d874f3c0a77c/src/oss/langgraph/checkpointers.mdx)。这两个更正只解释 LangGraph；OpenMuse 使用自己的 TaskWorker、Store 和任务状态，不能把 LangGraph 的具体恢复规则套过去。

## 4. 候选增量：审批绑定到具体动作内容与资源版本

一句话定义：批准必须指向一份确定的动作提案，包括执行身份、接收对象、动作参数、时效与相关资源版本，不能退化成可被任意新内容复用的布尔值。

领域：授权协议、并发控制、人机协作。优先增补 [[人机协同Interrupt]] 和 [[工具调用三段式流水线]]，互链 [[沙箱与审批正交]]、[[控制面与数据面]]；先在目标知识库检索“精确动作审批、审批指纹、版本绑定”再决定是否独立成篇。

自写例子：用户审阅“给测试地址甲发送草稿 A”。收件人换成乙、正文换成 B、连接换成另一账号，不能继续显示“此前已经批准”。对于更新或删除日历事件，用户看到的对象版本也需要保持对应，否则审批期间别人修改了事件，就可能操作另一份内容。

固定 OpenMuse 的 ActionService 在 propose 时把解析后的 input、connection、target 和 targetVersion 纳入 SHA-256；decide 检查 owner 下的记录、提交的 hash、到期时间、连接状态与连接身份，再由数据库原子 claim 消费 awaiting_review 状态。execute 接到保存的 connectionId 与 targetVersion。具体下游是否校验资源版本，还要继续跟踪适配器；仅检查 hash 字段存在不证明整个系统安全。

哈希用于内容关联，不是密码、签名、身份认证或完整授权。当前实现依赖可信的服务器、数据库和审阅入口，不能据此声称防住任意数据库篡改或所有检查/执行竞态。

来源：[actions.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/actions.ts)、[db.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/db.ts)、[actions.test.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/actions.test.ts)。测试文件存在属于源码证据，通过情况以本次日志为准。

## 5. 候选增量：租约领取与旧执行者写回拒绝

一句话定义：worker 用有期限的领取标识声明当前处理权，并在持久状态写回时核对它仍然是当前执行者，防止旧 worker 恢复后覆盖新任务状态。

领域：分布式任务调度、并发控制、故障恢复。与 [[多Agent协作乱序竞态]]、[[消息队列与异步削峰]]、[[Checkpoint存档与持久执行]] 相关；不是 Reducer 的同义词。

自写例子：A 领取任务后停止响应，B 在领取过期后获得新的 leaseId。A 恢复时手上仍有旧结果；若直接无条件保存，就可能覆盖 B。写回时比较当前 leaseId 与状态，能够拒绝不再拥有处理权的旧结果。

固定 TaskWorker 通过 Store.compareAndSwap 原子比较旧 status/leaseId（接管 running 任务还包括 leaseUntil），成功后写入新 UUID leaseId。checkpoint 仅在 leaseId 仍匹配且任务处于 running 时更新；heartbeat 条件续期失败会中止本地执行。暂停/取消也会改变状态与租约，使旧 checkpoint 失去写回条件。

边界很重要：此处是数据库任务状态上的条件写入，不能简写成“租约保证 exactly-once”。UUID 并不是单调递增的下游 fencing token。event 的 guard 与后续写日志是分开的调用；任意外部网络效果也不会因此自动进入同一个数据库原子操作。已经派发的外部请求可能在取消后完成。

来源：[worker.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/engine/worker.ts)、[db.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/db.ts)、[service.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/engine/service.ts)。本次实际运行一个进程中的多个 worker 与真实 PGlite，只按该范围报告，不能称为多进程 PostgreSQL 或分布式故障验收。

## 6. 候选增量：不确定外部写入是一种必须保留的结果

一句话定义：外部写请求已经可能被接收，但本地没有可靠回执时，结果应保留为未知；不能擅自当成失败再发送，也不能擅自标成成功。

领域：分布式系统、可靠性、外部副作用管理。优先给 [[证据状态机]] 和 [[工具调用生命周期]] 增补此例；在目标知识库查重“outcome_unknown、未知结果、uncertain write、重复副作用”后再决定独立条目。

自写例子：邮件服务可能已经接收测试请求，但确认响应途中连接断开。本地超时无法区分“没收到”与“收到了但回执丢了”。再次发送可能重复；显示已完成也没有证据。下一步应核对提供方记录或明确的幂等能力，再决定如何处理。

固定 OpenMuse 将执行器显式标记 outcomeUnknown/code=outcome_unknown 的错误保存为 outcome_unknown。重启恢复可将遗留 executing 动作也置为 outcome_unknown。再次 decide 遇到非 awaiting_review 状态会直接返回已有提案，不再自动调用执行器；任务重试路径对关联的未成功动作也要求先核对结果。

这不是“自动解决所有不确定写入”，也不是“没有响应就肯定没发出”。当前存储和控制路径保留不确定性；真实提供方对账、人工判断、补偿或创建替代动作仍需单独验收。不要把故意抛出的未知结果夹具写成真的发出过邮件。

来源：[actions.ts](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/actions.ts)、[db.ts recoverInterruptedActions](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/db.ts)、[service.ts retry](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/engine/service.ts)。

## 7. 项目案例：幂等键标识一次操作，不替调用方检查新意图

一句话定义：幂等键用来让同一逻辑操作的重放找到已有结果；如果把不同操作错误地复用同一键，系统可能返回旧操作，而不会替调用方识别新意图。

领域：API 设计、任务重放、可靠性。关联审批绑定、[[Checkpoint存档与持久执行]] 和 [[AgentHarness智能体挽具]]，优先作为本项目案例。

固定 ActionService.propose 在存在 idempotencyKey 时先计算其 SHA-256 作为动作 id，并按 owner 查已有动作；命中后直接返回，发生在解析新 raw input 和再次 prepare 之前。因此“同一个键、换了正文”不能当成可靠的修改草稿方式。审批内容哈希与幂等键派生 id 是两个用途不同的值。

合成实验可对比：同键同输入重放、同键改输入、新键改输入。记录返回 id、hash、正文、prepare 次数和 execute 次数。本次变式已观察到返回旧提案，详见第11节与原始日志；这应解释为当前实现契约，不能包装为自动冲突校验。

来源：[actions.ts propose](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/apps/server/src/actions.ts)。

## 8. 项目案例：持久任务、活着的宿主和外部服务分别验收

一句话定义：任务状态可以在数据库中存活，不代表执行宿主离线时仍能推进，也不代表任何恢复路径都能安全重放外部效果。

领域：任务运行平台、持久化、运维。优先增补 [[Checkpoint存档与持久执行]] 与 [[产物留痕与状态外置]]。

固定 README 说明：后台执行依赖宿主仍在运行；PGlite 不能被独立进程共享，独立 task worker 应按文档配置共享 PostgreSQL、数据目录和必要配置。一个进程内两个 worker 竞争同一 PGlite，是有价值但更窄的验证。

docs/VERIFICATION.md 记录的是 2026-09-16 的作者历史验收，其中 154 tests、真实浏览器与 Docker 描述不能作为这次的执行成绩。当前固定提交已晚于该记录；README、实现、历史测试报告之间出现差异时，应保留日期与证据等级，逐项核对。测试模拟服务回执也不能证明真实 Gmail、Calendar、模型、浏览器、桌面或 CopilotKit Intelligence 已连通。

来源：[README 持久化与运维](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/README.md#persistence-and-operation)、[作者历史验收](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/docs/VERIFICATION.md)。

## 9. 复用与合并建议

先核对目标知识库的同义概念与已有编辑，保留来源版本与旧正文历史。修正 LangGraph Interrupt/Checkpoint 的过度概括，再增补 OpenMuse 的精确审批、租约写回、不确定结果和幂等键案例。

同义内容合并、相关内容互链；项目笔记保留实际运行版本、历史日志、替身边界及未执行项，不因换了项目就复制测试成绩或新建同义概念。

## 10. 本轮实际全文核验的公开知识

以下 18 篇均固定于 [1043e9d6080bff7af9724162e2c44559fab63e40 的概念目录](https://github.com/Smashwinny/reminder_knowlege/tree/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念)，正文与固定索引指纹一致：

AgentHarness智能体挽具；Checkpoint存档与持久执行；JSONL事件日志与折叠模型；LLM工具调用；产物留痕与状态外置；人机协同Interrupt；工具调用三段式流水线；工具调用生命周期；技能路由器与授权硬门；接缝与桩实现StubSeam；沙箱与审批正交；程序化工具调用；证据优先质检ProofOverClaims；证据状态机；共享状态与Reducer；控制面与数据面；多Agent协作乱序竞态；消息队列与异步削峰。

原知识中的历史星标数、框架 API 名、产品配置和性能口径不在本次重验范围。本文没有宣称知识库全面正确，也没有替本人确认已经掌握。


## 11. 本轮实验结果 已测范围与未测范围

2026-10-05 11:46:11–11:46:23 UTC，在 Node v24.19.0 / npm 11.9.0 上运行原始核心测试和4项独立变式。原始 actions 12项、engine 8项、按名称选择 persistence 1项，共21项通过；独立变式4项通过。失败为0，四个进程均退出0且 NETWORK_GUARD attempts=0。源文件中共有22个原始测试定义，PostgreSQL连接池错误测试未被选择；该Node版本实际报告 skipped=0，不把它改写成 skipped=1。

独立审核者从最终 ZIP 新目录解压，在 11:51:11–11:52:32 UTC 执行说明中的六组完整命令，含 npm ci 安装16项依赖、核验15项上游文件指纹、分别重跑21+4项。全部命令通过；这是同25个用例的独立复跑，不是50个不同测试。

可沉淀的四个当前观察：

1. 改主题并换操作键，准备快照的hash改变；旧hash和错误拥有者被拒绝，提供方fixture调用0次
2. 改主题却复用原操作键，返回原有提案，保留原内容；动作记录仍1项
3. fixture抛出不确定结果后，真实PGlite正常关闭再打开仍保留outcome_unknown；再次批准不重复调用，fixture总调用1次
4. 在同进程内推进虚拟时钟60001毫秒使新Worker接管；旧checkpoint被拒绝，旧Worker下一守卫后的效果计数0，新处理器1次，总领取2次

真实部分是上游 Store SQL、PGlite、ActionService、TaskWorker；受控部分是输入、时钟、处理器和提供方fixture。没有真实邮件、日历、模型或电脑服务。上游版本fixture只验证保存版本传入execute，不验证Google的HTTP If-Match冲突。关闭再打开不等于崩溃或断电验收；网络guard不是操作系统级隔离。

练习包固定SHA-256：714ca8560289c4ec076a6b0ecb87a6c40b921fadd12c62cec89142d878994157。内含原样选取源码、MIT LICENSE、完整依赖锁与原始日志。PDF和HTML给出六步命令、目的、成功验证和失败判据；实验日志保留初次依赖恢复过程和独立复跑原始输出。
