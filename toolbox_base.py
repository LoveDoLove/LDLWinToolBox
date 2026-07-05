from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MENU_LOGO = "=" * 47
TOOLBOX_VERSION = "1.0.3"


@dataclass(slots=True)
class CommandResult:
    code: int
    stdout: str = ""
    stderr: str = ""


class Logger:
    def __init__(self, logfile: Path) -> None:
        self.logfile = logfile

    def _stamp(self) -> str:
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def write_raw(self, message: str) -> None:
        self.logfile.parent.mkdir(parents=True, exist_ok=True)
        with self.logfile.open("a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write(message)
            if not message.endswith("\n"):
                handle.write("\n")

    def log_only(self, level: str, message: str) -> None:
        self.write_raw(f"[{self._stamp()}] [{level}] {message}")

    def log(self, level: str, message: str) -> None:
        self.log_only(level, message)
        print(message)

    def section(self, title: str) -> None:
        self.log_only("INFO", "-" * 79)
        self.log("INFO", f"== {title} ==")

    def command_start(self, command: str) -> None:
        self.log_only("CMD", f"START {command}")

    def command_result(self, command: str, code: int) -> None:
        if code == 0:
            self.log_only("OK", f"END {command} exit={code}")
        else:
            self.log("WARN", f"END {command} exit={code} - check log details.")


def clear_screen() -> None:
    os.system("cls")


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def run_command(
    command: list[str] | str,
    *,
    shell: bool = False,
    capture: bool = True,
    check: bool = False,
) -> CommandResult:
    completed = subprocess.run(
        command,
        shell=shell,
        text=True,
        capture_output=capture,
        check=False,
    )
    if check and completed.returncode != 0:
        raise subprocess.CalledProcessError(
            completed.returncode, command, completed.stdout, completed.stderr
        )
    return CommandResult(
        completed.returncode, completed.stdout or "", completed.stderr or ""
    )


def run_and_log(
    logger: Logger,
    command: list[str] | str,
    display: str,
    *,
    shell: bool = False,
    capture_output: bool = True,
) -> CommandResult:
    logger.command_start(display)
    result = run_command(command, shell=shell, capture=capture_output)
    if result.stdout:
        logger.write_raw(result.stdout)
    if result.stderr:
        logger.write_raw(result.stderr)
    logger.command_result(display, result.code)
    return result


def prompt_yes_no(logger: Logger, prompt: str, context: str) -> bool:
    answer = input(prompt).strip()
    if answer.upper() == "Y":
        return True
    logger.log_only("INFO", f"{context} cancelled by user.")
    return False


def prompt_keyword(logger: Logger, prompt: str, expected: str, context: str) -> bool:
    answer = input(prompt).strip()
    if answer.upper() == expected.upper():
        return True
    logger.log_only("INFO", f"{context} cancelled by user.")
    return False


def prompt_drive(logger: Logger, prompt: str, context: str) -> str | None:
    options = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    choice = input(prompt).strip().upper()
    if choice == "0":
        logger.log_only("INFO", f"{context} cancelled by user.")
        return None
    if len(choice) != 1 or choice not in options:
        logger.log_only("WARN", f"Invalid {context} selection: {choice}")
        print("Invalid selection.")
        return ""
    return choice


def select_existing_drive(logger: Logger, context: str) -> str | None:
    choice = prompt_drive(
        logger, "Press 0 to return, or drive letter to continue (A-Z): ", context
    )
    if choice is None:
        return None
    if choice == "":
        return ""
    if not Path(f"{choice}:\\").exists():
        logger.log("ERROR", f"Drive {choice}: was not found.")
        return ""
    return choice


def create_restore_point(logger: Logger, description: str) -> bool:
    """Create a system restore point. Returns True on success, False on failure.

    If System Restore is disabled or PowerShell is unavailable, logs a warning
    and returns False without blocking the caller.
    """
    if not command_exists("powershell"):
        logger.log_only(
            "WARN",
            "Cannot create restore point: PowerShell is not available.",
        )
        return False
    ps = (
        "Checkpoint-Computer -Description 'LDLWinToolBox - "
        + description.replace("'", "''")
        + "' -RestorePointType MODIFY_SETTINGS"
    )
    logger.log_only("INFO", f"Creating system restore point: {description} ...")
    result = run_command(["powershell", "-NoProfile", "-Command", ps], capture=True)
    rc = result.code
    if rc == 0:
        logger.log_only("OK", f"Restore point created: {description}")
        print(">>> System restore point created successfully.")
        return True
    stderr = result.stderr.strip()
    logger.log_only("WARN", f"Restore point failed (exit={rc}): {stderr or 'unknown error'}")
    if "0x80070422" in stderr:
        print(">>> System Restore may be disabled. Enable it in System Properties to use this feature.")
    else:
        print(f">>> Restore point creation failed (exit={rc}). Continuing anyway.")
    return False


def write_session_header(
    logger: Logger, logfile: Path, script_file: Path, script_dir: Path
) -> None:
    now = datetime.now()
    header = [
        "=" * 79,
        "LDL Windows ToolBox Run Log",
        "=" * 79,
        f"Session ID : {now.strftime('%y%m%d%H%M%S')}",
        f"Started    : {now.strftime('%m/%d/%Y %H:%M:%S')}",
        f"Script     : {script_file}",
        f"Script Dir : {script_dir}",
        f"Work Dir   : {Path.cwd()}",
        f"User       : {os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}",
        f"Computer   : {os.environ.get('COMPUTERNAME', '')}",
        f"OS         : {platform.system()}",
        f"SystemRoot : {os.environ.get('SystemRoot', '')}",
        f"Temp       : {tempfile.gettempdir()}",
        f"Log File   : {logfile}",
        "=" * 79,
        "",
    ]
    logger.logfile.parent.mkdir(parents=True, exist_ok=True)
    logger.logfile.write_text("\n".join(header), encoding="utf-8", newline="\n")
    logger.log_only("INFO", "Logging initialized.")


def get_log_dir(script_dir: Path) -> Path:
    log_dir = script_dir / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    except OSError:
        print("Failed to create logs directory. Using script directory for logs.")
        return script_dir
