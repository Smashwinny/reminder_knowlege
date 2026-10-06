---
tags: [概念]
领域: 软件工程 / AI 协作
别名: [StubSeam, 桩实现, 接缝设计, seam, stub backend]
首次来源: "[[项目笔记/assbench]]"
---

# 接缝与桩实现 StubSeam

**一句话定义**：在依赖外部服务（模型 API、数据库、硬件）的位置预埋一个抽象接口（接缝 seam），并先插上一个零依赖的假实现（桩 stub），让整个骨架循环、日志、CLI 在没有真实服务、不花一分钱 API 费的情况下先跑通测好。

**属于领域**：软件工程 / 可测试性设计

**通俗理解**：先装插排再买电器。Ass Bench 的 `ModelClient` ABC + `StubModelClient` 就是范本——loop/scorer/steer 全骨架对着接口开发，stub 一插就能 `python -m ass_bench.cli run` 整圈跑通；真模型后端来了只需写一个子类注册进 `get_client()`，骨架零改动。

**怎么做**（三步）：
1. 把外部依赖收窄成一个最小接口（一个 `generate(prompt)` 方法就够）
2. 写一个行为可预期的假实现（stub 返回固定/伪随机值，不是报错）
3. 注册表模式接线（`get_client(backend)` 按名分发，未注册的显式 NotImplementedError 而非静默）

**与已有概念的关联**：
- [[零依赖编程]]：桩让骨架期零外部依赖，是它的架构化版本（零依赖是"不用库"，接缝是"隔离服务"）
- [[双数据源适配器隔离]]：统一接口隔离易变外部系统的同一思想，接缝是其开发期形态
- [[证据优先质检ProofOverClaims]]：骨架先用桩自证逻辑走通，真后端接入后再验真输出——两段验收各管各的

**首次接触于**：[[项目笔记/assbench]]（实验：stub 循环零 key 跑通 → 文字版真后端即插即换）

## Qwen-Image-2.1：合成回答直调函数不是模型后端已接通（2026-10-05）

[[项目笔记/qwen_image_2_1]] 的已有练习直接给未修改 `pe_core.py` 输入合成回答和图片标记，检查 profile、消息构造、解析与记录对象。它属于 fixture 驱动的函数级接口检查，没有通过模型客户端接通一个桩后端，也没有端到端生成循环；不能因为不需要权重就把任意离线实验统称为 stub 全链路。

两组计数分别报告：21 项上游源码预期行为检查，其中 2 个 profile、16 个解析用例、1 个消息顺序用例、2 个记录检查；另有 6 个自写消费者策略示例，2 接受、4 拒绝。后者重用选定回答，不把两组凑成“27 项上游测试”或模型成功率。`json_repair` 缺席是本次解析边界的条件，换依赖状态需重新核对。

没有运行真实提示改写、图片加载、模型权重推理、生成管线、API 或 GPU。本次知识合并复用已完成实验与审核证据，没有重新启动学习实验。Python 进程内审计守卫是防御性措施，不是操作系统沙箱或所有未知代码的安全保证。关联 [[Agent输出协议契约]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]。

来源：[固定核心源码](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)、[已有实验日志](../../qwen_image_2_1/delivery/qwen_image_2_1_experiment_log.md)、[已有独立审核日志](../../qwen_image_2_1/delivery/qwen_image_2_1_review_log.md)。

## Patchright Enhanced：真实包装层与惰性后端分别验收（2026-10-05）

[[项目笔记/patchright_enhanced]] 的已有实验读取固定提交的三个真实 TypeScript 模块，核对原始字节指纹后由 Node 24.19.0 去除类型语法并载入 VM。浏览器配置、应用配置和 BrowserManager 是被测真实实现；文件存在/建目录、代理标记、context.close 与 cleanupTempDir 是惰性替身，path.resolve 是纯路径运算。

20 个当前行为断言分为 4 个浏览器配置、9 个应用配置、7 个生命周期用例；全部匹配包括无效并发数未被拒绝及关闭失败后跳过清理。这类特征化测试记录“现在如何运行”，不能把 PASS 翻译为质量合格或缺陷已修复。查看器的 1 正例加 9 负例另计，不能相加成 30 个上游行为测试。

替身记录了 close 或 cleanup 调用，只能证明调用路径，不能证明浏览器进程已退出或目录已删除。没有导入外部浏览器依赖、启动浏览器、导航或运行真实代理；类型语法去除不等于 tsc 类型检查，VM 也不是任意不可信代码的强安全沙箱。关联 [[证据优先质检ProofOverClaims]]、[[证据状态机]]；原 Qwen 函数夹具与本例惰性依赖接缝的方式仍分别标明。

来源：[真实管理器](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/src/browser/browser-manager.ts)、[应用配置](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/src/config/index.ts)、[浏览器配置](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/src/config/browser.config.ts)；[历史实验日志](../../patchright_enhanced/delivery/patchright-enhanced-experiment.log)、[发布审核及历史证据复核](../../patchright_enhanced/delivery/patchright-enhanced-review.log)。

## NCE Reading：组件方法链通过，不等于浏览器和音频通过（2026-10-06）

[[项目笔记/nce_reading]] 的历史实验加载 14 个未改动上游 JavaScript 模块；实验子类仅覆盖 init() 停止自动目录启动，真实父类接线、解析、seek、句界处理与高亮保留。DOM、音频、存储、墙钟和定时器是替身，音频只记录属性/方法/事件，不模拟解码或发声。替身行结构只服务所测 LyricsView，不是完整 HTML 解析器。

所测点击经真实 LyricsView → ReadingSystem → AudioController，tick 触发句尾控制与 active 类更新。统一集合 72 项包括 55 项行为、16 项完整性、1 项保护；六分组共 77 次命中重复了保护项，不增加独立覆盖。零时长负 seek、重复时间零长度句段也按当前行为匹配，PASS 不表示缺陷已修复。

fetch 与全局 Audio 构造的抛错保护在已有记录中为零次尝试；该保护不是任意未知代码的强安全沙箱。异步请求代次、abort 和预取只作源码观察，没有真实网络竞态执行。真实浏览器、布局、移动端、自动播放、CORS、解码、音频听感与学习效果仍待各自证据，关联 [[证据优先质检ProofOverClaims]]、[[确定性快进与真渲染取证]]；不复制这些原则为新概念。

来源：[真实协调器](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/ReadingSystem.js)、[真实歌词视图](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/ui/LyricsView.js)；[历史实验日志](../../nce_reading/delivery/nce-player-experiment-log.md)、[发布审核及历史证据复核](../../nce_reading/delivery/nce-player-review-log.md)。

## Codex advanced：离线契约验证不是桩服务全链路（2026-10-06）

[[项目笔记/codex_advanced]] 实际运行自写 Python 验证器与 jsonschema 4.26.0，读取原样官方 ConfigToml / ClientRequest Draft-07 契约；没有运行 Codex CLI 或 App Server，也没有把桩模型接入其循环。它与前述 Qwen 的真实函数夹具、Patchright 的真实包装层加惰性依赖、NCE 的受控组件接线分别报告，不把所有离线实验统称为端到端。

历史完整集合 25 个合成样本为 8 个接受、14 个 schema 拒绝、3 个解析错误，全部匹配预期；分组与历史独立重放使用同一集合，不增加独立覆盖。四个上游文件指纹与两份 schema 自检也不累计成行为用例。

片段内引用白名单和外部引用检索报错约束验证器路径，不等于操作系统网络审计或未知代码强沙箱。没有真实登录、权益、模型列表、推理、账单、配置生效、协议时序、跨产品接力或原视频复现；未知保持未知。关联 [[Agent输出协议契约]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]。

来源：[固定配置契约](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/core/config.schema.json)、[固定请求契约](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/app-server-protocol/schema/json/ClientRequest.json)；[历史实验日志](../../codex_advanced/delivery/codex-advanced-experiment-log.md)、[发布审核及历史证据复核](../../codex_advanced/delivery/codex-advanced-review-log.md)。

## Route Studio：纯模块通过不证明控制器接缝无副作用（2026-10-06）

[[项目笔记/route_studio]] 的历史实验只加载包入口、gpx、motion，采用原点附近三点、无时间戳的 TEST_ONLY 输入；速度和横向波动均为 0。71 条检查断言包含输入/环境/指纹与行为检查，不是 71 个上游官方测试；借用的 7 个设置反例通过自写 harness 调用，没有运行上游测试模块。

已有静态审核发现 PlaybackController 构造会启动后台线程与设备发现；替换设备工厂并不能证明发现任务停止。因此没有导入或创建该控制器，也没有启动 CLI/Web。Motion 的内存状态推进与控制器暂停、取消、清理、持久化、设备发现、异常恢复分别验收，不能用前者代替后者。

current 在控制器源码中指最近成功发送的模拟坐标，不是设备读回；本实验连发送都没有执行。进程内导入/audit 守卫记录禁止 I/O 尝试为 0，不是 OS 网络审计或未知代码强沙箱。没有真机、定位发送、真实活动导出、传感器、浏览器或完整集成证据，关联 [[证据状态机]]、[[证据优先质检ProofOverClaims]]。

来源：[固定纯模块](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/motion.py)、[控制器，仅静态观察](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/playback.py)；[历史实验日志](../../route_studio/delivery/route-studio-experiment-log.md)、[发布审核及历史证据复核](../../route_studio/delivery/route-studio-review-log.md)。

## OpenMuse：真实 SQL、合成提供方与同进程竞争分开（2026-10-06）

[[项目笔记/openmuse]] 的已有实验执行真实 SQL Store、PGlite、ActionService 与 TaskWorker，数据库不是内存字典替身；execute/prepare、连接判断、任务处理器和时钟是受控 fixture。真实部分与替代部分逐一标明，不将“真实数据库”扩大成“真实外部服务已接通”。

计数是 21 项选取的原样上游测试（12 审批、8 引擎、1 持久化）以及 4 个自写变式。三个上游文件共 22 项定义，PostgreSQL 池错误测试未选择；实际 TAP skipped=0，不能伪写 skipped=1 或全量 22 通过。独立重放、15 项原件指纹与16项依赖完整性不增加独立行为覆盖。

同进程两个 worker 共享一个 PGlite；持久化是正常 close/reopen；目标版本测试只验证向 fixture 传值，不是 Google If-Match/ETag 冲突实验。60001 毫秒来自虚拟时钟推进；未知结果由 fixture 构造，不是真实邮件响应。没有跨进程 PostgreSQL、断电/强杀、账号/模型、浏览器、Docker/E2B 或全应用验证。网络守卫 attempts=0 仅报告所审路径，不是任意代码的强安全证明。

来源：[原始审批测试](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/actions.test.ts)、[引擎测试](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/engine.test.ts)、[所选持久化测试](https://github.com/CopilotKit/openmuse/blob/b06caad7005ac5b6d2b451752a3794a6ae1759c1/tests/persistence.test.ts)；[历史实验日志](../../openmuse/delivery/openmuse-experiment-log.md)、[发布审核及历史证据复核](../../openmuse/delivery/openmuse-review-log.md)。
