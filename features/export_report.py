from __future__ import annotations

import os
import re
import zipfile
from datetime import datetime
from pathlib import Path

from toolbox_base import MENU_LOGO, Logger, clear_screen, prompt_yes_no


def _gather_logs(log_dir: Path) -> list[Path]:
    if not log_dir.exists():
        return []
    return sorted(log_dir.glob("LDLWinToolBox_*.log"), key=os.path.getmtime, reverse=True)


def _generate_report(log_dir: Path, log_text: str) -> str:
    now = datetime.now()
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("LDL Windows ToolBox - Session Report")
    lines.append(f"Generated: {now.strftime('%m/%d/%Y %H:%M:%S')}")
    lines.append("=" * 60)
    lines.append("")

    session_match = re.search(r"Session ID\s*:\s*(\d+)", log_text)
    if session_match:
        lines.append(f"Session      : {session_match.group(1)}")

    start_match = re.search(r"Started\s*:\s*(.+)", log_text)
    if start_match:
        lines.append(f"Started      : {start_match.group(1).strip()}")

    user_match = re.search(r"User\s*:\s*(.+)", log_text)
    if user_match:
        lines.append(f"User         : {user_match.group(1).strip()}")

    comp_match = re.search(r"Computer\s*:\s*(.+)", log_text)
    if comp_match:
        lines.append(f"Computer     : {comp_match.group(1).strip()}")

    os_match = re.search(r"OS\s*:\s*(.+)", log_text)
    if os_match:
        lines.append(f"OS           : {os_match.group(1).strip()}")

    log_match = re.search(r"Log File\s*:\s*(.+)", log_text)
    if log_match:
        lines.append(f"Log File     : {log_match.group(1).strip()}")

    lines.append("")

    sections = re.findall(r"==\s*(.+?)\s*==", log_text)
    if sections:
        lines.append("Features Run:")
        for s in sections:
            lines.append(f"  - {s}")
        lines.append("")

    cmd_lines = re.findall(r"\[CMD\]\s+START\s+(.+)", log_text)
    if cmd_lines:
        lines.append("Commands Executed:")
        for cmd in cmd_lines:
            lines.append(f"  - {cmd}")
        lines.append("")

    warn_lines = re.findall(r"\[(WARN|ERROR)\]\s+(.+)", log_text)
    if warn_lines:
        lines.append("Warnings / Errors:")
        for level, msg in warn_lines:
            lines.append(f"  [{level}] {msg}")
        lines.append("")

    menu_lines = re.findall(r"\[INFO\] Menu selection:\s*(.+)", log_text)
    if menu_lines:
        lines.append("Menu Selections:")
        for m in menu_lines:
            lines.append(f"  - {m}")
        lines.append("")

    ok_lines = re.findall(r"\[OK\]\s+END\s+(.+?)\s+exit=0", log_text)
    fail_lines = re.findall(r"\[WARN\]\s+END\s+(.+?)\s+exit=(\d+)", log_text)
    if ok_lines or fail_lines:
        lines.append("Command Results:")
        for cmd in ok_lines:
            lines.append(f"  [OK] {cmd}")
        for cmd, code in fail_lines:
            lines.append(f"  [FAIL]({code}) {cmd}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("Report End")
    lines.append("=" * 60)
    return "\n".join(lines)


def export_report(logger: Logger, log_dir: Path) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("           EXPORT LOGS & REPORT")
    print(MENU_LOGO)
    logger.section("Export Logs & Report")

    export_dir = Path(log_dir.parent) / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    logs = _gather_logs(log_dir)
    if not logs:
        logger.log("INFO", "No log files found to export.")
        input("Press Enter to continue...")
        return

    print(f"  Found {len(logs)} log file(s).")

    current_log = str(logger.logfile)

    timestamp = datetime.now().strftime("%y%m%d%H%M%S")

    report_text = ""
    for log_file in logs:
        if str(log_file) == current_log:
            try:
                log_text = log_file.read_text(encoding="utf-8", errors="replace")
                report_text = _generate_report(log_dir, log_text)
            except OSError:
                pass
            break

    if report_text:
        report_name = f"report_{timestamp}.txt"
        report_path = export_dir / report_name
        try:
            report_path.write_text(report_text, encoding="utf-8", newline="\n")
            print(f"  Report file: {report_path}")
            logger.log_only("INFO", f"Report saved to {report_path}")
        except OSError as e:
            logger.log("ERROR", f"Failed to write report: {e}")

    if prompt_yes_no(
        logger,
        f"Archive all {len(logs)} log(s) to a ZIP file? (Y/N): ",
        "Log Archive",
    ):
        zip_name = f"LDLWinToolBox_logs_{timestamp}.zip"
        zip_path = export_dir / zip_name
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for log_file in logs:
                    arcname = log_file.name
                    zf.write(log_file, arcname)
                if report_text:
                    zf.writestr(report_name, report_text)
            print(f"  Archive created: {zip_path} ({_fmt_zip_size(zip_path)})")
            logger.log_only("INFO", f"Log archive saved to {zip_path}")
        except OSError as e:
            logger.log("ERROR", f"Failed to create archive: {e}")
    else:
        logger.log_only("INFO", "Log archive skipped by user.")

    logger.log_only("INFO", "EXPORT LOGS & REPORT COMPLETE")
    input("Press Enter to continue...")


def _fmt_zip_size(zip_path: Path) -> str:
    size = zip_path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
