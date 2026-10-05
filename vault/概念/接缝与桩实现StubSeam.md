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
