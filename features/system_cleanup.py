from __future__ import annotations

import os
import shutil
from pathlib import Path

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    create_restore_point,
    prompt_yes_no,
    run_and_log,
    run_command,
)


def drive_free_mb() -> int:
    ps = (
        f"[math]::Round((Get-CimInstance Win32_LogicalDisk"
        f" -Filter \"DeviceID='{os.environ.get('SYSTEMDRIVE', 'C:')}'\").FreeSpace / 1MB)"
    )
    result = run_command(["powershell", "-Command", ps], capture=True)
    text = (result.stdout or "").strip()
    try:
        return int(float(text))
    except ValueError:
        return 0


def _is_excluded(target: Path) -> bool:
    try:
        from features.cleanup_config import is_excluded
        return is_excluded(target)
    except Exception:
        return False


def _clean_dir(target: Path, logger: Logger) -> None:
    if not target.exists():
        logger.log_only("INFO", f"Skipping (not found): {target}")
        return
    if _is_excluded(target):
        logger.log("INFO", f"- Skipping (excluded): {target}")
        return
    logger.log("INFO", f"- Cleaning {target}")
    for child in target.iterdir():
        if _is_excluded(child):
            continue
        try:
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=False)
            else:
                child.unlink(missing_ok=True)
        except OSError as exc:
            logger.log_only("WARN", f"Failed to remove {child}: {exc}")


def _rebuild_dir(target: Path, logger: Logger) -> None:
    if _is_excluded(target):
        return
    logger.log("INFO", f"- Rebuilding {target}")
    target.mkdir(parents=True, exist_ok=True)


def _stop_services(logger: Logger) -> None:
    logger.log("INFO", "[1/4] Stopping background services...")
    for cmd in (["net", "stop", "wuauserv"], ["net", "stop", "bits"]):
        logger.log("INFO", f"- Stopping {cmd[-1]}...")
        run_and_log(logger, cmd, " ".join(cmd), capture_output=True)


def _start_services(logger: Logger) -> None:
    logger.log("INFO", "[4/4] Finalizing optimizations...")
    for cmd in (["net", "start", "wuauserv"], ["net", "start", "bits"]):
        logger.log("INFO", f"- Starting {cmd[-1]}...")
        run_and_log(logger, cmd, " ".join(cmd), capture_output=True)


def _get_targets() -> dict[str, list[Path]]:
    system_drive = os.environ.get("SYSTEMDRIVE", "C:")
    win_dir = Path(os.environ["WinDir"])

    def env_temp(name: str) -> Path | None:
        val = os.environ.get(name)
        return Path(val) / "Temp" if val else None

    return {
        "WindowsTemp": [win_dir / "Temp"],
        "UserTemp": [
            env_temp("TEMP"),
            env_temp("AppData"),
            env_temp("LocalAppData"),
        ],
        "Prefetch": [win_dir / "Prefetch"],
        "SoftwareDistribution": [win_dir / "SoftwareDistribution" / "Download"],
        "VendorRoots": [Path(f"{system_drive}\\{n}") for n in ("AMD", "NVIDIA", "INTEL")],
    }


def _select_targets(logger: Logger) -> str | None:
    while True:
        clear_screen()
        print(MENU_LOGO)
        print("        ADVANCED SYSTEM CLEANUP")
        print(MENU_LOGO)
        print("Select cleanup mode:")
        print("[1] All (full cleanup)")
        print("[2] Windows Temp only")
        print("[3] User Temp only")
        print("[4] Prefetch only")
        print("[5] SoftwareDistribution Downloads only")
        print("[6] Vendor Driver Roots only")
        print("[0] Cancel")
        print(MENU_LOGO)
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Cleanup target selection: {choice}")
        if choice == "0":
            return None
        if choice in ("1", "2", "3", "4", "5", "6"):
            return choice
        logger.log_only("WARN", f"Invalid target selection: {choice}")


def cleanup(logger: Logger) -> None:
    target_choice = _select_targets(logger)
    if target_choice is None:
        return

    is_all = target_choice == "1"
    targets = _get_targets()

    if is_all:
        selected_names = list(targets.keys())
    else:
        name_map = {"2": "WindowsTemp", "3": "UserTemp", "4": "Prefetch",
                     "5": "SoftwareDistribution", "6": "VendorRoots"}
        selected_names = [name_map[target_choice]]

    clear_screen()
    print(MENU_LOGO)
    print("        ADVANCED SYSTEM CLEANUP TOOL")
    print(MENU_LOGO)
    print(f"All operations are being logged to:\n{logger.logfile}")
    print(MENU_LOGO)
    logger.section("Advanced System Cleanup")
    if prompt_yes_no(
        logger,
        "Create a system restore point before proceeding? (Y/N): ",
        "Restore Point - Advanced System Cleanup",
    ):
        create_restore_point(logger, "Before Advanced System Cleanup")
    if not prompt_yes_no(
        logger,
        "Do you want to proceed? (Y/N): ",
        "Advanced System Cleanup",
    ):
        return

    free_before = drive_free_mb()
    logger.log_only("INFO", f"Free space before cleanup: {free_before} MB")

    if is_all or any(n in selected_names for n in ("WindowsTemp", "UserTemp", "SoftwareDistribution")):
        _stop_services(logger)

    print()
    logger.log("INFO", "[2/4] Deleting temporary and junk files...")

    clean_dirs: list[Path] = []
    for name in selected_names:
        if name == "VendorRoots":
            if is_all:
                if prompt_yes_no(logger, "Remove vendor driver directories (AMD, NVIDIA, INTEL)? (Y/N): ", "Vendor Driver Cleanup"):
                    clean_dirs.extend(targets["VendorRoots"])
            else:
                clean_dirs.extend(targets["VendorRoots"])
        else:
            clean_dirs.extend(d for d in targets[name] if d is not None)

    for d in clean_dirs:
        _clean_dir(d, logger)

    if target_choice == "6":
        _rebuild_clean_dir = False
    else:
        _rebuild_clean_dir = True

    if is_all:
        logger.log("INFO", "- Event Viewer logs are handled by menu option 6 using wevtutil.")

    if is_all or any(n in selected_names for n in ("WindowsTemp", "UserTemp", "Prefetch")):
        print()
        logger.log("INFO", "[3/4] Rebuilding directory structure...")
        for name in selected_names:
            if name != "VendorRoots":
                for d in targets[name]:
                    if d is not None:
                        _rebuild_dir(d, logger)

    if is_all or any(n in selected_names for n in ("WindowsTemp", "UserTemp", "SoftwareDistribution")):
        print()
        _start_services(logger)

    free_after = drive_free_mb()
    saved = max(0, free_after - free_before)
    logger.log_only("INFO", f"Free space after cleanup: {free_after} MB")
    logger.log("INFO", "SYSTEM CLEAN UP COMPLETE")
    logger.log("INFO", f"Total Space Freed: {saved} MB")
    input("Press Enter to continue...")
