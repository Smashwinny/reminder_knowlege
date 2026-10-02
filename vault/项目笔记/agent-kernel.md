---
tags: [项目]
类别: 知识学习类（六周【Agent 内核拆解】系列配套教程仓库）
上游仓库: https://github.com/yanhua1010/build-your-own-coding-agent
完成日期: 2026-10-03
---

# agent-kernel（Agent 内核拆解）

**这是什么**（一句话）：X 用户 @yanhua1010 六周拆解 pi（78k★）/codex（101k★）/grok-build（23k★）三个工业级 coding agent 的收官系列配套仓库——每篇带行号引用的源码解析笔记（notes/ 五篇）+ 一个可独立运行的 mini-agent 阶段代码（steps/ 五阶），从"Agent 就是个 while 循环（118 行）"一路拆到"沙箱与审批是两件独立的事"。触发链接：https://x.com/yanhua1010/status/2098728177288024247（收官帖："pi 这种也算工业级？加几个工具不就完了？"）。

**它给我什么能力**：①行号级读工业级 agent 源码的方法（先调用栈分层，再错误契约+事件序列闭合两个不变式）；②从零写 agent 的五阶路线（loop→协议层→工具流水线→压缩→安全）；③sandbox×approval 两轴评估任意 coding agent；④压缩算法完整实现细节；⑤136 条离线断言示范"不打网络怎么测 agent"。

**引入的概念**：
- [[沙箱与审批正交]] — 系列最核心洞见：两轴独立 + 能力≠默认姿态（grok-build 能力最强默认沙箱却是 off；默认强制沙箱的只有 codex 和 dsh）
- [[工具调用三段式流水线]] — prepare/execute/finalize + 截断整批作废 + 一票降级全票终止 + 并行三顺序刻意错开
- [[Compaction上下文压缩算法]] — 阈值/溢出双路径触发 + 切割点 + 结构化摘要 + 文件操作程序化提取
- [[Provider适配层与错误契约]] — API×Provider 两维 + "永不 reject / 工具必须抛"双规则

**实验记录**（全部真实运行）：
- **协议适配 shim**（exercise\anthropic-shim.mjs，130 行零依赖）：本机仅 z.ai Anthropic 端点可用（OpenAI 兼容端点无余额），写 OpenAI→Anthropic 双向转换（工具 schema 映射/tool_result 合并/SSE 合成/429 等 65s 重试），非流式+流式两路径 curl 实测通过
- **在线实验 1**：step01 mini-agent（118 行）经 shim 跑 glm-4.6 真任务"写秋天小诗+cat 确认"→2 次工具调用自主完成，poem.txt 落盘 ✅。坑：step01 的 `LLM_BASE_URL` 需含完整路径（含 /chat/completions）
- **在线实验 2**：读工作目录外文件 → safePath 拒绝 → 错误文本回灌 → 模型主动放弃绕过并解释沙箱设计——"错误不抛出，还给模型"教科书行为真机复现 ✅
- **离线四实验**：demo-order（3s/1s/2s 并行 3.0s vs 串行 6s，完成序 2-3-1 喂回序 1-2-3）；demo-compaction（799→594 tok 释放 205，切割点第 7 条）；demo-security（9 命令 5 危险、五姿态、env 清洗）；四个 test.mjs 共 136 断言 0 失败
- **坑**：Windows 无 macOS sandbox-exec，demo 按设计原样透传（test.mjs 亦有对应断言，非缺失）

**后续可深入的方向**：照 mini-agent 实现清单补 steering 队列和失败路径补发事件；对照 pi 源码读 792 行 agent-loop.ts 本体；用 Claude Code 的 /compact 行为反推其 compaction 参数。

**关联项目**：[[项目笔记/agent-harness]]（ECC 方法论，环境侧）、[[项目笔记/cmu-agents]]（课程作业版 agent loop/压缩）、[[项目笔记/openai-agents-api]]（托管 harness 与 codex sandbox 实测）、[[项目笔记/agentic_design_patterns]]（模式目录）
