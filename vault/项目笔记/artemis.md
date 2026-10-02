---
tags: [项目笔记]
项目: artemis
类别: 开源项目类
完成日期: 2026-10-03
上游: https://github.com/google/artemis
---

# ARTEMIS（google/artemis）

**是什么**：谷歌开源的 Android GUI Agent 框架（2026-08-13 创建，10.9k★，Apache-2.0）——自然语言指令直接转成可靠的真机操作；内置 MCP 服务器让 Claude Code / Antigravity 等 IDE 拿到"操控手机"的 5 个工具（mobile_run_task / get_device_state / diagnose / inspect_trace / manage_tasks）；官方宣称 AndroidWorld 基准 99%+ 任务完成率。README 明确署名复用 minitap-ai/mobile-use（third_party/ 带 NOTICE，评论区"套皮不署名"传言不实）。

**架构一图流**：入口层（CLI/Web 控制台/SDK/MCP 服务器）→ Agent 层（15 角色 ≈2 万行：Flash 循环 + Pro 的 LangGraph 7 节点图 planner→perception→operator→execution_check→validator→summarizer→exit_settlement，带 convergence_gate 收敛闸门）→ 动作/观察层（12 个标准动作 + 截图/XML 融合 + 多供应商模型路由 Gemini/Claude/GPT-4o/Ollama）→ 驱动层（AndroidAdbDriver / Cloud / Mock）→ 真机。

**双模式**：⚡Flash=单 LLM 反应式循环（3~5s/步，click_sequence 连击抢瞬逝 UI，无图无 Checker）；🧭Pro=多 Agent 闭环（~30s/轮，活计划+verify 检查项、verification_level 四档 off/final/checkpoints/strict、只读 Checker 终审）。

**带来的新概念**（3 个）：
- [[GUIAgent与多模态定位]] — 元素索引→坐标→视觉三层 fallback + 坐标自愈
- [[双边缘上下文压缩]] — ScrubEdgeCompressor：文本边缘 depth1 / 截图边缘 depthK，冻结不变量
- [[预执行安全网与执行事件]] — 动前核查 + incident 挂上下文 + fast-action burst

**互链的已有概念**：[[Agent循环]]（Flash 循环的手机版）、[[LangGraph与Agent编排]]（Pro 图，State 用 take_last/sticky_or Reducer、extra="forbid"）、[[程序化工具调用]]（对偶：逐动作点菜 vs click_sequence 打包）、[[MCP协议]]/[[MCP服务器]]/[[工具调用生命周期]]（mcp_server 生产实现）、[[Compaction上下文压缩算法]]/[[上下文预算与战略压缩]]（压缩第三流派）、[[接缝与桩实现StubSeam]]（官方自带 MockDeviceDriver+FakeChatModel）、[[证据优先质检ProofOverClaims]]（rules.md：先探索验证再写测试）。

**实验做了什么**（2026-10-03，Windows 11，无安卓真机——诚实走"仓库+核心逻辑+官方桩"路线）：
1. uv sync 装环境 + 全量单测：**2473 passed / 18 failed / 8 skipped（99%）**；坑①Windows 临时目录 pytest-of-Windows PermissionError 577 errors → `--basetemp` 指本地全清；坑②CLI 直跑被设备发现拦（No Android device found）
2. ex2 亲手驱动 MockDeviceDriver：5 动作全 True，action_history 流水账如实记录；坑：get_current_package 是 async 忘 await
3. ex3 源码级拓扑提取：Pro 图 7 节点、12 动作集、角色行数榜（video_analyzer 5415 > explorer 3598 > operator 2458 > validator 2251 > flash 2137）→ exercise/pro_graph.json
4. ex4 双边缘压缩验证：scrub_edge + ledger + memory **169 测全绿**；附带发现 test_explorer 13 失败=MagicMock 撞严格枚举校验（测试基建问题非功能缺陷）

**坑与结论**：
- 坑：`ARTEMIS_FAKE_LLM=1` 必须设，否则大量测试/实例化要 API key；`ARTEMIS_MOCK_DRIVER=1` 只影响驱动层，CLI 入口仍有设备发现门槛——无真机走 pytest/脚本层，不走 CLI 端到端
- 坑：Windows 下 pytest 必带 `--basetemp`（系统 Temp 目录 ACL 问题），GBK 环境必带 `PYTHONUTF8=1`
- 结论：GUI Agent 的工程难题（定位/压缩/自愈/编排/集成）在这一个仓库里都有生产级参考答案；学习价值 > 立刻上生产价值（真机玩法需补一台测试机）

**产出**：`artemis/ARTEMIS-小白指南.pdf`（12 问彩色图文）+ `artemis/artemis_guide.html` + `artemis/exercise/`（ex2/ex3 脚本 + pro_graph.json）
