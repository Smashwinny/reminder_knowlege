# 拾遗任务 Worker 作业指南

Claude 和 Codex 使用同一份指南。先读根目录 `AGENTS.md`、`CLAUDE.md` 与 `tools/reminder_workflow.md`。本指南自 2026-10-04 起替代旧的多 worker 直接写网站、纲要与 Git 流程。

## 领取前

使用 `tools/reminder_pipeline.py sync` 获取网站真实状态。每个 worker 使用唯一 owner，以 claim 领取一条；过期租约不会被自动回收。旧网站进行中、旧队列进行中及已完成条目受保护，只有确认旧执行者停止后，协调者才可明确 adopt。开始写项目材料前锁定项目，不能与其他任务同时修改同一目录。

## 阶段一 内容分析

读取原链接并判断实质内容。网站摘要只是线索；优先查作者、官方项目文档与仓库。原文不可读时，候选项目只能写成候选，不能冒充原帖真实目标。学习不限制技术领域，能否免费实验也不能决定是否值得学习。

分类支持 learning / non_learning / duplicate / needs_review / blocked，分别为学习、非学习、重复增补、证据不足、环境受阻。每条记录至少保留具体分析理由和证据 URL，关联已完成项目与知识库。用 classify 写入独立报告，补全可确认事实、未确认事项和建议下一步，然后 release。

最新用户已确认：完整学习也自动执行；初步阶段不调用 start/ready/review，核实学习类再进入完整阶段。新流程仅保存分析标签，task.state 完成由用户点击；不调用旧 publish 或修改 Git。不能把来源不可访问、知识已掌握、闭源或缺少 API 当成非学习而跳过。

## 阶段二 已授权的自动完整学习

仅对当前来源已核实、获准列表中且没有其他执行者的 learning 任务执行 start，绑定一个项目目录。严格按 `.claude/skills/learn-project/SKILL.md` 学习：疑问清单 → 图文解答 → 能力清单 → 实际执行的实验 → 鲜艳彩色 PDF/HTML → 知识入库。

worker 只写自己任务的报告、工作日志和所属项目目录。实验材料放 exercise，真实命令与输出保留到 experiment_log，不能编造结果。上游代码放 repo，模型、依赖缓存和运行数据不提交。知识库先只读查重，将概念笔记/合并建议放项目内的知识入库提案；协调者统一合并 vault、更新总览。

进度保存到 `完成/工作日志/<task_id>.md`，记录来源判断、每步真实验证、产物及限制。租约不足时 renew，不让其他 agent 猜测任务是否还在运行。

## 交付与验收

向协调者提交 manifest，包含 topic、project_dir、pdf、html、exercise_dir、experiment_log、vault_note、source_urls，可选 report_path。协调者完成知识入库后，ready 检查文件及来源关联；独立 reviewer 必须查看 PDF 页面、核对实测证据与知识库合并，并用 review 记录具体意见。换一个名称不能代替实际独立检查。

最新标签流程不调用旧 publish。完整学习经 ready/review 后，持有全局协调者租约的人通过 reminder_dot_agent.py 保存真实产物及“已完成完整分析”标签；非学习与非链接类保存对应分类标签。task.state 不由智能体更改，完成由用户本人点击。标签保存后回读确认，只记录分析完成时间；用户点击完成并由网站回读确认后，才可记任务完成时间。当前标签工具不自动追加原完成纲要，未确认结果保留待同步。

旧 `shiyi_sync.py done/viewed` 已关闭。worker 不直接调用底层 upload_task，不修改 `完成/00-纲要.md`、历史队列或共享 vault，不进行 git add/commit/push。协调者按明确文件清单统一提交，禁止 git add -A、强推、绕过 hooks 和重置共享工作区。

## 返回协调者的信息

汇报 task_id、分类、3–5 句内容依据、证据 URL、已验证产物、尚未验证或受阻事项，以及当前领取是否释放。不要将“分类完成”“本地学习完成”“网站确认完成”和“Git 推送完成”混成同一状态。
