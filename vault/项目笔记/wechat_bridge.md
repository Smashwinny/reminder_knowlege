---
tags: [项目笔记, 用户主动分享, 批次交接, 结果边界]
学习审核日期: 2026-10-05
上游仓库: https://github.com/freestylefly/WeChatBridge
固定版本: 07b88822debc3bd544ae7a83bc207633b29c3a04
许可: MIT；保留LICENSE与第三方声明
验证范围: Linux上真实Windows.Core组件；自建合成输入与定向harness
---

# WeChatBridge：主动分享、批次可见性与投递状态

## 是什么，能学到什么

WeChatBridge 面向用户主动选择聊天并由微信导出归档，再通过系统分享交给批次处理与目标应用的路线。它与持续收信机器人、读取微信数据库的工具不同；本次实际实验仅覆盖固定版本可在 Linux 调用的真实 Windows.Core 组件，没有操作真实微信或原生分享界面。

可以学习五件事：保留源归档与派生产物；拆开 manifest、intent、state；检查 Staging 到 Ready 的可见性边界；对一次性请求和重试保留准确语义；用目标实际回执限定 Delivered 等状态。文件留下、请求被消费、应用收到和模型处理完成不能互相替代。

## 与已有知识的合并

- [[原样捕获与工序分离]]：追加用户导出归档、转换产物和模型解释分层，并收窄旧“天然免疫提示注入”的绝对说法
- [[产物留痕与状态外置]]：追加清单、意图、状态与集合账本的区别，以及常规消费者只见 Ready 的批次边界
- [[工具调用生命周期]]：追加顺序一次性消费、时间新鲜度与并发/外部效果不同的案例；不新建同义“恰好一次交接”概念
- [[证据状态机]]：追加 Delivering→Retry、Copied/Delivered 的实际证据层；能重试不证明上一轮无效果
- [[Agent网关与消息通道]]：相关入口背景，主动文件分享不等同常驻消息网关
- [[本地优先与文件监听]]、[[内容寻址与镜像分层]]：本地文件与标识/内容摘要分别理解，随机批次 GUID 不是内容寻址
- [[Handoff交接简报续跑]]：它是跨会话上下文摘要，本项目是批次动作请求，名称相近也不合并为同一机制
- [[提示注入]]、[[沙箱与审批正交]]、[[Agent输出协议契约]]、[[接缝与桩实现StubSeam]]、[[证据优先质检ProofOverClaims]]：复用资料不自带指令权、校验分层与组件验收边界

[[项目笔记/wechat_hermes_notebot]] 是写入捕获/同步，[[项目笔记/wechat-ai-memory]] 是导出/规范化，[[项目笔记/wechat-intelligence-hub]] 是只读分析；它们的历史测试不构成本项目集成证据。[[项目笔记/easel]]、[[项目笔记/openmuse]] 提供薄索引、显示状态、幂等键和未知效果的相关案例；[[项目笔记/route_studio]]、[[项目笔记/codex_advanced]] 提供解析/契约/实际运行的分层对照。旧版本、性能、权限与测试数量不迁移为 WeChatBridge 事实。

## 已有六步实验与计数

历史环境为 Linux x86_64 / Debian 13，官方 .NET SDK 10.0.401、运行时 10.0.12。练习包含 46 份逐字节保留的 Windows.Core 源码、项目和资源文件；自建 harness 直接调用这些真实实现，没有仿写 ZIP 解析器或状态机替代上游。构建为 0 warnings、0 errors，没有外部 NuGet 包依赖；这不是完整上游测试套件或原生应用构建。

六条教材命令依次为 setup、verify、fixtures、build、test、report。作者最终六步与历史独立审核的新解包重放均退出 0；独立审核复用已下载官方 SDK，但重新核对归档 SHA-512 与 4907 个 SDK 普通文件，没有复用旧构建产物。该范围不等于从零冷安装全链路。此次公开知识整理没有执行 SDK、安装、生成夹具、构建或重跑实验。

42 个用例均为自写的定向检查：

- 21 项归档检查：stored/deflate、中文多行/BOM/CRLF、附件字节及选定损坏、CRC、加密标记、大小声明、路径和取消等拒绝输入
- 8 项暂存检查：发布前不可见、提交后可见、原 ZIP 指纹、同名处理、失败回滚、大小限制、扩展名边界、取消及来源符号链接
- 6 项意图/状态检查：注入 +89/+90 秒、顺序消费与同进程新 Reader、损坏意图删除、状态/上下文、Copied 模型值以及未来时间的现状
- 7 项收集检查：冻结顺序、冻结期间编辑限制及迟到分组、同进程新 Service 恢复、移除/撤销、手工构造中断状态、较新 schema 拒绝、聊天名与保护中的保留期行为

作者最终 42/42、历史独立审核同 42/42，失败为 0；不相加为 84 个不同用例。初次 harness 为 41/42：I05 错将保留小数秒的内存时间与整秒 JSON 时间比较，修正仅在自建断言，改为比较持久化值；上游字节未变。最初计时工具不存在的失败也保留，不包装为一次通过。

输入是 20 个合成文件，其中正常聊天仅两条虚构中文消息与 64 字节 sample.bin 附件；该附件不是图片，没有真实图片/视频渲染证据。历史参考报告的 68 个普通输出文件指纹描述那次运行；随机 GUID、运行时间和路径可随重放变化，不能要求整份输出报告逐位恒定。

## 核心观察与坑

1. **源归档与派生解释分开。** 收集账本引用原 ZIP，不把所有归档改写合并成一份新 ZIP。保存它支持回看来源，却不证明微信全部聊天都被导出，或 TXT/附件/Markdown 转换无损
2. **清单不是认证或完整性证书。** manifest 记录版本、批次与条目 GUID、时间、动作、相对路径、类型、长度和来源顺序；intent 是短期动作请求，state 是后续处理记录。随机 GUID 不等于内容哈希，manifest 没有文件摘要字段；同批次 ID 去重不等于聊天内容去重
3. **Ready 只说明批次已可见。** StageAsync 在 Staging 写文件与清单，CommitAsync 补意图/可选状态再 Directory.Move 到 Ready，Reader 只枚举 Ready。已有检查看到提交前后可见性改变，不证明跨卷原子性、断电持久性，或剪贴板/应用/模型与文件系统共同事务
4. **扩展名不等于有效归档。** S06 中 23 字节 not-a-zip.zip 被 InboxWriter 接收并发布到 Ready，而另一个归档校验用例拒绝同一内容。接收校验与 ZIP 结构/CRC 校验是不同入口，不把一个入口通过写成所有层都有效
5. **新鲜度不等于权限或完整防重放。** 注入 +89 秒得到 Ready，恰好 +90 秒得到 Expired 并消费文件；未来一小时的 RequestedAt 满足当前 age<90 秒单边条件。没有真实等待这些时长，也没有证明系统检查了非未来下界
6. **消费一次与执行一次不同。** ConsumeIntent 先读文件并删除，再解析和判断新鲜度。顺序二次调用及同进程新 Reader 不再取得请求，不证明并发原子领取；删除后、动作前失败也不证明目标发生过效果。源码注释里的“永不重放”不是并发验收
7. **恢复范围与失败输入要精确。** C05 只测试 schemaVersion=8 的较新账本被拒且文件未覆盖，没有同时覆盖任意损坏 JSON。恢复用例是在同一测试进程内新建 Reader/Service 重读磁盘，部分中断状态由 harness 构造；不是强杀、断电、跨机或多消费者故障注入

## Delivered、Retry 与真实目标结果

CollectionService.Freeze 检查成员与聊天名，先保存 Delivering，再返回冻结批次。重新加载账本可将遗留 Delivering 变为 Retry，并提示先确认目标附件；原件还在方便继续处理，但 Retry 不证明上一轮肯定未粘贴。

固定 BatchOutcomeKind.Delivered 的源码口径为目标应用激活及粘贴请求，DeliveryEngine 在按键注入流程后登记结果。这个口径不是接收服务器回执，不证明上传完成、模型读取或分析成功；本次没有调用真实剪贴板、前台控制或粘贴接口。Copied 用例也只核对模型元数据。

本地归档路径与向目标 AI 应用传递的路径分开判断。即便一个捕获组件不联网，也不能保证后续接收应用永不上传；实际发送前仍应核对内容、接收方及其处理方式。此次没有传递真实聊天、调用目标 Agent 或写入真实知识库。

## 捕获安全表述的收窄

[[原样捕获与工序分离]] 旧“只保存不执行让捕获 Agent 天然免疫”过于绝对。原学习材料已经指出：捕获阶段不执行内容可以减少风险，后续模型读取时仍须当作不可信资料，保留指令/数据边界与最小权限。保真不授予行动权限，也不等于注入防护测试通过。本次只追加该范围说明，不改写历史正文。

## 未验证范围与材料边界

未执行 macOS Share Extension、辅助功能、OCR、App Group 签名；未执行 Windows WPF、Share Target、Win32 投递、实际剪贴板/粘贴；未读取微信数据库或真实聊天文件。Linux 核心编译和跨平台协议文档不能证明原生功能等价。

没有并发消费者、端到端 exactly-once、真实进程崩溃/断电、跨卷移动、完整路径安全审计、未知外部效果对账或模型效果证据。顺序消费、同进程新对象恢复、原件保留和 Retry 入口是各自有限的观察，不能合成“永不丢失、永不重复”。

项目 MIT 许可及第三方声明保留；练习中的 46 份 Core 文件与自写 harness 明确分开。最终原始 ZIP 为 105 个成员、104 项内嵌清单记录；早期 71 项清单不是最终包口径。本次清理副本的摘要另见配套日志，不能以文件整理次数增加实验成绩。

原指南为 ReportLab 直接生成的 15 页 PDF，历史审核与本地副本审核分别查看实际渲染页面。HTML 只做结构核查；历史浏览器视觉和 HTML→PDF 路线受阻，本次未重试。教材示意图不是原生应用运行截图；材料完成也不代表读者已经掌握。

## 最新公开知识读取范围

此次合并基于 GitHub main 快照 66d9eeee243544aece8ab2b366e8604b354458f4。通过连接器取得并核对完整 UTF-8 字节、Git blob SHA 与 SHA-256：MOC、学习方法、仓库说明、两份模板、上方列出的 13 篇概念及 7 篇项目，共 25 份正文。与此前已读正文精确一致者，用字节证据复用阅读；元数据不计正文。

该快照有 306 篇概念与 110 篇项目；其余 293 篇概念、103 篇项目仅做路径/标题筛查，未全文阅读。筛查包括 WeChatBridge、wechat_bridge、WeChat-Bridge、微信流、主动分享、批次、原子发布、一次性意图、交接和投递状态等。结论限于当前公开快照及实际已读范围，不声称全库正文无重复、其他设备副本已核对或“从未学过”。

本次新增项目笔记、向四篇既有概念追加案例/范围更正、在 MOC 增加入口；不新增概念，不改写历史正文与累计计数。原学习的 394 条公开索引元数据、15 篇实际正文、379 篇未读正文范围是较早阶段，单独保留。

## 六份配套材料

- [彩色 PDF 指南](../../wechat_bridge/delivery/wechat-bridge-guide.pdf)
- [HTML 指南](../../wechat_bridge/delivery/wechat-bridge-guide.html)
- [核心练习包](../../wechat_bridge/delivery/wechat-bridge-exercise.zip)
- [历史实验日志](../../wechat_bridge/delivery/wechat-bridge-experiment-log.md)
- [知识笔记](../../wechat_bridge/delivery/wechat-bridge-knowledge.md)
- [独立审核日志](../../wechat_bridge/delivery/wechat-bridge-review-log.md)

## 固定来源

- [项目定位](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/README.md)、[共享契约](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/shared/README.md)、[MIT LICENSE](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/LICENSE)、[第三方声明](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/THIRD-PARTY-NOTICES.md)
- [暂存与提交](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/InboxModels.cs)、[请求消费](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/InboxReader.cs)、[请求新鲜度](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/ShareAction.cs)、[状态定义](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/BatchState.cs)
- [集合账本与恢复](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Collections/BatchCollection.cs)、[集合冻结](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Collections/CollectionService.cs)、[归档解析](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Archive/WeChatNativeArchive.cs)、[投递，仅静态观察](https://github.com/freestylefly/WeChatBridge/blob/07b88822debc3bd544ae7a83bc207633b29c3a04/windows/src/WeChatBridge.Windows.Core/Delivery/DeliveryEngine.cs)

返回 [[00-总览|知识库总览]]。
