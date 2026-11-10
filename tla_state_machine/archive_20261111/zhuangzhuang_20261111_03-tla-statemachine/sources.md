# 来源、版本、可读性与访问日期

统一访问：2026-11-11 Asia/Shanghai。所有报告时间按Asia/Shanghai（UTC+8）；非Git帖子/网页不伪造commit SHA，人工转录/摘录不假装原始API快照。原始GitHub发行元数据保留接口自带时间，说明中另作时区换算。

## 原帖与两层引用
- [X0] https://x.com/i/status/2112783187667734833 — 原帖全文可读；规范URL https://x.com/0xlangeai/status/2112783187667734833 ；创建2026-10-21 13:49:00 Asia/Shanghai。SHA不适用。
- [X1] https://x.com/poteto/status/2112736749281759566 — 通过展开引用读到note_tweet全文；创建2026-10-21 10:44:28 Asia/Shanghai。SHA不适用。
- [X2] https://x.com/poteto/status/2111926622278521253 — 两次长文请求仍无note_tweet，正文截断，部分可读；创建2026-10-19 05:05:19 Asia/Shanghai。缺文未补写。SHA不适用。
- https://pbs.twimg.com/media/HVHyOOYa4AA9MlZ.jpg — 已下载并Read，假想通知状态图；不是本轮实测。
- https://pbs.twimg.com/media/HU8SDLJbcAA_51s.png — 已下载并Read，仅猫与公式趣味图，不能补齐发布帖。

整理原文与阅读边界见sources/x-reading.md；未声称读完评论区。原帖全文可读，不标整项受阻。X0所称作者已找到几个bug，未由可读原作者材料独立核实，不作为本轮成果。

## pstack官方一手仓库
canonical https://github.com/cursor/plugins/tree/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack
主仓main SHA `de8ee15dd1194627d21eb5fcd41cb1873208dabb`；插件元数据0.15.36，作者Lauren Tan，MIT。提交时间2026-11-10 11:28:06 Asia/Shanghai。已浅克隆并稀疏检出pstack，只读研究，不提交/推送。
- https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/skills/create-formal-verification-skill/SKILL.md — [P1]全文实读；选目标、选工具、让检查能失败、范围与覆盖记录。
- https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/skills/maintain-formal-verification-skill/SKILL.md — [P2]全文实读；模型漂移、业务bug、同步基线与维护判读。
- https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/skills/statechart/SKILL.md — [P3]全文实读；状态/转移标签、终态、图形压缩与报告边界；未执行其mise安装或渲染脚本。
- https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/docs/guide/06-verify-and-ship.md — 实读1–115，尤其96–114形式化验证；没有执行文中开PR/发布/日程建议。
- https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/.cursor-plugin/plugin.json — 全文实读；当前版本与作者/仓库。
- https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/LICENSE — 全文实读，原样保留MIT文本。

发现线索（不是一手）：https://github.com/backnotprop/pstack ，固定镜像08547969e1dffaa6457ea65141cc62c1d9a2eef1。初次搜索命中，读README1–70与技能后发现standalone mirror并纠正；不将其重写的跨宿主说明当作原作者源码。仓库元数据“fork=false”也不改变README明确的镜像身份。该镜像保存在本项mirror-discovery，仅溯源，不用于实验。

## 知识库查重与旧成果风格
知识库 https://github.com/Smashwinny/reminder_knowlege ，首先git ls-remote确认main仍为 `a8674777e18302b8804b137212b1396cbfe5a747`，只读复用已克隆快照；不改共享_common。总览与旧HTML风格沿用前项已实读的相同SHA；本项另搜索相关词并读下列笔记。pstack/TLA+/形式化验证/模型检查没有直接项目成果，仅“不变量”命中与其他领域无损压缩等有关，不能当作已有TLA知识。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md — 沿用前项已读总览，并在本项全文关键词检索。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/LangGraph与Agent编排.md — 全文实读；是运行编排状态图，不等于形式化检查。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/工具调用生命周期.md — 全文实读；读取/删除非原子与外部副作用边界。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/动作投递语义与安全重试.md — 全文实读；动作投递与业务完成不同。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/证据状态机.md — 实读1–49；未知/自述/成功应分开。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/agent_desktop/agent_desktop-小白指南.html — 前项已研究旧风格；本项复用01-elyterminal/_tools模板的卡片/问答/图示与分页。

相关命中留存sources/dedup-hits.txt与dedup-state-hits.txt；只补新增的模型检查/反例与同步合同，不重复LangGraph或安全重试定义。

## 官方TLC与Java发行
- [T1] https://docs.tlapl.us/using:tlc:start — 全文WebFetch可读；动态文档，无本轮Git SHA。人工摘录见tlc-reading.md，实际支持参数以下载JAR的-help输出为准。
- [T2] https://github.com/tlaplus/tlaplus/releases/tag/v1.7.4 — 官方发布正文/资产可读，实际下载；tag SHA `5a47802b5c391f59ecdd44117981f4ff8c0656ba`；TLC2显示2.19 rev5a47802。
- https://api.github.com/repos/tlaplus/tlaplus/releases/latest — 公开元数据本轮返回v1.7.4，已保存tlaplus-release.json；不把“latest接口返回值”外推为所有开发版的最新。
- https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar — 实际取回2,274,532字节。发布正文SHA1已核对；本地SHA256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`，不冒称官方SHA256或签名认证。
- https://github.com/tlaplus/tlaplus/blob/5a47802b5c391f59ecdd44117981f4ff8c0656ba/LICENSE — 通过固定raw URL实际取回并Read，MIT；本地sources/TLC-LICENSE。TLC与pstack的许可/版权各自保留。
- https://api.github.com/repos/adoptium/temurin21-binaries/releases/latest — 公开元数据返回jdk-21.0.13+9，已保存java-release.json。
- https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.13%2B9 — 发行标识；本轮读API资产元数据，不冒称读完页面正文。
- https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.13%2B9/OpenJDK21U-jre_x64_linux_hotspot_21.0.13_9.tar.gz — 实际下载52,181,297字节，只在本项目录解压；SHA256 `a535a1df9c6284d9618872984e026ae0352d1f7e9e0605425c0e6114f47351dd` 与发布校验文件及GitHub资产digest一致。JRE按其自带许可，不沿用pstack的MIT。
- https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.13%2B9/OpenJDK21U-jre_x64_linux_hotspot_21.0.13_9.tar.gz.sha256.txt — 已实际读取并核对。工具详细锁值与路径见toolchain.json。

## 只作搜索发现，不当核心证据
https://learning.tlapl.us/intro/tlc-config/ 、https://learning.tlapl.us/intro/platform/ 、https://lamport.org/tla/safety-liveness.pdf 及搜索结果中的其他pstack移植仓库仅用于发现。未全文实读/下载这些页面/论文，不将其声称作为已读一手正文；核心结论来自上方官方技能、Wiki、固定发行与真实输出。

## 边界声明
未安装或调用pstack插件、未执行官方statechart脚本，未运行付费模型/API。按手册原则自编合成模型/代码与候选验收合同，真实调用官方TLC。未把TLC有限模型通过当作数学定理证明、真实产品验收、任意规模/活性保证或独立审核。

补充发现元数据URL：https://api.github.com/repos/backnotprop/pstack （只读归属元数据）；https://api.github.com/repos/tlaplus/tlaplus/contents?ref=5a47802b5c391f59ecdd44117981f4ff8c0656ba （只读根目录定位LICENSE）。本地JSON留存，不当作行为验证。
