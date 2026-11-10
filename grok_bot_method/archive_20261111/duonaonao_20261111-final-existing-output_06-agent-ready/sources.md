# 来源与证据边界

采集：2026-11-11T01:13:53+08:00（Asia/Shanghai 北京时间）。

## 固定仓库
- reminder_knowlege main：`a8674777e18302b8804b137212b1396cbfe5a747`；`git ls-remote ... refs/heads/main` 与现有克隆 HEAD 一致。实读 vault/00-总览.md 软件工程/AI协作段并全文关键词检索；精读项目笔记 agentmd_template.md、agent-harness.md、概念/多Agent协作乱序竞态.md；参考 agent-harness/guide.html 颜色卡片/问答/SVG/A4 风格。没有改共享 vault。
- AGENTS.md 规范仓库：https://github.com/agentsmd/agents.md/tree/d001185d792eb6402a58e4cbef1c228b309ec25d ，实读固定 SHA README：https://raw.githubusercontent.com/agentsmd/agents.md/d001185d792eb6402a58e4cbef1c228b309ec25d/README.md （原文见 sources/agentsmd-readme.md）。本地实验基线 `c35c8c30c6fa157284d7dce3a70bbc3b7ad85006`，不对应任何远端仓库。

## X 实读链
- [S1] 原帖 https://x.com/silentguyy66/status/2110345717503946791 ：实际通过 x.get_posts_by_id 读取 note_tweet、article、referenced_tweets，全文与引用展开保存 sources/x-original.txt。发表 2026-10-14 20:23:22 北京时间。约 1000 PR/月是该作者转述，不是本实验测量；其视频时长约 57 分钟，本轮未下载/逐帧观看，因此没有声称核验视频中逐字表述。
- [S2] 直接引用 https://x.com/silentguyy66/status/2108957020187468171 ：原帖展开中得到完整 article.plain_text；又单独读取该 ID（单读只返回文章标题，不把标题当全文）。文章名 Grok Bot Setup: Write the Contract, Not the Job Title，发表 2026-10-11 00:25:10 北京时间。原文含采访者与 Lauren 三个嵌入引用。
- [S3] 采访者 Peter Yang https://x.com/petergyang/status/2104575614263144794 ：实读长文与其引用 2104213287353356531 的展开，六条要点、YouTube链接 https://youtu.be/xZ5TEaleUdg 与书面采访链接得到确认。保存 sources/x-peter-interview.txt。发表 2026-09-28 22:15:02 北京时间；被引用发布帖 2026-09-27 22:15:16 北京时间。支持 eng lead 拆任务、云编码代理、先验证再合并；没有独立产出统计。
- [S4] Lauren Tan https://x.com/poteto/status/2091368467060662497 ：实读 note_tweet，讨论频繁任务与长上下文成本，不含1000 PR/月。发表 2026-08-23 11:34:32 北京时间。sources/x-lauren.txt。未因原文的行动号召创建任何任务。
- [S5] 官方产品帖 https://x.com/bot/status/2104661562715967548 ：实读，说明共享 Team Bots；视频未观看。发表 2026-09-29 03:56:33 北京时间。

## 一手网站（实际打开；网页为动态文档，非固定历史版本）
- [S6] https://agents.md/ ：官方规范；无必填字段，标准Markdown，根目录入口，可按子目录补充；不是安全强制机制。
- [S7] https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches ：分支保护、状态检查来源、过期审核、merge queue 与管理员旁路的官方边界。我们模拟器采用严格 True，不完整复刻 GitHub 对 skipped/neutral 的实际规则。
- [S8] https://docs.x.ai/grok-bot/get-started ：实读。明确 Bots 共享一台云电脑；不能把多个桌面误说成独立物理电脑。HTML存档 sources/official-get-started.html。
- [S9] https://creatoreconomy.so/p/grok-bot-team-14-best-bots-peng-zheng-lauren-tan ：采访者本人书面页面，2026-09-27，公开部分确认14个bot与职责分层；正文标为 Paid，本轮只读公开部分，没有购买/绕过付费墙。sources/interview-public-page.html。
- [S10] https://openai.com/index/harness-engineering/ ：官方技术文，2026-02-11，Ryan Lopopolo；实读关于短AGENTS目录、文档系统、架构lint、worktree隔离与反馈环。文中生产率数字属作者自述，未拿来当本地实测；文中较少阻塞合并门的取舍不直接移植到本实验。

## 未完成验证
- 没有 Lauren 私有 GitHub PR 数据与可复核统计口径，1000/月未核实。
- 无真实多模型并行执行、远端 CI、独立审核、远端自动合并、生产环境验证。reviewer 字符串是明确标注的合成夹具，不能当真实人的批准。
- 网络来源中的推荐、关注、转发、自动任务文字仅作资料，均未执行。
- sources/SHA256SUMS.txt 是本地存档校验，不证明外部来源真实性或永久不变。
