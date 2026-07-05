from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, prompt_yes_no, run_command


def _capture_cmd(logger: Logger, cmd: list[str], label: str, lines: list[str]) -> None:
    if not command_exists(cmd[0]):
        lines.append(f"[SKIP] {label}: {cmd[0]} not found")
        return
    result = run_command(cmd, capture=True)
    lines.append(f"=== {label} ===")
    if result.code == 0:
        lines.append(result.stdout.strip())
    else:
        lines.append(f"(exit={result.code})")
    lines.append("")


_SNAPSHOT_DIR: str | None = None


def _get_snapshot_dir(script_dir_str: str | None = None) -> Path:
    global _SNAPSHOT_DIR
    if _SNAPSHOT_DIR is not None:
        return Path(_SNAPSHOT_DIR)
    base = Path(script_dir_str) if script_dir_str else Path.cwd()
    snap_dir = base / "exports" / "network_snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    _SNAPSHOT_DIR = str(snap_dir)
    return snap_dir


def _list_snapshots(script_path_str: str | None = None) -> list[Path]:
    snap_dir = _get_snapshot_dir(script_path_str)
    if not snap_dir.exists():
        return []
    files = sorted(snap_dir.glob("network_snapshot_*.txt"), reverse=True)
    return files


def network_snapshot(logger: Logger, script_dir: Path | None = None) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              NETWORK SNAPSHOT")
    print(MENU_LOGO)
    logger.section("Network Snapshot")

    lines: list[str] = []
    ts = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    lines.append(f"Network Snapshot captured at {ts}")
    lines.append("=" * 60)
    lines.append("")

    _capture_cmd(logger, ["ipconfig", "/all"], "IPCONFIG /ALL", lines)
    _capture_cmd(logger, ["route", "print"], "ROUTE PRINT", lines)
    _capture_cmd(
        logger,
        ["netsh", "interface", "show", "interface"],
        "NETSH INTERFACE SHOW",
        lines,
    )
    _capture_cmd(logger, ["netsh", "wlan", "show", "interfaces"], "WLAN INTERFACES", lines)
    _capture_cmd(logger, ["netstat", "-ano"], "NETSTAT -ANO", lines)

    output = "\n".join(lines)

    print("  Current Network State:")
    print()
    ip_lines = [l for l in lines if "IPv4 Address" in l or "Default Gateway" in l or "DNS Servers" in l]
    for l in ip_lines[:10]:
        print(f"    {l.strip()}")
    print()
    print(f"  Full snapshot saved to log ({len(lines)} lines).")

    logger.write_raw(output)
    logger.log_only("INFO", "Network snapshot written to log file.")

    snap_dir = _get_snapshot_dir()
    snap_file = snap_dir / f"network_snapshot_{datetime.now():%y%m%d%H%M%S}.txt"
    with open(snap_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    print(f"  Snapshot file: {snap_file}")

    logger.log_only("INFO", f"Snapshot saved to {snap_file}")

    existing = _list_snapshots()
    if len(existing) >= 2:
        prev_snap = existing[1]
        if prompt_yes_no(
            logger,
            f"Compare with previous snapshot ({prev_snap.name})? (Y/N): ",
            "Compare Snapshots",
        ):
            logger.log_only("INFO", f"Comparing with {prev_snap.name}")
            prev_text = prev_snap.read_text(encoding="utf-8", errors="replace")
            curr_text = output
            import difflib
            diff = list(difflib.unified_diff(
                prev_text.splitlines(),
                curr_text.splitlines(),
                fromfile=prev_snap.name,
                tofile=snap_file.name,
                lineterm="",
            ))
            if diff:
                print()
                print("  --- Differences from previous snapshot ---")
                for d in diff[:60]:
                    print(f"  {d}")
                if len(diff) > 60:
                    print(f"  ... ({len(diff) - 60} more lines)")
                logger.write_raw("\n".join(diff))
            else:
                print("  No differences detected.")
            logger.log_only("INFO", "Snapshot comparison complete.")

    logger.log_only("INFO", "NETWORK SNAPSHOT COMPLETE")
    input("Press Enter to continue...")
