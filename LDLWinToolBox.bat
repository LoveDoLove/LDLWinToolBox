@echo off
setlocal EnableDelayedExpansion

:: --- AUTO ADMIN REQUEST ---
:: Check for Administrator privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32%\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit /B
)
pushd "%CD%"
CD /D "%~dp0"
:: --- END AUTO ADMIN ---

:main_menu
cls
echo ===============================================
echo            LDL Windows ToolBox
echo ===============================================
echo [1] Advanced System Cleanup
echo [2] Clear Event Viewer Logs
echo [3] Manual SSD TRIM (Optimized for KC3000)
echo [4] Exit
echo ===============================================
set /p toolbox_choice="Select an option: "

if "%toolbox_choice%"=="1" goto cleanup
if "%toolbox_choice%"=="2" goto event_logs
if "%toolbox_choice%"=="3" goto ssd_trim
if "%toolbox_choice%"=="4" exit
goto main_menu

:cleanup
cls
echo ===============================================
echo        ADVANCED SYSTEM CLEANUP TOOL
echo ===============================================
echo.
echo [1/4] Stopping background services...
net stop wuauserv >nul 2>&1
net stop bits >nul 2>&1

echo [2/4] Deleting temporary and junk files...
del /s /f /q "%WinDir%\Temp\*.*" >nul 2>&1
del /s /f /q "%WinDir%\Prefetch\*.*" >nul 2>&1
del /s /f /q "%Temp%\*.*" >nul 2>&1
del /s /f /q "%AppData%\Temp\*.*" >nul 2>&1
del /s /f /q "%LocalAppdata%\Temp\*.*" >nul 2>&1
del /s /f /q "%WinDir%\SoftwareDistribution\Download\*.*" >nul 2>&1
del /s /f /q "%WinDir%\System32\winevt\Logs\*.*" >nul 2>&1
rd /s /q "%SYSTEMDRIVE%\AMD" >nul 2>&1
rd /s /q "%SYSTEMDRIVE%\NVIDIA" >nul 2>&1
rd /s /q "%SYSTEMDRIVE%\INTEL" >nul 2>&1

echo [3/4] Rebuilding directory structure...
for %%d in ("%WinDir%\Temp" "%WinDir%\Prefetch" "%Temp%" "%AppData%\Temp" "%LocalAppdata%\Temp") do (
    rd /s /q "%%~d" >nul 2>&1
    md "%%~d" >nul 2>&1
)

echo [4/4] Finalizing optimizations...
ipconfig /flushdns >nul 2>&1
net start wuauserv >nul 2>&1
net start bits >nul 2>&1
echo.
echo SYSTEM CLEAN UP COMPLETE!
pause
goto main_menu

:event_logs
cls
echo ===============================================
echo          CLEAR EVENT VIEWER LOGS
echo ===============================================
for /F "tokens=*" %%G in ('wevtutil.exe el') DO (
    echo clearing "%%G"
    wevtutil.exe cl "%%G"
)
echo.
echo All Event Logs have been cleared!
pause
goto main_menu

:ssd_trim
cls
echo ===============================================
echo        MANUAL SSD TRIM TOOL (KC3000)
echo ===============================================
echo.
echo Current Drives Connected:
powershell -Command "Get-Volume | Where-Object { $_.DriveLetter -ne $null } | Select-Object @{Name='Drive';Expression={$_.DriveLetter + ':'}}, FileSystemLabel, @{Name='Size(GB)';Expression={[math]::round($_.Size / 1GB, 2)}} | ft -AutoSize"
echo.
set /p trim_drive="Enter Drive Letter to TRIM (e.g. C): "
set trim_drive=%trim_drive::=%
set trim_drive=%trim_drive: =%
if "%trim_drive%"=="" goto main_menu

echo.
echo -----------------------------------------------
echo Optimizing Drive %trim_drive%: ...
echo -----------------------------------------------
defrag %trim_drive%: /L /V
echo.
echo -----------------------------------------------
echo Done.
echo [1] Return to Menu
echo [2] Exit
set /p final="Choose an option: "
if "%final%"=="1" goto main_menu
exit