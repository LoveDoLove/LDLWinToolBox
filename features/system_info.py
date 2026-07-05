from __future__ import annotations

import ctypes
import os
import platform
import shutil
import subprocess
import winreg
from datetime import datetime

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, run_command


class _MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


def _fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def _fmt_uptime(ms: int) -> str:
    days = ms // 86400000
    rem = ms % 86400000
    hours = rem // 3600000
    rem = rem % 3600000
    minutes = rem // 60000
    seconds = rem % 60000 // 1000
    if days:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    return f"{minutes}m {seconds}s"


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


def system_info(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              SYSTEM INFORMATION")
    print(MENU_LOGO)
    logger.section("System Information")

    kernel32 = ctypes.windll.kernel32

    os_edition = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
        "ProductName",
    ) or platform.system()
    os_build = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
        "CurrentBuild",
    ) or platform.version()
    os_display = f"{os_edition} (Build {os_build})"

    cpu_name = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        "ProcessorNameString",
    ) or platform.processor()
    cpu_cores = os.cpu_count() or 0
    cpu_display = f"{cpu_name} ({cpu_cores} logical cores)"

    memory_status = _MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(_MEMORYSTATUSEX)
    kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
    total_ram = memory_status.ullTotalPhys
    avail_ram = memory_status.ullAvailPhys
    used_ram = total_ram - avail_ram
    ram_pct = memory_status.dwMemoryLoad
    ram_display = f"{_fmt_bytes(used_ram)} / {_fmt_bytes(total_ram)} ({ram_pct}% used)"

    sys_drive = os.environ.get("SystemDrive", "C:")
    du = shutil.disk_usage(f"{sys_drive}\\")
    disk_total = du.total
    disk_free = du.free
    disk_used = du.total - du.free
    disk_pct = du.used * 100 // du.total
    disk_display = f"{_fmt_bytes(disk_used)} / {_fmt_bytes(disk_total)} ({disk_pct}% used), {_fmt_bytes(disk_free)} free"

    uptime_ms = kernel32.GetTickCount64()
    uptime_display = _fmt_uptime(uptime_ms)

    computer = os.environ.get("COMPUTERNAME", "N/A")
    user = f"{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}"
    boot_time = _reg_str(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Power",
        "LastBootTime",
    )
    boot_display = boot_time if boot_time else "N/A"

    print(f"  Computer Name : {computer}")
    print(f"  User          : {user}")
    print(f"  OS            : {os_display}")
    print(f"  CPU           : {cpu_display}")
    print(f"  Memory        : {ram_display}")
    print(f"  System Drive  : {sys_drive}")
    print(f"  Disk          : {disk_display}")
    print(f"  Uptime        : {uptime_display}")
    print()

    for line in (
        f"Computer : {computer}",
        f"User     : {user}",
        f"OS       : {os_display}",
        f"CPU      : {cpu_display}",
        f"Memory   : {ram_display}",
        f"Disk ({sys_drive}): {disk_display}",
        f"Uptime   : {uptime_display}",
        f"LastBoot : {boot_display}",
    ):
        logger.log_only("INFO", line)

    input("Press Enter to continue...")
