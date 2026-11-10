# 合入候选（仅建议，不执行）

查重快照：Smashwinny/reminder_knowlege main `a8674777e18302b8804b137212b1396cbfe5a747`。总览/树中未见 pi-purge 专项；不据此声称所有400+目录内容已全文查重。

已实读复用：vault/概念/接缝与桩实现StubSeam.md、提示词权威边界.md、沙箱与审批正交.md，vault/项目笔记/agent-kernel.md 与该项目 HTML 的彩色问答卡/大号重点/内联SVG/实验步骤风格。额外复用 box 的 /workspace/pi-audit/pi-architecture-audit.md，只用于历史 Pi 背景，当前源码另读 `b30d54b8aebe6408e02d1473446d25f8083da68f`。

建议新增 vault/项目笔记/pi-purge.md：
- 记录0.2.1固定历史与0.2.4当前的区别，不收录历史对抗人设或“一键破甲”安装指南。
- 三模式是字符串变换，append 实为前置；replace 是两个独立精确锚点删除，当前Pi文案变化会退化。
- enabled会复位，mode/source不复位；模块顶层状态不是天然会话对象；status可陈旧；reload文档与实现不符。
- 兼容范围声明≠兼容验证；0.84.2锚点匹配，当前1.5.2只验证组合/退化路径，CLI/RAE待验。

仅增补既有概念（不造同义新词、不改累计计数）：
1. 提示词权威边界：字符串重写权限与真正授权/工具权限分层。
2. 接缝与桩实现StubSeam：真实扩展+真实构造函数+路径/skills桩的混合实验；不是端到端。
3. 沙箱与审批正交：strict去掉规则文字不撤销工具权限，强边界仍在OS/调用代码。
4. 证据优先质检ProofOverClaims：README、peer范围、单元PASS、当前兼容、模型效果分层。

实测凭据：experiment-log.md；26条自写检查、上游9组+环境源各自独立记录；PASS包含已观察缺陷，非独立审核、非生产安全证明。不合入vault、不发Git、不勾任务、不建队列。
