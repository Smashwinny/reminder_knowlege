# One-shot local transfer. Dot is not given access to this computer or its token.
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot '../完成/.pipeline/dot-backup-config.json')
)

$ErrorActionPreference = 'Stop'
$reminderRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
    Write-Output '尚未设置本机 Dot 报告备份的账户与列表；未访问网站，未安装定时任务。'
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
if ($PSCmdlet.ShouldProcess('本人已确认的拾遗分析列表', '只读拉取报告并校验保存到本机私有备份目录')) {
    & python $backupTool backup --account-id $accountGuid.ToString() --list-id $listGuid.ToString() --root $reminderRoot
    if ($LASTEXITCODE -ne 0) {
        throw '本次报告备份没有完成；云端原件与原本机副本保留。'
    }
}
