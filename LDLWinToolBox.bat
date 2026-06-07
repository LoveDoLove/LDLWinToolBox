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
set "SCRIPT_FILE=%~f0"
set "SCRIPT_DIR=%~dp0"
:: --- END AUTO ADMIN ---

:: --- INITIALIZE LOGGING ---
for /f "delims=" %%a in ('powershell -Command "Get-Date -Format yyMMddHHmmss"') do set "LOG_TIME=%%a"
set "LOG_DIR=%~dp0logs"
if not exist "!LOG_DIR!" md "!LOG_DIR!" >nul 2>&1
if not exist "!LOG_DIR!" (
    echo Failed to create logs directory. Using script directory for logs.
    set "LOG_DIR=%~dp0"
)
set "LOGFILE=!LOG_DIR!\LDLWinToolBox_!LOG_TIME!.log"
call :init_log

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
echo [10] View Log History
echo [11] Exit
echo ===============================================
echo Log: !LOGFILE!
echo ===============================================
set /p toolbox_choice="Select an option: "
call :log_only INFO "Menu selection: !toolbox_choice!"

if "!toolbox_choice!"=="1" goto cleanup
if "!toolbox_choice!"=="2" goto sys_repair
if "!toolbox_choice!"=="3" goto win_sxs
if "!toolbox_choice!"=="4" goto app_update
if "!toolbox_choice!"=="5" goto net_reset
if "!toolbox_choice!"=="6" goto event_logs
if "!toolbox_choice!"=="7" goto ssd_trim
if "!toolbox_choice!"=="8" goto bitlocker_disable
if "!toolbox_choice!"=="9" goto kill_browser_ai
if "!toolbox_choice!"=="10" goto log_history
if "!toolbox_choice!"=="11" (
    call :log INFO "Exiting LDL Windows ToolBox."
    exit
)
call :log WARN "Invalid menu selection: !toolbox_choice!"
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
call :log_section "Advanced System Cleanup"
call :log INFO "Calculating current free space..."
for /f "usebackq" %%a in (`powershell -Command "[math]::Round((Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='%SYSTEMDRIVE%'\").FreeSpace / 1MB)"`) do set "free_before_mb=%%a"
call :log_only INFO "Free space before cleanup: !free_before_mb! MB"

call :log INFO "[1/4] Stopping background services..."

call :log INFO "- Stopping Windows Update (wuauserv)..."
call :log_command_start "net stop wuauserv"
net stop wuauserv >> "!LOGFILE!" 2>&1
call :log_result "net stop wuauserv" !errorlevel!

call :log INFO "- Stopping Background Intelligent Transfer Service (bits)..."
call :log_command_start "net stop bits"
net stop bits >> "!LOGFILE!" 2>&1
call :log_result "net stop bits" !errorlevel!

echo.
call :log INFO "[2/4] Deleting temporary and junk files..."

for %%f in (
    "%WinDir%\Temp\*.*"
    "%WinDir%\Prefetch\*.*"
    "%Temp%\*.*"
    "%AppData%\Temp\*.*"
    "%LocalAppdata%\Temp\*.*"
    "%WinDir%\SoftwareDistribution\Download\*.*"
) do (
    call :log INFO "- Cleaning %%~f"
    call :log_command_start "del /s /f /q %%~f"
    del /s /f /q "%%~f" >> "!LOGFILE!" 2>&1
    call :log_result "del /s /f /q %%~f" !errorlevel!
)

call :log INFO "- Event Viewer logs are handled by menu option 6 using wevtutil."

for %%d in (
    "%SYSTEMDRIVE%\AMD"
    "%SYSTEMDRIVE%\NVIDIA"
    "%SYSTEMDRIVE%\INTEL"
) do (
    if exist "%%~d" (
        call :log INFO "- Removing Directory %%~d"
        call :log_command_start "rd /s /q %%~d"
        rd /s /q "%%~d" >> "!LOGFILE!" 2>&1
        call :log_result "rd /s /q %%~d" !errorlevel!
    )
)

echo.
call :log INFO "[3/4] Rebuilding directory structure..."
for %%d in ("%WinDir%\Temp" "%WinDir%\Prefetch" "%Temp%" "%AppData%\Temp" "%LocalAppdata%\Temp") do (
    call :log INFO "- Rebuilding %%~d"
    call :log_command_start "rd /s /q %%~d"
    rd /s /q "%%~d" >> "!LOGFILE!" 2>&1
    call :log_result "rd /s /q %%~d" !errorlevel!
    call :log_command_start "md %%~d"
    md "%%~d" >> "!LOGFILE!" 2>&1
    call :log_result "md %%~d" !errorlevel!
)

echo.
call :log INFO "[4/4] Finalizing optimizations..."

call :log INFO "- Starting Windows Update (wuauserv)..."
call :log_command_start "net start wuauserv"
net start wuauserv >> "!LOGFILE!" 2>&1
call :log_result "net start wuauserv" !errorlevel!

call :log INFO "- Starting Background Intelligent Transfer Service (bits)..."
call :log_command_start "net start bits"
net start bits >> "!LOGFILE!" 2>&1
call :log_result "net start bits" !errorlevel!

for /f "usebackq" %%a in (`powershell -Command "[math]::Round((Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='%SYSTEMDRIVE%'\").FreeSpace / 1MB)"`) do set "free_after_mb=%%a"
set /a "space_saved_mb=free_after_mb - free_before_mb"
if !space_saved_mb! LSS 0 set "space_saved_mb=0"
call :log_only INFO "Free space after cleanup: !free_after_mb! MB"

echo.
call :log INFO "SYSTEM CLEAN UP COMPLETE"
call :log INFO "Total Space Freed: !space_saved_mb! MB"
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
call :log_section "System Integrity Repair"
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" (
    call :log INFO "System Integrity Repair cancelled by user."
    goto main_menu
)

echo.
call :log INFO "[1/2] Running System File Checker (SFC)..."
call :log_command_start "sfc /scannow"
sfc /scannow >> "!LOGFILE!" 2>&1
call :log_result "sfc /scannow" !errorlevel!

call :log INFO "[2/2] Running DISM RestoreHealth..."
call :log_command_start "DISM /Online /Cleanup-Image /RestoreHealth"
DISM /Online /Cleanup-Image /RestoreHealth >> "!LOGFILE!" 2>&1
call :log_result "DISM /Online /Cleanup-Image /RestoreHealth" !errorlevel!

echo.
call :log INFO "SYSTEM INTEGRITY REPAIR COMPLETE"
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
call :log_section "Windows Component Store Cleanup"
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" (
    call :log INFO "Windows Component Store Cleanup cancelled by user."
    goto main_menu
)

echo.
call :log INFO "Cleaning Windows Component Store..."
call :log_command_start "DISM.exe /Online /Cleanup-Image /StartComponentCleanup"
DISM.exe /Online /Cleanup-Image /StartComponentCleanup >> "!LOGFILE!" 2>&1
call :log_result "DISM.exe /Online /Cleanup-Image /StartComponentCleanup" !errorlevel!

echo.
call :log INFO "WINSXS CLEANUP COMPLETE"
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
call :log_section "Update Installed Apps"
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" (
    call :log INFO "Update Installed Apps cancelled by user."
    goto main_menu
)

echo.
call :log INFO "Upgrading all installed applications (this may take a while)..."
call :log_command_start "winget upgrade --all"
winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements >> "!LOGFILE!" 2>&1
call :log_result "winget upgrade --all" !errorlevel!

echo.
call :log INFO "APP UPDATE COMPLETE"
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
call :log_section "Complete Network Reset"
set /p confirm="Do you want to proceed? (Y/N): "
if /i "!confirm!" NEQ "Y" (
    call :log INFO "Complete Network Reset cancelled by user."
    goto main_menu
)

echo.
call :log INFO "Resetting Winsock..."
call :log_command_start "netsh winsock reset"
netsh winsock reset >> "!LOGFILE!" 2>&1
call :log_result "netsh winsock reset" !errorlevel!

call :log INFO "Resetting TCP/IP..."
call :log_command_start "netsh int ip reset"
netsh int ip reset >> "!LOGFILE!" 2>&1
call :log_result "netsh int ip reset" !errorlevel!

call :log INFO "Flushing DNS..."
call :log_command_start "ipconfig /flushdns"
ipconfig /flushdns >> "!LOGFILE!" 2>&1
call :log_result "ipconfig /flushdns" !errorlevel!

echo.
call :log INFO "NETWORK RESET COMPLETE. Please RESTART your computer."
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
call :log_section "Clear Event Viewer Logs"

for /F "tokens=*" %%G in ('wevtutil.exe el') DO (
    call :log INFO "- Clearing log: %%G"
    call :log_command_start "wevtutil.exe cl %%G"
    wevtutil.exe cl "%%G" >> "!LOGFILE!" 2>&1
    call :log_result "wevtutil.exe cl %%G" !errorlevel!
)
echo.
call :log INFO "EVENT LOGS CLEARED"
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
call :log_section "Manual SSD TRIM"
echo Current Drives Connected:
call :log_only INFO "Current drives connected:"
powershell -Command "Get-Volume | Where-Object { $_.DriveLetter -ne $null } | Select-Object @{Name='Drive';Expression={$_.DriveLetter + ':'}}, FileSystemLabel, @{Name='Size(GB)';Expression={[math]::round($_.Size / 1GB, 2)}} | ft -AutoSize"
powershell -Command "Get-Volume | Where-Object { $_.DriveLetter -ne $null } | Select-Object @{Name='Drive';Expression={$_.DriveLetter + ':'}}, FileSystemLabel, @{Name='Size(GB)';Expression={[math]::round($_.Size / 1GB, 2)}} | ft -AutoSize" >> "!LOGFILE!" 2>&1
echo.
choice /c 0ABCDEFGHIJKLMNOPQRSTUVWXYZ /n /m "Press 0 to return, or drive letter to TRIM (A-Z): "
set "drive_choice=!errorlevel!"
if "!drive_choice!"=="1" (
    call :log INFO "Manual SSD TRIM cancelled by user."
    goto main_menu
)
call :set_drive_from_choice !drive_choice!
set "trim_drive=!selected_drive!"
call :log_only INFO "Selected TRIM drive: !trim_drive!:"
if not exist "!trim_drive!:\" (
    call :log ERROR "Drive !trim_drive!: was not found."
    pause
    goto main_menu
)

echo.
echo -----------------------------------------------
echo Optimizing Drive !trim_drive!: ...
echo Optimizing Drive !trim_drive!: ... >> "!LOGFILE!"
echo -----------------------------------------------
call :log_command_start "defrag !trim_drive!: /L /V"
defrag !trim_drive!: /L /V > "%TEMP%\defrag_out.txt" 2>&1
set "defrag_rc=!errorlevel!"
type "%TEMP%\defrag_out.txt"
type "%TEMP%\defrag_out.txt" >> "!LOGFILE!"
del /q "%TEMP%\defrag_out.txt" >nul 2>&1
call :log_result "defrag !trim_drive!: /L /V" !defrag_rc!

echo.
echo -----------------------------------------------
call :log INFO "SSD TRIM COMPLETE"
echo [1] Return to Menu
echo [2] Exit
set /p final="Choose an option: "
call :log_only INFO "SSD TRIM final selection: !final!"
if "!final!"=="1" goto main_menu
call :log INFO "Exiting LDL Windows ToolBox."
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
call :log_section "Disable BitLocker"
where manage-bde.exe >nul 2>&1
if errorlevel 1 (
    call :log ERROR "manage-bde.exe was not found on this system."
    pause
    goto main_menu
)

echo Current BitLocker status:
call :log_only INFO "Current BitLocker status:"
manage-bde -status
call :log_command_start "manage-bde -status"
manage-bde -status >> "!LOGFILE!" 2>&1
call :log_result "manage-bde -status" !errorlevel!
echo.
choice /c 0ABCDEFGHIJKLMNOPQRSTUVWXYZ /n /m "Press 0 to return, or drive letter to disable BitLocker (A-Z): "
set "drive_choice=!errorlevel!"
if "!drive_choice!"=="1" (
    call :log INFO "Disable BitLocker cancelled by user."
    goto main_menu
)
call :set_drive_from_choice !drive_choice!
set "bitlocker_drive=!selected_drive!"
call :log_only INFO "Selected BitLocker drive: !bitlocker_drive!:"
if not exist "!bitlocker_drive!:\" (
    call :log ERROR "Drive !bitlocker_drive!: was not found."
    pause
    goto main_menu
)

echo.
echo Selected drive status:
call :log_only INFO "Selected BitLocker drive status for !bitlocker_drive!:"
manage-bde -status !bitlocker_drive!:
call :log_command_start "manage-bde -status !bitlocker_drive!:"
manage-bde -status !bitlocker_drive!: >> "!LOGFILE!" 2>&1
call :log_result "manage-bde -status !bitlocker_drive!:" !errorlevel!
echo.
set confirm=
set /p confirm="Type DISABLE to start decryption for !bitlocker_drive!: "
if /i "!confirm!" NEQ "DISABLE" (
    call :log INFO "Disable BitLocker confirmation not provided. Returning to menu."
    goto main_menu
)

echo.
call :log INFO "Starting BitLocker decryption on !bitlocker_drive!: ..."
call :log_command_start "manage-bde -off !bitlocker_drive!:"
manage-bde -off !bitlocker_drive!: >> "!LOGFILE!" 2>&1
set "bitlocker_rc=!errorlevel!"
call :log_result "manage-bde -off !bitlocker_drive!:" !bitlocker_rc!
if not "!bitlocker_rc!"=="0" (
    call :log ERROR "BITLOCKER DISABLE FAILED. Check !LOGFILE!."
) else (
    call :log INFO "BITLOCKER DECRYPTION STARTED. Check Windows BitLocker status for progress."
)

echo.
echo Updated status:
call :log_only INFO "Updated BitLocker status for !bitlocker_drive!:"
manage-bde -status !bitlocker_drive!:
call :log_command_start "manage-bde -status !bitlocker_drive!:"
manage-bde -status !bitlocker_drive!: >> "!LOGFILE!" 2>&1
call :log_result "manage-bde -status !bitlocker_drive!:" !errorlevel!
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

:init_log
> "!LOGFILE!" (
    echo ===============================================================================
    echo LDL Windows ToolBox Run Log
    echo ===============================================================================
    echo Session ID : !LOG_TIME!
    echo Started    : %DATE% %TIME%
    echo Script     : !SCRIPT_FILE!
    echo Script Dir : !SCRIPT_DIR!
    echo Work Dir   : %CD%
    echo User       : %USERDOMAIN%\%USERNAME%
    echo Computer   : %COMPUTERNAME%
    echo OS         : %OS%
    echo SystemRoot : %SystemRoot%
    echo Temp       : %TEMP%
    echo Log File   : !LOGFILE!
    echo ===============================================================================
    echo.
)
call :log_only INFO "Logging initialized."
exit /b

:log
set "LOG_LEVEL=%~1"
set "LOG_MESSAGE=%~2"
set "LOG_STAMP=%DATE% %TIME%"
>> "!LOGFILE!" echo [!LOG_STAMP!] [!LOG_LEVEL!] !LOG_MESSAGE!
echo !LOG_MESSAGE!
exit /b

:log_only
set "LOG_LEVEL=%~1"
set "LOG_MESSAGE=%~2"
set "LOG_STAMP=%DATE% %TIME%"
>> "!LOGFILE!" echo [!LOG_STAMP!] [!LOG_LEVEL!] !LOG_MESSAGE!
exit /b

:log_section
call :log_only INFO "-------------------------------------------------------------------------------"
call :log INFO "== %~1 =="
exit /b

:log_command_start
call :log_only CMD "START %~1"
exit /b

:log_result
set "LOG_COMMAND=%~1"
set "LOG_CODE=%~2"
if "!LOG_CODE!"=="0" (
    call :log_only OK "END !LOG_COMMAND! exit=!LOG_CODE!"
) else (
    call :log WARN "END !LOG_COMMAND! exit=!LOG_CODE! - check log details."
)
exit /b

:log_history
cls
echo ===============================================
echo              VIEW LOG HISTORY
echo ===============================================
echo Log directory:
echo !LOG_DIR!
echo ===============================================
echo.
call :log_section "View Log History"

set "LOG_LIST=%TEMP%\LDLWinToolBox_logs_%RANDOM%.tmp"
dir /b /o-d "!LOG_DIR!\LDLWinToolBox_*.log" > "!LOG_LIST!" 2>nul
if errorlevel 1 (
    call :log INFO "No log history found."
    if exist "!LOG_LIST!" del /q "!LOG_LIST!" >nul 2>&1
    pause
    goto main_menu
)

set "log_count=0"
for %%N in (1 2 3 4 5 6 7 8 9) do set "log_%%N="
for /f "usebackq delims=" %%L in ("!LOG_LIST!") do (
    if !log_count! LSS 9 (
        set /a "log_count+=1"
        set "log_!log_count!=%%L"
        for %%A in ("!LOG_DIR!\%%L") do echo [!log_count!] %%L - %%~zA bytes - %%~tA
    )
)
del /q "!LOG_LIST!" >nul 2>&1

if "!log_count!"=="0" (
    call :log INFO "No log history found."
    pause
    goto main_menu
)

echo.
echo [0] Return to Menu
choice /c 0123456789 /n /m "Press 0 to return, or 1-9 to view a log: "
set "log_choice=!errorlevel!"
if "!log_choice!"=="1" (
    call :log INFO "View Log History returned to menu."
    goto main_menu
)
set /a "log_index=!log_choice!-1"
set "selected_log="
if "!log_index!"=="1" set "selected_log=!log_1!"
if "!log_index!"=="2" set "selected_log=!log_2!"
if "!log_index!"=="3" set "selected_log=!log_3!"
if "!log_index!"=="4" set "selected_log=!log_4!"
if "!log_index!"=="5" set "selected_log=!log_5!"
if "!log_index!"=="6" set "selected_log=!log_6!"
if "!log_index!"=="7" set "selected_log=!log_7!"
if "!log_index!"=="8" set "selected_log=!log_8!"
if "!log_index!"=="9" set "selected_log=!log_9!"

if "!selected_log!"=="" (
    call :log WARN "Invalid log history selection: !log_index!"
    pause
    goto log_history
)

cls
echo ===============================================
echo Viewing Log:
echo !selected_log!
echo ===============================================
echo Path: !LOG_DIR!\!selected_log!
echo ===============================================
echo.
call :log_only INFO "Viewing log history file: !selected_log!"
more "!LOG_DIR!\!selected_log!"
echo.
pause
goto log_history

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
call :log_section "Kill Browser AI"
call :log_only WARN "Remote script source: https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1"
set confirm=
set /p confirm="Type KILL to run Kill Browser AI: "
if /i "!confirm!" NEQ "KILL" (
    call :log INFO "Kill Browser AI cancelled by user."
    goto main_menu
)

echo.
call :log INFO "Running Kill Browser AI..."
call :log_command_start "PowerShell remote kill_ai.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { iwr -useb 'https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1' | iex; exit 0 } catch { Write-Error $_; exit 1 }" >> "!LOGFILE!" 2>&1
set "kill_ai_rc=!errorlevel!"
call :log_result "PowerShell remote kill_ai.ps1" !kill_ai_rc!
if not "!kill_ai_rc!"=="0" (
    call :log ERROR "KILL BROWSER AI FAILED. Check !LOGFILE!."
) else (
    call :log INFO "KILL BROWSER AI COMPLETE."
)
pause
goto main_menu
