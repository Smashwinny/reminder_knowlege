@echo off
setlocal
where pwsh.exe >nul 2>nul
if not errorlevel 1 (
    pwsh.exe -NoLogo -NoProfile -File "%~dp0tools\reminder_manual_sync.ps1" %*
    goto :result
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe" -NoLogo -NoProfile -File "%~dp0tools\reminder_manual_sync.ps1" %*
    goto :result
)
powershell.exe -NoLogo -NoProfile -File "%~dp0tools\reminder_manual_sync.ps1" %*
:result
set "reminderSyncExit=%ERRORLEVEL%"
echo.
echo Reminder sync exit code: %reminderSyncExit%
pause
exit /b %reminderSyncExit%
