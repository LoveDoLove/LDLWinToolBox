from __future__ import annotations

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    command_exists,
    create_restore_point,
    prompt_keyword,
    prompt_yes_no,
    run_and_log,
    select_existing_drive,
)


def bitlocker_disable(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("          DISABLE BITLOCKER (PLAN)")
    print(MENU_LOGO)
    print("WARNING: This starts BitLocker decryption for the")
    print("selected drive and turns BitLocker off.")
    print("-> Decryption can take a long time.")
    print("-> Keep the PC powered on until Windows finishes.")
    print("-> Do this only when protection is no longer needed.")
    print(MENU_LOGO)
    logger.section("Disable BitLocker")
    if not command_exists("manage-bde"):
        logger.log(
            "ERROR",
            "manage-bde.exe is required for BitLocker management, but it was not found.",
        )
        input("Press Enter to continue...")
        return
    print("Current BitLocker status:")
    logger.log_only("INFO", "Current BitLocker status:")
    status_result = run_and_log(
        logger, ["manage-bde", "-status"], "manage-bde -status"
    )
    if status_result.stdout:
        print(
            status_result.stdout,
            end="" if status_result.stdout.endswith("\n") else "\n",
        )
    if status_result.stderr:
        print(
            status_result.stderr,
            end="" if status_result.stderr.endswith("\n") else "\n",
        )
    print()
    drive = select_existing_drive(logger, "Disable BitLocker")
    if drive is None:
        return
    if drive == "":
        logger.log(
            "ERROR", "No valid drive was selected for Disable BitLocker."
        )
        input("Press Enter to continue...")
        return
    logger.log_only("INFO", f"Selected BitLocker drive: {drive}:")
    print("\nSelected drive status:")
    logger.log_only(
        "INFO", f"Selected BitLocker drive status for {drive}:"
    )
    status_result = run_and_log(
        logger,
        ["manage-bde", "-status", f"{drive}:"],
        f"manage-bde -status {drive}:",
    )
    if status_result.stdout:
        print(
            status_result.stdout,
            end="" if status_result.stdout.endswith("\n") else "\n",
        )
    if status_result.stderr:
        print(
            status_result.stderr,
            end="" if status_result.stderr.endswith("\n") else "\n",
        )
    print()
    if prompt_yes_no(
        logger,
        "Create a system restore point before proceeding? (Y/N): ",
        "Restore Point - Disable BitLocker",
    ):
        create_restore_point(logger, "Before Disabling BitLocker")
    if not prompt_keyword(
        logger,
        f"Type DISABLE to start decryption for {drive}: ",
        "DISABLE",
        "Disable BitLocker",
    ):
        return
    logger.log("INFO", f"Starting BitLocker decryption on {drive}: ...")
    result = run_and_log(
        logger,
        ["manage-bde", "-off", f"{drive}:"],
        f"manage-bde -off {drive}:",
    )
    if result.code != 0:
        logger.log("ERROR", "BITLOCKER DISABLE FAILED. Check log.")
    else:
        logger.log(
            "INFO",
            "BITLOCKER DECRYPTION STARTED. Check Windows BitLocker status for progress.",
        )
    print("\nUpdated status:")
    logger.log_only("INFO", f"Updated BitLocker status for {drive}:")
    status_result = run_and_log(
        logger,
        ["manage-bde", "-status", f"{drive}:"],
        f"manage-bde -status {drive}:",
    )
    if status_result.stdout:
        print(
            status_result.stdout,
            end="" if status_result.stdout.endswith("\n") else "\n",
        )
    if status_result.stderr:
        print(
            status_result.stderr,
            end="" if status_result.stderr.endswith("\n") else "\n",
        )
    input("Press Enter to continue...")
