# Codex advanced 协议与配置知识笔记

历史学习日期：2026-10-05 UTC。本文保留固定来源、公开知识关联、历史实验和适用边界。本次公开整理未重跑实验；动态文档结论只对应当时核查，不代表永久规则。

本提案聚焦Codex接口、配置与协议的可核验证据。原视频未观看，不把独立官方资料学习写成视频复现；无账户小实验也不能证明订阅权益、真实模型任务或跨产品集成已经成功。

## 1. 查重范围和结果

固定公开索引含394条元数据，实际全文读取并核验24篇相关公开笔记，其余370篇只查元数据。公开索引固定于Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352；相关公开正文固定于1043e9d6080bff7af9724162e2c44559fab63e40。

在历史公开索引标题/路径和24篇公开正文中，没有找到Codex advanced/app-server的既有完整学习项目。名称检查覆盖英语、简繁体中文、空格/下划线/连接符变体。已有codex_quota_mcp、codex-dual-home、openai-agents-api等相关项目，所以本轮应增补接口与配置证据，而非重做旧项目。

该结论仅针对历史快照的实际阅读范围，不覆盖其他版本或370篇未读正文，不能写成“全库无重复”或“从未学过”。笔记存在也不等于读者已经掌握。

## 2. 先复用已有概念

- [[codex_quota_mcp]]、[[规划执行分账]]：复用按任务阶段安排工作的思想；旧模型、价格、次数、比例和节省金额是历史材料，不代表当前权益。分阶段本身不保证分属不同计费池或必然省钱
- [[上下文接力]]、[[产物留痕与状态外置]]：用文档显式保留目标、约束、决定、证据和验收条件。接力仍可能丢失或过时，不能承诺“零损耗”
- [[CODEX_HOME多实例隔离]]、[[codex-dual-home]]：复用状态与配置隔离视角。目录不是身份本身，换目录不增加额度，也不构成OS沙箱；历史版本和本机行为不能直接移植到当前实验
- [[AgentHarness智能体挽具]]、[[openai-agents-api]]、[[托管Harness与会话即资源]]：只作架构关联。app-server、CLI、MCP服务器、Agents SDK和托管API的对象与方法须分别核对
- [[OAuth资源发现]]：仅说明远程MCP资源元数据发现，不能代替Codex认证流程或用户账户权限证据
- [[Agent输出协议契约]]、[[单一馈送与schema冻结]]：复用结构校验与版本演进思路，但未知字段是否允许应由本项目实际schema决定
- [[Provider适配层与错误契约]]：区分协议格式和服务方；特定框架的错误处理契约不能成为Codex规则，兼容API外观也不保证完整可替换
- [[沙箱与审批正交]]、[[沙箱三态与Executor]]、[[代码管边界提示词管判断]]：把执行环境、系统边界、审批和当次授权分开，不拿字段声明当实际授权

## 3. 优先增补：解析、契约与运行结果分层

一句话定义：数据可解析、符合目标版本的结构契约、满足协议状态与权限、最终完成任务，是需要独立证据的不同判断。

领域：协议工程、配置管理、软件验收。

普通例子：一份JSON文本能被读取，只证明语法可解析；某字段类型符合schema，并不证明引用的资源存在、调用顺序正确、账户有权益或执行环境允许操作。一次schema通过也不证明模型真的运行。

知识关联：[[Agent输出协议契约]]、[[证据优先质检ProofOverClaims]]。已有Qwen项目已经补充解析与语义校验，Patchright项目已经补充配置转发与实际生效，本轮应追加Codex实例，不再另造同义“验证分层”条目。

合并时应保留输入、schema版本、被调用的真实程序、预期拒绝层、实际错误和未测项。若测试运行的是独立验证器，写“schema检查”；若运行真实服务进程并收到响应，写清实际请求/响应范围；两者不能互换。

本节是方法与合并建议，具体方法名、字段和实测数量须以本轮官方来源及实验日志为准。

## 4. 项目案例：身份、权益、路由与环境分别核对

一句话定义：谁在调用、可使用哪项服务、请求交给哪个提供方、动作在哪里及按什么权限执行，是四类不同问题。

领域：系统集成、认证授权、故障定位。

普通例子：配置中的服务地址格式正确，不证明网络可达；认证成功，不证明某模型可用；服务权益满足，不证明当前文件或网络操作得到许可。诊断应记录失败层，而不是把所有失败写成“账号坏了”。

关联：[[OAuth资源发现]]、[[Provider适配层与错误契约]]、[[控制面与数据面]]、[[沙箱与审批正交]]。AI Native已有知识区分发现、批准与当次执行，可直接互链；Metrik已有知识区分本地用量、官方额度、估算费用与真实账单，也可只作关联。

合并建议：优先作为Codex项目的排查框架，不因换了四格图就新建同义概念。若目标知识库已有同义内容，增补此例即可。范围内未进行真实登录或账户调用，就应明确保留未知，不能以无凭据错误响应推断用户实际权益。

## 5. 优先增补：配置整体版本化与证据定位

一句话定义：可复现结论需要同时固定程序/源码、schema、配置、输入和验证方法，而非只记一个产品名字。

领域：可复现工程、版本管理、接口升级。

普通例子：两个同名字段在不同版本中可能有不同枚举、默认值或生命周期；一个旧文档允许的输入，可能在新schema中被拒绝。必须把观察绑定到实际版本，不把历史默认值推广成永久规则。

关联：[[单一馈送与schema冻结]]、[[产物留痕与状态外置]]、[[证据状态机]]。Qwen已有“模型检查点与提示协议一起版本化”的项目案例，可作相关链接，但模型配置与Codex协议并非同一种机制。

增补方向：记录版本与来源链接、文件指纹、合成样本身份、完整命令、原始响应和检查结果。指纹证明文件相同，不证明其中所有事实或设计都正确。未知字段容忍策略按具体schema验证，不能从另一个项目的兼容原则直接推断。

## 6. 优先增补：无账户实验的正向价值与结论边界

一句话定义：使用固定官方代码或契约配合合成输入，可验证明确的本地接口行为；未连接的账户、模型、服务和部署环节仍须另行验收。

领域：可测试性、接口研究、实验设计。

关联：[[接缝与桩实现StubSeam]]、[[证据优先质检ProofOverClaims]]。既有Colab、Qwen、Patchright和NCE记录已充分区分本地组件、替身与真实服务。本轮只加一个范围更精确的Codex案例，不重复建立“mock不是端到端”同义概念。

检查正向样本时说明实际接受层；检查负样本时说明拒绝来自解析器、schema、协议状态或其他层。故意错误被观察到可以是测试符合预期，不能据此宣称系统整体安全。测试只运行到哪里，结论就写到哪里。

原视频、个人订阅、真实模型任务、付费API、托管环境、性能节省与跨产品接力，都不因小实验成功而自动获得验证。本轮若只读到官方说明，就标“官方说明”；只审源码就标“源码观察”；没有运行就保留“未实测”。

## 7. 本轮实际实验与来源

官方源码固定为 openai/codex@823ea830c0fd418b09ff02d36cad9a1fff66465b，保留未经改写的 ConfigToml 与 ClientRequest 两份 Draft-07 schema，以及 Apache 2.0 LICENSE 与 NOTICE。每份原文用 Git blob SHA-1 和 SHA-256 核验。实验运行的是 Python 3.12.14、jsonschema 4.26.0、referencing 0.37.0；没有执行 Codex CLI 或 App Server。

独立 ZIP 新解包后的六步实测：配置 9 项（3 接受、6 schema 拒绝），协议 13 项（5 接受、8 schema 拒绝），坏文本 3 项（3 解析错误）；全量 25 项均符合预期。拒绝反例也显示 PASS，含义是预期与观察一致。完整命令、输出、错误路径和逐步耗时见同包实验日志；不把结果复写成在线运行成功。

明确的新案例：配置未知顶层键和 Provider 键被拒绝；所测协议 envelope/ClientInfo 的额外字段却被接受。合成模型名及不存在的 threadId 可以通过形状校验。未知字段策略必须精确到目标 schema 与对象，不是统一的“宽容输入”原则。

2026-10-05 的官方资料核查还揭示两类版本陷阱：项目级 .codex/config.toml 中 model_provider 与 model_providers 会被忽略；untrusted 审批策略在核查日文档中标为退役。以上是文档结论，未做运行时加载或安全设置实验。固定 schema 里的字段和枚举不自动成为当前建议。

认证与集成方面，官方支持明确授权的 ChatGPT 登录集成，但有应用类型、作用域与使用条件；不是通用免费 API。model/list 可能是内置目录，不是账户模型权限的证明。本轮没有登录、令牌操作、模型目录读取、推理或账单核查。

### 官方依据

- [认证与用量路线](https://learn.chatgpt.com/docs/auth)
- [Cloud 运行环境](https://learn.chatgpt.com/docs/cloud)
- [配置基础](https://learn.chatgpt.com/docs/config-file/config-basic)
- [高级配置](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [App Server 对象与生命周期](https://learn.chatgpt.com/docs/app-server)
- [有明确授权边界的 ChatGPT 登录集成](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server)
- [固定 ConfigToml schema](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/core/config.schema.json)
- [固定 ClientRequest schema](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/app-server-protocol/schema/json/ClientRequest.json)

## 8. 复用建议与边界

先核对目标知识库中的同义概念，保留已有编辑；同义合并，相关互链。项目笔记应保留精确接口与版本、历史实验范围、逐项结果和未测项。

来源、输入、完整命令、原始输出、练习代码与独立审核应一同保留。不要从旧项目复制测试数量、耗时、账单、平台能力或默认配置，也不能将静态契约验证写成真实运行时成功。

## 9. 实际全文核验的公开知识来源

以下24篇正文均固定于1043e9d6080bff7af9724162e2c44559fab63e40，仅作为查重和概念关联。历史外部事实未在本轮逐项重新验证，不附公开正文全集或私人原文。

1. [AgentHarness智能体挽具](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AgentHarness%E6%99%BA%E8%83%BD%E4%BD%93%E6%8C%BD%E5%85%B7.md)
   UTF-8 2913 字节；SHA-256 6ea191b1ea84eb9ba3c53db9b02a55450af255775dc2006fc8cba7df72126014

2. [Agent输出协议契约](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Agent%E8%BE%93%E5%87%BA%E5%8D%8F%E8%AE%AE%E5%A5%91%E7%BA%A6.md)
   UTF-8 1742 字节；SHA-256 85b2ef5207651ba4807bd3da205a45c72c1fe38a5cb8ce91a052f66dea5bba4e

3. [MCP协议](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/MCP%E5%8D%8F%E8%AE%AE.md)
   UTF-8 1720 字节；SHA-256 f241531981004f1580b331a37b9e38ca96875e368ac03d687aab199daac284d6

4. [MCP模型上下文协议](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md)
   UTF-8 1683 字节；SHA-256 ae666167533a8ad49319a380b3b4fbcd54c7153c5f019b6eee275440f6809aef

5. [OAuth资源发现](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/OAuth%E8%B5%84%E6%BA%90%E5%8F%91%E7%8E%B0.md)
   UTF-8 1438 字节；SHA-256 6f7d1027e1144482b6484afbad0834b13101e9ffa2299e9216d88a80863ca9fb

6. [Provider适配层与错误契约](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Provider%E9%80%82%E9%85%8D%E5%B1%82%E4%B8%8E%E9%94%99%E8%AF%AF%E5%A5%91%E7%BA%A6.md)
   UTF-8 3175 字节；SHA-256 6747c71d9ab9e007e5dd35330e4c733613e111498b987fdca973828259503986

7. [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)
   UTF-8 2389 字节；SHA-256 6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb

8. [代码管边界提示词管判断](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%A3%E7%A0%81%E7%AE%A1%E8%BE%B9%E7%95%8C%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%AE%A1%E5%88%A4%E6%96%AD.md)
   UTF-8 1427 字节；SHA-256 82baf8f30c908b3ea424d15f82b6d3124e40b3c1b023961bfd0c8abd1eb8b86d

9. [托管Harness与会话即资源](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%89%98%E7%AE%A1Harness%E4%B8%8E%E4%BC%9A%E8%AF%9D%E5%8D%B3%E8%B5%84%E6%BA%90.md)
   UTF-8 2905 字节；SHA-256 596bf0d1e5d38c769bf4b5fd6baa8201a7c442bd23c237fc2338218bac8d49fa

10. [接缝与桩实现StubSeam](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A5%E7%BC%9D%E4%B8%8E%E6%A1%A9%E5%AE%9E%E7%8E%B0StubSeam.md)
   UTF-8 1752 字节；SHA-256 83decb2724ea3ac736e0f9c4c89e17e043504be4733162e6ee44d7988c976804

11. [控制面与数据面](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A7%E5%88%B6%E9%9D%A2%E4%B8%8E%E6%95%B0%E6%8D%AE%E9%9D%A2.md)
   UTF-8 1575 字节；SHA-256 90267f9bf8041185daf02ce384e1367c4c8e3ed32beccf4dc6ae7ae9c7ef7409

12. [沙箱三态与Executor](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%89%E6%80%81%E4%B8%8EExecutor.md)
   UTF-8 2157 字节；SHA-256 4d1113c17b1c8a8568ad3b44e73c7393ff7f7b4a6be44c3cd5bc3e620b1107a1

13. [沙箱与审批正交](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%8E%E5%AE%A1%E6%89%B9%E6%AD%A3%E4%BA%A4.md)
   UTF-8 3248 字节；SHA-256 a9e65c39d85a821884b50e6e2a4a1a1944cd18c4fd7961cb8a6c9f65cd645a41

14. [能力运行时](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%83%BD%E5%8A%9B%E8%BF%90%E8%A1%8C%E6%97%B6.md)
   UTF-8 1411 字节；SHA-256 1341c5c402b01ed0cc6641b8b4ba4b9be0024c03ec443b2300e0453bbe121678

15. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   UTF-8 3593 字节；SHA-256 c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

16. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   UTF-8 2488 字节；SHA-256 4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

17. [codex-claude-resets](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/codex-claude-resets.md)
   UTF-8 3316 字节；SHA-256 515198a3054222a95894759eba570680f28a09d66442c7c866e9e20ff5169e22

18. [codex_quota_mcp](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/codex_quota_mcp.md)
   UTF-8 2699 字节；SHA-256 664c96a58fcbd5e6f32a71ab98fa344c400f1e22ae11d85f67ea0af5f9225d74

19. [openai-agents-api](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/openai-agents-api.md)
   UTF-8 5012 字节；SHA-256 c80e7aabc79f801648b54771f77ea335a35e8201defd7d9ba80b2b6a90007ba9

20. [CODEX_HOME多实例隔离](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/CODEX_HOME%E5%A4%9A%E5%AE%9E%E4%BE%8B%E9%9A%94%E7%A6%BB.md)
   UTF-8 1795 字节；SHA-256 81725a3e1b2a365f520c0aca258dfb9dfd6d2ad7d8475a70320079f37244f4f1

21. [上下文接力](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%B8%8A%E4%B8%8B%E6%96%87%E6%8E%A5%E5%8A%9B.md)
   UTF-8 1770 字节；SHA-256 7ab2e857b835ba0f5d0b30fd83c622675a1e1e6f67b1f5538892e15158cb0123

22. [单一馈送与schema冻结](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8D%95%E4%B8%80%E9%A6%88%E9%80%81%E4%B8%8Eschema%E5%86%BB%E7%BB%93.md)
   UTF-8 2063 字节；SHA-256 f64efd7b90ed3b9ada3c19c50e350d1ef9676fb0229f254155a5f170eb854425

23. [规划执行分账](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%A7%84%E5%88%92%E6%89%A7%E8%A1%8C%E5%88%86%E8%B4%A6.md)
   UTF-8 1862 字节；SHA-256 0173aafd60db7d2be2c4be99da544a7297eb31b11750131ce2c92f28e9070439

24. [codex-dual-home](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/codex-dual-home.md)
   UTF-8 2086 字节；SHA-256 cd09e5b3e63813c7fb6f532c6bd15a22e97213baa0cd7d441fd68c201eac504e
