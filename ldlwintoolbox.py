from __future__ import annotations

import ctypes
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from toolbox_base import (
    Logger,
    clear_screen,
    get_log_dir,
    write_session_header,
)
from features.bitlocker_disable import bitlocker_disable
from features.browser_ai_killer import kill_browser_ai
from features.event_log_clear import event_logs
from features.log_viewer import log_history
from features.low_latency_mode import low_latency_mode
from features.network_reset import net_reset
from features.ssd_trim import ssd_trim
from features.system_cleanup import cleanup
from features.system_repair import sys_repair
from features.winget_upgrade import app_update
from features.winsxs_cleanup import component_store_cleanup


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


def main_menu(logger: Logger, log_dir: Path) -> None:
    while True:
        clear_screen()
        print("===============================================")
        print("           LDL Windows ToolBox")
        print("===============================================")
        print(" ── System Cleanup ──")
        print("[1] Advanced System Cleanup")
        print("[2] Windows Component Store Cleanup (WinSxS)")
        print("[3] Clear Event Viewer Logs")
        print(" ── System Repair & Update ──")
        print("[4] System Integrity Repair (SFC + DISM)")
        print("[5] Update All Installed Apps (Winget)")
        print(" ── Network ──")
        print("[6] Complete Network Reset")
        print(" ── Performance ──")
        print("[7] Manual SSD TRIM")
        print("[8] Low Latency Mode (ViVeTool)")
        print(" ── Security & Privacy ──")
        print("[9] Disable BitLocker (Plan)")
        print("[10] Kill Browser AI")
        print(" ── Tools ──")
        print("[11] View Log History")
        print("───────────────────────────────────────────────")
        print("[12] Exit")
        print("===============================================")
        print(f"Log: {logger.logfile}")
        print("===============================================")
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Menu selection: {choice}")

        if choice == "1":
            cleanup(logger)
        elif choice == "2":
            component_store_cleanup(logger)
        elif choice == "3":
            event_logs(logger)
        elif choice == "4":
            sys_repair(logger)
        elif choice == "5":
            app_update(logger)
        elif choice == "6":
            net_reset(logger)
        elif choice == "7":
            ssd_trim(logger)
        elif choice == "8":
            low_latency_mode(logger)
        elif choice == "9":
            bitlocker_disable(logger)
        elif choice == "10":
            kill_browser_ai(logger)
        elif choice == "11":
            log_history(logger, log_dir)
        elif choice == "12":
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
    logger = Logger(logfile)
    write_session_header(logger, logfile, script_file, script_dir)
    try:
        main_menu(logger, log_dir)
    except KeyboardInterrupt:
        logger.log("INFO", "User cancelled the session with Ctrl+C.")


if __name__ == "__main__":
    main()
