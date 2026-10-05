# AI Native 企业 Agent 基础设施知识笔记

历史学习日期：2026-10-05 UTC。本文保留固定来源、相关公开知识与历史教学实验结果。公开整理未重跑实验；知识关联用于复用，不代表读者已经掌握。

## 学习范围与知识查重

来源是《AI Native 研发范式实践手册》第三章“基础设施”，印刷 pp33–61 / PDF 38–66，共29页。官方文件共68页；没有声称全书精读。文件 27,286,928 字节，SHA-256：6929f3e9e57fef9550129d457ba82ac40a4a9368e1c5926c6ac2206d8aaeced3。

[官方 PDF](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf)

固定公开知识索引 394 条元数据，全文读取并核验36篇相关概念/项目笔记，其余358篇仅元数据。

公开知识索引提交：1f61909da967cea8bc68dbfaffc642a4331b3352。相关公开正文提交：1043e9d6080bff7af9724162e2c44559fab63e40。此范围仅描述原学习时实际读取的公开快照，不是整个知识库的全文覆盖，也不代表其他版本已经核验。

## 1. 优先增补：任务授权与委派范围逐级收缩

一句话定义：Agent 的每次行动都要落在用户权限、Agent 能力上限、平台策略、本次委托及运行限制共同允许的范围内；子任务取得的权限不能超过父任务。

领域：Agent 基础设施、最小权限、委派治理。

已有知识：[[AgentHarness智能体挽具]] 已包括最小权限与停止条件；[[多智能体协作]] 和 [[子智能体咨询]] 已讲分工与预算；[[代码管边界提示词管判断]] 已强调执行层硬边界。因此不重复建立“Harness”或“多 Agent”同义笔记。新增案例重点是“用户有权”不自动等于“Agent 有权代做”，以及每一跳委托的收缩与可核查责任。

例子：用户允许父任务读取虚构项目A的说明与附录。负责检查附录的子任务只得到附录的 read 权限和更短有效期；它不能读取另一项目B，也不能因为父任务工具菜单里存在 write 就拥有写权限。主体、任务和环境名称只是标识，真实部署还需要可信身份与授权证据；本例字符串本身不提供身份认证。

建议先并入 [[AgentHarness智能体挽具]] 的权限小节，并链接 [[子智能体咨询]]、[[沙箱与审批正交]]。只有确认确无同义内容，才考虑独立“委派权限收缩”条目。

来源：[印刷 p53 / PDF 58](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=58)。这是手册的架构原则；是否由具体产品实现仍需逐项验证。

## 2. 优先增补：发现、批准与当次执行分层

一句话定义：工具可发现、请求曾被批准、当前资源调用可执行，是不同状态；执行点必须根据真实目标和当前授权重新检查。

领域：工具安全、策略执行、接口治理。

已有 [[LLM工具调用]]、[[工具调用生命周期]]、[[MCP协议]]、[[MCP模型上下文协议]] 已足够解释菜单与调用；MCP Toolbox 的既有实验证明 readOnlyHint 不会替代数据库权限。本次不重复 readOnlyHint 对照，而补充身份、委托、策略决策和下游凭证的职责分离。

身份认证回答主体是谁；委托说明为何可代表用户；策略授权判断当前能做什么；凭证让下游验证一次准入。模型输出的资源名、自报“已批准”或成功 OAuth 登录，均不能省略工具/动作/资源层面的执行检查。

示例：能列出 read_document 不代表能读取任何文档；曾允许项目A，不代表目标改成项目B后仍可沿用原结论。进入处理函数前与真实打开资源前，应有明确的可信判定链。

合并方向：[[工具调用三段式流水线]] 增补调用前检查，[[控制面与数据面]] 增补资源侧复核；与 [[Agent输出协议契约]] 互链。两个旧 MCP 条目应检查同义合并，不再新增第三种同义命名。

来源：[印刷 pp51–53 / PDF 56–58](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=56)。

## 3. 优先增补：权限撤销与运行生命周期联动

一句话定义：授权不仅有有效期，还要在撤销、任务结束、运行环境关闭或风险变化时停止新的使用，失效相应缓存及凭证，并处理已建立的下游会话。

领域：权限生命周期、运行平台、故障与风险控制。

已有 [[工具暴露单调性]] 已说明工具名可保留而每次 handler 必须实时检查权限；[[托管Harness与会话即资源]]、[[沙箱三态与Executor]]、[[产物留痕与状态外置]] 已说明会话、环境与持久产物分层。本轮增量是把父子委托状态、当前运行实例和资源执行时点连起来。

短有效期只缩小滥用窗口，不能代替主动撤销。真实系统还应停止签发、清除多层允许缓存、处理下游会话与长连接。撤销不能让已经返回的内容自动“没被看过”；顺序单进程测试也不能证明跨服务传播延迟或中断正在执行的请求。

例子：根委托曾成功读取。撤销之后，用原根委托或原子委托再请求都应拒绝；仅界面显示 revoked 不够。重新创建新的根委托也不应无条件复活旧子委托。

合并方向：优先给 [[工具暴露单调性]] 加撤销验证案例，链接 [[沙箱与审批正交]] 和 [[托管Harness与会话即资源]]，再决定是否值得独立成概念。

来源：[印刷 p52 / PDF 57](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=57)、[印刷 p53 / PDF 58](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=58)。

## 4. 项目案例：结构化的补充授权请求

一句话定义：缺少批准时，系统返回明确的待授权状态，暂停执行，并让用户或资源负责人在可信界面确认主体、资源、动作与时效。

领域：人机协作、权限协议。

手册区分 allow、deny 与 challenge。challenge 不是让模型猜一条403报错，更不是允许模型自行编造“确认完成”。它应携带需要谁确认、确认什么、何种方式与有效期，模型只收到高层状态。

合并方向：作为 [[Agent输出协议契约]] 与 [[代码管边界提示词管判断]] 的授权接口案例。不要把业务返回403自动等同为可交给模型继续绕行的挑战。

来源：[印刷 p54 / PDF 59](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=59)。本次教学程序只实现 allow/deny，没有实现 Challenge 或真实审批界面。

## 5. 团队资产治理不代替资源授权

一句话定义：知识、Skill、规则与工具配置需要来源、版本、责任人、评审和更新机制；它们被分发或加载，并不自动批准后续操作。

领域：团队 Harness、知识治理、软件供应链。

已有 [[团队Harness的Git原生分发]]、[[资源命名空间分发]]、[[teamai-cli]]、[[AgentSkills技能包]]、[[技能路由器与授权硬门]] 可直接复用。增补“角色订阅与 namespace 控制资产分发，资源权限由执行点另行判断”。一个 skill 经PR评审并不自动授予数据库写权限。

[[WikiSkill共演化循环]] 与 [[知识层永不回滚原则]] 是特定研究方法，不能泛化为知识不会错或永不删除。企业知识仍需纠错、撤回、分级访问与来源追溯。工具返回与检索材料中的指令不能自行获得更高权威。

来源：[印刷 pp37–42 / PDF 42–47](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=42)。该段依据来源研究者逐页阅读核对；旧项目的历史星标数、版本、厂商服务条件和实验表现未在本轮重验。

## 6. 可观测性增补：权限决定也要成为证据

一句话定义：将任务、Agent、运行实例、委托、工具、资源、策略版本、允许/拒绝原因和实际执行结果关联起来，才能复查动作是否按当时规则发生。

领域：可观测性、审计、验收。

已有 [[JSONL事件日志与折叠模型]]、[[产物留痕与状态外置]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]。本轮新增权限与撤销路径的关联，而不是再次解释 JSONL。不要仅记录“调用成功”，还应记录“因哪条规则拒绝、是否实际触达资源”。

JSONL 不天然防篡改、不天然完整、不自动支持乱序/幂等；合成日志也不证明模型自主执行。系统健康指标、行为轨迹和任务结果是不同层面。审计只保留必要元数据与脱敏引用，避免凭证和完整业务内容进入一般日志。

来源：[印刷 p53 / PDF 58](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=58)、[印刷 pp59–61 / PDF 64–66](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=64)。

## 本轮实验结论与项目笔记

项目：ai_native_handbook。阅读范围是第三章全部29页，另核对结论页。中心收获是把任务授权随执行生命周期重验，并保留允许与拒绝的可核对证据。

实际运行一个六步学习实验：第一条命令生成三个合成文件、执行完整测试并自动重复两套新初始化场景；其余五条命令复核范围、撤销、故意错误对照、审计和可复现性。六条命令均实际执行，退出码0。原样命令、UTC时间、输出与验证标准见实验日志。

17/17 用例满足预期，包含16个正确设计行为检查和1个故意不安全缓存反例。正确路径撤销后的后续根/子请求均拒绝，读取次数0；从已撤销父委托签发新子委托也被拒绝。错误缓存反例在撤销后仍读取1次合成文件，表示漏洞成功暴露，不是安全通过。

每套29条审计事件；两套规范化结果一致、3个合成文件指纹不变。作者另把稳定ZIP解压到新目录，按指南六条原样命令重放，规范化哈希与包内证据一致：3b06607940423ac1ef5b51f66efa5dd0040725734b183616189e68a786afbaef。

程序只是同一受信 Python 进程内的独立教学状态机，身份为虚构字符串，授权为可信夹具记录。未实现真实认证、OAuth/MCP、凭证代理、Challenge审批、运行环境关闭检查；未验证同进程抗绕过、并发TOCTOU、符号链接竞态、分布式撤销、真实会话终止、崩溃恢复或日志防篡改。父委托更新是否错误复活旧子委托亦未测。设计原则与已实现用例须分开。

坑与结论：不要只看17/17；需要单独解释负对照，以及整例读取数与“拒绝后/撤销后读取数”的差别。固定哈希证明字节一致，不证明所有事实正确。已有资料里关于产品版本、价格、性能或默认配置的历史主张没有在本轮重验。

## 复用与合并建议

复用时保留来源版本、实验范围和未验证事项；优先给已有概念增加具体证据，避免重复起名。只在确有独立价值且没有同义项时新增概念。索引元数据没有命中，不能据此推断未读正文没有相关知识；历史文件的哈希一致，也不代表所有外部主张已重新核验。

## 实际全文读取的公开知识清单

以下均固定在 1043e9d6080bff7af9724162e2c44559fab63e40，仅列来源与指纹，不批量转载正文。

1. [AgentHarness智能体挽具](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AgentHarness%E6%99%BA%E8%83%BD%E4%BD%93%E6%8C%BD%E5%85%B7.md)
   UTF-8 2913 字节；SHA-256：6ea191b1ea84eb9ba3c53db9b02a55450af255775dc2006fc8cba7df72126014

2. [沙箱与审批正交](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%8E%E5%AE%A1%E6%89%B9%E6%AD%A3%E4%BA%A4.md)
   UTF-8 3248 字节；SHA-256：a9e65c39d85a821884b50e6e2a4a1a1944cd18c4fd7961cb8a6c9f65cd645a41

3. [Realpath路径沙箱防逃逸](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Realpath%E8%B7%AF%E5%BE%84%E6%B2%99%E7%AE%B1%E9%98%B2%E9%80%83%E9%80%B8.md)
   UTF-8 2222 字节；SHA-256：27fa9c9b9398c58478f775b3ddd4d86fb1c653bae6c20896d8f083eac8640798

4. [子智能体咨询](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%AD%90%E6%99%BA%E8%83%BD%E4%BD%93%E5%92%A8%E8%AF%A2.md)
   UTF-8 1719 字节；SHA-256：e335e6e4ae07d6709b7ce8afa1e3ee5fd8f31e8da4b1f385a73a56fb4cdcc8eb

5. [多智能体协作](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%E5%8D%8F%E4%BD%9C.md)
   UTF-8 1852 字节；SHA-256：4fab7458831e68632ba21869d352f8764df27295f47d5f358419b2b4eae8db90

6. [托管Harness与会话即资源](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%89%98%E7%AE%A1Harness%E4%B8%8E%E4%BC%9A%E8%AF%9D%E5%8D%B3%E8%B5%84%E6%BA%90.md)
   UTF-8 2905 字节；SHA-256：596bf0d1e5d38c769bf4b5fd6baa8201a7c442bd23c237fc2338218bac8d49fa

7. [沙箱三态与Executor](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%89%E6%80%81%E4%B8%8EExecutor.md)
   UTF-8 2157 字节；SHA-256：4d1113c17b1c8a8568ad3b44e73c7393ff7f7b4a6be44c3cd5bc3e620b1107a1

8. [LLM工具调用](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/LLM%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md)
   UTF-8 2229 字节；SHA-256：4db3a2123f84c55bcfbddbfedd6cf578d6043e1a4cb09790c8b555f4a5a54269

9. [工具调用生命周期](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.md)
   UTF-8 1411 字节；SHA-256：9f8e203fdc45687ecf8625edc7fe4fc3c766850385879f97623333710d2c5481

10. [AgentSkills技能包](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AgentSkills%E6%8A%80%E8%83%BD%E5%8C%85.md)
   UTF-8 1536 字节；SHA-256：bb055a1f106f721c5c71a3a2b359c16d11190fbc261c772d63a7bbc3782f011b

11. [MCP协议](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/MCP%E5%8D%8F%E8%AE%AE.md)
   UTF-8 1720 字节；SHA-256：f241531981004f1580b331a37b9e38ca96875e368ac03d687aab199daac284d6

12. [MCP模型上下文协议](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md)
   UTF-8 1683 字节；SHA-256：ae666167533a8ad49319a380b3b4fbcd54c7153c5f019b6eee275440f6809aef

13. [技能路由器与授权硬门](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8A%80%E8%83%BD%E8%B7%AF%E7%94%B1%E5%99%A8%E4%B8%8E%E6%8E%88%E6%9D%83%E7%A1%AC%E9%97%A8.md)
   UTF-8 2140 字节；SHA-256：8e122f9a4d1cb581bbc11303a0952f46b81b8d8251c938067e38db926f90ff4e

14. [工具暴露单调性](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%B7%A5%E5%85%B7%E6%9A%B4%E9%9C%B2%E5%8D%95%E8%B0%83%E6%80%A7.md)
   UTF-8 1962 字节；SHA-256：3d1f9a9cf03ced75ffe37d005dc96bbfbf7b92117992e9ea75ac1a52c11151b2

15. [本地MCP端点安全四道门](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%9C%AC%E5%9C%B0MCP%E7%AB%AF%E7%82%B9%E5%AE%89%E5%85%A8%E5%9B%9B%E9%81%93%E9%97%A8.md)
   UTF-8 2558 字节；SHA-256：1f7cfcb79846015e78c94fcb6391e09ffc9f4b1e236c29ac391dd20fda686cff

16. [团队Harness的Git原生分发](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%9B%A2%E9%98%9FHarness%E7%9A%84Git%E5%8E%9F%E7%94%9F%E5%88%86%E5%8F%91.md)
   UTF-8 2655 字节；SHA-256：6fc6dad23e13bc97fcbba9d6a1c8609032340e11102f3f1a7585c09a809b3a3a

17. [控制面与数据面](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A7%E5%88%B6%E9%9D%A2%E4%B8%8E%E6%95%B0%E6%8D%AE%E9%9D%A2.md)
   UTF-8 1575 字节；SHA-256：90267f9bf8041185daf02ce384e1367c4c8e3ed32beccf4dc6ae7ae9c7ef7409

18. [提示注入](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8F%90%E7%A4%BA%E6%B3%A8%E5%85%A5.md)
   UTF-8 1201 字节；SHA-256：3ab16d4d46a9df5e0d31f3114abae23cbe184a2187720a2d73174bf76b778e0b

19. [提示词权威边界](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8F%90%E7%A4%BA%E8%AF%8D%E6%9D%83%E5%A8%81%E8%BE%B9%E7%95%8C.md)
   UTF-8 1807 字节；SHA-256：f51e1a1b69e257f494a76b6ae0bab8e110f64913c402ca28e554ab3012ba5e16

20. [代码管边界提示词管判断](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%A3%E7%A0%81%E7%AE%A1%E8%BE%B9%E7%95%8C%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%AE%A1%E5%88%A4%E6%96%AD.md)
   UTF-8 1427 字节；SHA-256：82baf8f30c908b3ea424d15f82b6d3124e40b3c1b023961bfd0c8abd1eb8b86d

21. [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)
   UTF-8 2389 字节；SHA-256：6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb

22. [JSONL事件日志与折叠模型](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/JSONL%E4%BA%8B%E4%BB%B6%E6%97%A5%E5%BF%97%E4%B8%8E%E6%8A%98%E5%8F%A0%E6%A8%A1%E5%9E%8B.md)
   UTF-8 1776 字节；SHA-256：8346f3ddd229a2fb8fe929ee0a4916f44ecf17700818581ef3f57c4c7495a5ea

23. [预执行安全网与执行事件](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E9%A2%84%E6%89%A7%E8%A1%8C%E5%AE%89%E5%85%A8%E7%BD%91%E4%B8%8E%E6%89%A7%E8%A1%8C%E4%BA%8B%E4%BB%B6.md)
   UTF-8 2542 字节；SHA-256：d35ddffcd836094286f12ae9dc8213ffbdbd4653daa527fe3658efdaa495ce3c

24. [工具调用三段式流水线](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8%E4%B8%89%E6%AE%B5%E5%BC%8F%E6%B5%81%E6%B0%B4%E7%BA%BF.md)
   UTF-8 2723 字节；SHA-256：0a153b39360c2293562800a1ed5665790d3250172804c2cff405876d2101fb97

25. [知识层永不回滚原则](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%9F%A5%E8%AF%86%E5%B1%82%E6%B0%B8%E4%B8%8D%E5%9B%9E%E6%BB%9A%E5%8E%9F%E5%88%99.md)
   UTF-8 2227 字节；SHA-256：2bf4e6b2201b68e057739e5a143cc8fe83a6e2a2e2e9695439095c1858a734cc

26. [WikiSkill共演化循环](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/WikiSkill%E5%85%B1%E6%BC%94%E5%8C%96%E5%BE%AA%E7%8E%AF.md)
   UTF-8 2812 字节；SHA-256：d0024cc6888f816da51db07df204f56dc7061838f985dd7a36e700dcda488038

27. [teamai-cli](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/teamai-cli.md)
   UTF-8 2796 字节；SHA-256：90ebb1acb3bb8ca58ba789b660ef4d870adf1a090d2bf68acd2e4d67162eb6c9

28. [agent-harness](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/agent-harness.md)
   UTF-8 4013 字节；SHA-256：8264dcccd6f95ba233b84d80d3996326cca8f84d54477fd99dc6553c474e3856

29. [agent-kernel](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/agent-kernel.md)
   UTF-8 3536 字节；SHA-256：825d06b3df7fa95605e8743864b9ba9ef7b85a1ca053f8f40aa64ecfb6bf6da4

30. [openai-agents-api](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/openai-agents-api.md)
   UTF-8 5012 字节；SHA-256：c80e7aabc79f801648b54771f77ea335a35e8201defd7d9ba80b2b6a90007ba9

31. [资源命名空间分发](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%B5%84%E6%BA%90%E5%91%BD%E5%90%8D%E7%A9%BA%E9%97%B4%E5%88%86%E5%8F%91.md)
   UTF-8 2214 字节；SHA-256：622038810ca479e3c8b9a40c648dc78500e004e92afe8756c07590427e797fd1

32. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   UTF-8 3593 字节；SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

33. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   UTF-8 2488 字节；SHA-256：4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

34. [能力运行时](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%83%BD%E5%8A%9B%E8%BF%90%E8%A1%8C%E6%97%B6.md)
   UTF-8 1411 字节；SHA-256：1341c5c402b01ed0cc6641b8b4ba4b9be0024c03ec443b2300e0453bbe121678

35. [图环挽具三层工程](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%9B%BE%E7%8E%AF%E6%8C%BD%E5%85%B7%E4%B8%89%E5%B1%82%E5%B7%A5%E7%A8%8B.md)
   UTF-8 2188 字节；SHA-256：98589e10e74ed478b3ddd9058f5c5593c666d70b6c777318a338fb5c86c72acc

36. [Agent输出协议契约](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Agent%E8%BE%93%E5%87%BA%E5%8D%8F%E8%AE%AE%E5%A5%91%E7%BA%A6.md)
   UTF-8 1742 字节；SHA-256：85b2ef5207651ba4807bd3da205a45c72c1fe38a5cb8ce91a052f66dea5bba4e

