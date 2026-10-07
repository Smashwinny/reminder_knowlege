# 本机工具补齐

本目录是显式文件白名单，不是整个仓库备份。当前公开知识 main 不含最新 Dot / pipeline 全套工具，所以不能仅 clone 就执行新回迁命令。包内集成工具来自当前工作区快照，基准提交 8536dae；登录示例为本手册新增，tools/reminder_workflow.md 为无历史任务数据的教学摘要；SHA256 见包根 `package_manifest.json`。

## 新干净 clone 才用复制示例

在 Windows PowerShell 7 中先检查自己的新 clone；若已有 agent、用户改动、运行队列或暂存文件，不执行整包复制，交唯一协调者逐文件 diff 和合并。此段只安装列举的方法与工具，不启用学习日程。

```powershell
$reminderPack = 'C:\YOUR_UNPACK_PATH\本机工具补齐'
$reminderTarget = 'F:\reminder'
git -C $reminderTarget status --short
# 确认是新、无本机运行状态的干净 clone 后继续
$reminderFiles = Get-Content -LiteralPath "$reminderPack/install-files.json" -Raw | ConvertFrom-Json
foreach ($reminderFile in $reminderFiles) {
  $reminderFrom = Join-Path $reminderPack $reminderFile
  $reminderTo = Join-Path $reminderTarget $reminderFile
  New-Item -ItemType Directory -Force (Split-Path -Parent $reminderTo) | Out-Null
  Copy-Item -LiteralPath $reminderFrom -Destination $reminderTo
}
Set-Location $reminderTarget
```

包内 `install-files.json` 全是相对固定白名单路径；先打开检查后运行。`-Force` 只创建目录，没有递归删除或移动。已有工作区即使 git status 干净，也可能存在未跟踪运行状态，仍不能整包覆盖。

## 排除本机私密运行文件

新 clone 检查 `.gitignore` 和 `.git/info/exclude`，缺失项才追加：

```powershell
@'
/tools/.shiyi_token
/完成/.pipeline/
/完成/记录/
/完成/分析报告/
/完成/流水线纲要.md
/vault/复习/
/reminder-dot/repo/
/output/
'@ | Add-Content -LiteralPath .git/info/exclude
git check-ignore tools/.shiyi_token 完成/.pipeline/dot-backup-config.json
```

ignore 对已跟踪历史文件无效；不能据此把整个工作区 add。旧缓存不作为实时网站真值。公开成果发布按独立发布副本、明确文件名执行。

## 先看帮助，再做正式配置

```powershell
python tools/reminder_pipeline.py --help
python tools/reminder_dot_backup.py --help
python tools/reminder_dot_agent.py --help
python tools/reminder_coordinator.py --help
python tools/private_login_example.py --help
python -m unittest tools.test_reminder_pipeline tools.test_reminder_coordinator tools.test_reminder_dot_backup tools.test_reminder_dot_agent
```

帮助与这些离线测试使用 Python 标准库；生产凭据只走环境变量或私有 `.shiyi_token`。本包登录示例仅用于新实例的私密交互，未替读者执行正式登录。测试通过仍需真实网站身份、授权、回读与完整交付联调。

当前 `reminder_dot_http.SITE`、`shiyi_sync.BASE` 固定本人服务域名；自建实例先按包根 `逐终端补充命令.md` 两处都修改。备份触发默认 F:\reminder，换路径须检查脚本参数和任务回读。

## 规则优先级

当前 AGENTS 明确：Dot 云端学习、本机唯一协调者合并知识和 Git；自动分类与完整学习已获用户范围授权；任务完成由本人点。原 skill、CLI help 和长工作流的历史段落可能仍保留“手动选择开始”等旧文本，以当前授权和 AGENTS 为准。worker 不改共享 vault、网站完成状态或 Git；不得运行旧 shiyi_sync done/viewed 或旧 publish 勾选任务。

包内技能方法保留可追溯原件，不把历史“全仓 add / 自动 rebase”建议应用到当前共享工作区。正式源码维护应在负责人的私有流程完成，不能借这个工具包发布整个本机仓库历史。
