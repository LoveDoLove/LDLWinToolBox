from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    prompt_yes_no,
    run_and_log,
)


def sys_repair(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("        SYSTEM INTEGRITY REPAIR (SFC + DISM)")
    print(MENU_LOGO)
    print("WARNING: This process can take 15-45 minutes.")
    print("-> It CAN be safely interrupted by closing the window.")
    print("-> However, it is recommended to let it finish.")
    print(MENU_LOGO)
    logger.section("System Integrity Repair")
    if not prompt_yes_no(
        logger, "Do you want to proceed? (Y/N): ", "System Integrity Repair"
    ):
        return
    for cmd, label in (
        (["sfc", "/scannow"], "System File Checker"),
        (
            ["dism", "/Online", "/Cleanup-Image", "/RestoreHealth"],
            "DISM RestoreHealth",
        ),
    ):
        if not command_exists(cmd[0]):
            logger.log(
                "ERROR",
                f"{cmd[0]} is required for {label}, but it was not found.",
            )
            input("Press Enter to continue...")
            return
        logger.log("INFO", f"Running {label}...")
        run_and_log(logger, cmd, " ".join(cmd), capture_output=True)
    logger.log("INFO", "SYSTEM INTEGRITY REPAIR COMPLETE")
    input("Press Enter to continue...")
