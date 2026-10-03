---
tags: [项目笔记]
项目: openai-agents-api
类别: 知识学习类（OpenAI Agents API 平台发布拆解：托管 Codex harness + 开源仓库取证）
完成日期: 2026-10-03
---

# openai-agents-api — OpenAI Agents API（托管 Codex harness）

## 这是什么
2026-09-10 OpenAI 发布 Agents API（public beta）：把开源 Codex harness 搬上云端变成 REST API。应用侧只发任务收事件；模型循环、上下文压缩、断点恢复、subagent 编排、沙箱全由 OpenAI 托管。官方文档 developers.openai.com/api/docs/guides/agents-api/*（支持 `.md` 后缀抓纯文本），开源仓库 github.com/openai/codex（Apache-2.0，127k+ stars）。

## 带来的概念
- [[托管Harness与会话即资源]] — harness SaaS 化总纲 + 三层运行时选型
- [[沙箱三态与Executor]] — none / openai_hosted / self_hosted 三态架构

互链（已有概念，无重复建条）：[[AgentHarness智能体挽具]]（七职责对上 131 crates）、[[程序化工具调用]]（被产品化为开关）、[[上下文预算与战略压缩]]、[[Checkpoint存档与持久执行]]、[[工单任务图与前沿调度]]、[[多Agent协作乱序竞态]]、[[控制面与数据面]]。

## 实验做了什么（全部零 key 零费用，exercise\ 下）
- **ex1 SDK 内省**：openai 2.54.0 无 `beta.agents`，升级 3.24.0 后命名空间齐全；sessions 子资源 turns/events/items/subagents/artifacts/traces/stream；161 个 agent 类型；subagent 生命周期三件套（Create/Interrupt/Close）都是 item；还发现 vault_ids / output_type / environments / vaults 资源。
- **ex2 无 key 真请求**：`POST /v1/agents/sessions` 无 key→401（"A valid actor biscuit is required"，OpenAI 内部鉴权术语），假 key→401，不存在端点→404。端点真实存在。
- **ex3 会话体构造器**：三架构场景请求体构造 + 契约校验（环境三态/工具枚举/并发上限）全 PASS，负向用例（none 环境带工作区）被拦。
- **ex4 harness 源码取证**：131 crates / 5094 个 .rs / 2,002,055 行；推文五大能力全部钉到源码坐标（compact.rs / rmcp-client / agent/control/execution.rs / sandboxing / rollout）。
- **ex5 本地 CLI 沙箱**：`npm i -g @openai/codex`（0.160.0）；`codex sandbox` 沙箱内 python 命令真跑成功、写文件被 PermissionError 拦死（文件未落盘）——生产沙箱零费用实物教学。本机为 ChatGPT 登录态，为不耗配额未跑真实 agent 任务。

## 坑与结论
- `openai-agents` 0.20.0（旧 Agents SDK）与新 SDK 3.x 依赖冲突——两代产品并存，别混。
- 开发者文档 404 常见：正确入口是 `/api/docs/guides/agents`，页面加 `.md` 得纯文本。
- 计费无"API 附加费"，但沙箱按容器时长计费——**账单放大器 = 循环圈数 × 沙箱时长 × subagent 并发**。
- 数据仅美国驻留、不支持 ZDR（self_hosted 也不改变）；API key 权限拆分 api.agents.read/write + api.responses.write，key 永不进沙箱。
- harness 云端与本地 CLI 同源（同一套开源实现），学 harness 机制可零成本在本地做。

## 产出
- `openai-agents-api/OpenAIAgentsAPI-小白指南.pdf`（12 问彩色，5 实验全记录）
- `openai-agents-api/openai_agents_api_guide.html`（PDF 源）
- `openai-agents-api/exercise/ex1~ex5`（脚本 + harness_forensics.json + session_bodies.json）
- 拾遗任务 edc8f196（MaxForAI 推文 → 官方公告/文档/开源仓库三级查证，判学习类）

## 补遗：sitin 科普文拆解（拾遗任务 6628a24f，2026-10-03）
同一主题的第二条拾遗链接：sitin 的 X 文章《Agents API来了，Codex背后的这套能力终于开放了》（文章 ID 2100394871265820672，2026-09-18）。判学习类，走增补路线（不重复建项目/概念，只做查重合并）。增量与产出：
- 新增概念 [[产物留痕与状态外置]]——文章金句"不要让 AI 靠记忆硬撑"，与 Checkpoint（怎么续跑）/JSONL 事件日志（怎么留痕）互补
- 文章独有增量（官方文档不讲的认知框架）：Agent≈Model+Harness 五问、长任务轮次论（不是一直想，是工具结果喂回来再决策）、工具按任务开放（最小授权）、子agent"独立并行/共享串行"判据、验收标准写进任务（构建通过≠完成）、Codex=成品餐厅 vs Agents API=开放后厨（不是把 App 嵌进产品）
- ex6_mini_harness.py：200 行纯标准库 mini-harness，六步实测文章六大主张全过（模型零状态字段/产物链落盘/session 重启续接+追加要求/并行只读+串行写/Gate 拒收谎报/验收进配置 A/B 4:4 PASS）；坑：环境无 flask → ModuleNotFoundError 顶掉 RuntimeError 伏笔，改本地 miniflask 桩模块
- 事实核对：文章主张 vs 官方文档全部吻合，无虚构；文末 HiAPI.ai 广告为作者自家推广
- `openai-agents-api/AgentsAPI科普拆解篇-小白指南.pdf`（10 问彩色 7 SVG + ex6 六步实录）
