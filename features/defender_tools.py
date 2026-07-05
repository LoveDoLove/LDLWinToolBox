from __future__ import annotations

import subprocess

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, prompt_yes_no, run_command


def _ps_get(cmdlet: str) -> str:
    if not command_exists("powershell"):
        return "PowerShell not available"
    result = run_command(
        ["powershell", "-NoProfile", "-Command", cmdlet],
        capture=True,
    )
    if result.code != 0:
        return ""
    return result.stdout.strip()


def _show_defender_status(logger: Logger) -> None:
    script = (
        "$s=Get-MpComputerStatus; "
        "Write-Output $s.AntivirusEnabled; "
        "Write-Output $s.AMServiceEnabled; "
        "Write-Output $s.AMProductVersion; "
        "Write-Output $s.AntispywareEnabled; "
        "Write-Output $s.RealTimeProtectionEnabled; "
        "Write-Output $s.NISEnabled; "
        "Write-Output $s.QuickScanAge; "
        "Write-Output $s.FullScanAge; "
        "Write-Output $s.DefinitionAge; "
        "Write-Output $s.DefinitionVersion; "
        "Write-Output $s.LastQuickScanSource; "
        "Write-Output $s.LastFullScanSource"
    )
    raw = _ps_get(script)
    lines = raw.splitlines()
    fields = [
        "Antivirus Enabled",
        "AMService Enabled",
        "AM Product Version",
        "Antispyware Enabled",
        "Real-Time Protection",
        "Network Inspection System",
        "Quick Scan Age (days)",
        "Full Scan Age (days)",
        "Definition Age (days)",
        "Definition Version",
        "Last Quick Scan Source",
        "Last Full Scan Source",
    ]
    print(f"  {'Status Field':<30} {'Value':<20}")
    print(f"  {'-'*30} {'-'*20}")
    for field, val in zip(fields, lines):
        display = val if val else "N/A"
        print(f"  {field:<30} {display:<20}")
    print()

    for field, val in zip(fields, lines):
        logger.log_only("INFO", f"{field}: {val}")

    age_ranges = {
        "Quick Scan Age (days)": (lines[6] if len(lines) > 6 else ""),
        "Full Scan Age (days)": (lines[7] if len(lines) > 7 else ""),
        "Definition Age (days)": (lines[8] if len(lines) > 8 else ""),
    }
    for label, age_str in age_ranges.items():
        try:
            age = int(age_str)
            if age > 7:
                print(f"  >>> {label} is {age} days. A scan is recommended.")
        except (ValueError, TypeError):
            pass


def defender_tools(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("         WINDOWS DEFENDER STATUS & SCAN")
    print(MENU_LOGO)
    logger.section("Defender Status")

    if not command_exists("powershell"):
        logger.log("ERROR", "PowerShell is required for Defender status.")
        input("Press Enter to continue...")
        return

    _show_defender_status(logger)

    if command_exists("MpCmdRun.exe"):
        logger.section("Signature Update via MpCmdRun")
        print("Checking for signature updates...")
        result = run_command(
            [
                "MpCmdRun.exe",
                "-SignatureUpdate",
            ],
            capture=True,
        )
        if result.code == 0:
            print("Signatures are up to date.")
        else:
            print(f"Signature update returned exit code {result.code}.")
        logger.log_only("INFO", f"MpCmdRun -SignatureUpdate exit={result.code}")

    logger.section("Quick Scan")
    if prompt_yes_no(logger, "Run a Windows Defender Quick Scan? (Y/N): ", "Quick Scan"):
        script = "Start-MpQuickScan"
        print("Running Quick Scan (this may take several minutes)...")
        logger.log_only("CMD", "START-MPQUICKSCAN")
        result = run_command(
            ["powershell", "-NoProfile", "-Command", script],
            capture=True,
        )
        rc = result.code
        logger.command_result("Start-MpQuickScan", rc)
        if rc == 0:
            print("Quick Scan completed successfully.")
        else:
            print(f"Quick Scan returned exit code {rc}.")

    logger.log_only("INFO", "DEFENDER STATUS CHECK COMPLETE")
    input("Press Enter to continue...")
