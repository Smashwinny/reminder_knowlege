---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/JCodesMore/ai-website-cloner-template
完成日期: 2026-10-02
---

# ai-website-cloner（AI 网站克隆模板）

**这是什么**：GitHub 35.6k star 的"提示词工程包 + Next.js 16 脚手架"——给 AI 编程智能体（Claude Code 推荐/Cursor/Codex/OpenCode）一个 URL，按五阶段流水线（侦察→地基→组件规格→并行构建→组装QA）把网站一对一复刻成干净的 Next.js 应用。核心资产是 506 行 `.agents/skills/clone-website/SKILL.md`，真正干活的工人是 AI agent。

**它给我什么能力**：迁移老站到 Next.js、重建丢失源码的站、克隆喜欢的站逐行学大厂前端手法、快速生成改版底稿。完整克隆需浏览器 MCP（Chrome/Playwright）；禁止钓鱼/盗用品牌资产。

**引入的概念**：
- [[GitWorktree并行隔离]] — 多 builder 并行施工互不打架的物理隔离
- [[规格书先行SpecDriven]] — getComputedStyle 实测值写 spec 当合同，禁止目测

**实验记录**（全部真实运行）：
1. `npm install` → exit 0；`npm run check`（lint+typecheck+build）→ exit 0，Compiled successfully 9.0s；
2. `npm start` + curl localhost:3000 → HTTP 200 / 6727 字节首页；
3. 自写 `exercise/recon.mjs`（无浏览器版侦察：fetch+正则清点资产+技术栈指纹）：example.com → 713B/0 资产；nextjs.org → 65 img、77 内联 SVG、isNextJs=true。
4. 坑：String.match 带 /g 忽略捕获组，需非全局正则另取组；完整克隆流程卡在"必须有浏览器 MCP"（skill 的 Pre-Flight 硬检查）。

**关键工程纪律**（值得复用）：交互模型先行判定（先滚动观察再点击，判定错=整个组件重写）；150 行复杂度预算（超了就切小块派工）；每次合并必须 build 绿；builder 提示词内联完整规格零猜测。

**后续可深入的方向**：装 Playwright MCP 后用 Claude Code 真跑一次 `/clone-website`；读 `node_modules/next/dist/docs/` 了解 Next.js 16 破坏性变更。
