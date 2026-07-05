from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    prompt_keyword,
    run_and_log,
)

GIST_URL = "https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1"


def kill_browser_ai(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              KILL BROWSER AI")
    print(MENU_LOGO)
    print("WARNING: This downloads and executes a remote")
    print("PowerShell script from the configured gist URL.")
    print("-> It may close browser or AI-related processes.")
    print("-> Network access is required.")
    print("-> Do not run if you do not trust the source.")
    print(MENU_LOGO)
    print("Source:")
    print(GIST_URL)
    print()
    logger.section("Kill Browser AI")
    logger.log_only("WARN", f"Remote script source: {GIST_URL}")
    if not prompt_keyword(logger, "Type KILL to run Kill Browser AI: ", "KILL", "Kill Browser AI"):
        return
    if not command_exists("powershell"):
        logger.log(
            "ERROR",
            "powershell.exe is required for Kill Browser AI, but it was not found.",
        )
        input("Press Enter to continue...")
        return
    logger.log("INFO", "Running Kill Browser AI...")
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        f"try {{ iwr -useb '{GIST_URL}' | iex; exit 0 }} catch {{ Write-Error $_; exit 1 }}",
    ]
    result = run_and_log(logger, cmd, "PowerShell remote kill_ai.ps1")
    if result.code != 0:
        logger.log("ERROR", "KILL BROWSER AI FAILED. Check log.")
    else:
        logger.log("INFO", "KILL BROWSER AI COMPLETE.")
    input("Press Enter to continue...")
