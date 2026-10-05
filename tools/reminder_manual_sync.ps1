# Manual private backup plus reviewed, explicit-file Git publication.
[CmdletBinding()]
param(
    [string]$ConfigPath = '',
    [string]$PythonPath = '',
    [switch]$LocalOnly,
    [switch]$LegacyLocalPublisher,
    [switch]$StatusOnly
)
$ErrorActionPreference = 'Stop'
$manualToolFolder = $PSScriptRoot
if (-not $manualToolFolder) { $manualToolFolder = [IO.Path]::GetDirectoryName($MyInvocation.MyCommand.Path) }
$reminderRoot = (Resolve-Path -LiteralPath (Join-Path $manualToolFolder '..')).Path
if (-not $ConfigPath) { $ConfigPath = Join-Path $reminderRoot '完成/.pipeline/dot-backup-config.json' }
if (-not $PythonPath) {
    $bundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    if (Test-Path -LiteralPath $bundledPython -PathType Leaf) { $PythonPath = $bundledPython }
    else {
        $runtime = Get-Command python -ErrorAction SilentlyContinue
        if ($runtime) { $PythonPath = $runtime.Source }
        else {
            throw 'Python is unavailable; supply -PythonPath with an installed Python 3.10+ runtime.'
        }
    }
}
$null = & $PythonPath -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'Python 3.10 or newer is required.' }
$syncArguments = @('-X', 'utf8', (Join-Path $manualToolFolder 'reminder_manual_sync.py'), '--root', $reminderRoot, '--config', $ConfigPath)
if ($StatusOnly) { $syncArguments += 'status' }
else {
    $syncArguments += 'sync'
    if ($LocalOnly) { $syncArguments += '--local-only' }
    if ($LegacyLocalPublisher) { $syncArguments += '--legacy-local-publisher' }
    else { $syncArguments += '--cloud-only' }
}
& $PythonPath @syncArguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
