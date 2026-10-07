# User-authorized logon backup only; no periodic classification or computer access grant.
[CmdletBinding(SupportsShouldProcess = $true)]
param()
$ErrorActionPreference = 'Stop'
$reminderRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$taskName = 'Reminder-Dot-Backup-OnLogon'
$description = 'Reminder guarded local backup on logon; no learning, model, vault merge or Git.'
$jobPath = Join-Path $PSScriptRoot 'reminder_dot_backup_job.ps1'
$powerShellRuntime = (Get-Command pwsh -ErrorAction Stop).Source
$pythonRuntime = (Get-Command python -ErrorAction Stop).Source
$taskUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$arguments = '-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -File "{0}" -PythonPath "{1}"' -f $jobPath, $pythonRuntime
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing -and ($existing.Description -ne $description -or
    @($existing.Actions).Count -ne 1 -or $existing.Actions[0].Execute -ne $powerShellRuntime -or
    $existing.Actions[0].Arguments -ne $arguments)) {
    throw 'Existing task does not match this backup entry point; no overwrite.'
}
if ($PSCmdlet.ShouldProcess($taskName, 'Register the fixed guarded backup script for this user logon')) {
    $action = New-ScheduledTaskAction -Execute $powerShellRuntime -Argument $arguments -WorkingDirectory $reminderRoot
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User $taskUser
    $principal = New-ScheduledTaskPrincipal -UserId $taskUser -LogonType Interactive -RunLevel Limited
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable `
        -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 15)
    Register-ScheduledTask -TaskName $taskName -Description $description -Action $action `
        -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
    $saved = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
    if (@($saved.Actions).Count -ne 1 -or $saved.Actions[0].Arguments -ne $arguments) {
        throw 'Registered task readback does not match the fixed entry point.'
    }
    [ordered]@{ taskName = $saved.TaskName; state = [string]$saved.State;
        trigger = 'user_logon'; modelStarted = $false; credentialsInArguments = $false;
        configured = (Test-Path -LiteralPath (Join-Path $reminderRoot '完成/.pipeline/dot-backup-config.json'))
    } | ConvertTo-Json
}
