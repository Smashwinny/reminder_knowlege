---
tags: [项目笔记, 配置契约, 协议验证]
学习审核日期: 2026-10-05
上游仓库: https://github.com/openai/codex
固定来源: 823ea830c0fd418b09ff02d36cad9a1fff66465b
许可: Apache-2.0；保留上游LICENSE与NOTICE
验证范围: 独立Python验证器对固定Draft-07契约的合成输入检查
---

# Codex advanced：配置、请求形状与运行证据的边界

## 是什么，能学到什么

本项目以固定版本 openai/codex 的 ConfigToml 和 ClientRequest 两份 JSON Schema 为材料，学习如何分别核对配置语法、字段契约、请求结构与实际运行结果。它是已有离线契约实验的整理，不是原视频复现或当前账户使用教程；原视频未观看、未核验。

可以带走四种能力：给同一字段设计正反例；定位解析器与 schema 的不同拒绝层；按具体对象核对未知字段政策；把程序版本、契约、输入与实际调用对象一起记录。配置能解析、请求形状通过，都不证明配置已生效、线程存在、账户有权益或模型执行成功。

## 与已有知识的合并

- [[Agent输出协议契约]]：追加解析、固定 schema 与运行语义分层的 Codex 案例；既有 Qwen 解析/消费者约束和 AI Native 授权状态案例继续保留，不新建“验证分层”同义概念
- [[单一馈送与schema冻结]]：追加 ConfigToml 与 ClientRequest 的未知字段差异；不把旧 SideCrab 的兼容策略推广成所有 schema 的规则
- [[接缝与桩实现StubSeam]]：追加“独立验证器读取官方契约”这一实际执行层；它既不是 Codex 进程，也不是已经接通的桩服务或端到端任务
- [[证据优先质检ProofOverClaims]]、[[证据状态机]]、[[产物留痕与状态外置]]：复用证据范围与文件留痕纪律，哈希相同证明字节相同，不证明全部事实或运行行为正确
- [[CODEX_HOME多实例隔离]]、[[沙箱与审批正交]]、[[Provider适配层与错误契约]]、[[AgentHarness智能体挽具]]：用于区分状态目录、执行边界、服务方与运行框架；目录不等于身份，schema 字段不等于真实权限，其他框架的错误契约不能直接成为 Codex 规则
- [[规划执行分账]]、[[上下文接力]]：只复用分阶段与文档交接的视角；此次没有测额度、费用、节省或跨产品接力，不能承诺零损耗或套用旧价格/次数

已读 [[项目笔记/codex_quota_mcp]]、[[项目笔记/codex-dual-home]]、[[项目笔记/codex-claude-resets]]、[[项目笔记/openai-agents-api]]，主题分别涉及分工、目录、公告证据及托管接口，均不替代本项目的固定契约检查。[[项目笔记/qwen_image_2_1]]、[[项目笔记/patchright_enhanced]]、[[项目笔记/ai_native_handbook]]、[[项目笔记/metrik]] 提供解析、配置、授权和计量的相关案例；旧项目的版本、数量、权益与实测成绩不迁移成本项目事实。

## 已有六步实验与计数

历史学习于 2026-10-05 UTC 使用 Python 3.12.14、jsonschema 4.26.0、referencing 0.37.0。六步依次为独立 ZIP 解包与环境核对、四份上游文件和两份 Draft-07 schema 核对、配置组、请求组、畸形语法组及完整集合。作者与历史独立审核均留下逐步命令、stdout、stderr、退出码和时间；此次公开整理只复核已有证据，没有重新运行学习实验。

- 配置组 9 个合成样本：3 个结构接受，6 个 schema 拒绝
- 请求组 13 个合成样本：5 个结构接受，8 个 schema 拒绝
- 畸形语法组 3 个合成样本：1 个 JSON 解析错误、2 个 TOML 解析错误；尚未进入 schema 校验
- 完整集合共 25 个独立样本，25/25 与各自预期相符：8 accept、14 reject、3 parse_error，预期不符为 0
- 分组、完整集合与历史独立重放使用同一批样本，不累加成 50 或 75 个独立测试；四个文件指纹和两份 schema 检查也不与样本数相加

这里的 PASS 包括故意错误被预期层拒绝，只表示断言与观察一致，不表示 Codex 官方测试全通过、模型成功率为 100%、系统安全或生产可用。历史独立审核逐例对比结果、错误、输入指纹与来源清单一致，不增加未测功能的覆盖。

## 核心观察与坑

1. **布尔值不能用字符串冒充。** 合成配置的 model=42 因类型拒绝，requires_openai_auth 的字符串 false 不是布尔值；负重试次数违反 minimum。拒绝来自独立 Draft7Validator，不能写成 Codex 启动报错
2. **同项目的未知字段规则也不同。** 所测 ConfigToml 顶层及 ModelProviderInfo 未知字段被拒绝；所测 ClientRequest 请求对象及 ClientInfo 附加字段通过。后者不能推出所有层级、所有方法或运行时都接受未知字段
3. **空配置通过不是运行配置已经可用。** 空对象在该固定 ConfigToml 契约中通过，只说明这次结构检查没有缺字段错误；没有验证默认值填充、配置优先级、有效模型、服务地址或实际连接
4. **方法和参数按目标分支检查。** initialize 的缺 id、缺 clientInfo.version 和字段类型错误被拒；未知方法没有匹配的请求分支；turn/start 缺 threadId 或 text 类型错误被拒。保存完整错误及匹配方法分支错误，以免把其他分支的噪声当本方法问题
5. **合成模型名与线程只证明形状。** 字符串形式的模型名和合成 turn/start 请求通过 schema，不代表服务端认识模型、线程实际存在、握手完成、调用顺序合法或拥有权限；实验没有发出这些请求
6. **语法错误先于结构错误。** 缺 JSON 结束部分、TOML 字符串未闭合和重复键在解析层失败；错误类型分别记录为 JSONDecodeError / TOMLDecodeError，不混记为协议拒绝

## 固定来源与运行对象分开

两份 schema 取自 openai/codex 的同一提交 823ea830c0fd418b09ff02d36cad9a1fff66465b，练习保留原样 ConfigToml、ClientRequest、LICENSE 与 NOTICE；四份文件的字节数、SHA-256 和 Git blob SHA 均有记录。实际运行的是自写 Python 验证器与 jsonschema 库，没有运行 Codex CLI 或 App Server。

原学习只读过已安装 CLI 的 0.159.2 清单，没有执行该二进制，也没有证明它与上述源码提交等价。程序版本、源码提交、schema 与执行对象必须分别标识；不能把“机器上装了某版”当成该版已验证。

验证器只允许片段内引用，并让外部 schema 引用检索报错；合成配置未作为实时配置写入，未读取凭证。这是所审阅实验路径的限制，不是操作系统级网络审计或任意未知代码的强安全沙箱。

## 未验证范围与材料边界

没有 CLI/App Server 运行、真实协议传输、握手/时序、配置加载与优先级、真实登录或认证、账户/模型权益、模型列表、推理、账单、额度或 token 节省、托管环境、跨产品集成、性能或原视频复现证据。官方源码许可不授予付费服务权益；这里只记录固定材料的 Apache-2.0 许可，并完整保留其 LICENSE 与 NOTICE。

原指南 PDF 由 ReportLab 直接生成，共 12 页，历史审核逐页查看渲染页面；HTML 只有结构核查，原浏览器视觉和 HTML→PDF 路径未完成，此次没有重试。图示为教学示意，不是 Codex 运行截图。公开副本的检查范围见配套审核日志；材料整理完成不代表读者已经掌握或完成全部实际操作。

## 最新公开知识读取范围

此次合并基于 GitHub main 快照 ad4242e88337434fe8a784fd51717ca4a4fd753c。通过 GitHub 连接器取得并逐份核对完整 UTF-8 字节、Git blob SHA 与 SHA-256，实际阅读 MOC、学习方法、仓库说明、两份模板、上方列出的 12 篇已有概念及 8 篇项目，共 25 份正文。

该快照有 306 篇概念和 107 篇项目笔记；另 294 篇概念、99 篇项目只筛查路径/标题，未全文阅读。命名检查涵盖 Codex advanced、Codex 进阶、app-server、ConfigToml、ClientRequest、schema/契约/解析/验证等；在本次已读范围内，相关原则已有条目，按案例增补即可。不能据此宣称全库正文无重复、其他设备副本已核对或“从未学过”。

本次新增本项目笔记、向三篇已有概念追加案例并在 MOC 加入口，不新增概念，不改写既有正文或历史累计计数。早期材料中 394 条公开元数据、24 篇实际公开正文、370 篇未读正文是原学习阶段的读取范围，与本次较新快照分开。

## 六份配套材料

- [彩色 PDF 指南](../../codex_advanced/delivery/codex-advanced-guide.pdf)
- [HTML 指南](../../codex_advanced/delivery/codex-advanced-guide.html)
- [离线练习包](../../codex_advanced/delivery/codex-advanced-exercise.zip)
- [历史实验日志](../../codex_advanced/delivery/codex-advanced-experiment-log.md)
- [知识笔记](../../codex_advanced/delivery/codex-advanced-knowledge-notes.md)
- [发布审核及历史证据复核](../../codex_advanced/delivery/codex-advanced-review-log.md)

## 固定来源

- [ConfigToml 契约](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/core/config.schema.json)
- [ClientRequest 契约](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/app-server-protocol/schema/json/ClientRequest.json)
- [Apache-2.0 LICENSE](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/LICENSE)、[NOTICE](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/NOTICE)

返回 [[00-总览|知识库总览]]。
