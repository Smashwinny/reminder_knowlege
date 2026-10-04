# 拾遗网站 → 本人 Dot → 本机与 Git

2026-10-04 最新用户授权：完整学习也自动执行，网站完成由用户点击。已在独立网站源码副本实现并进行本机验证；尚未部署到真实网站，也尚未连接本人 Dot。

2026-10-05 收信箱进展：Ubuntu 已修复并推送[移植候选 PR #3](https://github.com/Smashwinny/reminder/pull/3)，SHA `97ef3ccfb83b625f684d81eb86a781837f928d1b`。Windows 独立复测 20 项 Node 检查通过，并验证账户级 full 锁跨列表/授权、过期保护、UTF-8 知识分页/校验和当前范围排除。两个列表的 4 份合成报告及 12 个文件实际 Python 回迁通过，重复恢复新增 0 份。前轮两处修复请求均已通过复核；代码审阅通过，具体版本生产部署批准与真实 OAuth/云端学习仍待完成。详见[候选审阅记录](候选审阅.md)。

默认流程：本人选择网站账户与分析列表 → Dot 在云端读取获准原链接 → 自动分类及完整学习 → 实际产物与独立审核后打标签 → 电脑在线后校验复制报告及产物到本机 → 唯一协调者按 learn-project 第 8、9 步合并知识库、提交并推送 Git。用户自己点击任务完成，与这些阶段分别记录。

Git 沿用公开的 `Smashwinny/reminder_knowlege`，用户已确认只提交学习成果。私密原记录及分类报告只留网站与本机。电脑离线先保留云端原件，本机备份、vault 合并或 Git 推送未成功时保留各自的待同步状态。

旧本机 Codex 分类 heartbeat `automation-2` 已暂停，保持原队列和报告。当前只注册了 Windows 当前用户登录后的备份触发器 `Reminder-Dot-Backup-OnLogon`，它不运行分类、学习、模型或 Git。尚未创建 Dot 云端日程。

## 已准备的可审阅内容

- [网站权限、报告和领取接口](repo/sync-server/dot-integration.js)：服务端固定账户，OAuth 绑定一个本人维护的分析列表，读取原记录、保存报告/学习产物并派生任务标签；完成勾选由用户本人操作。
- [部署、私密性、连接与迁移说明](repo/docs/DOT_INTEGRATION.md)。
- [交给 Dot 的云端分类和回迁指令](repo/docs/DOT_TASK_PROMPT.md)：文本已准备，日程没有创建。
- [本机备份与原队列导入工具](../tools/reminder_dot_backup.py)：默认私有副本及 `handoff.json` 交接账本，不删除云端数据。完整产物的知识合并与 Git 收尾交给协调者继续现有 skill；可选分类导入使用既有领取接口。
- [本地智能体标签工具](../tools/reminder_dot_agent.py)：原队列领取、真实 ready/review 及协调者校验后交付完整标签。
- [本机登录备份入口](../tools/reminder_dot_backup_job.ps1)及[触发器安装脚本](../tools/install_reminder_dot_backup_trigger.ps1)：已注册并实际试运行，任务返回码为 0。由于账户与列表配置仍缺失，本次只记录待配置并退出，没有访问网站。配置确认后才调用[一次性备份脚本](../tools/reminder_dot_on_login.ps1)，拉取产物并记录知识入库/Git 待办；不启动本机模型分析、不向 Dot 授予电脑访问，也不冒充 vault 合并或 Git 推送已完成。
- [云端学习参考包](cloud-reference/README.md)：从已核实的公开知识仓库 main 提交 `1043e9d6080bff7af9724162e2c44559fab63e40` 生成固定版本索引，包含 298 条概念、96 份项目笔记及原 learn-project 方法链接。未包含本机未提交笔记、私密原记录或浏览器配置；不代表已经安装到 Dot 或实际完成云端学习。独立发布见[知识仓库草稿 PR #1](https://github.com/Smashwinny/reminder_knowlege/pull/1)。
- [界面预览](界面预览.png)：虚构账户与记录的本机测试页面。
- `website-dot.patch`：网站部署补丁，基线为 Smashwinny/reminder main 的 `282a64d1f0d25613aa0d31b6b144a2e34aaf8a4d`，应用前核对实际服务器代码和未提交改动。

## 尚未完成的连接

网站既有本机凭据已通过真实 `/api/auth/me` 只读确认有效；这不等于已经选定 Dot 可见列表或完成 OAuth 授权。当前 Windows 没有生产 SSH 密钥；原 Ubuntu Codex 已通过既有维护入口连接生产，完成只读检查、Linux 测试和生产整卷备份，见[服务器侧回信](https://github.com/Smashwinny/reminder/issues/1#issuecomment-5981435057)。它未部署本功能或修改线上任务。

继续接入需要：先把 Dot 功能移植到当前生产基线并验证；本人确认要开放的账户与列表（建议专用“Dot 待分析”列表）；核对实际个人插件使用的 OAuth 客户端登记方式、精确回调和本人登录同意。无需把任何密码、密钥或 token 发到聊天。

Dot 云端分析与本机回迁能力依据 [官方电脑连接说明](https://learn.chatgpt.com/docs/dots/computers-and-apps) 和 [定期任务说明](https://learn.chatgpt.com/docs/dots/tasks-and-memory)。将“仅指定列表”落实为服务端授权，是本实现的设计选择。唯一 Dot 实例身份没有得到官方认证资料的证明，当前边界是获本人同意的私有 OAuth 连接。

推荐保持严格范围：Dot 只连接网站；本机在线后由固定本地脚本拉取副本。不给 Dot 整台个人电脑的权限。将个人电脑连接给 Dot 是额外且更广的授权，不能再把“只读网站指定列表”视为它的全部能力。

## 本机验证

新增 Node 接口与 Python 迁移测试通过；浏览器验证三种标签、筛选、详情报告入口和用户点完成后标签保留。网站完整测试的一项原有 Unix 权限断言在 Windows 失败；未改原测试或削弱权限逻辑。浏览器以虚构账号核对正常登录、列表和中文报告展示；生产授权、云端日程和真实回迁仍待验收。

所有新增测试使用隔离数据；测试用合成产物不代表真实学习结果，生产记录未开始学习。本轮按用户要求提交网站源码和配套工具，Git同步记录见提交历史。

三种主要标签：已完成完整分析 / 初步判定非项目学习类 / 非链接类。

[任务标签预览](任务标签预览.png) 使用虚构测试数据，不是生产页面。

验证结果：12项Node相关验证、13项Python迁移与交付验证通过；原本地队列33项回归通过，共46项Python检查通过。交接账本区分私有原记录与公开学习成果，重复备份保留协调者已有同步记录，损坏账本不覆盖原件。前轮网站完整套件35/36通过，剩余为原有Windows上的Unix0600权限断言。模拟网站回迁4份报告及6份产物，再次回迁新增0份，云端原件保留。

网站源码提交：`be7e6fc`；默认 Dot → 本机/Git 规则追加提交：`243739d`；Ubuntu 交接说明提交：`aebba3e`。分支 `codex/automatic-analysis-tags` 已推送至网站仓库，并创建 [草稿 PR #2](https://github.com/Smashwinny/reminder/pull/2)，尚未合并或部署生产。知识仓库本机配套提交尚未推送，rebase 留待后续核对服务器与远端改动后进行。

2026-10-04 用户授权使用 [运维收信箱 issue #1](https://github.com/Smashwinny/reminder/issues/1) 协调另一台 Ubuntu 的 Codex。Ubuntu 已认领服务器侧，隔离 Linux 完整测试 36/36 通过，生产数据卷备份与 offsite 校验通过。它发现生产已有本分支缺少的图片同步、排序、上传保护和修复，不能直接部署 PR #2。现已[明确委托 Ubuntu 在独立分支移植](https://github.com/Smashwinny/reminder/issues/1#issuecomment-5981455951)，Windows 不再并行修改网站运行源码；只维护云端参考资料、本机回迁和知识仓库。候选版本、部署批准和真实 OAuth 验收仍待完成。

网站仓库现为私有，公开知识仓库只接收学习成果。知识参考包从公开 main 建立独立干净分支发布，不推送包含私有网站补丁的本机工作分支历史。详见 [Ubuntu 交接说明](repo/docs/DOT_UBUNTU_HANDOFF.md)。

本次在独立合成数据目录启动实际网站应用，绑定随机本机回环端口，完成 6 项集成验证：登录、OAuth/权限与列表隔离、报告领取/标签、HTTP server 重新创建后持久化回读、用户完成状态保留标签及限定范围导出。随后实际 Python 工具恢复合成导出：首次新增 1 份、重复新增 0 份，云端原件保留，未导入真实队列。运行使用 Node 而非 Docker，验证后临时 HTTP server 已关闭；没有改动生产或把合成报告当作真实学习。

本机登录触发已注册并完成安全试运行，账户/列表配置尚未填写；真实云端产物拉取尚未验收。生产移植/部署、Dot OAuth/日程、真实云端学习及本机协调者自动接续仍未接通，各阶段分别保留待办。最终学习目录继续使用 `F:\reminder`。
