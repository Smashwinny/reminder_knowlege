---
tags: [项目笔记]
项目: codex-claude-resets
类别: 开源项目类（source-available 非商业许可）
上游: https://github.com/shixi-11/codex-claude-resets
学习日期: 2026-10-03
来源: 拾遗队列 task c59e4f4d（x.com/11Shixi/status/2097766387821490562）
---

# codex-claude-resets — Codex/Claude 重置公告追踪器

## 一句话
Shixi Lin（@11Shixi）做的单页追踪站：每 30 分钟"听"六个官方 X 账号（@thsottiaux/@OpenAIDevs/@OpenAI/@ClaudeDevs/@AnthropicAI/@claudeai）的额度重置公告，验证过的下次重置时间按访客本地时区倒计时，九语言静态页；整个"数据库"就是一个 Git 仓库（data/*.json），GitHub Actions 提交、Vercel 构建。约 1200 行零依赖 JS。

## 带来的新概念
- [[证据状态机]] — kind×state 双标签：announced/reported/unconfirmed/information 四态，截断一票否决，规则升级全量重分类
- [[中继交叉印证]] — FxEmbed 发现 + X 官方 oEmbed 独立验证，author/ID/时间戳/文本前缀逐项咬合才入库，provenance 记 `x-oembed+fxembed`
- [[提交即部署]] — Actions cron 提交 data/*.json，Vercel Git 集成自动构建，git log 即审计日志

## 激活的已有概念
[[事实与判断分离]]（确定性规则分类，零 LLM）· [[健康探测三态]]（分平台健康记账，"没消息"≠"故障"，3 小时无成功即 stale）· [[AI味模式库与信号非证据]]（unconfirmed 信号不得驱动倒计时）· [[快照契约与不可变只读]]（失败保留旧记录）· [[数据源降级链]]（x-api→profile-relay→community-discovery 三档）· [[缓存]]（translations.json 绑定 fullText+contentHash 双键）· [[零依赖编程]]（node:test/内建 fetch/手写静态构建）

## 实验做了什么（2026-10-03 全真跑，Node v24.21.0，零依赖免 install）
1. `node --test`：60/60 全过（823ms）
2. `node scripts/build.mjs`：Built 9 locales, 78 events and 711 pages
3. `node scripts/serve.mjs` + curl：/ 313B meta-refresh 跳板 → /en/ 465KB 完整页，/zh/ 中文标题正常
4. `node scripts/collect.mjs` 真实采集：6×FxEmbed 时间线全 ok（候选 19/11/16/14/21/18），mode=profile-relay，78 记录保留
5. 直调 `evidence.mjs` classify()：6 组用例验证状态机，同一文本截断即跌 unconfirmed，RULES_VERSION 1.4.2

## 坑与结论
- **msedge 不在 PATH**：PDF 打印用完整路径 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- `classify(text, {truncated, author})` 第一参数是纯字符串，传对象会 `text.replace is not a function`
- 根路径 `/` 是 313 字节 meta-refresh 跳板，真页面在 locale 目录（/en/ /zh/…），canonical 指向生产域名
- 许可证是自定义非商业 source-available（不是 MIT）：学习/修改/分享随意，商用要书面许可
- 整页只存短摘录+内容哈希不整篇转载推文——引用量本身也是设计
- 调度错峰在 :07/:17/:27/:37/:47/:57，避开 GitHub 整点拥堵

## 产出
- `codex-claude-resets/CodexClaude重置追踪器-小白指南.pdf`（812KB，12 问卡片 + 10 SVG + 5 步实验）
- `codex-claude-resets/guide.html`（PDF 源）
- `codex-claude-resets/exercise/实验记录.md`
- repo 克隆于 `codex-claude-resets/repo` @ c2a9a70（gitignore 排除）
