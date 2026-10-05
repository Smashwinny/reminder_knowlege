# Ponytail 知识笔记与入库提案

日期：2026-10-05 UTC。项目：DietrichGebert/ponytail。固定版本：e15862bb04d04285233a164460ced063941d9ef5。

## 结论

Ponytail 提供一套编程取舍方法：先读懂任务与真实流程，再按七阶顺序选择最早够用的方案。少代码只有在必要功能、输入边界、安全、错误处理和可访问性保留时才有意义。提示文本不能替代程序约束和测试。

## 查重范围

已检索固定公开索引394条元数据，全文读取并核对5篇公开概念笔记；没有把其余389篇算作已读。索引版本为1f61909da967cea8bc68dbfaffc642a4331b3352，正文版本为1043e9d6080bff7af9724162e2c44559fab63e40。另完整读取网站既有HowToLiveBetter笔记1篇（四块合并），6202字节、SHA-256为12eb84e8e59202e18feb892416f4a345895b863ea5a9ce06c30d90ecbc86b3c9。这里只覆盖已发布快照与本轮获准列表知识；未读取最新Windows vault、私密原记录或未提交笔记。笔记存在不代表用户已经掌握，仍待本机回迁核对。

## 五篇已有概念如何复用

### AgentSkills技能包

沿用Skill是方法包、Tool是执行能力的区分。补充：Ponytail的文本、宿主载入、实际行为和结果测试是不同层次的证据。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AgentSkills%E6%8A%80%E8%83%BD%E5%8C%85.md

SHA-256：bb055a1f106f721c5c71a3a2b359c16d11190fbc261c772d63a7bbc3782f011b；字节数：1536；全文及哈希已核对。

### Agent指令文件AgentMd

沿用仓库规则作为行为基线的理解。补充：完整技能、紧凑规则、hook有不同职责和副作用；不能把安全措辞当作强制安全机制。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Agent%E6%8C%87%E4%BB%A4%E6%96%87%E4%BB%B6AgentMd.md

SHA-256：d301f65e52f62ebcf6066bf86fa6eadd34ee219b3549938c83738fe6ebb9fe90；字节数：2952；全文及哈希已核对。

### 事实与判断分离

旧网站笔记已经复用此概念。补充：上游作者基准、源码静态观察、本次确定性实验与工程判断必须分栏，不互相冒充。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%8B%E5%AE%9E%E4%B8%8E%E5%88%A4%E6%96%AD%E5%88%86%E7%A6%BB.md

SHA-256：53f5643580c0ab2e2860c6d2b25e3ea7eeb80cf806c1fdf4d989cab59319427b；字节数：1653；全文及哈希已核对。

### 证据优先质检ProofOverClaims

旧网站笔记已经复用证据优先；本次不新建同义条目。补充同契约测试、负对照、源码指纹与PDF逐页视觉检查的各自范围。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md

SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac；字节数：3593；全文及哈希已核对。

### 零依赖编程

沿用“优先考虑标准库、降低环境负担”。补充：Ponytail还先看需求和仓库复用，并允许合适的已装依赖；不能为零依赖重写可靠组件。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E9%9B%B6%E4%BE%9D%E8%B5%96%E7%BC%96%E7%A8%8B.md

SHA-256：d9f9e0573b244aa71337753d6410c92ffa9548e4f1835fe37dcc2a89b3fa8b91；字节数：995；全文及哈希已核对。

## 建议增量与合并方式

### 最小实现决策阶梯

定义：理解真实需求和调用链后，按“无需实现→现有代码→标准库→平台原生→已安装依赖→短小实现→最低必要代码”顺序选择最早足够的方案。领域：软件工程与编程智能体。关联：[[零依赖编程]]、[[AgentSkills技能包]]。这是对Ponytail方法的中文归纳，先做本机同义查重，再决定独立成篇还是补充现有条目。

### 保留边界的简化验证

定义：通过共同契约、同组输入和已知失败对照，检查简化前后仍保留必要功能和安全边界。领域：软件工程测试。关联：[[证据优先质检ProofOverClaims]]、[[事实与判断分离]]。优先作为旧概念的新案例；不能把“通过有限测试”升级为“完整安全”。

### 基准口径与适用范围

定义：模型、基线、任务集、样本数、指标和检查范围共同限定一个数字能表达什么。领域：实验方法。关联：[[事实与判断分离]]、[[证据优先质检ProofOverClaims]]。不需要为了新项目另建同义概念。

## 真实主实验结果

采用上游benchmarks/agentic/tasks.py中的sql-user任务，自写minimal.py和layered.py；两者都是参数化SQL。上游任务片段仅静态读取，MIT许可已随ZIP保留。契约在上游基础上明确类型、长度、NUL、稳定tuple输出和连接所有权。

2026-10-05T04:10:39Z至04:10:40Z实际执行六步，Python 3.12.14、SQLite 3.53.1。21项共享检查/版，共42项通过；1个故意不安全的字符串拼接负对照被识别。最小版10行、0类、1函数；分层版38行、5类、7函数。行数为非空非注释物理行（包括docstring），不是上游git diff口径。详细命令与实际输出见04-experiment-log.txt，代码与来源证据见03-exercises.zip。

最小版SHA-256：14c855a78592604641743f64965b4a0670fcab35c1a1f13f259ada05094ef8fa。
分层版SHA-256：3f9ea44c8bab2665e61c8cde11bb8f996dd024492a71db2340cede1e3b0176f2。

这是特定工程样例的概念验证，不是Haiku 4.5基准复现。没有API调用、模型token/费用/延迟测量、完整授权系统、生产数据库或全面安全测试。参数化让载荷成为数据，不会禁止所有看起来可疑但合法的用户名。

## 上游基准的阅读边界

2026-06-18历史报告：Haiku 4.5，12项真实仓库功能任务，每任务每组4次；LOC为git diff新增行（含注释）。作者报告Ponytail相对基线LOC约-54%、tokens -22%、费用-20%、时间-27%。旧单轮80–94%不属于同一口径。功能任务未启动服务或浏览器，当前评分器的correct主要据非零新增行判断，不能据此认定同功能已证明。

历史外科式任务共6项，其中安全率按5项安全任务×4次计算：Ponytail 20/20，YAGNI-oneliner 19/20。当前harness列7项是后续版本；“100% safe”只描述这组有限检查。还有单模型、n=4和4/192功能单元费用/时间缺失等限制。作者“唯一所有指标均降”的文案与YAGNI行也全下降的表格不一致，故本笔记只复述具体数值及有限安全分母。

## 来源与方法

- 项目定位与命令：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/README.md
- 七阶方法与边界：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/skills/ponytail/SKILL.md
- 紧凑规则载体：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/AGENTS.md
- 会话启动 hook：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/hooks/ponytail-activate.js
- 指令生成与模式过滤：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/hooks/ponytail-instructions.js
- 历史 agentic 结果：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/benchmarks/results/2026-06-18-agentic.md
- 真实 sql-user 任务：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/benchmarks/agentic/tasks.py
- 评分口径实现：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/benchmarks/agentic/run.py
- 当前 harness 说明：https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/benchmarks/agentic/README.md

原学习方法已实际读取：Smashwinny/reminder_knowlege@1043e9d6080bff7af9724162e2c44559fab63e40 的 .claude/skills/learn-project/SKILL.md；本轮云端说明固定在1f61909da967cea8bc68dbfaffc642a4331b3352的reminder-dot/cloud-reference/RUNNING_IN_DOT.md。本轮按明确授权直接用ReportLab生成A4 PDF，逐页渲染查看；HTML未做浏览器视觉验收，不声称它与PDF逐像素一致。

## 待本机回迁核对

先在最新知识库查重合并，再建立项目笔记与概念互链并更新索引。本轮仅为入库提案，没有修改Windows vault、提交或推送Git，也没有代用户点击任务完成。
