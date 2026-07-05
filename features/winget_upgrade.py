from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    create_restore_point,
    prompt_yes_no,
    run_and_log,
)


def app_update(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("         UPDATE INSTALLED APPS (WINGET)")
    print(MENU_LOGO)
    print("WARNING: Silently updates all apps installed via Winget.")
    print("-> May take several minutes.")
    print("-> It CAN be safely interrupted.")
    print(MENU_LOGO)
    logger.section("Update Installed Apps")
    if prompt_yes_no(
        logger,
        "Create a system restore point before proceeding? (Y/N): ",
        "Restore Point - Update Installed Apps",
    ):
        create_restore_point(logger, "Before Winget App Upgrade")
    if not prompt_yes_no(logger, "Do you want to proceed? (Y/N): ", "Update Installed Apps"):
        return
    if not command_exists("winget"):
        logger.log(
            "ERROR",
            "winget is required for Winget update, but it was not found.",
        )
        input("Press Enter to continue...")
        return
    logger.log(
        "INFO",
        "[1/1] Upgrading all installed applications (this may take a while)...",
    )
    run_and_log(
        logger,
        [
            "winget",
            "upgrade",
            "--all",
            "--include-unknown",
            "--accept-package-agreements",
            "--accept-source-agreements",
        ],
        "winget upgrade --all",
    )
    logger.log("INFO", "APP UPDATE COMPLETE")
    input("Press Enter to continue...")
