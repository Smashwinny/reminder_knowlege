# Manus Studio 视频工作流知识入库提案（2026-11-22 审核修订）

> 关联任务：ab9eb890-494c-4eb5-b014-33e36147b454。原 worker 提案保留在 pending 文件，本文件记录协调者实际合并决定。

## 查重与合并结果

- 新建 [[分层时间轴人机接力]]：与 [[上下文接力]] 的规划文档搬运、[[人机协同Interrupt]] 的暂停恢复均不同。
- 向 [[人机协同Interrupt]] 追加 Manus 官方分层接力对照，明确 locked 是本地协议。
- 不新建“品牌上下文最小集”：四项仅为起步检查表，“最小”与“80% 偏差”无证据，不立项。
- 新建项目笔记 `vault/项目笔记/manus_studio_workflow.md`，MOC 加概念与项目索引。

## 审核修订

2026-11-22 官方 Video Editor 页面明确独立轨道、人工编辑和从修改继续，但未提 locked 字段或具体导出工作流。指南已把官方事实与本地 conservative protocol 分开。

原破坏测试只改 note 不覆盖人工 value，已修复为双路径：尊重锁定保留、删除保护覆盖。默认与自定义合成素材两命令全部断言 PASS。

审核版 PDF：`manus_studio_workflow/Manus-Studio视频工作流-小白指南-v2.pdf`，10 页全部逐页渲染检查；原 PDF 保留，不纳入 manifest。
