# Manual private backup plus reviewed, explicit-file Git publication.
[CmdletBinding()]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot '../完成/.pipeline/dot-backup-config.json'),
    [string]$PythonPath = '',
    [switch]$LocalOnly,
    [switch]$StatusOnly
)
$ErrorActionPreference = 'Stop'
$reminderRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if (-not $PythonPath) {
    $runtime = Get-Command python -ErrorAction SilentlyContinue
    if ($runtime) { $PythonPath = $runtime.Source }
    else {
        $PythonPath = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
        if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
            throw 'Python is unavailable; supply -PythonPath with an installed Python 3.10+ runtime.'
        }
    }
}
$null = & $PythonPath -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'Python 3.10 or newer is required.' }
$syncArguments = @('-X', 'utf8', (Join-Path $PSScriptRoot 'reminder_manual_sync.py'), '--root', $reminderRoot, '--config', $ConfigPath)
if ($StatusOnly) { $syncArguments += 'status' }
else {
    $syncArguments += 'sync'
    if ($LocalOnly) { $syncArguments += '--local-only' }
}
& $PythonPath @syncArguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
