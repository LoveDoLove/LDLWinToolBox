@echo off
setlocal EnableDelayedExpansion

:: --- AUTO ADMIN REQUEST ---
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32%\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit /B
)
pushd "%CD%"
CD /D "%~dp0"
:: --- END AUTO ADMIN ---

:: --- INITIALIZE LOGGING ---
for /f "delims=" %%a in ('powershell -Command "Get-Date -Format yyMMddHHmmss"') do set "LOG_TIME=%%a"
set "LOGFILE=LDLWinToolBox_!LOG_TIME!.log"

echo =============================================== > "!LOGFILE!"
echo LDL Windows ToolBox Run Log >> "!LOGFILE!"
echo Date: !LOG_TIME! >> "!LOGFILE!"
echo =============================================== >> "!LOGFILE!"
echo. >> "!LOGFILE!"

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

if "!toolbox_choice!"=="1" goto cleanup
if "!toolbox_choice!"=="2" goto event_logs
if "!toolbox_choice!"=="3" goto ssd_trim
if "!toolbox_choice!"=="4" exit
goto main_menu

:cleanup
cls
echo ===============================================
echo        ADVANCED SYSTEM CLEANUP TOOL
echo ===============================================
echo All operations are being logged to:
echo !LOGFILE!
echo ===============================================
echo.
echo [1/4] Stopping background services...
echo [1/4] Stopping background services... >> "!LOGFILE!"

echo - Stopping Windows Update (wuauserv)...
echo - Stopping Windows Update (wuauserv)... >> "!LOGFILE!"
net stop wuauserv >> "!LOGFILE!" 2>&1

echo - Stopping Background Intelligent Transfer Service (bits)...
echo - Stopping Background Intelligent Transfer Service (bits)... >> "!LOGFILE!"
net stop bits >> "!LOGFILE!" 2>&1

echo.
echo [2/4] Deleting temporary and junk files...
echo [2/4] Deleting temporary and junk files... >> "!LOGFILE!"

for %%f in (
    "%WinDir%\Temp\*.*"
    "%WinDir%\Prefetch\*.*"
    "%Temp%\*.*"
    "%AppData%\Temp\*.*"
    "%LocalAppdata%\Temp\*.*"
    "%WinDir%\SoftwareDistribution\Download\*.*"
    "%WinDir%\System32\winevt\Logs\*.*"
) do (
    echo - Cleaning %%~f
    echo - Cleaning %%~f >> "!LOGFILE!"
    del /s /f /q "%%~f" >> "!LOGFILE!" 2>&1
)

for %%d in (
    "%SYSTEMDRIVE%\AMD"
    "%SYSTEMDRIVE%\NVIDIA"
    "%SYSTEMDRIVE%\INTEL"
) do (
    if exist "%%~d" (
        echo - Removing Directory %%~d
        echo - Removing Directory %%~d >> "!LOGFILE!"
        rd /s /q "%%~d" >> "!LOGFILE!" 2>&1
    )
)

echo.
echo [3/4] Rebuilding directory structure...
echo [3/4] Rebuilding directory structure... >> "!LOGFILE!"
for %%d in ("%WinDir%\Temp" "%WinDir%\Prefetch" "%Temp%" "%AppData%\Temp" "%LocalAppdata%\Temp") do (
    echo - Rebuilding %%~d
    echo - Rebuilding %%~d >> "!LOGFILE!"
    rd /s /q "%%~d" >> "!LOGFILE!" 2>&1
    md "%%~d" >> "!LOGFILE!" 2>&1
)

echo.
echo [4/4] Finalizing optimizations...
echo [4/4] Finalizing optimizations... >> "!LOGFILE!"

echo - Flushing DNS Resolver Cache...
echo - Flushing DNS Resolver Cache... >> "!LOGFILE!"
ipconfig /flushdns >> "!LOGFILE!" 2>&1

echo - Starting Windows Update (wuauserv)...
echo - Starting Windows Update (wuauserv)... >> "!LOGFILE!"
net start wuauserv >> "!LOGFILE!" 2>&1

echo - Starting Background Intelligent Transfer Service (bits)...
echo - Starting Background Intelligent Transfer Service (bits)... >> "!LOGFILE!"
net start bits >> "!LOGFILE!" 2>&1

echo.
echo SYSTEM CLEAN UP COMPLETE!
echo SYSTEM CLEAN UP COMPLETE! >> "!LOGFILE!"
pause
goto main_menu

:event_logs
cls
echo ===============================================
echo          CLEAR EVENT VIEWER LOGS
echo ===============================================
echo All operations are being logged to:
echo !LOGFILE!
echo ===============================================
echo.
echo Clearing Event Logs... >> "!LOGFILE!"

for /F "tokens=*" %%G in ('wevtutil.exe el') DO (
    echo - Clearing log: "%%G"
    echo - Clearing log: "%%G" >> "!LOGFILE!"
    wevtutil.exe cl "%%G" >> "!LOGFILE!" 2>&1
)
echo.
echo All Event Logs have been cleared!
echo All Event Logs have been cleared! >> "!LOGFILE!"
pause
goto main_menu

:ssd_trim
cls
echo ===============================================
echo        MANUAL SSD TRIM TOOL (KC3000)
echo ===============================================
echo All operations are being logged to:
echo !LOGFILE!
echo ===============================================
echo.
echo Current Drives Connected:
powershell -Command "Get-Volume | Where-Object { $_.DriveLetter -ne $null } | Select-Object @{Name='Drive';Expression={$_.DriveLetter + ':'}}, FileSystemLabel, @{Name='Size(GB)';Expression={[math]::round($_.Size / 1GB, 2)}} | ft -AutoSize"
echo.
set trim_drive=
set /p trim_drive="Enter Drive Letter to TRIM (e.g. C): "
if "!trim_drive!"=="" goto main_menu
set trim_drive=!trim_drive::=!
set trim_drive=!trim_drive: =!
if "!trim_drive!"=="" goto main_menu

echo.
echo -----------------------------------------------
echo Optimizing Drive !trim_drive!: ...
echo Optimizing Drive !trim_drive!: ... >> "!LOGFILE!"
echo -----------------------------------------------
defrag !trim_drive!: /L /V > "%TEMP%\defrag_out.txt" 2>&1
type "%TEMP%\defrag_out.txt"
type "%TEMP%\defrag_out.txt" >> "!LOGFILE!"
del /q "%TEMP%\defrag_out.txt" >nul 2>&1

echo.
echo -----------------------------------------------
echo Done.
echo Done. >> "!LOGFILE!"
echo [1] Return to Menu
echo [2] Exit
set /p final="Choose an option: "
if "!final!"=="1" goto main_menu
exit