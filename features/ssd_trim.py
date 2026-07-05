from __future__ import annotations

import tempfile
from pathlib import Path

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    create_restore_point,
    prompt_yes_no,
    run_command,
    select_existing_drive,
)


def get_volume_table() -> str:
    ps = (
        "Get-Volume | Where-Object { $_.DriveLetter -ne $null } "
        "| Select-Object @{Name='Drive';Expression={$_.DriveLetter + ':'}}, "
        "FileSystemLabel, @{Name='Size(GB)';Expression={[math]::round($_.Size / 1GB, 2)}} "
        "| Format-Table -AutoSize"
    )
    result = run_command(["powershell", "-NoProfile", "-Command", ps], capture=True)
    return (result.stdout or "") + (result.stderr or "")


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
        logger.log(
            "ERROR",
            "powershell.exe is required for Volume enumeration, but it was not found.",
        )
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
    if prompt_yes_no(
        logger,
        "Create a system restore point before proceeding? (Y/N): ",
        "Restore Point - Manual SSD TRIM",
    ):
        create_restore_point(logger, "Before SSD TRIM")
    if not prompt_yes_no(
        logger,
        f"Run SSD TRIM on drive {drive}:? (Y/N): ",
        "Manual SSD TRIM",
    ):
        return
    print(f"\nOptimizing Drive {drive}: ...")
    logger.write_raw(f"Optimizing Drive {drive}: ...")
    print("".join(["-" for _ in range(47)]))
    if not command_exists("defrag"):
        logger.log(
            "ERROR",
            "defrag.exe is required for SSD TRIM, but it was not found.",
        )
        input("Press Enter to continue...")
        return
    out_file = Path(tempfile.gettempdir()) / "defrag_out.txt"
    result = run_command(["defrag", f"{drive}:", "/L", "/V"], capture=True)
    out_file.write_text(
        (result.stdout or "") + (result.stderr or ""),
        encoding="utf-8",
        errors="replace",
    )
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
