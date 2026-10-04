# 最新运行方式（2026-10-04）

用户现已明确授权自动完整学习。网站限定账户/列表：自动初步分类 → 已核实学习项目自动 learn-project → 真实实验、PDF、知识笔记及独立审核 → 智能体保存分析标签 → 用户自己点任务完成。下述旧流程中的“手动选择后学习”和“publish自动标完成”属于历史机制，本轮不再采用；历史数据、未决发布恢复接口保留。

默认运行在本人 Dot 云端。报告与产物先留网站私有存储；电脑上线后本机固定脚本校验复制，唯一协调者续做现有 learn-project 第 8 步知识查重、合并 vault 和第 9 步 Git 提交/推送。用户确认沿用公开 `Smashwinny/reminder_knowlege`，只提交学习成果；私密原记录及分类报告仅保存在网站和本机。Dot 不接收本机凭据，不获取整台电脑权限。

`reminder_workflow_policy.json` 已声明默认 Dot、local/git 两个备份目标及 learning_artifacts_only 的 Git 范围。每次本机备份生成私有 `handoff.json`，分别记录网站保存、本机校验、知识合并、Git 同步。尚未完成第 8/9 步的完整报告保持 pending_coordinator；初步分类报告不进入公开 Git。交接账本不是第二套任务队列，不代表自动启动了本机智能体。协调者应核对当前网站范围和来源、原队列 owner 后继续，按明确文件清单提交，通过 hooks，推送回读成功才写 pushed 及提交 SHA。共享工作区不自动 rebase，按用户要求后续单独处理。

本机私有 `.pipeline`、`完成/分析报告/`、`完成/记录/` 和 `完成/流水线纲要.md` 已加入 Git 忽略规则。这不替代协调者对指南、练习和 vault 的内容检查；公开学习成果不能夹带私密原记录。已有历史提交不在本次改写范围内。

新接口和Dot指令见 reminder-dot/README.md。Dot需新 learning.write 授权，不自动扩大旧分类OAuth。未部署、未连接Dot、未保存新日程，旧本机heartbeat仍暂停。

2026-10-05：Ubuntu 修复候选 `97ef3ccfb83b625f684d81eb86a781837f928d1b` 已通过 Windows 独立代码复核：20 项联合检查通过；服务端 full 锁覆盖同账户不同列表/授权，过期锁不抢占；`reminder_list_knowledge_notes` 只读分页、UTF-8 重组/校验和当前范围排除通过。两个列表的 4 份合成报告及 12 个文件实际 Python 回迁通过，重复恢复新增 0 份。代码审阅通过不等于生产部署批准或真实 Dot 学习验收；这些后续步骤仍未执行。当前用户登录备份触发器已经注册并安全试运行；目标账户/列表未配置，真实云端拉取及协调者自动接续仍未验收。本机触发只复制产物，不运行周期分类、学习或 Git。

本地智能体必须先经原 reminder_pipeline claim/start/ready/review，完整标签由唯一协调者交付。网站标签工具示例（实际UUID/owner/lease/report和已审核analysis.json替换占位值）：

```powershell
python tools/reminder_dot_agent.py list-learning --account-id ACCOUNT --list-id LIST
python tools/reminder_dot_agent.py claim --account-id ACCOUNT --list-id LIST --task TASK --owner OWNER --stage full --report-id REPORT
python tools/reminder_dot_agent.py save --account-id ACCOUNT --list-id LIST --task TASK --owner OWNER --lease-id LEASE --stage full --analysis PROJECT/analysis.json --coordinator COORDINATOR
python tools/reminder_dot_agent.py release --account-id ACCOUNT --list-id LIST --task TASK --owner OWNER --lease-id LEASE
```

save full 重查审核指纹并读取实际文件，不能只交路径。不调用旧 publish/done/viewed、不改 task.state、不将标签当作用户已完成。云端知识笔记回迁后仍由协调者合并本机vault，再默认同步学习成果到 Git；原始备份保留私有，完整产物逐项校验。非链接类无HTTP证据时只备份，不造假进入旧分类接口。受阻单独记录，不反复启动同源失败学习。旧owner和旧进行中保护仍有效。

---

以下保留原队列及历史恢复说明；新自动学习/标签规则以上文为准。

# 拾遗学习协作流程

每条网站记录先进入本地台账，保留完整原文和网站摘要，并生成初步分析报告。自动阶段只读来源、分类和排队；用户说“开始学习某条/某主题”后才执行 learn-project 完整学习。

## 用户如何使用

- 查看 `完成/流水线纲要.md`：实时网站状态、分类结果、待选择的学习项目及报告入口。
- 查看 `完成/分析报告/<task_id>.md`：原记录、核对来源、分类理由、与已有知识的关联及推荐下一步。刚捕获的记录明确写“待分析”，不冒充已分析。
- 查看 `完成/00-纲要.md`：原有 87 条学习成果，已按完成时间整理。新学习的机器记录进入 `完成/记录/` 并由流水线生成 `完成/流水线纲要.md`。
- 在当前聊天指定记录或主题即可开始学习。若原帖证据缺失，可先提供实际目标链接，再选学习。

## 分类口径

| 类型 | 判据 | 后续 |
|---|---|---|
| 学习 | 有可核对的知识、原理、项目或可复现实践；不限制技术领域 | 排队等待用户选择 |
| 非学习 | 内容已核实，但没有本次学习任务所需的实质主题 | 记录理由；协调者可标网站进行中 |
| 重复增补 | 与已完成内容重叠 | 关联已有指南，列出值得补充的差异；不自动算完成 |
| 证据不足 | 原文、真实出链或项目身份未确认 | 保留待核实；不得当成非学习跳过 |
| 环境受阻 | 学习目标已明确，但执行条件缺失 | 记录障碍和可以验证的范围；不标完成 |

网站的“进行中”不等于被 agent 领取：旧流程也用它表示非学习记录已经查看。真正的领取以本机数据库为准。网站摘要只是线索，关键词匹配、搜索命中和读不到原文都不能替代来源核对。

## Codex 和 Claude 分工

每个 worker 先使用共享队列领取，使用唯一 owner 名称，任务运行中续约。仅修改该任务的报告、项目目录、实验材料和知识入库提案。完整学习开始前绑定项目，避免不同记录同时改同一个项目。

一个批次只有一个协调者；使用 `tools/reminder_coordinator.py acquire --owner <协调者名称>` 领取全局写入权。协调者统一验收、合并 vault、更新共享索引及同步网站，最后 release。过期领取不会被自动抢走，需原负责人释放或确认已停止后明确接管。

worker 不修改共享 vault/纲要/历史队列，不操作 Git，不使用旧 shiyi_sync 的 done/viewed。这样即使之后重新使用 Claude，也会遵循同一入口。已有旧进行中项单独保护，用户本次确认旧 Claude 已停止；自动分类不据此抢占以后新建的任务。

## 学习完成门槛

学习者按 `.claude/skills/learn-project/SKILL.md` 生成疑问清单、图文解答、能力清单、真实执行的实验和鲜艳的 PDF/HTML，保留输出证据。知识先查重，以提案交给协调者合并，更新项目笔记及知识库总览。

产物 manifest 记录项目、PDF、HTML、实验目录、实际输出日志、项目笔记和来源。队列先检查路径和文件，协调者还要查看 PDF 页面、核对实测输出和来源；文件存在不代表学习质量已通过。审核人与学习者不同，审核通过后才能发布。

发布前重新读取网站原记录；内容已变化或任务已删除就停止，避免将旧报告算作新内容完成。上传后回读确认，成功才记录上海时区的完成时间。超时或失败保留待同步，不显示“已完成”。再次发布不产生第二条完成记录。

Git 同步单独记录是否提交/推送成功，不与“网站已确认完成”混淆。协调者先查看暂存区，只提交本批次明确文件；禁止 git add -A。已有其他人的暂存文件时先查明归属。原本未提交的工作日志不包含在本次流程改动里。

## 自动检查的范围

原本机任务每 15 分钟检查网站，每次最多分析 5 条；只生成初步分析与分类结果，释放领取让用户选择。2026-10-04 用户要求改为本人 Dot 云端执行后，原本机 heartbeat automation-2 已暂停。Dot 网站接入已在独立源码副本准备并测试，真实网站部署、本人 OAuth 授权和 Dot 日程尚未完成，当前不能声称云端已在定时分类。

无论在哪运行，自动分类不执行完整学习、网站状态发布或 Git 提交。来源无法访问时保留证据不足，不循环重试同一条而阻塞后续记录。没有新增或可行动变化时保持安静。

原轮询需要电脑开机、Codex 应用运行及本机凭据有效。新的 Dot 接入采用网站服务端的限定账户/分析列表、OAuth、分类领取和报告存储；本机原 SQLite 只用于回迁后的共享学习队列，不能复制成多台设备各自调度的锁。默认只备份云端报告，明确使用 --import-queue 才经原 claim/classify/release 接口导入，不抢已有 owner 或旧保护记录。旧本机自动分类不得与 Dot 同时调度。

完整说明见 `reminder-dot/README.md` 和 `reminder-dot/repo/docs/DOT_INTEGRATION.md`。网站源码来自 Smashwinny/reminder 的独立副本 `reminder-dot/repo`，不是把当前知识仓库部署成网站。第一版计划在 Dot 中保存云端 15 分钟任务；即时事件触发尚未实现。接入验收后，电脑关机时由 Dot 云端继续工作；回迁用固定本机脚本拉取，不给 Dot 个人电脑权限。`tools/reminder_dot_on_login.ps1` 的登录备份触发器已注册并安全试运行，但目标账户/列表、真实云端拉取和协调者自动接续尚未验收。个人电脑连接是可选的额外扩大授权方式，当前没有连接。

## 当前迁移情况

2026-10-04 接入时，网站 495 条：未开始 39、进行中 322、完成 134。旧人工队列保留 436 条：已完成 89、非学习 89、进行中待核查 8、待处理 250。旧纲要的 87 份 PDF 全部存在，编号与时间顺序已修复；不会把网站的 134 条完成直接宣称为 134 次合格学习。

原文件备份保存在 `完成/.pipeline/history/`；本地运行库与原始快照已从 Git 排除。源记录、独立分析、学习产物和完成记录均保留在仓库内，便于查看和恢复。共享领取锁仅保护共同使用这个本地目录的 agent，不能保护多个 Git 克隆目录或多台设备。

## 操作者命令

用户可直接在聊天指定项目；以下命令供协调者和 worker 使用。TASK_ID、OWNER、PROJECT、COORDINATOR 为实际领取信息。

```powershell
python tools/reminder_pipeline.py sync
python tools/reminder_pipeline.py status
python tools/reminder_pipeline.py claim --owner OWNER --task TASK_ID
python tools/reminder_pipeline.py classify --task TASK_ID --owner OWNER --kind learning --reason "核实后的分析与理由" --evidence "https://官方来源"
python tools/reminder_pipeline.py release --task TASK_ID --owner OWNER
```

用户选定后，开始完整学习：

```powershell
python tools/reminder_pipeline.py start --task TASK_ID --owner OWNER --project PROJECT
python tools/reminder_pipeline.py renew --task TASK_ID --owner OWNER
```

产物交付后，协调者完成知识合并和独立审核：

```powershell
python tools/reminder_coordinator.py acquire --owner COORDINATOR
python tools/reminder_pipeline.py ready --task TASK_ID --owner OWNER --manifest PROJECT/manifest.json
python tools/reminder_pipeline.py review --task TASK_ID --owner OWNER --reviewer COORDINATOR --notes "实际核对结果及限制"
python tools/reminder_pipeline.py publish --task TASK_ID --owner OWNER --coordinator COORDINATOR
python tools/reminder_pipeline.py render
python tools/reminder_coordinator.py release --owner COORDINATOR
```

manifest 示例（所有路径均为仓库内真实产物；不复制占位路径通过验收）：

```json
{
  "topic": "项目学习主题",
  "project_dir": "project_name",
  "pdf": "project_name/项目小白指南.pdf",
  "html": "project_name/guide.html",
  "exercise_dir": "project_name/exercise",
  "experiment_log": "project_name/exercise/experiment_output.txt",
  "vault_note": "vault/项目笔记/project_name.md",
  "source_urls": ["https://官方来源"],
  "report_path": "完成/分析报告/TASK_ID.md"
}
```

`adopt --ack-stopped` 仅用于明确接管已确认停止的旧任务。`publish` 失败不得 release 或声称已完成，先保留发布意图再重试确认。以上队列工具不自行执行模型学习或 Git；定时任务由 Codex 读取来源完成分类。

## 不确定发布的恢复

发布前后的意图在独立 journal 中原子保存；进程退出后也保留。若上传结果未知且原文、状态或产物已发生冲突，正常发布与释放会停止，避免把旧结果套到新记录。协调者先查看当前任务与网站状态，再明确执行：

```powershell
python tools/reminder_pipeline.py reconcile --task TASK_ID --owner ORIGINAL_OWNER --coordinator COORDINATOR --ack-conflict --reason "核实的冲突、当前网站状态和取消旧发布的理由"
```

reconcile 只读网站、归档旧意图、保存审计理由并释放原任务锁，保留待核查；不会撤销网站状态或称学习已完成。此操作不能由自动分类定时任务执行。

manifest 可选 `experiment_files`，用仓库相对路径列出真正的实验材料。未指定时自动忽略 node_modules、虚拟环境、Git目录和构建缓存；依赖文件不算自己的实验成果。

## 已授权接管的旧待处理记录

用户已确认旧 Claude 停止并由 Codex 接手。`完成/旧待处理接管清单.json` 冻结了当时 250 条“待处理”的 ID，只授权初步分析和分类。自动任务优先新记录，也可对清单中的尚未分类、无 owner、未完成且不重复的记录用 adopt --ack-stopped 领取；每次必须核对历史队列仍为待处理。8 条旧进行中及旧已完成、非学习条目不在此授权范围内，继续待核查。

旧记录网站可能已经是“进行中”，分类后仍保留网站保护，用户选定完整学习时由协调者明确接管后 start。这与新记录直接从 learning_queued 开始的路径不同，但均不会自动执行学习或标完成。
