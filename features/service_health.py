from __future__ import annotations

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, run_command

_CRITICAL_SERVICES = [
    ("wuauserv", "Windows Update"),
    ("BITS", "Background Intelligent Transfer"),
    ("TrustedInstaller", "Windows Modules Installer"),
    ("sppsvc", "Software Protection"),
    ("winmgmt", "WMI"),
    ("Dnscache", "DNS Client"),
    ("Dhcp", "DHCP Client"),
    ("NlaSvc", "Network Location Awareness"),
    ("EventLog", "Windows Event Log"),
    ("Audiosrv", "Windows Audio"),
    ("Themes", "Themes"),
    ("Spooler", "Print Spooler"),
    ("WSearch", "Windows Search"),
    ("MpsSvc", "Windows Defender Firewall"),
    ("BFE", "Base Filtering Engine"),
    ("LanmanWorkstation", "Workstation"),
    ("LanmanServer", "Server"),
    ("WlanSvc", "WLAN AutoConfig"),
    ("RpcSs", "Remote Procedure Call (RPC)"),
    ("DcomLaunch", "DCOM Server Process Launcher"),
]


def _get_services_ps(service_names: list[str]) -> dict[str, str | None]:
    if not command_exists("powershell"):
        return {}
    names = ",".join(f"'{n}'" for n in service_names)
    cmd = (
        f"Get-Service -Name {names} -ErrorAction SilentlyContinue "
        "| ForEach-Object { $_.Name + '|' + $_.Status + '|' + $_.DisplayName }"
    )
    result = run_command(
        ["powershell", "-NoProfile", "-Command", cmd],
        capture=True,
    )
    if result.code != 0:
        return {}
    out: dict[str, str | None] = {}
    for line in result.stdout.splitlines():
        parts = line.strip().split("|", 2)
        if len(parts) >= 2:
            out[parts[0]] = parts[1]
    return out


def _sc_status(name: str) -> str | None:
    if not command_exists("sc"):
        return None
    result = run_command(["sc", "query", name], capture=True)
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


def service_health(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("             SERVICE HEALTH CHECK")
    print(MENU_LOGO)
    logger.section("Service Health Check")

    names = [s[0] for s in _CRITICAL_SERVICES]
    ps_status = _get_services_ps(names)

    print(f"  {'Status':<15} {'Service Name':<20} {'Display Name':<40}")
    print(f"  {'-' * 15} {'-' * 20} {'-' * 40}")

    running = 0
    stopped = 0
    unknown = 0

    for name, display_name in _CRITICAL_SERVICES:
        status = ps_status.get(name) or _sc_status(name) or "UNKNOWN"
        status_upper = status.upper()
        if status_upper in ("RUNNING", "START_PENDING"):
            running += 1
        elif status_upper in ("STOPPED", "STOP_PENDING", "PAUSED", "PAUSE_PENDING"):
            stopped += 1
        else:
            unknown += 1

        status_display = status[:14] if len(status) > 14 else status
        print(f"  {status_display:<15} {name:<20} {display_name:<40}")

    print()
    total = len(_CRITICAL_SERVICES)
    print(f"  Running: {running} / Stopped: {stopped} / Unknown: {unknown} / Total: {total}")
    if stopped:
        print("  >>> Some critical services are stopped. Check manually if issues persist.")
    print()

    logger.log_only(
        "INFO",
        f"Services: {running} running, {stopped} stopped, {unknown} unknown of {total}",
    )

    for name, _ in _CRITICAL_SERVICES:
        status = ps_status.get(name)
        if status:
            logger.log_only("INFO", f"{name}: {status}")

    logger.log_only("INFO", "SERVICE HEALTH CHECK COMPLETE")
    input("Press Enter to continue...")
