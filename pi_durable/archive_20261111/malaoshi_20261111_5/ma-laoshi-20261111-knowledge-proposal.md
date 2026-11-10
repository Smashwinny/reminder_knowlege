# 合入建议（仅候选，未改共享vault）

建议新增 vault/项目笔记/pi-durable.md；提议概念《持久化进度与可见性双层》《持久睡眠与宿主唤醒》《SQLite命名空间隔离》。

查重固定main a8674777e18302b8804b137212b1396cbfe5a747，已读总览与《Checkpoint存档与持久执行》《Compaction上下文压缩算法》。保留旧Checkpoint笔记里OpenMuse的外部效果边界，补Pi Durable checkpoint/阶段重入的实例；不把LangGraph、CLI压缩算法、Durable当同实现。

新增证据：prefix同时覆盖表/索引；baseline非所有system前移；100ms展示与1000ms落盘窗；onWake不是零费用承诺；1.4.0 SQLite迁移有回滚边界。

实证：同一SQLite文件alpha/beta两存储ID均为2但内容隔离且可重开；faux流0/400ms总提交批次27/9、文档批次25/7；6文件245测试通过。计数不是远端IO或作者性能。

0.84.2不适用为内置CLI能力；独立库实验不改本机。待验证：真实模型/Cloudflare/强杀/多进程争用。合入时保留四类来源标签和SHA b30d54b8aebe6408e02d1473446d25f8083da68f。
