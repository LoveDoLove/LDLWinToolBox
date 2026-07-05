from __future__ import annotations

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, prompt_yes_no, run_command


def _bcdedit(args: list[str]) -> str:
    if not command_exists("bcdedit"):
        return ""
    result = run_command(["bcdedit"] + args, capture=True)
    return result.stdout.strip() if result.code == 0 else f"(exit={result.code})"


def _reagentc(args: list[str]) -> str:
    if not command_exists("reagentc"):
        return ""
    result = run_command(["reagentc"] + args, capture=True)
    return result.stdout.strip() if result.code == 0 else f"(exit={result.code})"


def _has_safeboot() -> bool:
    output = _bcdedit(["/enum", "{current}"])
    return "safeboot" in output.lower()


def recovery_tools(logger: Logger) -> None:
    while True:
        has_sb = _has_safeboot()
        clear_screen()
        print(MENU_LOGO)
        print("        RECOVERY & SAFE MODE TOOLS")
        print(MENU_LOGO)
        print(f"  Safe Mode active : {'Yes' if has_sb else 'No'}")
        print(MENU_LOGO)
        print("[1] View Boot Configuration")
        print("[2] Boot to Safe Mode (Minimal)")
        print("[3] Boot to Safe Mode (Networking)")
        print("[4] Boot to Safe Mode (Command Prompt)")
        print("[5] Restore Normal Boot")
        print("[6] Boot to Recovery Environment (WinRE)")
        print("[7] Check WinRE Status")
        if has_sb:
            print("[8] Boot Normally on Next Restart")
        print("[0] Return to Main Menu")
        print(MENU_LOGO)
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Recovery Tools sub-menu selection: {choice}")

        if choice == "1":
            logger.section("Boot Configuration")
            output = _bcdedit(["/enum"])
            print(output if output else "Unable to read boot configuration.")
            logger.write_raw(output)
            input("Press Enter to continue...")

        elif choice == "2":
            logger.section("Safe Mode — Minimal")
            print("WARNING: This will set Safe Mode boot on next restart.")
            if prompt_yes_no(logger, "Set Safe Mode (Minimal)? (Y/N): ", "Safe Mode Minimal"):
                output = _bcdedit(["/set", "{current}", "safeboot", "minimal"])
                print(output)
                logger.write_raw(output)
                if prompt_yes_no(logger, "Restart now? (Y/N): ", "Restart"):
                    run_command(["shutdown", "/r", "/t", "5"], capture=False)
                    logger.log_only("INFO", "System restart initiated.")
            input("Press Enter to continue...")

        elif choice == "3":
            logger.section("Safe Mode — Networking")
            print("WARNING: This will set Safe Mode with Networking on next restart.")
            if prompt_yes_no(logger, "Set Safe Mode (Networking)? (Y/N): ", "Safe Mode Networking"):
                output = _bcdedit(["/set", "{current}", "safeboot", "network"])
                print(output)
                logger.write_raw(output)
                if prompt_yes_no(logger, "Restart now? (Y/N): ", "Restart"):
                    run_command(["shutdown", "/r", "/t", "5"], capture=False)
                    logger.log_only("INFO", "System restart initiated.")
            input("Press Enter to continue...")

        elif choice == "4":
            logger.section("Safe Mode — Command Prompt")
            print("WARNING: This will set Safe Mode with Command Prompt on next restart.")
            if prompt_yes_no(logger, "Set Safe Mode (Command Prompt)? (Y/N): ", "Safe Mode CmdPrompt"):
                output = _bcdedit(["/set", "{current}", "safeboot", "minimal"])
                print(output)
                out2 = _bcdedit(["/set", "{current}", "safebootalternateshell", "yes"])
                print(out2)
                logger.write_raw(output + "\n" + out2)
                if prompt_yes_no(logger, "Restart now? (Y/N): ", "Restart"):
                    run_command(["shutdown", "/r", "/t", "5"], capture=False)
                    logger.log_only("INFO", "System restart initiated.")
            input("Press Enter to continue...")

        elif choice == "5":
            logger.section("Restore Normal Boot")
            print("WARNING: This will remove Safe Mode and restore normal boot.")
            if prompt_yes_no(logger, "Restore normal boot? (Y/N): ", "Restore Normal Boot"):
                out1 = _bcdedit(["/deletevalue", "{current}", "safeboot"])
                print(out1)
                out2 = _bcdedit(["/deletevalue", "{current}", "safebootalternateshell"])
                print(out2)
                logger.write_raw(out1 + "\n" + out2)
                print("Normal boot restored. Reboot is recommended.")
            input("Press Enter to continue...")

        elif choice == "6":
            logger.section("Boot to Recovery Environment")
            print("WARNING: This will restart into Windows Recovery Environment.")
            if prompt_yes_no(logger, "Restart to WinRE now? (Y/N): ", "Boot to WinRE"):
                run_command(["shutdown", "/r", "/o", "/t", "5"], capture=False)
                logger.log_only("INFO", "System restart to WinRE initiated.")
            input("Press Enter to continue...")

        elif choice == "7":
            logger.section("WinRE Status")
            output = _reagentc(["/info"])
            print(output if output else "Unable to query WinRE status.")
            logger.write_raw(output)
            print()
            if command_exists("reagentc"):
                logger.section("Enable / Disable WinRE")
                if prompt_yes_no(logger, "Enable Windows Recovery Environment? (Y/N): ", "Enable WinRE"):
                    out = _reagentc(["/enable"])
                    print(out)
                    logger.write_raw(out)
                if prompt_yes_no(logger, "Disable Windows Recovery Environment? (Y/N): ", "Disable WinRE"):
                    out = _reagentc(["/disable"])
                    print(out)
                    logger.write_raw(out)
            input("Press Enter to continue...")

        elif choice == "8" and has_sb:
            logger.section("Boot Normally on Next Restart")
            out1 = _bcdedit(["/deletevalue", "{current}", "safeboot"])
            print(out1)
            out2 = _bcdedit(["/deletevalue", "{current}", "safebootalternateshell"])
            print(out2)
            logger.write_raw(out1 + "\n" + out2)
            print("Safe Mode cleared. System will boot normally on next restart.")
            input("Press Enter to continue...")

        elif choice == "0":
            logger.log("INFO", "Recovery Tools returned to main menu.")
            return

        else:
            logger.log("WARN", f"Invalid Recovery Tools selection: {choice}")
