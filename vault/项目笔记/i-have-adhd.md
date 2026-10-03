---
tags: [项目笔记]
项目: i-have-adhd
类别: 开源项目类（Agent Skill / 输出设计）
上游: https://github.com/ayghri/i-have-adhd
学习日期: 2026-10-03
---

# i-have-adhd — 管住 AI 编程助手"废话嘴"的 Agent Skill

**是什么**：ayghri/i-have-adhd（52,965★，MIT，2026-05 创建）。本体是一个 142 行的 `skills/i-have-adhd/SKILL.md`：把临床《The Adult ADHD Tool Kit》的注意力管理原则翻译成 LLM 输出规范——5 条认知事实 → 10 条规则（行动先行/多步编号/收尾给 2 分钟钩子/压支线/每轮重述状态/分钟级时间估计/成果可见/错误只说因和修/列表≤5/禁开场白复盘客套话）+ 6 条逃生舱 + 发送前五删检查。周边是多 harness 打包（Claude Code/Antigravity/Gemini/OpenCode/Kimi/Qwen/OpenAI/pi 八种插头）、SessionStart hook 常开模式、自带评测体系。

**带来什么新概念**（详见笔记本体）：
- [[答案埋葬与行动先行]] — 病名与解法；五删检查可机器化
- [[格式压力编因]] — 规则8"错误必报因"在证据不足时会压出硬编原因（官方评测 partial-success −0.63 的机制假设）

**实验做了什么**（exercise\，全部真实运行、零 API 费）：
- exp1 SKILL.md 结构契约体检 **28/28 PASS**（frontmatter/关闭短语与扩展 STOP_PHRASES 逐字对账/10 规则标题/6 逃生舱/规则9 红线）
- exp2 去埋葬体检器 **4/4**：README 官方 Before 抓下 3 违规、After 放行、自造正反例同向；终检句（只读首末行）成立
- exp3 always-on hook Python 等价复刻 **10/10 PASS**（剥头正则 + CRLF/无头/正文含 --- /只有头 四夹具）；上游 .mjs 被安全策略拦未执行，源码逐行对照
- exp4 上游 eval 聚合器：validate/plan PASS；合成数据 measure delta 手工核算一致（tok −75.4%/cost −40%/chars −88.6%）；负 token 拒收
- exp5 考卷普查：14 用例/12 类别/风险 4低6中4高/criteria 29 条

**坑与结论**：
- 上游 pytest 全套被本机 [Code from External] 安全策略拦，未绕行，如实记录
- RESULTS.md 的 agent-owned-edit 用例**任何条件都不可能通过**（runner 传 --tools "" 而判分要求动手改仓库）——用例设计与测试环境自相矛盾的示范
- 增益集中在状态汇报类用例；有明确输出合同的用例（code-answer）增量为零——逃生舱按设计生效
- 发布门槛教科书：无 blocker + 正确性/安全差距≤0.1 + 加权分高于 baseline + 竞品对比必须同 cases/models/trials/rubric

**产出**：`i-have-adhd\i-have-adhd-小白指南.pdf`（12 问，7 张 SVG）＋ guide.html ＋ exercise\ 三个自写实验脚本与合成数据。
