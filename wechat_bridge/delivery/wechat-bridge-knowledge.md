# WeChatBridge 用户主动分享批次交接与结果边界知识笔记

日期：2026-10-05 UTC。本稿结合已核验知识、固定源码与真实Linux核心组件实验：自建42个用例全部通过，独立审核者从冻结ZIP新解包后复跑同42个用例亦通过。收获是分清捕获来源、批次可见性、动作请求与目标实际效果。本文保留历史固定来源、公开知识关联、组件实验与未测项；本次本地副本整理未重跑实验。

## 1 查重范围

公开索引固定于Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352；相关公开笔记正文固定于1043e9d6080bff7af9724162e2c44559fab63e40。

索引共394条元数据，本轮全文读取并核验15篇相关公开笔记，其余379篇仅元数据检索。

WeChatBridge、wechat_bridge、WeChat-Bridge在上述元数据和已读正文中无名称命中。该历史公开范围不覆盖其他版本或379篇未读正文，不能称“全库无重复”。笔记存在不等于读者已掌握，哈希一致不证明历史事实正确；不借用旧产品版本、默认配置、星标或实验数量为本项目背书。

来源：[固定知识索引](https://github.com/Smashwinny/reminder_knowlege/blob/1f61909da967cea8bc68dbfaffc642a4331b3352/reminder-dot/cloud-reference/knowledge-index.json)。

## 2 先区分项目，再复用概念

[[wechat_hermes_notebot]]已有“消息入口→常驻Agent网关→专用profile→原样笔记/Git同步”。本项目解决另一种入口：用户主动选择聊天并让微信导出ZIP，再通过系统分享交给本地批次及目标应用。它不是持续收信bot，不通过读取微信数据库来获得记录。[[wechat-ai-memory]]的导出/规范化、[[wechat-intelligence-hub]]的只读分析只作路线关联，旧项目实验不构成本项目集成证据。

优先复用[[原样捕获与工序分离]]、[[Agent网关与消息通道]]、[[产物留痕与状态外置]]、[[证据状态机]]、[[工具调用生命周期]]、[[沙箱与审批正交]]及[[证据优先质检ProofOverClaims]]。Easel已有薄索引和多层状态；OpenMuse已有精确审批、幂等键与未知外部结果；不另造一批同义“安全/恢复/证据”概念。

固定源码：[freestylefly/WeChatBridge@07b88822debc3bd544ae7a83bc207633b29c3a04](https://github.com/freestylefly/WeChatBridge/tree/07b88822debc3bd544ae7a83bc207633b29c3a04)。第3至7节的机制说明以固定源码为依据；具体已执行用例在第8节单列。编译或某个测试通过，不代表全部机制、原生UI或端到端链路通过。

## 3 增补原样捕获：原始归档、转换产物和模型解释分层

一句话定义：把用户主动导出的原始文件作为可追溯输入保留，转换文本/Markdown与模型解释分别作为后续派生产物，不用摘要覆盖来源。

领域：知识捕获、数据来源与格式转换。优先增补[[原样捕获与工序分离]]，与[[产物留痕与状态外置]]互链。

WeChatBridge的批次收集账本引用原ZIP，集合本身不把它们重写合并为一份新ZIP。保留归档便于重新核对，但“保留导出文件”不等于微信里的全部聊天被完整导出，也不等于TXT解析、附件提取和Markdown渲染没有损失。

教学例子：保留两份虚构聊天ZIP及其来源顺序，再另存整理结果；如果结果漏了附件，可回到源ZIP定位遗漏工序。此次实际夹具是两条虚构中文消息和64字节sample.bin二进制附件，stored/deflate两种压缩形式包含同一份内容。sample.bin不是图片，没有验证真实图片/视频渲染。

旧[[原样捕获与工序分离]]把“只保存不执行”称为天然免疫提示注入，应收窄：捕获阶段不执行内容能减少风险；后来模型读取同一内容时，它仍是不可信资料，仍需最小权限、指令/数据分离和敏感行动检查。保真不是授权。

来源：[批次收集账本](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Collections/BatchCollection.cs)、[项目定位](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/README.md)。

## 4 增补产物契约：清单、意图、状态分别存放

一句话定义：清单描述这一批有哪些文件，意图说明这次请求什么动作，状态记录本地处理进展；三个对象各有生命周期，不能互相代替。

领域：文件协议、进程交接、可追溯性。优先增补[[产物留痕与状态外置]]，互链Easel项目的薄索引与工序状态案例。

Windows Core的manifest包含schema版本、批次GUID、UTC时间、动作，以及文件GUID、显示名、相对路径、内容类型、字节数和来源索引；intent保存一次性动作请求；state保存结果、目标、聊天名、场景等后续状态。条目GUID由随机生成，不是内容哈希；该manifest也没有文件摘要字段。

自写例子：同一ZIP再次导入生成另一批次GUID，两个批次可以包含相同字节。集合SeenBatchIDs防止同一批次ID再次追加，但不能据此断言它按聊天内容去重。[[内容寻址与镜像分层]]是“以内容摘要寻址”，这里只作对比，不将两者合并为同义概念。

字节数和路径也不是签名、身份认证或文件完整性的证明。清单写成功、文件能读取、ZIP结构/CRC有效、解析语义正确、目标确实接受，需要逐层检查。

来源：[InboxModels](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/InboxModels.cs)、[BatchState](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/BatchState.cs)、[集合去重](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Collections/BatchCollection.cs)。

## 5 项目案例：原子发布只保证它覆盖的边界

一句话定义：先在不可见的暂存区写完整一批文件，再用一次目录移动将其发布给消费者，可以把“半成品可见”与“完整批次可见”分开。

领域：文件系统协议、批次发布、故障恢复。先作为项目案例增补[[产物留痕与状态外置]]，复用前查重“staging/ready、原子发布、原子批次”，再决定是否独立成篇。

StageAsync在Staging复制文件并写manifest，CommitAsync补intent和可选初始state，最后Directory.Move到Ready；Reader只枚举Ready。这个结构使常规消费者在发布前看不到暂存批次。它没有让剪贴板、目标应用、模型服务与文件系统加入一个共同事务；也不能仅靠源码阅读证明断电持久性或跨文件系统原子性。

共享文档写“校验ZIP”，但此固定Windows StageAsync的输入校验检查存在、重解析点、扩展名和大小，并不解析ZIP结构或CRC。文件接收与归档解析是分开的检查位置，不能把它们压成一个笼统“已验证”。

本轮S06实际观察到：23字节的not-a-zip.zip可以被InboxWriter提交至Ready；另一个归档校验用例拒绝同一内容。这个有限负例证实接收层与解析层是不同检查位置，不将其扩大为所有归档格式或全部安全分支均已覆盖。

来源：[StageAsync/CommitAsync](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/InboxModels.cs)、[共享契约](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/shared/README.md)。

## 6 项目案例：一次性意图不等于恰好一次外部效果

一句话定义：消费后删除的短期请求能减少常规重复触发，但不能单独证明目标动作既不遗漏也不重复。

领域：动作交接、重试语义、外部副作用。优先增补[[工具调用生命周期]]和[[证据状态机]]，关联OpenMuse已有幂等键/未知结果案例。这里的“一次性交接”是批次动作请求，不是[[Handoff交接简报续跑]]里的跨对话上下文摘要，名称相近也不应合并。

ConsumeIntent先读取并删除intent文件，再解析和检查新鲜度。I01用注入时间RequestedAt+89秒得到Ready，顺序再次消费及同一进程中新建Reader后得到None；I02在注入的恰好+90秒得到Expired并消费文件。IsFresh条件是age<90秒；I06把RequestedAt设成注入当前时间之后1小时，实际得到true。它没有检查时间非未来的下界。这是本地新鲜度判断，不能当身份验证、完整防重放令牌或下游幂等键；这些用例没有真实等待89/90秒。

读取和删除不是原子claim，源码注释里“第二个窗口永不重放”不能代替并发测试；删除后、动作前崩溃也可能留下未执行动作。这里不宣称已发现或已验证可利用漏洞，只限定证据范围。

自写例子：一个请求已被删除，随后进程退出。文件已不可再次消费，仍不能推知目标是否收到了附件。应核对目标现状和状态证据，再由用户决定重试，不能自动把“请求消失”显示成“处理完成”。

来源：[ConsumeIntent](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/InboxReader.cs)、[BatchIntent](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/ShareAction.cs)。

## 7 增补证据状态：可以重试不等于上次没有效果

一句话定义：本地保存、粘贴请求、目标接受、上传完成和模型处理是不同事件；状态标签必须按实际观察层解释。

领域：验收设计、恢复流程、未知结果处理。优先给[[证据状态机]]和[[工具调用生命周期]]补案例，与Easel展示状态、OpenMuse outcome_unknown互链，不新建同义“失败恢复”笔记。

CollectionService.Freeze检查成员存在和聊天名，保存Delivering再返回冻结批次；重启加载会将遗留Delivering变为Retry，并提示先确认目标附件。原ZIP保留让恢复可行，但Retry不等于上一轮肯定没有粘贴。

固定BatchOutcomeKind.Delivered的口径是激活目标App并粘贴；DeliveryEngine在按键注入流程之后登记成功。这不是收件服务器回执，也不证明目标模型已读取、已上传或已输出分析。目标App可能吞掉粘贴，代码自身也把这一点列为产品层差距。

本地优先同样有边界：Share Extension缺乏网络权限，不意味着接收文件的AI App永不联网。把聊天交给特定目标前应核对具体内容、接收应用及其后续数据处理方式；本地归档路线与AI传递路线不能共用“数据永不离机”的总承诺。

来源：[集合冻结](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Collections/CollectionService.cs)、[中断恢复](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Collections/BatchCollection.cs)、[投递实现](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Delivery/DeliveryEngine.cs)。

## 8 本轮实际实验与独立重放

环境为Linux x86_64、Debian 13，官方.NET SDK 10.0.401、运行时10.0.12。将固定提交的46个Windows.Core源码、项目与资源文件逐字节纳入练习，上游模块未修改，自建harness直接调用真实核心实现；没有用仿写的ZIP解析器或状态机代替上游。构建输出0 warnings、0 errors，没有外部NuGet包依赖。SDK按官方归档SHA-512核验，保留MIT许可及第三方声明。

主实验有六条实际执行命令，依次为setup、verify、fixtures、build、test、report，均通过。作者六步重放中的测试发生于2026-10-05 14:27:56–14:27:57 UTC；独立审核者于14:29:43–14:29:54 UTC从冻结ZIP新解包，按相同六条命令重新执行并全部退出0。独立重放复用了已下载的官方SDK，但重新核对归档摘要及4,907个SDK普通文件，没有复用旧构建产物或缓存。最终冻结包核对104项清单文件及46项未修改Core文件；早期作者阶段清单71项不是最终包口径。

42个用例都是此次自建harness针对真实上游的定向检查，不是完整上游xUnit或macOS测试套件：

- 21项归档检查：stored/deflate解析与精确附件字节、中文多行/BOM/CRLF、未知TXT不捏造消息、仅附件归档的未知消息数，以及空/损坏/CRC/加密标记/超限声明/不支持方法/重复条目拒绝；还覆盖路径越界、绝对路径、符号链接条目、大小写别名、安全目标目录、取消及非法日期等指定夹具
- 8项暂存检查：发布前Reader不见Staging，提交后Ready可见且源ZIP摘要保持；同名文件改名不覆盖；非法第二项回滚、注入单文件/总量限制、扩展名不等于有效ZIP、预取消和来源符号链接拒绝
- 6项意图/状态检查：注入+89/+90秒边界、顺序消费与新Reader不重放、损坏意图删除、首次状态及上下文持久化、Copied仅模型元数据、未来时间被单边新鲜度条件接受。没有调用剪贴板API
- 7项收集检查：冻结顺序和原件摘要、冻结期间拒绝编辑及迟到批次分组；新建CollectionService加载磁盘账本后Delivering变Retry且同批次不重复收集；移除/撤销恢复字节与顺序、手工构造的中断移除磁盘状态恢复；schemaVersion=8账本被拒绝且未覆盖；显式聊天名要求；保护中的收集不被保留期清理，即使对应manifest不可读

作者最终42/42通过，独立审核42/42通过，失败均0。这是同42个用例的独立重放，不能相加写成84个不同用例。结果只覆盖列出的输入和分支。初次harness执行41/42：I05错误比较保留小数秒的内存时间与上游按整秒保存的JSON时间；修正仅发生在自建断言，改为比较两个持久化时间值，上游指纹未变。原失败和修正后的原始日志均保留。初次计时也因/usr/bin/time不存在失败，随后使用实际可用计时方式，不借此改动上游。

恢复检查是在同一测试进程内新建Reader/Service并重读磁盘状态，部分中断状态由harness显式构造，不是进程强杀、断电、跨机或多消费者并发故障注入。路径安全测试也不是穷举安全审计。新建服务后出现Retry只证明状态转换，并没有制造或观察真实重复粘贴。

练习包含20个合成输入文件，冻结参考报告列出68个本次生成的普通输出文件指纹。随机GUID、绝对路径和运行时间会改变，一次运行的完整输出摘要不要求在重放中逐位一致；源文件与合成输入摘要按指定清单核验。参数、每步命令、UTC时间、断言、原始结果和失败判据保留在实验日志、练习包及独立审核日志，不把组件耗时当产品性能基准。

历史原始ZIP为194,829字节，SHA-256：217652744cb061165213920046b3ee319f416f7fd3a800107c99bbbe239a7842。当前副本只规范化路径与整理说明，当前 ZIP 指纹见实验日志。

证据定位：练习包reference/six-step-test-results.json、reference/six-step-experiment-report.json及EXPERIMENT_LOG.md保存作者记录；同组交付的审核日志记录新解包后的六条命令与独立结果。

## 9 未测边界与复用建议

未执行macOS Share Extension、辅助功能/OCR/App Group签名；未执行Windows WPF、Share Target、Win32前台控制和剪贴板/粘贴；未读取真实微信数据库或真实聊天文件；未写个人知识库；未向真实目标Agent投递、上传或请求推理。Windows目录、共享协议表及Linux核心构建不能证明macOS/Windows全部功能等价。Delivered的目标App激活/粘贴口径属于源码观察，不是本轮已验收的原生效果。

未测试并发消费者、端到端恰好一次、真实进程崩溃/断电持久性、跨卷目录移动或未知外部效果对账。顺序consume-once、新对象恢复、保留原ZIP与Retry入口是分别成立的有限结果，不应合并为“永不丢失、永不重复”。本地处理也不证明下游AI App不联网或不上传。

复用时先核对目标知识库中的同义条目与已有编辑，保留历史版本和案例。优先修正原样捕获笔记中的“天然免疫”绝对说法，再补产物契约、分层验证与不确定结果案例。同义内容合并、相关机制互链，不能用组件结果代替原生端到端验收。

## 10 本轮全文核验的公开知识

原样捕获与工序分离；Agent网关与消息通道；wechat_hermes_notebot；wechat-ai-memory；wechat-intelligence-hub；产物留痕与状态外置；证据状态机；证据优先质检ProofOverClaims；接缝与桩实现StubSeam；沙箱与审批正交；本地优先与文件监听；Handoff交接简报续跑；内容寻址与镜像分层；提示注入；工具调用生命周期。

这些正文均固定于[公开知识版本1043e9d](https://github.com/Smashwinny/reminder_knowlege/tree/1043e9d6080bff7af9724162e2c44559fab63e40/vault)，可在该固定版本的 vault 目录按上述笔记名称查阅。教学稿只保留相关公开知识的来源与关联。
