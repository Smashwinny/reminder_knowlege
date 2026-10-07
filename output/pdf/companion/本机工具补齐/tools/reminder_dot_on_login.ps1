# One-shot transfer and handoff to learn-project steps 8/9.
# Dot is not given access to this computer or its token; this script does not run an agent.
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot '../完成/.pipeline/dot-backup-config.json'),
    [string]$PythonPath = 'python'
)

$ErrorActionPreference = 'Stop'
$reminderRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
    Write-Output '尚未设置本机 Dot 报告备份的账户与列表；未访问网站，未启动学习或 Git。'
    return
}
$backupSettings = Get-Content -LiteralPath $ConfigPath -Raw -Encoding utf8 | ConvertFrom-Json
$accountGuid = [guid]::Empty
$listGuid = [guid]::Empty
if (-not [guid]::TryParse([string]$backupSettings.accountId, [ref]$accountGuid) -or
    -not [guid]::TryParse([string]$backupSettings.listId, [ref]$listGuid) -or
    $accountGuid -eq [guid]::Empty -or $listGuid -eq [guid]::Empty) {
    throw '请设置真实且已经本人确认的账户 UUID 与分析列表 UUID；未读取任何网站记录。'
}
$backupTool = Join-Path $reminderRoot 'tools/reminder_dot_backup.py'
if ($PSCmdlet.ShouldProcess('本人已确认的拾遗分析列表', '校验备份产物，并记录协调者的知识入库与 Git 同步交接')) {
    & $PythonPath $backupTool backup --account-id $accountGuid.ToString() --list-id $listGuid.ToString() --root $reminderRoot
    if ($LASTEXITCODE -ne 0) {
        throw '本次报告备份没有完成；云端原件与原本机副本保留。'
    }
    Write-Output '本机副本已校验；知识入库与 Git 同步状态见 handoff.json，由唯一协调者继续 learn-project 第 8、9 步。私密原记录不提交公开仓库。'
}
