from __future__ import annotations

import os
import shutil
from pathlib import Path

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
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

    logger.log(
        "INFO",
        "- Event Viewer logs are handled by menu option 6 using wevtutil.",
    )
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
