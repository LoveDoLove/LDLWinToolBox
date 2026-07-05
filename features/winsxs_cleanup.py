from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    prompt_yes_no,
    run_and_log,
)


def component_store_cleanup(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("      WINDOWS COMPONENT STORE CLEANUP (WinSxS)")
    print(MENU_LOGO)
    print("WARNING: This deeply cleans old Windows Update files.")
    print("-> It can take 10-30 minutes and may appear stuck.")
    print("-> DO NOT interrupt this process (can corrupt updates).")
    print(MENU_LOGO)
    logger.section("Windows Component Store Cleanup")
    if not prompt_yes_no(
        logger,
        "Do you want to proceed? (Y/N): ",
        "Windows Component Store Cleanup",
    ):
        return
    if not command_exists("dism"):
        logger.log(
            "ERROR",
            "dism is required for DISM component cleanup, but it was not found.",
        )
        input("Press Enter to continue...")
        return
    logger.log("INFO", "Cleaning Windows Component Store...")
    run_and_log(
        logger,
        ["dism", "/Online", "/Cleanup-Image", "/StartComponentCleanup"],
        "DISM.exe /Online /Cleanup-Image /StartComponentCleanup",
    )
    logger.log("INFO", "WINSXS CLEANUP COMPLETE")
    input("Press Enter to continue...")
