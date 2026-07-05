from __future__ import annotations

import subprocess
import winreg

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, run_command


def _reg_str(key: int, subkey: str, value: str) -> str | None:
    try:
        with winreg.OpenKey(key, subkey) as k:
            data, _ = winreg.QueryValueEx(k, value)
            return str(data)
    except OSError:
        return None


def _reg_dword(key: int, subkey: str, value: str) -> int | None:
    try:
        with winreg.OpenKey(key, subkey) as k:
            data, _ = winreg.QueryValueEx(k, value)
            return int(data)
    except OSError:
        return None


def _sc_query(service: str) -> str | None:
    if not command_exists("sc"):
        return None
    result = run_command(["sc", "query", service], capture=True)
    if result.code != 0:
        return None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.upper().startswith("STATE"):
            parts = line.split()
            if len(parts) >= 4:
                codes = {
                    1: "STOPPED",
                    2: "START_PENDING",
                    3: "STOP_PENDING",
                    4: "RUNNING",
                    5: "CONTINUE_PENDING",
                    6: "PAUSE_PENDING",
                    7: "PAUSED",
                }
                return codes.get(int(parts[2]), parts[2])
    return None


_AU_STATES = {
    1: "Disabled",
    2: "Not configured",
    3: "Enabled - notify before download",
    4: "Enabled - auto download, notify to install",
    5: "Enabled - auto download and install on schedule",
}


def windows_update(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("            WINDOWS UPDATE STATUS")
    print(MENU_LOGO)
    logger.section("Windows Update Status")

    svc = _sc_query("wuauserv")
    if svc:
        print(f"  Service (wuauserv) : {svc}")
    else:
        print("  Service (wuauserv) : Unable to query")

    au_state = _reg_dword(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update",
        "AUState",
    )
    if au_state is not None:
        label = _AU_STATES.get(au_state, f"Unknown ({au_state})")
        print(f"  Auto Update Config : {label}")
    else:
        print("  Auto Update Config : N/A (registry key not found)")

    last_install = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Install",
        "LastSuccessTime",
    )
    if last_install:
        print(f"  Last Install      : {last_install}")
    else:
        print("  Last Install      : No record found")

    last_search = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Search",
        "LastSuccessTime",
    )
    if last_search:
        print(f"  Last Search       : {last_search}")
    else:
        print("  Last Search       : No record found")

    notify = _reg_dword(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update",
        "IncludeRecommendedUpdates",
    )
    if notify is not None:
        print(f"  Recommended Updates : {'Included' if notify else 'Not included'}")

    detection = _reg_dword(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update",
        "DetectionState",
    )
    if detection is not None:
        print(f"  Detection State   : {detection}")

    deferred = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\WindowsUpdate\UpdatePolicy\Policy",
        "DeferQualityUpdates",
    )
    if deferred:
        print(f"  Quality Updates   : Deferred")
    else:
        print(f"  Quality Updates   : Not deferred")

    if svc == "RUNNING" and last_install:
        from datetime import datetime, timedelta

        try:
            dt = datetime.strptime(last_install, "%Y-%m-%d %H:%M:%S")
            days_ago = (datetime.now() - dt).days
            if days_ago > 30:
                print(f"  >>> Last update was {days_ago} days ago. Consider running [5] Winget upgrade.")
        except ValueError:
            pass

    print()
    for line in (
        f"Service (wuauserv): {svc or 'N/A'}",
        f"AutoUpdate state: {au_state}",
        f"Last install: {last_install or 'N/A'}",
        f"Last search: {last_search or 'N/A'}",
    ):
        logger.log_only("INFO", line)

    logger.section("Check for updates via UsoClient")
    if command_exists("usoclient"):
        print("Running UsoClient ScanInstallWait (this may take a moment)...")
        result = run_command(["usoclient", "StartScan"], capture=True)
        if result.code == 0:
            print("UsoClient completed successfully.")
        else:
            print(f"UsoClient returned exit code {result.code}.")
    else:
        print("UsoClient not found (Windows 10 1809+ required).")

    logger.log_only("INFO", "WINDOWS UPDATE STATUS CHECK COMPLETE")
    input("Press Enter to continue...")
