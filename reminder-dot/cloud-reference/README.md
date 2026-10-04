# Dot 云端学习参考包

本包用于让 Dot 在本机离线时按已有学习方法工作，并参考**已经公开发布**的知识笔记。
这是可读取的作业资料，不表示已在真实 Dot 环境安装 skill、连接插件或完成能力验收。

先读 [云端执行说明](RUNNING_IN_DOT.md)，再读 [知识索引](knowledge-index.md)。
完整索引及原 learn-project 方法的固定版本链接、SHA256 见 [knowledge-index.json](knowledge-index.json)。
原 skill 已发布在知识仓库，按索引的 `skill.url` 读取；不复制用户级 skill，也不修改本机两份 skill。

索引只列原已发布提交中的概念/项目笔记链接与校验值，没有复制完整 vault，
没有本机未提交笔记、原任务/分类报告、`.obsidian` 配置、令牌或运行队列。
读取旧笔记时声明固定来源版本，不能当作最新本机知识视图。

索引由 `tools/reminder_dot_reference.py` 生成。更新前在线确认公开知识仓库 main 的实际 SHA，
安全 fetch 后，用该 SHA 运行生成器；生成器只读相同的 origin/main Git 对象，不读取工作树笔记。
输出再由唯一协调者审核、按明确文件清单提交。缓存索引不可冒充新的在线核验结果。

网站、Dot 授权/日程、实际云端学习和本机上线备份分别验收。
Windows 最终目录仍为原知识仓库；Ubuntu 仅负责网站服务，不能代替本机完成 vault 合并。
