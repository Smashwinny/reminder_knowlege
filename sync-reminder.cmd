@echo off
setlocal
where pwsh.exe >nul 2>nul
if errorlevel 1 (
    powershell.exe -NoLogo -NoProfile -File "%~dp0tools\reminder_manual_sync.ps1" %*
) else (
    pwsh.exe -NoLogo -NoProfile -File "%~dp0tools\reminder_manual_sync.ps1" %*
)
set "reminderSyncExit=%ERRORLEVEL%"
echo.
echo Reminder sync exit code: %reminderSyncExit%
pause
exit /b %reminderSyncExit%
