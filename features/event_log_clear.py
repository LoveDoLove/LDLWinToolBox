from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    create_restore_point,
    prompt_yes_no,
    run_and_log,
    run_command,
)


def event_logs(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("          CLEAR EVENT VIEWER LOGS")
    print(MENU_LOGO)
    print(f"All operations are being logged to:\n{logger.logfile}")
    print(MENU_LOGO)
    logger.section("Clear Event Viewer Logs")
    if not command_exists("wevtutil"):
        logger.log(
            "ERROR",
            "wevtutil.exe is required for Event Viewer logs, but it was not found.",
        )
        input("Press Enter to continue...")
        return
    if prompt_yes_no(
        logger,
        "Create a system restore point before proceeding? (Y/N): ",
        "Restore Point - Clear Event Viewer Logs",
    ):
        create_restore_point(logger, "Before Clearing Event Viewer Logs")
    if not prompt_yes_no(
        logger,
        "Clear all Event Viewer logs? (Y/N): ",
        "Clear Event Viewer Logs",
    ):
        return
    result = run_command(["wevtutil", "el"], capture=True)
    logs = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    for entry in logs:
        logger.log("INFO", f"- Clearing log: {entry}")
        run_and_log(logger, ["wevtutil", "cl", entry], f"wevtutil.exe cl {entry}")
    logger.log("INFO", "EVENT LOGS CLEARED")
    input("Press Enter to continue...")
