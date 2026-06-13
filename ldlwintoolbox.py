from __future__ import annotations

import ctypes
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MENU_LOGO = "=" * 47
GIST_URL = "https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1"


@dataclass(slots=True)
class CommandResult:
    code: int
    stdout: str = ""
    stderr: str = ""


class Logger:
    def __init__(self, logfile: Path, script_file: Path, script_dir: Path) -> None:
        self.logfile = logfile
        self.script_file = script_file
        self.script_dir = script_dir

    def _stamp(self) -> str:
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def write_raw(self, message: str) -> None:
        self.logfile.parent.mkdir(parents=True, exist_ok=True)
        with self.logfile.open("a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write(message)
            if not message.endswith("\n"):
                handle.write("\n")

    def log_only(self, level: str, message: str) -> None:
        self.write_raw(f"[{self._stamp()}] [{level}] {message}")

    def log(self, level: str, message: str) -> None:
        self.log_only(level, message)
        print(message)

    def section(self, title: str) -> None:
        self.log_only("INFO", "-" * 79)
        self.log("INFO", f"== {title} ==")

    def command_start(self, command: str) -> None:
        self.log_only("CMD", f"START {command}")

    def command_result(self, command: str, code: int) -> None:
        if code == 0:
            self.log_only("OK", f"END {command} exit={code}")
        else:
            self.log("WARN", f"END {command} exit={code} - check log details.")


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> None:
    script = Path(__file__).resolve()
    uv_exe = shutil.which("uv")
    if uv_exe:
        params = f'run -- python "{script}"'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", uv_exe, params, None, 1)
        return
    params = f'"{script}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)


def ensure_admin() -> None:
    if is_admin():
        return
    print("Requesting administrative privileges...")
    relaunch_as_admin()
    raise SystemExit(0)


def clear_screen() -> None:
    os.system("cls")


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def run_command(command: list[str] | str, *, shell: bool = False, capture: bool = True, check: bool = False) -> CommandResult:
    completed = subprocess.run(
        command,
        shell=shell,
        text=True,
        capture_output=capture,
        check=False,
    )
    if check and completed.returncode != 0:
        raise subprocess.CalledProcessError(completed.returncode, command, completed.stdout, completed.stderr)
    return CommandResult(completed.returncode, completed.stdout or "", completed.stderr or "")


def run_and_log(logger: Logger, command: list[str] | str, display: str, *, shell: bool = False, capture_output: bool = True) -> CommandResult:
    logger.command_start(display)
    result = run_command(command, shell=shell, capture=capture_output)
    if result.stdout:
        logger.write_raw(result.stdout)
    if result.stderr:
        logger.write_raw(result.stderr)
    logger.command_result(display, result.code)
    return result


def prompt_yes_no(logger: Logger, prompt: str, context: str) -> bool:
    answer = input(prompt).strip()
    if answer.upper() == "Y":
        return True
    logger.log_only("INFO", f"{context} cancelled by user.")
    return False


def prompt_keyword(logger: Logger, prompt: str, expected: str, context: str) -> bool:
    answer = input(prompt).strip()
    if answer.upper() == expected.upper():
        return True
    logger.log_only("INFO", f"{context} cancelled by user.")
    return False


def prompt_drive(logger: Logger, prompt: str, context: str) -> str | None:
    options = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    choice = input(prompt).strip().upper()
    if choice == "0":
        logger.log_only("INFO", f"{context} cancelled by user.")
        return None
    if len(choice) != 1 or choice not in options:
        logger.log_only("WARN", f"Invalid {context} selection: {choice}")
        print("Invalid selection.")
        return ""
    return choice


def write_session_header(logger: Logger, logfile: Path, script_file: Path, script_dir: Path) -> None:
    now = datetime.now()
    header = [
        "=" * 79,
        "LDL Windows ToolBox Run Log",
        "=" * 79,
        f"Session ID : {now.strftime('%y%m%d%H%M%S')}",
        f"Started    : {now.strftime('%m/%d/%Y %H:%M:%S')}",
        f"Script     : {script_file}",
        f"Script Dir : {script_dir}",
        f"Work Dir   : {Path.cwd()}",
        f"User       : {os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}",
        f"Computer   : {os.environ.get('COMPUTERNAME', '')}",
        f"OS         : {platform.system()}",
        f"SystemRoot : {os.environ.get('SystemRoot', '')}",
        f"Temp       : {tempfile.gettempdir()}",
        f"Log File   : {logfile}",
        "=" * 79,
        "",
    ]
    logger.logfile.parent.mkdir(parents=True, exist_ok=True)
    logger.logfile.write_text("\n".join(header), encoding="utf-8", newline="\n")
    logger.log_only("INFO", "Logging initialized.")


def get_log_dir(script_dir: Path) -> Path:
    log_dir = script_dir / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    except OSError:
        print("Failed to create logs directory. Using script directory for logs.")
        return script_dir


def get_volume_table() -> str:
    ps = (
        "Get-Volume | Where-Object { $_.DriveLetter -ne $null } "
        "| Select-Object @{Name='Drive';Expression={$_.DriveLetter + ':'}}, "
        "FileSystemLabel, @{Name='Size(GB)';Expression={[math]::round($_.Size / 1GB, 2)}} "
        "| Format-Table -AutoSize"
    )
    result = run_command(["powershell", "-NoProfile", "-Command", ps], capture=True)
    return (result.stdout or "") + (result.stderr or "")


def select_existing_drive(logger: Logger, context: str) -> str | None:
    choice = prompt_drive(logger, "Press 0 to return, or drive letter to continue (A-Z): ", context)
    if choice is None:
        return None
    if choice == "":
        return ""
    if not Path(f"{choice}:\\").exists():
        logger.log("ERROR", f"Drive {choice}: was not found.")
        return ""
    return choice


def cleanup(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("        ADVANCED SYSTEM CLEANUP TOOL")
    print(MENU_LOGO)
    print(f"All operations are being logged to:\n{logger.logfile}")
    print(MENU_LOGO)
    logger.section("Advanced System Cleanup")

    free_before = drive_free_mb()
    logger.log_only("INFO", f"Free space before cleanup: {free_before} MB")

    logger.log("INFO", "[1/4] Stopping background services...")
    for cmd in (["net", "stop", "wuauserv"], ["net", "stop", "bits"]):
        logger.log("INFO", f"- Stopping {cmd[-1]}...")
        run_and_log(logger, cmd, " ".join(cmd), capture_output=True)

    print()
    logger.log("INFO", "[2/4] Deleting temporary and junk files...")
    def env_temp_dir(name: str) -> Path | None:
        value = os.environ.get(name)
        return Path(value) / "Temp" if value else None

    temp_targets = [
        Path(os.environ["WinDir"]) / "Temp",
        Path(os.environ["WinDir"]) / "Prefetch",
        Path(os.environ["TEMP"]),
        env_temp_dir("AppData"),
        env_temp_dir("LocalAppData"),
        Path(os.environ["WinDir"]) / "SoftwareDistribution" / "Download",
    ]
    for target in temp_targets:
        if target is None:
            continue
        logger.log("INFO", f"- Cleaning {target}")
        if target.exists():
            for child in target.iterdir():
                try:
                    if child.is_dir():
                        shutil.rmtree(child, ignore_errors=False)
                    else:
                        child.unlink(missing_ok=True)
                except OSError as exc:
                    logger.log_only("WARN", f"Failed to remove {child}: {exc}")

    logger.log("INFO", "- Event Viewer logs are handled by menu option 6 using wevtutil.")
    system_drive = os.environ.get("SYSTEMDRIVE", "C:")
    for root_name in ("AMD", "NVIDIA", "INTEL"):
        root = Path(f"{system_drive}\\{root_name}")
        if root.exists():
            logger.log("INFO", f"- Removing Directory {root}")
            shutil.rmtree(root, ignore_errors=True)

    print()
    logger.log("INFO", "[3/4] Rebuilding directory structure...")
    for target in temp_targets[:5]:
        if target is None:
            continue
        logger.log("INFO", f"- Rebuilding {target}")
        target.mkdir(parents=True, exist_ok=True)

    print()
    logger.log("INFO", "[4/4] Finalizing optimizations...")
    for cmd in (["net", "start", "wuauserv"], ["net", "start", "bits"]):
        logger.log("INFO", f"- Starting {cmd[-1]}...")
        run_and_log(logger, cmd, " ".join(cmd), capture_output=True)

    free_after = drive_free_mb()
    saved = max(0, free_after - free_before)
    logger.log_only("INFO", f"Free space after cleanup: {free_after} MB")
    logger.log("INFO", "SYSTEM CLEAN UP COMPLETE")
    logger.log("INFO", f"Total Space Freed: {saved} MB")
    input("Press Enter to continue...")


def drive_free_mb() -> int:
    ps = (
        f"[math]::Round((Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='{os.environ.get('SYSTEMDRIVE', 'C:')}'\").FreeSpace / 1MB)"
    )
    result = run_command(["powershell", "-Command", ps], capture=True)
    text = (result.stdout or "").strip()
    try:
        return int(float(text))
    except ValueError:
        return 0


def sys_repair(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("        SYSTEM INTEGRITY REPAIR (SFC + DISM)")
    print(MENU_LOGO)
    print("WARNING: This process can take 15-45 minutes.")
    print("-> It CAN be safely interrupted by closing the window.")
    print("-> However, it is recommended to let it finish.")
    print(MENU_LOGO)
    logger.section("System Integrity Repair")
    if not prompt_yes_no(logger, "Do you want to proceed? (Y/N): ", "System Integrity Repair"):
        return
    for cmd, label in ((["sfc", "/scannow"], "System File Checker"), (["dism", "/Online", "/Cleanup-Image", "/RestoreHealth"], "DISM RestoreHealth")):
        if not command_exists(cmd[0]):
            logger.log("ERROR", f"{cmd[0]} is required for {label}, but it was not found.")
            input("Press Enter to continue...")
            return
        logger.log("INFO", f"Running {label}...")
        run_and_log(logger, cmd, " ".join(cmd), capture_output=True)
    logger.log("INFO", "SYSTEM INTEGRITY REPAIR COMPLETE")
    input("Press Enter to continue...")


def component_store_cleanup(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("      WINDOWS COMPONENT STORE CLEANUP (WinSxS)")
    print(MENU_LOGO)
    print("WARNING: This deeply cleans old Windows Update files.")
    print("-> It can take 10-30 minutes and may appear stuck.")
    print("-> DO NOT interrupt this process (can corrupt updates).")
    print(MENU_LOGO)
    logger.section("Windows Component Store Cleanup")
    if not prompt_yes_no(logger, "Do you want to proceed? (Y/N): ", "Windows Component Store Cleanup"):
        return
    if not command_exists("dism"):
        logger.log("ERROR", "dism is required for DISM component cleanup, but it was not found.")
        input("Press Enter to continue...")
        return
    logger.log("INFO", "Cleaning Windows Component Store...")
    run_and_log(logger, ["dism", "/Online", "/Cleanup-Image", "/StartComponentCleanup"], "DISM.exe /Online /Cleanup-Image /StartComponentCleanup")
    logger.log("INFO", "WINSXS CLEANUP COMPLETE")
    input("Press Enter to continue...")


def app_update(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("         UPDATE INSTALLED APPS (WINGET)")
    print(MENU_LOGO)
    print("WARNING: Silently updates all apps installed via Winget.")
    print("-> May take several minutes.")
    print("-> It CAN be safely interrupted.")
    print(MENU_LOGO)
    logger.section("Update Installed Apps")
    if not prompt_yes_no(logger, "Do you want to proceed? (Y/N): ", "Update Installed Apps"):
        return
    if not command_exists("winget"):
        logger.log("ERROR", "winget is required for Winget update, but it was not found.")
        input("Press Enter to continue...")
        return
    logger.log("INFO", "Upgrading all installed applications (this may take a while)...")
    run_and_log(
        logger,
        ["winget", "upgrade", "--all", "--include-unknown", "--accept-package-agreements", "--accept-source-agreements"],
        "winget upgrade --all",
    )
    logger.log("INFO", "APP UPDATE COMPLETE")
    input("Press Enter to continue...")


def net_reset(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("            COMPLETE NETWORK RESET")
    print(MENU_LOGO)
    print("This will reset your network adapters to factory defaults.")
    print("-> A system restart will be required afterward.")
    print(MENU_LOGO)
    logger.section("Complete Network Reset")
    if not prompt_yes_no(logger, "Do you want to proceed? (Y/N): ", "Complete Network Reset"):
        return
    for cmd, label in ((["netsh", "winsock", "reset"], "netsh winsock reset"), (["netsh", "int", "ip", "reset"], "netsh int ip reset"), (["ipconfig", "/flushdns"], "ipconfig /flushdns")):
        if not command_exists(cmd[0]):
            logger.log("ERROR", f"{cmd[0]} is required for {label}, but it was not found.")
            input("Press Enter to continue...")
            return
        logger.log("INFO", label.replace("netsh ", "Resetting ").replace("ipconfig ", "Flushing "))
        run_and_log(logger, cmd, label)
    logger.log("INFO", "NETWORK RESET COMPLETE. Please RESTART your computer.")
    input("Press Enter to continue...")


def event_logs(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("          CLEAR EVENT VIEWER LOGS")
    print(MENU_LOGO)
    print(f"All operations are being logged to:\n{logger.logfile}")
    print(MENU_LOGO)
    logger.section("Clear Event Viewer Logs")
    if not command_exists("wevtutil"):
        logger.log("ERROR", "wevtutil.exe is required for Event Viewer logs, but it was not found.")
        input("Press Enter to continue...")
        return
    result = run_command(["wevtutil", "el"], capture=True)
    logs = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    for entry in logs:
        logger.log("INFO", f"- Clearing log: {entry}")
        run_and_log(logger, ["wevtutil", "cl", entry], f"wevtutil.exe cl {entry}")
    logger.log("INFO", "EVENT LOGS CLEARED")
    input("Press Enter to continue...")


def ssd_trim(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("        MANUAL SSD TRIM TOOL (KC3000)")
    print(MENU_LOGO)
    print(f"All operations are being logged to:\n{logger.logfile}")
    print(MENU_LOGO)
    logger.section("Manual SSD TRIM")
    print("Current Drives Connected:")
    logger.log_only("INFO", "Current drives connected:")
    if not command_exists("powershell"):
        logger.log("ERROR", "powershell.exe is required for Volume enumeration, but it was not found.")
        input("Press Enter to continue...")
        return
    volume_text = get_volume_table()
    print(volume_text, end="" if volume_text.endswith("\n") else "\n")
    logger.write_raw(volume_text)
    print()
    drive = select_existing_drive(logger, "Manual SSD TRIM")
    if drive is None:
        return
    if drive == "":
        logger.log("ERROR", "No valid drive was selected for Manual SSD TRIM.")
        input("Press Enter to continue...")
        return
    logger.log_only("INFO", f"Selected TRIM drive: {drive}:")
    print(f"\nOptimizing Drive {drive}: ...")
    logger.write_raw(f"Optimizing Drive {drive}: ...")
    print("".join(["-" for _ in range(47)]))
    if not command_exists("defrag"):
        logger.log("ERROR", "defrag.exe is required for SSD TRIM, but it was not found.")
        input("Press Enter to continue...")
        return
    out_file = Path(tempfile.gettempdir()) / "defrag_out.txt"
    result = run_command(["defrag", f"{drive}:", "/L", "/V"], capture=True)
    out_file.write_text((result.stdout or "") + (result.stderr or ""), encoding="utf-8", errors="replace")
    print(out_file.read_text(encoding="utf-8", errors="replace"), end="")
    logger.write_raw(out_file.read_text(encoding="utf-8", errors="replace"))
    try:
        out_file.unlink()
    except OSError:
        pass
    logger.command_result(f"defrag {drive}: /L /V", result.code)
    logger.log("INFO", "SSD TRIM COMPLETE")
    print("[1] Return to Menu")
    print("[2] Exit")
    final = input("Choose an option: ").strip()
    logger.log_only("INFO", f"SSD TRIM final selection: {final}")
    if final == "2":
        raise SystemExit(0)


def bitlocker_disable(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("          DISABLE BITLOCKER (PLAN)")
    print(MENU_LOGO)
    print("WARNING: This starts BitLocker decryption for the")
    print("selected drive and turns BitLocker off.")
    print("-> Decryption can take a long time.")
    print("-> Keep the PC powered on until Windows finishes.")
    print("-> Do this only when protection is no longer needed.")
    print(MENU_LOGO)
    logger.section("Disable BitLocker")
    if not command_exists("manage-bde"):
        logger.log("ERROR", "manage-bde.exe is required for BitLocker management, but it was not found.")
        input("Press Enter to continue...")
        return
    print("Current BitLocker status:")
    logger.log_only("INFO", "Current BitLocker status:")
    status_result = run_and_log(logger, ["manage-bde", "-status"], "manage-bde -status")
    if status_result.stdout:
        print(status_result.stdout, end="" if status_result.stdout.endswith("\n") else "\n")
    if status_result.stderr:
        print(status_result.stderr, end="" if status_result.stderr.endswith("\n") else "\n")
    print()
    drive = select_existing_drive(logger, "Disable BitLocker")
    if drive is None:
        return
    if drive == "":
        logger.log("ERROR", "No valid drive was selected for Disable BitLocker.")
        input("Press Enter to continue...")
        return
    logger.log_only("INFO", f"Selected BitLocker drive: {drive}:")
    print("\nSelected drive status:")
    logger.log_only("INFO", f"Selected BitLocker drive status for {drive}:")
    status_result = run_and_log(logger, ["manage-bde", "-status", f"{drive}:"], f"manage-bde -status {drive}:")
    if status_result.stdout:
        print(status_result.stdout, end="" if status_result.stdout.endswith("\n") else "\n")
    if status_result.stderr:
        print(status_result.stderr, end="" if status_result.stderr.endswith("\n") else "\n")
    print()
    if not prompt_keyword(logger, f"Type DISABLE to start decryption for {drive}: ", "DISABLE", "Disable BitLocker"):
        return
    logger.log("INFO", f"Starting BitLocker decryption on {drive}: ...")
    result = run_and_log(logger, ["manage-bde", "-off", f"{drive}:"], f"manage-bde -off {drive}:")
    if result.code != 0:
        logger.log("ERROR", "BITLOCKER DISABLE FAILED. Check log.")
    else:
        logger.log("INFO", "BITLOCKER DECRYPTION STARTED. Check Windows BitLocker status for progress.")
    print("\nUpdated status:")
    logger.log_only("INFO", f"Updated BitLocker status for {drive}:")
    status_result = run_and_log(logger, ["manage-bde", "-status", f"{drive}:"], f"manage-bde -status {drive}:")
    if status_result.stdout:
        print(status_result.stdout, end="" if status_result.stdout.endswith("\n") else "\n")
    if status_result.stderr:
        print(status_result.stderr, end="" if status_result.stderr.endswith("\n") else "\n")
    input("Press Enter to continue...")


def list_log_history(log_dir: Path, logger: Logger) -> list[Path]:
    entries = sorted(log_dir.glob("LDLWinToolBox_*.log"), key=lambda path: path.stat().st_mtime, reverse=True)
    return entries[:9]


def log_history(logger: Logger, log_dir: Path) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              VIEW LOG HISTORY")
    print(MENU_LOGO)
    print(f"Log directory:\n{log_dir}")
    print(MENU_LOGO)
    logger.section("View Log History")
    if not command_exists("more"):
        logger.log("ERROR", "more.com is required for Log History viewer, but it was not found.")
        input("Press Enter to continue...")
        return
    logs = list_log_history(log_dir, logger)
    if not logs:
        logger.log("INFO", "No log history found.")
        input("Press Enter to continue...")
        return
    for idx, path in enumerate(logs, start=1):
        stat = path.stat()
        ts = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"[{idx}] {path.name} - {stat.st_size} bytes - {ts}")
    print()
    print("[0] Return to Menu")
    choice = input("Press 0 to return, or 1-9 to view a log: ").strip()
    if choice == "0":
        logger.log("INFO", "View Log History returned to menu.")
        return
    try:
        index = int(choice) - 1
    except ValueError:
        logger.log("WARN", f"Invalid log history selection: {choice}")
        input("Press Enter to continue...")
        return
    if index < 0 or index >= len(logs):
        logger.log("WARN", f"Invalid log history selection: {choice}")
        input("Press Enter to continue...")
        return
    selected = logs[index]
    print(MENU_LOGO)
    print("Viewing Log:")
    print(selected.name)
    print(MENU_LOGO)
    print(f"Path: {selected}")
    print(MENU_LOGO)
    logger.log_only("INFO", f"Viewing log history file: {selected.name}")
    subprocess.run(["more", str(selected)], shell=False)
    input("Press Enter to continue...")


def kill_browser_ai(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              KILL BROWSER AI")
    print(MENU_LOGO)
    print("WARNING: This downloads and executes a remote")
    print("PowerShell script from the configured gist URL.")
    print("-> It may close browser or AI-related processes.")
    print("-> Network access is required.")
    print("-> Do not run if you do not trust the source.")
    print(MENU_LOGO)
    print("Source:")
    print(GIST_URL)
    print()
    logger.section("Kill Browser AI")
    logger.log_only("WARN", f"Remote script source: {GIST_URL}")
    if not prompt_keyword(logger, "Type KILL to run Kill Browser AI: ", "KILL", "Kill Browser AI"):
        return
    if not command_exists("powershell"):
        logger.log("ERROR", "powershell.exe is required for Kill Browser AI, but it was not found.")
        input("Press Enter to continue...")
        return
    logger.log("INFO", "Running Kill Browser AI...")
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        f"try {{ iwr -useb '{GIST_URL}' | iex; exit 0 }} catch {{ Write-Error $_; exit 1 }}",
    ]
    result = run_and_log(logger, cmd, "PowerShell remote kill_ai.ps1")
    if result.code != 0:
        logger.log("ERROR", "KILL BROWSER AI FAILED. Check log.")
    else:
        logger.log("INFO", "KILL BROWSER AI COMPLETE.")
    input("Press Enter to continue...")


def main_menu(logger: Logger, log_dir: Path) -> None:
    while True:
        clear_screen()
        print("===============================================")
        print("           LDL Windows ToolBox")
        print("===============================================")
        print("[1] Advanced System Cleanup (with Space Calculator)")
        print("[2] System Integrity Repair (SFC + DISM)")
        print("[3] Windows Component Store Cleanup (WinSxS)")
        print("[4] Update All Installed Apps (Winget)")
        print("[5] Complete Network Reset")
        print("[6] Clear Event Viewer Logs")
        print("[7] Manual SSD TRIM (Optimized for KC3000)")
        print("[8] Disable BitLocker (Plan)")
        print("[9] Kill Browser AI")
        print("[10] View Log History")
        print("[11] Exit")
        print("===============================================")
        print(f"Log: {logger.logfile}")
        print("===============================================")
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Menu selection: {choice}")

        if choice == "1":
            cleanup(logger)
        elif choice == "2":
            sys_repair(logger)
        elif choice == "3":
            component_store_cleanup(logger)
        elif choice == "4":
            app_update(logger)
        elif choice == "5":
            net_reset(logger)
        elif choice == "6":
            event_logs(logger)
        elif choice == "7":
            ssd_trim(logger)
        elif choice == "8":
            bitlocker_disable(logger)
        elif choice == "9":
            kill_browser_ai(logger)
        elif choice == "10":
            log_history(logger, log_dir)
        elif choice == "11":
            logger.log("INFO", "Exiting LDL Windows ToolBox.")
            return
        else:
            logger.log("WARN", f"Invalid menu selection: {choice}")


def main() -> None:
    ensure_admin()
    script_file = Path(__file__).resolve()
    script_dir = script_file.parent
    os.chdir(script_dir)
    log_dir = get_log_dir(script_dir)
    log_time = datetime.now().strftime("%y%m%d%H%M%S")
    logfile = log_dir / f"LDLWinToolBox_{log_time}.log"
    logger = Logger(logfile, script_file, script_dir)
    write_session_header(logger, logfile, script_file, script_dir)
    try:
        main_menu(logger, log_dir)
    except KeyboardInterrupt:
        logger.log("INFO", "User cancelled the session with Ctrl+C.")


if __name__ == "__main__":
    main()
