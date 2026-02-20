# LDL Windows ToolBox - User Prompt Guide

This guide explains how to navigate and use the different modules within the `LDLWinToolBox.bat` script.

## 1. Launching the Tool

The script automatically checks for Administrator privileges.

- **If prompted by UAC:** Click "Yes" to allow the tool to perform system-level optimizations.
- **Log Generation:** Every run creates a timestamped log file (`LDLWinToolBox_yyMMddHHmmss.log`) in the same folder as the script to record all detailed operations.
- **Main Menu:** Use the numeric keys `1-8` to select your desired operation.

## 2. Main Features

- **[1] Advanced System Cleanup:** Deep cleans temporary system data. Visualizes current folder processing and calculates total Space Freed (MB) at completion.
- **[2] System Integrity Repair (SFC + DISM):** Scans the OS for corrupted files and repairs them from the Windows cache. Will warn users before running (takes 15-45mins, can be safely interrupted).
- **[3] Windows Component Store Cleanup (WinSxS):** Removes old Windows Update install files. Will heavily warn users NOT to interrupt this process as it may corrupt future updates.
- **[4] Update All Installed Apps (Winget):** Uses Windows Package Manager to blindly update installed software automatically.
- **[5] Complete Network Reset:** Resets Winsock, TCP/IP, and DNS cache. Requires a system restart when finished.
- **[6] Clear Event Viewer Logs:** Clears all system, security, and application logs into a clean state.
- **[7] Manual SSD TRIM:** Queries your NVMe volumes via PowerShell and runs manual garbage collection on them. Type only the drive letter (e.g., `C`) when prompted.

## 3. General User Actions

- **Confirmations:** Whenever a tool mentions it will take a long time, type `Y` to continue or any other key to abort and return to the menu.
- **Exiting the Tool:** Select Option `8` from the main menu or Option `2` from the TRIM sub-menu to safely close the application.

## 4. Rules for Better Prompts (Future Development)

When interacting with AI to update or expand this toolbox, utilize the following rules to ensure quality and consistency:

1. **Specify Standard Windows Commands:** Always request that updates are written using native `.bat` syntax.
2. **Reiterate Privilege Requirements:** Remind the AI that the tool operates with auto-requested Administrator privileges so it can formulate commands confidently.
3. **Preserve Documentation:** Explicitly state: "Keep all previous analysis and history intact. Only append your updates to `ANALYSIS.md` and `PROMPT_GUIDE.md`."
4. **Demand Input Sanitization:** Instruct the AI to incorporate proper variable trimming and sanitization for any newly added menus requiring user input.
5. **Enforce Clean Verbosity:** Demand that scripts echo clear, friendly summaries to the console, while routing "scary" raw verbose output smoothly into the `!LOGFILE!`.
6. **Require Process Warnings:** Insist that the AI implements safety checks `(Y/N)` explicitly stating if long-running processes are safe to abandon/interrupt via window closing.
