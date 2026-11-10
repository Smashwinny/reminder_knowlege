# 合入候选：dsh-plugins-57（不自行合入）

查重：公开main `a8674777e18302b8804b137212b1396cbfe5a747`。已复用总览、vault/项目笔记/archify.md、dsh_plugin_upgrade_skill.md、概念/源码取证图.md与archify彩色HTML风格；未重跑archify，更不把其旧实验当本次实测。

建议候选路径 vault/项目笔记/dsh_plugins_57_conflicts.md。与item-4共用同一长文引用，协调者可合并来源段，但保留本项数据表与实验增量，避免重复推荐全文。

新增证据：57项对应52根，51公共200/1次404；2组同名不同作者；完整包名比展示名/row id更适合作键。当前dsh-web-all有23直接依赖，重叠任务看板与SSH；现有mountOnce能在受测条件下跨模块副本去重、排队交接，不能写成“合集重复必崩”。

增补既有概念：
- 接缝与桩实现StubSeam：真实mountOnce + 假effect/dispose，不是完整宿主。
- 先量后优化性能法：manifest字节/依赖扇出/热解析与冷启动分层。
- 开源验货三查：API许可字段、包声明和LICENSE正文可能不同；MIT附条与非商业许可分别记录。
- 源码取证图：复用archify，关系按固定SHA文件/行号追溯。

25条自写检查通过；没有上游全量测试或独立审核通过。推荐只作条件候选：上下文billion-context、侧栏better-sidebar、看板task-board，SSH按需；先匹配宿主版本再单项验证。下载量全部作者说法。没有Git发布、vault合入、提醒/看板计划/用户任务勾选。
