---
tags: [项目笔记, Agent基础设施, 权限生命周期]
学习日期: 2026-10-05
来源: AI Native 研发范式实践手册
阅读范围: 第三章基础设施，印刷33–61页，PDF38–66页
验证范围: 自编Python单进程概念实验
---

# AI Native 手册：Agent 基础设施与任务授权

## 学习对象与证据层

本项目围绕《AI Native 研发范式实践手册》第三章“基础设施”，学习 Harness、知识与工具治理、运行环境、身份与委托、执行授权、Guardrail 和可观测性如何分工。原学习实际逐页查看该章全部 29 页（印刷 pp33–61 / PDF 38–66），另查封面、目录及结论；没有声称精读全书。

来源为 [官方 PDF](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf)，版本路径 0.0.1。原文件共 68 页、27,286,928 字节，SHA-256 为 `6929f3e9e57fef9550129d457ba82ac40a4a9368e1c5926c6ac2206d8aaeced3`。本项目提供独立总结和官方链接，不将原 PDF 或页面图打包再分发。

手册给出阶段性实践与参考架构；有关厂商内部平台的描述是手册作者陈述，没有被本项目独立验收。结论页明确提到部分基础设施仍在建设和验证。本项目的程序为独立自编教学状态机，不是手册或阿里巴巴提供的实现，没有运行手册中的 OpenCode 示例、企业平台或模型集成。

## 可以带走什么

1. 把“模型提出动作”与“系统批准资源访问”分开，找到调用前检查与资源侧执行点
2. 区分身份、任务委托、策略判定和下游凭证，避免将登录或工具菜单当成全面授权
3. 给父子委托设置资源、动作、期限与当前状态约束，并以撤销后的新请求检查失效效果
4. 设计正确路径和故意错误负对照，逐请求核对判定、真正读取与审计，而非只看总通过数
5. 明确知识治理、运行隔离、任务可复现和行为可观测的不同证据，避免把教学实验扩大成生产安全证明

## 与已有知识的合并

- [[AgentHarness智能体挽具]]：追加任务委托逐级收缩案例；关联 [[多智能体协作]]、[[子智能体咨询]]、[[沙箱与审批正交]]
- [[工具调用三段式流水线]]：追加准备阶段放行后资源侧仍需重验；关联 [[控制面与数据面]]、[[LLM工具调用]]、[[工具调用生命周期]]
- [[工具暴露单调性]]：追加父子撤销与错误允许缓存对照，区分工具快照和执行许可；不把教学程序当作 MCP 实现
- [[Agent输出协议契约]]：追加结构化 Challenge 的文档案例；关联 [[人机协同Interrupt]]，明确实验未实现该功能
- [[JSONL事件日志与折叠模型]]：追加许可、撤销及实际 I/O 的关联证据；不重复建立日志概念或继承其他项目的幂等、乱序或防篡改保证

其余相关主题保留在本项目中：[[团队Harness的Git原生分发]]、[[资源命名空间分发]] 与 [[AgentSkills技能包]] 管知识资产的来源、版本和分发，不自动授予后续资源权限；[[技能路由器与授权硬门]]、[[代码管边界提示词管判断]] 管执行侧边界。[[WikiSkill共演化循环]] 与 [[知识层永不回滚原则]] 是特定研究语境，不能泛化为知识不会出错或不需要纠错、撤回。[[提示注入]]、[[提示词权威边界]] 提醒检索材料或工具返回中的文字不自行获得授权地位。

[[托管Harness与会话即资源]]、[[沙箱三态与Executor]]、[[产物留痕与状态外置]] 用于区分运行实例、持久产物和恢复依据；本程序没有实现这些平台机制。[[Realpath路径沙箱防逃逸]] 与 [[本地MCP端点安全四道门]] 提供相关安全问题背景，其原项目测试不迁移为本次实测。

[[项目笔记/mcp_toolbox]] 已有 readOnlyHint 与真实数据库拒写对照；这里新增的是委托生命周期，不重复其试验。[[项目笔记/google_colab_cli]]、[[项目笔记/metrik]]、[[项目笔记/qwen_image_2_1]] 分别提供记录、计量和契约的证据边界，旧项目的数量、版本、价格与能力不外推为本项目事实。

## 原有六步实验

已有学习实验只用 Python 标准库、三个合成文本文件、虚构主体标识与可信授权夹具。同一受信进程内的 `Broker` 管理固定资源目录、任务/运行实例绑定、资源与动作范围、到期和父委托撤销状态。请求不能用自报“已批准”字段新增权限；路径来自固定夹具目录。

六条教材命令依次完成：生成合成夹具并执行两套新初始化场景；检查委托范围；检查撤销；查看故意不安全缓存对照；检查审计；核对可复现性。原日志记录六条命令均退出 0。历史作者与独立审核均从新解压目录按原命令重放；此次公开知识整理复用这些证据，没有重新执行实验。

- 17/17 用例满足各自预期，其中 16 项是正常设计行为检查，1 项是故意不安全缓存反例
- 正确路径允许根委托与更窄子委托读取；错误任务或运行实例、越界资源、write 动作、未知委托与到期边界请求被拒
- 子委托扩资源、扩动作、延长到期时间均被拒；撤销父委托后，既有根/子委托的后续读取为 0，新子委托申请也被拒
- 错误缓存反例确实在撤销后读到 1 次合成文件，表明缺陷被成功展示；不是安全通过或生产修复证明
- 每套 29 条审计事件；历史独立 I/O spy 记录 19 次资源请求、8 次实际合成文件读取，拒绝路径读取数为 0。资源请求、委派/撤销事件、实际读取和用例数是不同统计对象
- 两套规范化结果一致，3 个合成文件指纹前后不变；规范化 SHA-256 为 `3b06607940423ac1ef5b51f66efa5dd0040725734b183616189e68a786afbaef`

撤销用例的整例读取数包含撤销前成功读取；“撤销后 0 次”不等于“整例 0 次”。字节一致仅说明输入/输出可对账，不能单独证明设计完整或事实正确。详见 [完整命令与实验日志](../../ai_native_handbook/delivery/ai_native_handbook-experiment-log.md) 及 [独立发布审核（含历史证据复核）](../../ai_native_handbook/delivery/ai_native_handbook-review-log.md)。

## 没有验证的部分

程序没有真实身份认证、OAuth/MCP、凭证代理、Challenge 或真实审批界面、运行环境关闭检查。没有验证模型工具选择、企业平台集成、同进程恶意代码绕过、注册表或日志篡改、OS 沙箱、并发 TOCTOU、符号链接竞态、分布式撤销传播、正在执行的请求中断、真实会话终止、崩溃恢复，或父委托更新后旧子委托是否错误复活。它不能收回已返回的数据，也不是生产授权系统或安全证明。

手册的 Guardrail 例子强调检查范围与当前目标绑定，UNKNOWN 不能提升成 PASS；通过某组检查也不等于获得另一目标的操作许可。该讨论与 [[护栏模式Guardrails]]、[[证据状态机]] 有关，但本实验没有实现手册的 Guardrail 服务。系统指标、行为轨迹和最终任务结果也应分别取证，见 [[证据优先质检ProofOverClaims]]。

## 最新公开知识读取范围

本次合并基于公开 GitHub main 快照 `8657aafe1659ab41f560f804f18bc6b44a669748`。通过连接器完整读取并逐文件核对 Git blob SHA、UTF-8 字节数与 SHA-256：MOC、原学习方法、仓库说明、两份模板、37 篇相关概念、8 篇相关项目笔记，共 50 份正文。

该树有 304 篇概念、103 篇项目笔记；另 267 篇概念与 95 篇项目笔记仅做路径/标题层筛查，没有全文阅读。除上文涉及的概念，还全文读取 [[能力运行时]]、[[图环挽具三层工程]]、[[预执行安全网与执行事件]]、[[只读闸门三原则]]、[[缓存有效期与发布边界]]、[[接缝与桩实现StubSeam]]、[[MCP协议]] 与 [[MCP模型上下文协议]]。8 篇项目为 agent-harness、agent-kernel、openai-agents-api、teamai-cli、mcp_toolbox、google_colab_cli、metrik、qwen_image_2_1。

此次只新增本项目笔记、向五篇已有概念追加案例，并在 MOC 增加入口；不新增同义概念，不改写历史累计计数或既有正文。读取与查重限于该公开快照，不声称全库正文或其他副本已核验；原学习较早的读取范围另记在配套知识笔记中。

## 六份配套学习材料

- [彩色 PDF 指南](../../ai_native_handbook/delivery/ai_native_handbook-guide.pdf)
- [HTML 指南](../../ai_native_handbook/delivery/ai_native_handbook-guide.html)
- [离线练习包](../../ai_native_handbook/delivery/ai_native_handbook-exercise.zip)
- [实验日志](../../ai_native_handbook/delivery/ai_native_handbook-experiment-log.md)
- [知识笔记](../../ai_native_handbook/delivery/ai_native_handbook-knowledge-notes.md)
- [审核日志](../../ai_native_handbook/delivery/ai_native_handbook-review-log.md)

返回 [[00-总览|知识库总览]]。

## 来源定位

- [基础设施章节起点，印刷 p33 / PDF 38](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=38)
- [行动前审查与资源侧复核，印刷 p38 / PDF 43](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=43)
- [知识治理与工具评测，印刷 pp39–42 / PDF 44–47](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=44)
- [身份、委托、策略、凭证和 Challenge，印刷 pp51–54 / PDF 56–59](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=56)
- [Guardrail 证据与范围，印刷 p58 / PDF 63](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=63)
- [可观测性，印刷 pp59–61 / PDF 64–66](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=64)
- [阶段性总结与成熟度限定，印刷 p62 / PDF 67](https://g.alistatic.com/s/v/ainativeinfra/ai-native-handbook/0.0.1/ai-native-handbook.pdf#page=67)
