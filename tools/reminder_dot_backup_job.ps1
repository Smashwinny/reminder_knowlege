# One-shot private backup and read-only cloud Git receipt verification; no model or push.
[CmdletBinding()]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot '../完成/.pipeline/dot-backup-config.json'),
    [string]$PythonPath = 'python'
)
$ErrorActionPreference = 'Stop'
$reminderRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$privateStatusDir = Join-Path $reminderRoot '完成/.pipeline'
[IO.Directory]::CreateDirectory($privateStatusDir) | Out-Null
$statusPath = Join-Path $privateStatusDir 'dot-backup-job-status.json'

function Write-BackupStatus([string]$Status, [string]$Reason, [string]$ExceptionType = '') {
    $state = [ordered]@{
        schema = 'reminder-dot-backup-job-v1'
        checkedAt = [DateTimeOffset]::UtcNow.ToString('o')
        status = $Status
        reason = $Reason
        exceptionType = $ExceptionType
        cloudDeleted = $false
        modelStarted = $false
        knowledgeMerged = $false
        gitRun = $false
        gitPublicationRun = $false
        cloudReadback = $true
    }
    [IO.File]::WriteAllText($statusPath, ($state | ConvertTo-Json) + "`n", [Text.UTF8Encoding]::new($false))
}

if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
    Write-BackupStatus 'pending_configuration' 'Allowed account/list not configured; no website access.'
    return
}
try {
    # Keep command output private. Only stage status is recorded, never token/config contents.
    $null = & (Join-Path $PSScriptRoot 'reminder_manual_sync.ps1') -ConfigPath $ConfigPath -PythonPath $PythonPath
    if ($LASTEXITCODE -ne 0) { throw 'Cloud readback or private backup failed.' }
    Write-BackupStatus 'local_backup_verified' 'Private originals verified; reviewed cloud Git receipts checked. Inspect manual-sync-status.json for pending work and conflicts.'
}
catch {
    Write-BackupStatus 'failed' 'Backup incomplete; cloud and existing local copies retained. Run the local backup script privately for details.' $_.Exception.GetType().Name
    exit 1
}
