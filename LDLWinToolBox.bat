@echo off
setlocal EnableDelayedExpansion

:: --- AUTO ADMIN REQUEST ---
fltmc >nul 2>&1
if errorlevel 1 (
    echo Requesting administrative privileges...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
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
echo [1] Advanced System Cleanup (with Space Calculator)
echo [2] System Integrity Repair (SFC + DISM)
echo [3] Windows Component Store Cleanup (WinSxS)
echo [4] Update All Installed Apps (Winget)
echo [5] Complete Network Reset
echo [6] Clear Event Viewer Logs
echo [7] Manual SSD TRIM (Optimized for KC3000)
echo [8] Disable BitLocker (Plan)
echo [9] Kill Browser AI
echo [10] Exit
echo ===============================================
set /p toolbox_choice="Select an option: "

if "!toolbox_choice!"=="1" goto cleanup
if "!toolbox_choice!"=="2" goto sys_repair
if "!toolbox_choice!"=="3" goto win_sxs
if "!toolbox_choice!"=="4" goto app_update
if "!toolbox_choice!"=="5" goto net_reset
if "!toolbox_choice!"=="6" goto event_logs
if "!toolbox_choice!"=="7" goto ssd_trim
if "!toolbox_choice!"=="8" goto bitlocker_disable
if "!toolbox_choice!"=="9" goto kill_browser_ai
if "!toolbox_choice!"=="10" exit
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
echo Calculating current free space...
for /f "usebackq" %%a in (`powershell -Command "[math]::Round((Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='%SYSTEMDRIVE%'\").FreeSpace / 1MB)"`) do set "free_before_mb=%%a"

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
) do (
    echo - Cleaning %%~f
    echo - Cleaning %%~f >> "!LOGFILE!"
    del /s /f /q "%%~f" >> "!LOGFILE!" 2>&1
)

echo - Event Viewer logs are handled by menu option 6 using wevtutil.
echo - Event Viewer logs are handled by menu option 6 using wevtutil. >> "!LOGFILE!"

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

echo - Starting Windows Update (wuauserv)...
echo - Starting Windows Update (wuauserv)... >> "!LOGFILE!"
net start wuauserv >> "!LOGFILE!" 2>&1

echo - Starting Background Intelligent Transfer Service (bits)...
echo - Starting Background Intelligent Transfer Service (bits)... >> "!LOGFILE!"
net start bits >> "!LOGFILE!" 2>&1

for /f "usebackq" %%a in (`powershell -Command "[math]::Round((Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='%SYSTEMDRIVE%'\").FreeSpace / 1MB)"`) do set "free_after_mb=%%a"
set /a "space_saved_mb=free_after_mb - free_before_mb"
if !space_saved_mb! LSS 0 set "space_saved_mb=0"

echo.
echo SYSTEM CLEAN UP COMPLETE!
echo SYSTEM CLEAN UP COMPLETE! >> "!LOGFILE!"
echo -^> Total Space Freed: !space_saved_mb! MB
echo -^> Total Space Freed: !space_saved_mb! MB >> "!LOGFILE!"
pause
goto main_menu

:sys_repair
cls
echo ===============================================
echo        SYSTEM INTEGRITY REPAIR (SFC + DISM)
echo ===============================================
echo WARNING: This process can take 15-45 minutes.
echo -^> It CAN be safely interrupted by closing the window.
echo -^> However, it is recommended to let it finish.
echo ===============================================
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" goto main_menu

echo.
echo [1/2] Running System File Checker (SFC)...
echo Running SFC >> "!LOGFILE!"
sfc /scannow >> "!LOGFILE!" 2>&1

echo [2/2] Running DISM RestoreHealth...
echo Running DISM RestoreHealth >> "!LOGFILE!"
DISM /Online /Cleanup-Image /RestoreHealth >> "!LOGFILE!" 2>&1

echo.
echo SYSTEM INTEGRITY REPAIR COMPLETE!
echo SYSTEM INTEGRITY REPAIR COMPLETE! >> "!LOGFILE!"
pause
goto main_menu

:win_sxs
cls
echo ===============================================
echo      WINDOWS COMPONENT STORE CLEANUP (WinSxS)
echo ===============================================
echo WARNING: This deeply cleans old Windows Update files.
echo -^> It can take 10-30 minutes and may appear stuck.
echo -^> DO NOT interrupt this process (can corrupt updates).
echo ===============================================
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" goto main_menu

echo.
echo Cleaning Windows Component Store...
echo Running WinSxS Cleanup >> "!LOGFILE!"
DISM.exe /Online /Cleanup-Image /StartComponentCleanup >> "!LOGFILE!" 2>&1

echo.
echo WINSXS CLEANUP COMPLETE!
echo WINSXS CLEANUP COMPLETE! >> "!LOGFILE!"
pause
goto main_menu

:app_update
cls
echo ===============================================
echo         UPDATE INSTALLED APPS (WINGET)
echo ===============================================
echo WARNING: Silently updates all apps installed via Winget.
echo -^> May take several minutes.
echo -^> It CAN be safely interrupted.
echo ===============================================
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" goto main_menu

echo.
echo Upgrading all installed applications (this may take a while)...
echo Running Winget Upgrade All >> "!LOGFILE!"
winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements >> "!LOGFILE!" 2>&1

echo.
echo APP UPDATE COMPLETE!
echo APP UPDATE COMPLETE! >> "!LOGFILE!"
pause
goto main_menu

:net_reset
cls
echo ===============================================
echo            COMPLETE NETWORK RESET
echo ===============================================
echo This will reset your network adapters to factory defaults.
echo -^> A system restart will be required afterward.
echo ===============================================
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" goto main_menu

echo.
echo Resetting Winsock...
echo Resetting Winsock >> "!LOGFILE!"
netsh winsock reset >> "!LOGFILE!" 2>&1

echo Resetting TCP/IP...
echo Resetting TCP/IP >> "!LOGFILE!"
netsh int ip reset >> "!LOGFILE!" 2>&1

echo Flushing DNS...
echo Flushing DNS >> "!LOGFILE!"
ipconfig /flushdns >> "!LOGFILE!" 2>&1

echo.
echo NETWORK RESET COMPLETE! Please RESTART your computer.
echo NETWORK RESET COMPLETE! >> "!LOGFILE!"
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
echo EVENT LOGS CLEARED!
echo EVENT LOGS CLEARED! >> "!LOGFILE!"
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
choice /c 0ABCDEFGHIJKLMNOPQRSTUVWXYZ /n /m "Press 0 to return, or drive letter to TRIM (A-Z): "
set "drive_choice=!errorlevel!"
if "!drive_choice!"=="1" goto main_menu
call :set_drive_from_choice !drive_choice!
set "trim_drive=!selected_drive!"
if not exist "!trim_drive!:\" (
    echo Drive !trim_drive!: was not found.
    echo TRIM drive not found: !trim_drive!: >> "!LOGFILE!"
    pause
    goto main_menu
)

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
echo SSD TRIM COMPLETE!
echo SSD TRIM COMPLETE! >> "!LOGFILE!"
echo [1] Return to Menu
echo [2] Exit
set /p final="Choose an option: "
if "!final!"=="1" goto main_menu
exit

:bitlocker_disable
cls
echo ===============================================
echo          DISABLE BITLOCKER (PLAN)
echo ===============================================
echo WARNING: This starts BitLocker decryption for the
echo selected drive and turns BitLocker off.
echo -^> Decryption can take a long time.
echo -^> Keep the PC powered on until Windows finishes.
echo -^> Do this only when protection is no longer needed.
echo ===============================================
echo.
where manage-bde.exe >nul 2>&1
if errorlevel 1 (
    echo manage-bde.exe was not found on this system.
    echo manage-bde.exe was not found. >> "!LOGFILE!"
    pause
    goto main_menu
)

echo Current BitLocker status:
echo Current BitLocker status: >> "!LOGFILE!"
manage-bde -status
manage-bde -status >> "!LOGFILE!" 2>&1
echo.
choice /c 0ABCDEFGHIJKLMNOPQRSTUVWXYZ /n /m "Press 0 to return, or drive letter to disable BitLocker (A-Z): "
set "drive_choice=!errorlevel!"
if "!drive_choice!"=="1" goto main_menu
call :set_drive_from_choice !drive_choice!
set "bitlocker_drive=!selected_drive!"
if not exist "!bitlocker_drive!:\" (
    echo Drive !bitlocker_drive!: was not found.
    echo BitLocker drive not found: !bitlocker_drive!: >> "!LOGFILE!"
    pause
    goto main_menu
)

echo.
echo Selected drive status:
echo Selected BitLocker drive status for !bitlocker_drive!: >> "!LOGFILE!"
manage-bde -status !bitlocker_drive!:
manage-bde -status !bitlocker_drive!: >> "!LOGFILE!" 2>&1
echo.
set confirm=
set /p confirm="Type DISABLE to start decryption for !bitlocker_drive!: "
if /i "!confirm!" NEQ "DISABLE" goto main_menu

echo.
echo Starting BitLocker decryption on !bitlocker_drive!: ...
echo Starting BitLocker decryption on !bitlocker_drive!: >> "!LOGFILE!"
manage-bde -off !bitlocker_drive!: >> "!LOGFILE!" 2>&1
if errorlevel 1 (
    echo BITLOCKER DISABLE FAILED. Check !LOGFILE!.
    echo BITLOCKER DISABLE FAILED. >> "!LOGFILE!"
) else (
    echo BITLOCKER DECRYPTION STARTED. Check Windows BitLocker status for progress.
    echo BITLOCKER DECRYPTION STARTED. >> "!LOGFILE!"
)

echo.
echo Updated status:
echo Updated BitLocker status for !bitlocker_drive!: >> "!LOGFILE!"
manage-bde -status !bitlocker_drive!:
manage-bde -status !bitlocker_drive!: >> "!LOGFILE!" 2>&1
pause
goto main_menu

:set_drive_from_choice
set "selected_drive="
if "%~1"=="2" set "selected_drive=A"
if "%~1"=="3" set "selected_drive=B"
if "%~1"=="4" set "selected_drive=C"
if "%~1"=="5" set "selected_drive=D"
if "%~1"=="6" set "selected_drive=E"
if "%~1"=="7" set "selected_drive=F"
if "%~1"=="8" set "selected_drive=G"
if "%~1"=="9" set "selected_drive=H"
if "%~1"=="10" set "selected_drive=I"
if "%~1"=="11" set "selected_drive=J"
if "%~1"=="12" set "selected_drive=K"
if "%~1"=="13" set "selected_drive=L"
if "%~1"=="14" set "selected_drive=M"
if "%~1"=="15" set "selected_drive=N"
if "%~1"=="16" set "selected_drive=O"
if "%~1"=="17" set "selected_drive=P"
if "%~1"=="18" set "selected_drive=Q"
if "%~1"=="19" set "selected_drive=R"
if "%~1"=="20" set "selected_drive=S"
if "%~1"=="21" set "selected_drive=T"
if "%~1"=="22" set "selected_drive=U"
if "%~1"=="23" set "selected_drive=V"
if "%~1"=="24" set "selected_drive=W"
if "%~1"=="25" set "selected_drive=X"
if "%~1"=="26" set "selected_drive=Y"
if "%~1"=="27" set "selected_drive=Z"
exit /b

:kill_browser_ai
cls
echo ===============================================
echo              KILL BROWSER AI
echo ===============================================
echo WARNING: This downloads and executes a remote
echo PowerShell script from the configured gist URL.
echo -^> It may close browser or AI-related processes.
echo -^> Network access is required.
echo -^> Do not run if you do not trust the source.
echo ===============================================
echo.
echo Source:
echo https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1
echo.
set confirm=
set /p confirm="Type KILL to run Kill Browser AI: "
if /i "!confirm!" NEQ "KILL" goto main_menu

echo.
echo Running Kill Browser AI...
echo Running Kill Browser AI remote script. >> "!LOGFILE!"
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { iwr -useb 'https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1' | iex; exit 0 } catch { Write-Error $_; exit 1 }" >> "!LOGFILE!" 2>&1
if errorlevel 1 (
    echo KILL BROWSER AI FAILED. Check !LOGFILE!.
    echo KILL BROWSER AI FAILED. >> "!LOGFILE!"
) else (
    echo KILL BROWSER AI COMPLETE.
    echo KILL BROWSER AI COMPLETE. >> "!LOGFILE!"
)
pause
goto main_menu
