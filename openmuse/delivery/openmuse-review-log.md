# OpenMuse 独立审核与公开副本检查

历史实验与独立复跑日期：2026-10-05 UTC。公开副本审核日期：2026-10-06 UTC。

结论：通过本次限定范围的内容、历史证据、公开副本和知识合并检查。本次没有安装依赖、重跑实验、创建数据库、启动上游应用或连接外部服务。历史结果仍是 21 项选取的上游测试加 4 项自写变式，未把重复运行、来源指纹或依赖数量累加为新测试成绩。

## 1. 独立性和本次检查范围

本次审查者没有编写或改动作者的前五份公开交付，也没有编写知识库候选正文；只编写本审核日志。检查绑定最终文件字节，覆盖历史命令与 TAP、固定源码与 MIT LICENSE、依赖锁、归档成员、文字、链接和知识库差异，并实际查看最终 PDF 全部 23 页。

已直接读取 ActionService、SQL Store、TaskWorker 的关键路径及测试选择脚本和自写变式，按固定提交核对 15 份上游副本。三份原测试文件的定义数为 12、8、2，共 22 项；选择器实际执行持久化中的 nested-directory 用例，另一个 PostgreSQL pool-error 用例未选择。作者原始 TAP 与历史独立 TAP 均为 12、8、1、4 通过，fail=0、skipped=0、NETWORK_GUARD attempts=0。这里的“未选择”不等于 TAP 输出 skipped=1。

真实被测层是 PGlite SQL、Store、ActionService 与 TaskWorker；外部提供方、连接状态、处理器和时钟为合成或受控输入。同进程 worker 共享数据库、正常 close/reopen 和虚拟时钟分别标注，没有升级为分布式部署、断电耐久性、真实 Google 或完整产品验收。

## 2. 当前公开文件与历史原件指纹

以下五份为本次实际检查的公开副本。本日志是第六份，自己的最终指纹由配套发布清单记录，不写入自身制造自指哈希。
- openmuse-guide.pdf：91183 字节；SHA-256 b9c96c64c8de20ccb907130d1a16fc59519ad16a5b14e289fae4203033f72596
- openmuse-guide.html：72159 字节；SHA-256 c0da9958fda72811391f1da92afdf8bbe1de5b57e4ea393a1e6970bffd4dcb4a
- openmuse-core-exercise.zip：211314 字节；SHA-256 000c275f9603644f0aecd9313a1a6ccd1e066e3099a9aeaf580ff93c0f0cc8d5
- openmuse-experiment-log.md：38783 字节；SHA-256 80d57ac51ffed6c563add44265225dc60835dcba579fb9c630753d3f0577216f
- openmuse-knowledge-notes.md：16787 字节；SHA-256 bc60272f1c6d528844af13e6fc7372e143f25c6f13bdeb96fd6be1b6956b2fe2

六份公开交付的原始字节合计低于 1,000,000 字节，不以额外压缩后的大小替代。历史六份原始文件合计 444225 字节，以下原始指纹仅作来源对照，不冒充当前公开文件指纹。
- openmuse-guide.pdf：历史原始 91299 字节；SHA-256 503496400a5437d94aac4da7c48069bf848c154aa4fa6142eee6fdc0476e3d0f
- openmuse-guide.html：历史原始 72201 字节；SHA-256 e0c0a5ccd9a901a53d2c04916c007b491964afe0ecbf5aea19f718498e3d481b
- openmuse-core-exercise.zip：历史原始 211031 字节；SHA-256 714ca8560289c4ec076a6b0ecb87a6c40b921fadd12c62cec89142d878994157
- openmuse-experiment-log.md：历史原始 39182 字节；SHA-256 1affbd3a4a83d9d874576243befd6f74c6ddf482f63ee070e0d9532c3e778e18
- openmuse-knowledge-notes.md：历史原始 17589 字节；SHA-256 480b9005977321e51cbc8588f948f287d8ca209da976bfc89650b0635882b044
- openmuse-review-log.md：历史原始 12923 字节；SHA-256 b21dcac1ad4ceea19442f53d2bba04d048b320fd3ed2a538f58414d59663d3ce

## 3. 2026-10-05 的历史独立复跑记录

以下保留历史审核的六组执行摘要、时间与原始日志指纹。这些描述只属于原日期，本次读取旧证据，没有再次执行。当前实验日志保留相应完整输出，环境专属绝对路径已改为角色占位符；下列日志哈希指向规范化前的历史字节。


历史原始练习 ZIP SHA-256（公开整理前）：714ca8560289c4ec076a6b0ecb87a6c40b921fadd12c62cec89142d878994157。211031 字节，37 个成员。历史审核者在当时不存在的新目录解压，没有复用作者的 node_modules、数据库、HOME 或 npm 缓存。Node v24.19.0，npm 11.9.0，Linux/Bash/Python 3。下列均在新解压的 openmuse-core-exercise 目录运行。

1. 11:51:11 UTC：node --version; npm --version; python3 verify-exercise.py。退出 0，SOURCE_SHA256_OK files=15，NPM_LOCK_INTEGRITY_OK packages=16
2. 11:51:26–11:51:33 UTC：bash install-deps.sh; python3 verify-exercise.py。安装 16 项约 7 秒；安装与验证分别退出 0，没有关闭 TLS 验证
3. 11:51:48–11:51:49 UTC：bash run-core.sh actions。12 tests / 12 pass / 0 fail / EXIT_CODE=0 / NETWORK_GUARD attempts=0
4. 11:51:58–11:52:04 UTC：bash run-core.sh engine; cat rawlogs/04-original-engine.log。8 tests / 8 pass / 0 fail，运行与 cat 均退出 0，guard=0
5. 11:52:16–11:52:18 UTC：bash run-core.sh persistence; cat rawlogs/05-original-persistence.log。1 test / 1 pass / 0 fail / 0 skipped，运行与 cat 均退出 0，guard=0
6. 11:52:28–11:52:32 UTC：bash run-core.sh characterization; cat rawlogs/06-changed-input-characterization.log; python3 verify-exercise.py。4 tests / 4 pass / 0 fail，运行、cat、最后验证均退出 0；guard=0，15 项源码与 16 项依赖再次匹配

以上完整 stdout/stderr、时间和退出码已逐字核对并收录在同包 openmuse-experiment-log.md 的“最终ZIP新目录解压后的独立复跑完整日志”中。四组 TAP 日志 SHA-256 如下；cat 造成的重复显示不算额外执行。

- 03-original-actions.log：3170 字节；47b7a976d37b7c5b5254d7979e19bdb389c51891feaf87d2cc37e9cb87e6292f
- 04-original-engine.log：2254 字节；7ddb01cf33724ab637ce885da4cc1ebe451f883bb29f0b2c9bc206c74742c145
- 05-original-persistence.log：1032 字节；83cfdebdfa12d44412f07202235664cbbe80dce3b4cc274705f5d296968d69f0
- 06-changed-input-characterization.log：2221 字节；df84ccebb36f4438cacd4c7c77f439f0001fc56fe5c54bee5e475951e5574d55

唯一用例数是 21 项选取的上游测试 + 4 项作者变式。审核者重跑同一批用例，不把它累加成 50 项。三个源测试文件共有 22 项定义；--test-name-pattern 仅选择 persistence 中的 nested-directory 用例，另一项 PostgreSQL pool-error 测试被排除。该 Node 版本实际输出 skipped=0，不能伪造 skipped=1。

## 4. 来源、依赖与最终 ZIP

源码固定为 [CopilotKit/openmuse@b06caad7005ac5b6d2b451752a3794a6ae1759c1](https://github.com/CopilotKit/openmuse/tree/b06caad7005ac5b6d2b451752a3794a6ae1759c1)。审查者只读既存 Git 对象，并将十份固定来源的最新只读响应与历史源码字节独立比较，全部一致；下列练习内十五份原样材料逐项 SHA-256 匹配。没有因核对来源而运行源码。

- tests/actions.test.ts：10483 字节；SHA-256 baa448c5f858e362be6557af82dd9e398a10e202f3f0d269874c7b630a7cf632
- tests/engine.test.ts：7136 字节；SHA-256 1611d660e1e143c76845c6b8c1a28945f0c6b86ca5f17aed2fdbe0c637649b91
- tests/persistence.test.ts：1337 字节；SHA-256 1e41834c58c69b321542dda237abea7519c654f717e0e51f5b037f7e8f1d4df4
- apps/server/src/actions.ts：7063 字节；SHA-256 c582553123509c90b6fb02911717d2f1338e22ed55d02295002ebdb0f7dae229
- apps/server/src/db.ts：5985 字节；SHA-256 0d3f309e99f5fbd750c19bb07e0de07c69dab76522764432232db43d9e3c0b04
- apps/server/src/errors.ts：233 字节；SHA-256 1b9236cd303b2958dd30e5f9ec376847be30b37826f621ab02404f6e3104bc31
- apps/server/src/log.ts：1214 字节；SHA-256 9debacc65d2da0fb12fa2861f1ae77e0343ec285d74a19e0d1c1b7e1fbf44337
- apps/server/src/engine/worker.ts：8358 字节；SHA-256 5cc2bfc9534a948dd04064e2d135e08226038fda4e5725eb48d4fcffd3e539c7
- apps/server/src/engine/finance.ts：3197 字节；SHA-256 43ec54ee80dfa88538fd731487ba6554bc3f3496dd11ad5d91ba6367fcb76b7c
- packages/domain/src/index.ts：5380 字节；SHA-256 dae862eec7a934bd8787a58dc1a54d25964f93ede4ea2cafc0f6d866179a9a94
- LICENSE：1078 字节；SHA-256 399a9cccf1b228c9e8ad348ef66a0a5802d438d46735d0d068390925aee5ee36
- README.md：18605 字节；SHA-256 d8f55448a8b8295d890f30740d73175b8629a6f5048d72d3ae988d99c74f50f4
- docs/VERIFICATION.md：12243 字节；SHA-256 b26600a2b31897d8c2f4b3b7c79e74566a416785cf2fb052385884716796a070
- package.json：2146 字节；SHA-256 d76755429cb5c923a4e7d71a71c57c6d132e1c27c68ab3abf8f4161a4323291d
- pnpm-lock.yaml：515621 字节；SHA-256 c11d69720ce517f68ad6f17943edd1e88ed81f662b8fdb63e61fbf083f9e1446

上游完整 MIT LICENSE 和 Copyright (c) 2026 OpenMuse contributors 原样保留。项目许可不等于第三方服务免费、依赖统一采用相同许可或账户已经获得使用资格。

16 项直接/传递 npm 依赖的精确版本、官方 registry 地址和 SHA-512 完整性值均与固定上游 pnpm 锁匹配。安装脚本仍采用 npm ci、ignore-scripts 和独立配置/缓存目录，保留正常代理与证书变量，没有关闭证书检查。这里只检查脚本、锁和历史记录，没有重新安装；Node v24.19.0、npm 11.9.0 和依赖版本均标成原实验环境。

最终 ZIP 有 37 个唯一成员，无路径逃逸、绝对成员路径或符号链接，CRC 无错误。bundle-file-sha256.json 对其余 36 个当前成员重算均匹配。全部 15 份上游材料、MIT LICENSE、自写测试、运行脚本、锁文件及 experiment-result.json 保持原字节；没有 node_modules、缓存、数据库、账户配置或真实凭证。

与原 ZIP 相比共九个成员变化：README 的公开说明与来源措辞；source-manifest.json 的一条来源说明；六份历史 rawlog 的环境绝对路径替换；以及依赖这些字节的 bundle 校验清单。source-manifest 的其他字段不变。六份 rawlog 除三类路径替换外逐字一致，错误、警告、时间、耗时、命令参数、观察值和测试数量未改变。

README 明确区分两套指纹：experiment-result.json 保存的是规范化前历史日志的 SHA-256；bundle-file-sha256.json 校验当前公开成员。规范化后的日志不能冒充原始字节。实验日志中 23 个命令/输出代码块在同样路径替换后与历史原文一致，保留初次配置、DNS、证书失败和之后成功的恢复记录，没有删失败后宣称一次通过。六组学习命令在 PDF、HTML、README 与日志中一致。

## 5. 核心结论与不能越过的边界

- 新操作键配合修改主题产生不同内容 hash；旧 hash 或错误主体的决定被拒，提供方 fixture 调用为 0
- 同一操作键配合修改主题返回原先持久化提案、原内容和原 hash，只保留一个动作；这不是新内容等价检查
- 目标版本测试证明保存 revision-1 并把它传给注入的 execute；fixture 返回 succeeded，不证明真实 Google、If-Match 或 ETag 冲突被拦截
- 领取与 checkpoint 使用 SQL 条件更新。guard 检查中止、当前领取身份和 running 状态，不直接比较 leaseUntil；UUID 身份也不是外部服务强制执行的单调 fencing token
- 接管变式只把虚拟时钟推进 60001 毫秒：总领取 2 次、新处理器 1 次、旧 checkpoint 被拒、旧下一次受守卫效果为 0。没有真实等待一分钟或多进程故障测试
- 未知结果来自合成提供方错误；真实 PGlite 正常关闭、重开和恢复后仍保留 outcome_unknown，再决定不自动调用 execute，总 fixture 调用为 1。没有真实邮件、远程回执丢失或外部对账
- 取消测试仅覆盖下一次实际调用 guard 的路径。已派发请求可能继续完成，guard 与后续效果不是同一原子事务，不能推出外部 exactly-once
- 引擎最后一项只证明运行记录写入失败后 worker.stop 能完成且任务为 failed，没有证明后续所有任务都会继续

源码中的浏览器、Docker 和 E2B 是分别核对的实现路径，本次没有启动任何一种后端。原 docs/VERIFICATION.md 的 2026-09-16、154 项测试及演示属于上游历史报告，没有挪成本次成绩。原始介绍网页未成功读取，其宣传不作为已验证事实。

## 6. 最终 PDF 逐页与 HTML 检查

当前 PDF 由 ReportLab 直接生成，共 23 页 A4。审查者独立将精确冻结文件用 pdftoppm 渲染为 100 DPI PNG，并逐页实际查看第 1 至 23 页，没有用提取文字代替视觉验收。

- 第 1 页：封面、十二问目录、历史日期和公开阅读边界完整
- 第 2 至 4 页：应用分层、状态/运行记录/产物及真实 PGlite 与重开边界清楚
- 第 5 至 8 页：CAS、领取身份、恢复状态及取消边界一致
- 第 9 至 11 页：版本传参、重复操作键、未知结果和 fixture 范围清楚
- 第 12 至 14 页：浏览器/Docker/E2B 并列图、证据等级、五项能力和五个用途完整
- 第 15 页：21+4、22 定义/1 未选、skipped=0 及环境范围正确
- 第 16 至 21 页：六组完整命令、历史执行时间、观察与失败判据可读，无命令越界
- 第 22 页：LangGraph 粒度勘误与历史公开知识范围保留
- 第 23 页：来源、MIT、未测能力与公开整理限制清楚

所有页面未见裁切、重叠、缺字、空白页、损坏图示或错误页码；PDF 无 JavaScript、表单或附加文件。字体缓存警告未阻止渲染，图像检查正常，未改系统设置。PDF 指纹与最初逐页查看的文件保持一致。

HTML 有 23 个 section、12 个递进问题、12 个可解析 SVG、6 组命令；问题锚点唯一且全部目录链接有效。40 个固定源码链接逐项核对到正确文件和有效行号。HTML 无脚本、表单、外部图片或外部样式加载。HTML 浏览器视觉与 HTML 转 PDF 原路线受限，本次未重试；直接 PDF 视觉检查不替代这两项验收。

## 7. 知识合并与精确历史保留

本次候选以 main 的 3cda5466a6a4c6359a412e596c5934859a9ef9f3 为基线，树为 ea308ac4fa91b783c5e155ba0ce7177650dfd64f。读取范围为 MOC、学习方法、仓库说明、两份模板、18 篇概念和 5 篇项目，共 28 份正文；全部正文的字节数、SHA-256 与基线 blob 对应。精确字节相同的内容可复用既有阅读，元数据不冒充全文。

基线有 306 篇概念、109 篇项目；其余 288 篇概念、104 篇项目只筛查路径/标题，未宣称全库全文无重复。原学习的 394 条公开元数据、18 篇已读公开正文及 376 篇未读正文仍属较早阶段，计数不混合。

候选恰有六份知识文件：新增 openmuse 项目；向人机协同Interrupt、Checkpoint存档与持久执行、证据状态机、接缝与桩实现StubSeam 四篇已有概念追加勘误或案例；在 MOC 插入领域入口及项目行。没有新建同义概念。四篇概念完整旧正文仍是新文件前缀；MOC 只有两块插入，无删除或替换。移除新增块可逐字节恢复旧文件及其指纹，历史标签、累计计数、既有项目和无关工具文件保持原样。新增双链唯一解析，配套文件相对链接有效。

LangGraph 更正依 [官方 Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) 与 [固定 Checkpointers 文档](https://github.com/langchain-ai/docs/blob/f17ce09ae2fc2b0bb30306b1ce78d874f3c0a77c/src/oss/langgraph/checkpointers.mdx)：中断节点从开头重入，前置副作用需要考虑重执行；完整快照位于 super-step 边界，节点 pending writes 与整份快照分开。固定文档的 51063 字节及 SHA-256 5f2e70e77394fc0eeab391251e31b607e73fcba2a005acfa535640aa2478b409 与历史保存正文一致。这是对原材料已有窄更正的核对，没有 LangGraph 运行，也没有将其恢复机制套给 OpenMuse。

## 8. 公开内容边界与结论

检查覆盖六份公开交付的文字、PDF 提取文本与元数据、ZIP 所有成员，以及知识文件的新增内容。未发现非公开账号/对象标识、环境专属路径、私人笔记原文、真实凭证或原始来源帖地址。角色路径标记只说明历史日志中的位置角色；原本公开的历史知识正文按原字节保留，新增内容不引入其背景标识。

本次检查通过只适用于这组精确公开候选，仍不包含完整应用构建/启动、真实账号、Google/ETag、模型、浏览器/桌面、Docker/E2B、多进程 PostgreSQL、强杀/断电、生产安全或外部效果恰好一次。网络 guard 的零计数只属于历史所测路径，不能当作未知代码的强安全沙箱证明。

材料整理和审核通过不代表读者已经掌握。Git 发布是否成功须以之后实际发布及回读另行确认，不能由本日志推断。
