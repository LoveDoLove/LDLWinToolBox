from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    prompt_yes_no,
    run_and_log,
)


def net_reset(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("            COMPLETE NETWORK RESET")
    print(MENU_LOGO)
    print("This will reset your network adapters to factory defaults.")
    print("-> A system restart will be required afterward.")
    print(MENU_LOGO)
    logger.section("Complete Network Reset")
    if not prompt_yes_no(
        logger, "Do you want to proceed? (Y/N): ", "Complete Network Reset"
    ):
        return
    for cmd, label in (
        (["netsh", "winsock", "reset"], "netsh winsock reset"),
        (["netsh", "int", "ip", "reset"], "netsh int ip reset"),
        (["ipconfig", "/flushdns"], "ipconfig /flushdns"),
    ):
        if not command_exists(cmd[0]):
            logger.log(
                "ERROR",
                f"{cmd[0]} is required for {label}, but it was not found.",
            )
            input("Press Enter to continue...")
            return
        logger.log(
            "INFO",
            label.replace("netsh ", "Resetting ").replace("ipconfig ", "Flushing "),
        )
        run_and_log(logger, cmd, label)
    logger.log(
        "INFO", "NETWORK RESET COMPLETE. Please RESTART your computer."
    )
    input("Press Enter to continue...")
