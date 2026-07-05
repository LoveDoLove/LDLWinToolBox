from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from toolbox_base import MENU_LOGO, Logger, clear_screen


def list_log_history(log_dir: Path, logger: Logger) -> list[Path]:
    entries = sorted(
        log_dir.glob("LDLWinToolBox_*.log"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return entries[:9]


def paginate_log_file(path: Path) -> None:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"Unable to open log file: {exc}")
        input("Press Enter to continue...")
        return

    if not lines:
        print("(Log file is empty.)")
        input("Press Enter to continue...")
        return

    terminal_size = shutil.get_terminal_size(fallback=(80, 24))
    page_size = max(10, terminal_size.lines - 6)
    page = 0

    while True:
        start = page * page_size
        if start >= len(lines):
            page = max(0, (len(lines) - 1) // page_size)
            start = page * page_size
        end = min(start + page_size, len(lines))

        clear_screen()
        print(MENU_LOGO)
        print(f"Viewing Log: {path.name}")
        print(MENU_LOGO)
        print(f"Path: {path}")
        print(MENU_LOGO)
        print(f"Lines {start + 1}-{end} of {len(lines)}")
        print(MENU_LOGO)
        for line in lines[start:end]:
            print(line)
        print(MENU_LOGO)

        if end >= len(lines):
            input("End of log. Press Enter to return to the menu...")
            return

        choice = input("Press Enter for more, [B]ack, or [Q]uit: ").strip().upper()
        if choice == "Q":
            return
        if choice == "B":
            page = max(0, page - 1)
            continue
        page += 1


def log_history(logger: Logger, log_dir: Path) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              VIEW LOG HISTORY")
    print(MENU_LOGO)
    print(f"Log directory:\n{log_dir}")
    print(MENU_LOGO)
    logger.section("View Log History")
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
    paginate_log_file(selected)
    logger.log("INFO", "View Log History returned to menu.")
