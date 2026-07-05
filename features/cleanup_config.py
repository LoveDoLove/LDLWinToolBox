from __future__ import annotations

import json
import os
from pathlib import Path

from toolbox_base import MENU_LOGO, Logger, clear_screen


_CONFIG_DIR: str | None = None


def _get_config_dir() -> Path:
    global _CONFIG_DIR
    if _CONFIG_DIR is not None:
        return Path(_CONFIG_DIR)
    p = Path.cwd() / "config"
    p.mkdir(parents=True, exist_ok=True)
    _CONFIG_DIR = str(p)
    return p


_EXCLUSIONS_FILE: str | None = None


def _get_exclusions_path() -> Path:
    global _EXCLUSIONS_FILE
    if _EXCLUSIONS_FILE is not None:
        return Path(_EXCLUSIONS_FILE)
    p = _get_config_dir() / "exclusions.json"
    _EXCLUSIONS_FILE = str(p)
    return p


def _load_exclusions() -> list[str]:
    path = _get_exclusions_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def _save_exclusions(exclusions: list[str]) -> bool:
    path = _get_exclusions_path()
    try:
        path.write_text(
            json.dumps(exclusions, indent=2, ensure_ascii=False),
            encoding="utf-8",
            newline="\n",
        )
        return True
    except OSError:
        return False


def _path_resolve(entry: str) -> str:
    expanded = os.path.expandvars(entry)
    return str(Path(expanded).resolve()) if expanded else entry


def _matches_exclusion(target: Path) -> bool:
    resolved = str(target.resolve()).lower()
    for entry in _load_exclusions():
        excl = os.path.expandvars(entry)
        excl_res = str(Path(excl).resolve()).lower() if excl else entry.lower()
        if resolved.startswith(excl_res):
            return True
    return False


def get_exclusions() -> list[str]:
    return list(_load_exclusions())


def is_excluded(target: Path) -> bool:
    return _matches_exclusion(target)


def cleanup_config(logger: Logger) -> None:
    while True:
        exclusions = _load_exclusions()
        total = len(exclusions)
        clear_screen()
        print(MENU_LOGO)
        print("         CLEANUP EXCLUSION LIST")
        print(MENU_LOGO)
        if exclusions:
            print(f"  Exclusions ({total}):")
            for i, entry in enumerate(exclusions, 1):
                print(f"    {i}. {entry}")
        else:
            print("  No exclusions configured.")
        print(MENU_LOGO)
        print("[1] Add Exclusion Path")
        print("[2] Remove Exclusion by Number")
        print("[3] Clear All Exclusions")
        print("[0] Return to Main Menu")
        print(MENU_LOGO)
        print("  Tip: Use %WinDir%, %TEMP%, %SystemDrive% variables.")
        print(MENU_LOGO)
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Cleanup Config sub-menu selection: {choice}")

        if choice == "1":
            logger.section("Add Exclusion")
            path = input("Enter path to exclude: ").strip()
            if not path:
                print("Empty path ignored.")
                input("Press Enter to continue...")
                continue
            resolved = _path_resolve(path)
            if any(e.lower() == path.lower() or _path_resolve(e).lower() == resolved.lower() for e in exclusions):
                print(f"'{path}' is already in the exclusion list.")
                input("Press Enter to continue...")
                continue
            exclusions.append(path)
            if _save_exclusions(exclusions):
                logger.log("INFO", f"Exclusion added: {path} (resolved: {resolved})")
                print(f"Added: {path}")
            else:
                logger.log("ERROR", "Failed to write exclusions file.")
            input("Press Enter to continue...")

        elif choice == "2":
            if not exclusions:
                print("No exclusions to remove.")
                input("Press Enter to continue...")
                continue
            logger.section("Remove Exclusion")
            try:
                idx_str = input(f"Enter number to remove (1-{total}): ").strip()
                idx = int(idx_str) - 1
                if idx < 0 or idx >= total:
                    print(f"Invalid number. Enter 1-{total}.")
                    input("Press Enter to continue...")
                    continue
                removed = exclusions.pop(idx)
                if _save_exclusions(exclusions):
                    logger.log("INFO", f"Exclusion removed: {removed}")
                    print(f"Removed: {removed}")
                else:
                    logger.log("ERROR", "Failed to write exclusions file.")
            except ValueError:
                print("Invalid input.")
            input("Press Enter to continue...")

        elif choice == "3":
            if not exclusions:
                print("No exclusions to clear.")
                input("Press Enter to continue...")
                continue
            logger.section("Clear All Exclusions")
            from toolbox_base import prompt_yes_no
            if prompt_yes_no(logger, "Clear all exclusions? (Y/N): ", "Clear Exclusions"):
                if _save_exclusions([]):
                    logger.log("INFO", "All exclusions cleared.")
                    print("All exclusions removed.")
                else:
                    logger.log("ERROR", "Failed to write exclusions file.")
            input("Press Enter to continue...")

        elif choice == "0":
            logger.log("INFO", "Cleanup Config returned to main menu.")
            return

        else:
            logger.log("WARN", f"Invalid Cleanup Config selection: {choice}")
