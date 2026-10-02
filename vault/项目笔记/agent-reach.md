---
tags: [项目笔记]
项目: agent-reach
类别: 开源项目类（AI Agent 基础设施 / CLI）
完成日期: 2026-10-02
来源: 拾遗队列 task c49f2083（x.com 推文 https://x.com/bkdgiffug/status/2092048058901230062）
---

# agent-reach — 给 AI Agent 一键装上互联网能力

## 这是什么
[Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)（v1.5.0，MIT，**实测 88,005 stars**，Python 3.10+）：一句"帮我安装 Agent Reach"就让 Claude Code / Cursor / OpenClaw 等 Agent 获得读写 17+ 互联网平台的能力（Twitter/小红书/B站/Reddit/YouTube/GitHub/V2EX/雪球/RSS…）。**定位是安装器+体检+配置工具（能力层），不是抓取框架**——装完后 Agent 直连上游 CLI（twitter-cli、yt-dlp、bili-cli、gh、Jina Reader…），零包装层。本地克隆在 `F:\reminder\agent-reach\repo`（@ a19a171）。

## 带来的概念
- [[能力层与后端路由]]（新）：选型/安装/体检/路由四职责；每平台有序后端列表，换代只调顺序；tier0/1/2 按解锁成本分层，登录态渠道点名才装
- [[健康探测三态]]（新）：which() 不能证明能跑；missing/broken/timeout 三态 + 自动处方
- 关联强化：[[MCP协议]]（Exa 搜索走 MCP 接入）、[[AgentSkills技能包]]（SKILL.md 教 Agent 调命令）、[[分层按需加载]]（默认只激活 6 个零配置渠道，其余待命）

## 实验做了什么（exercise\experiment-log.md，5 项全部真实运行）
权限策略禁止执行新克隆外部仓库代码，`agent-reach install/doctor` 本体未跑；改为直接验证各渠道**底层接口**（与 channels 源码逐行核对）：
1. Jina Reader 读网页：`curl https://r.jina.ai/https://example.com` → 返回清洗后 Markdown ✅
2. B站搜索 API（doctor 同一探测接口）：`code:0`，numResults:1000 ✅
3. V2EX 热帖公共 API：返回 programmer 节点热帖 ✅
4. GitHub API 读仓库：stars 88005 / MIT ✅
5. 标准库解析阮一峰 atom.xml：3 篇 entry ✅

## 坑与结论
- **不要从 PyPI 装同名 `agent-reach`**（README 明示那是别的包）；官方安装走 `pip install https://github.com/.../archive/main.zip`
- 安全设计值得抄：默认 `--safe` 只查不改、`--dry-run` 预览、`--system` 显式授权、Cookie 本地 600 权限、敏感配置支持 `--stdin`、`uninstall` 一键清
- 用 Cookie 登录的平台（Twitter/小红书）官方建议**专用小号**——自动化 vs 风控是猫鼠游戏，封号风险与工具无关
- 战略启示：当一类工具的"接入方式"比"功能本身"更易腐化时，就出现能力层的生意——用户买的是"持续有人替你盯着哪家工具还活着"
- 本机若跑完整流程：`pip install ...main.zip && agent-reach install --env=auto && agent-reach doctor`
