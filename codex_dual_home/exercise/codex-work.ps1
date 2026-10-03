# codex-work.ps1 — 一键进入二号 Codex 实例（独立 HOME，独立登录/配置/历史）
# 用法: .\codex-work.ps1            → 交互界面（二号家）
#       .\codex-work.ps1 doctor     → 给二号家做体检
$env:CODEX_HOME = Join-Path $env:USERPROFILE ".codex-work"
if (-not (Test-Path $env:CODEX_HOME)) { New-Item -ItemType Directory -Force $env:CODEX_HOME | Out-Null }
codex @args
