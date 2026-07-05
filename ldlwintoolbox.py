from __future__ import annotations

import ctypes
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from features.bitlocker_disable import bitlocker_disable
from features.browser_ai_killer import kill_browser_ai
from features.cleanup_config import cleanup_config
from features.defender_tools import defender_tools
from features.disk_health import disk_health
from features.driver_inventory import driver_inventory
from features.event_log_clear import event_logs
from features.export_report import export_report
from features.log_viewer import log_history
from features.low_latency_mode import low_latency_mode
from features.network_reset import net_reset
from features.network_snapshot import network_snapshot
from features.recovery_tools import recovery_tools
from features.self_update import self_update
from features.service_health import service_health
from features.ssd_trim import ssd_trim
from features.system_cleanup import cleanup
from features.system_info import system_info
from features.system_repair import sys_repair
from features.windows_update import windows_update
from features.winget_upgrade import app_update
from features.winsxs_cleanup import component_store_cleanup
from toolbox_base import (
    TOOLBOX_VERSION,
    Color,
    Logger,
    clear_screen,
    cprint,
    get_log_dir,
    prompt_yes_no,
    write_session_header,
)


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


def _print_header(is_admin_user: bool) -> None:
    bold = Color.BOLD
    cyan = Color.CYAN
    yellow = Color.YELLOW
    cprint("─" * 47, Color.DIM)
    cprint("       ⚙  LDL Windows ToolBox", bold, cyan)
    cprint(f"               v{TOOLBOX_VERSION}", Color.DIM)
    if not is_admin_user:
        cprint("          ★ READ-ONLY MODE ★", bold, yellow)
    cprint("─" * 47, Color.DIM)


def _print_section(title: str) -> None:
    cprint(f" ── {title} ──", Color.BOLD, Color.GREEN)


def _print_item(key: str, desc: str) -> None:
    cprint(f" [{key}] {desc}", Color.WHITE)


def main_menu(logger: Logger, log_dir: Path, script_dir: Path, is_admin_user: bool) -> None:
    while True:
        clear_screen()
        _print_header(is_admin_user)
        if is_admin_user:
            _print_section("System Cleanup")
            _print_item("1", "Advanced System Cleanup")
            _print_item("2", "Windows Component Store Cleanup (WinSxS)")
            _print_item("3", "Clear Event Viewer Logs")
            _print_section("System Repair & Update")
            _print_item("4", "System Integrity Repair (SFC + DISM)")
            _print_item("5", "Update All Installed Apps (Winget)")
            _print_section("Network")
            _print_item("6", "Complete Network Reset")
            _print_section("Performance")
            _print_item("7", "Manual SSD TRIM")
            _print_item("8", "Low Latency Mode (ViVeTool)")
            _print_section("Security & Privacy")
            _print_item("9", "Disable BitLocker (Plan)")
            _print_item("10", "Kill Browser AI")
            _print_section("Recovery")
            _print_item("11", "Recovery & Safe Mode Tools")
        else:
            cprint("  (Admin features hidden. Press [R] to restart as admin.)", Color.DIM)
        _print_section("Diagnostics")
        _print_item("12", "System Information")
        _print_item("13", "Windows Update Status")
        _print_item("14", "Defender Status & Quick Scan")
        _print_item("15", "Service Health Check")
        _print_item("16", "Disk Health & SMART Summary")
        _print_item("17", "Driver Inventory")
        _print_item("18", "Network Snapshot")
        _print_item("19", "Export Logs & Report")
        _print_section("Tools")
        _print_item("20", "View Log History")
        _print_item("21", "Check for Updates")
        _print_item("22", "Cleanup Exclusion List")
        cprint(Color.DIM + "───────────────────────────────────────────────" + Color.RESET)
        if not is_admin_user:
            cprint(" [R] Restart as Administrator", Color.YELLOW)
        cprint(" [23] Exit", Color.RED)
        cprint(Color.DIM + "═" * 47 + Color.RESET)
        cprint(f" Log: {logger.logfile}", Color.DIM)
        cprint(Color.DIM + "═" * 47 + Color.RESET)
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Menu selection: {choice}")

        if not is_admin_user and choice.upper() == "R":
            logger.log("INFO", "User requested admin restart.")
            relaunch_as_admin()
            continue

        if not is_admin_user and choice in (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
        ):
            logger.log("WARN", f"Admin feature {choice} blocked in read-only mode.")
            print("This feature requires administrator privileges.")
            input("Press Enter to continue...")
            continue

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
            recovery_tools(logger)
        elif choice == "12":
            system_info(logger)
        elif choice == "13":
            windows_update(logger)
        elif choice == "14":
            defender_tools(logger)
        elif choice == "15":
            service_health(logger)
        elif choice == "16":
            disk_health(logger)
        elif choice == "17":
            driver_inventory(logger)
        elif choice == "18":
            network_snapshot(logger, script_dir)
        elif choice == "19":
            export_report(logger, log_dir)
        elif choice == "20":
            log_history(logger, log_dir)
        elif choice == "21":
            self_update(logger)
        elif choice == "22":
            cleanup_config(logger)
        elif choice == "23":
            if not prompt_yes_no(
                logger,
                "Are you sure you want to exit? (Y/N): ",
                "Exit",
            ):
                continue
            logger.log("INFO", "Exiting LDL Windows ToolBox.")
            return
        else:
            logger.log("WARN", f"Invalid menu selection: {choice}")


def main() -> None:
    script_file = Path(__file__).resolve()
    script_dir = script_file.parent
    os.chdir(script_dir)
    log_dir = get_log_dir(script_dir)
    log_time = datetime.now().strftime("%y%m%d%H%M%S")
    logfile = log_dir / f"LDLWinToolBox_{log_time}.log"
    logger = Logger(logfile)
    write_session_header(logger, logfile, script_file, script_dir)
    admin_user = is_admin()
    if not admin_user:
        logger.log_only("WARN", "Started without admin privileges - read-only mode.")
        print("Running in read-only mode. Admin features (1-11) are hidden.")
        print("Press Enter to continue...")
        input()
    try:
        main_menu(logger, log_dir, script_dir, admin_user)
    except KeyboardInterrupt:
        logger.log("INFO", "User cancelled the session with Ctrl+C.")


if __name__ == "__main__":
    main()
