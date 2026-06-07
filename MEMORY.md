# MEMORY.md

Last updated: 2026-06-07

## User Preferences

- User prefers Chinese-language collaboration when discussing work, while repository documentation may remain English if that matches the existing files.
- Always analyze the current project first, then analyze prompt/history files, then apply future rules while preserving history.
- Use Windows BAT/Command standard commands for this project.
- Follow RTK command discipline from `C:\Users\LoveDoLove\.codex\RTK.md`; in this PowerShell environment, use `rtk cmd /c ...` for standard Windows commands.
- Keep changes surgical and verifiable. Do not refactor unrelated code.
- Skill packages under `.agents/skills/` must be cloned from public GitHub open-source skills, not authored manually in this repository.

## Project Snapshot

- App name: `LDLWinToolBox`
- Repository path: `D:\Projects\WinProjects\LDLWinToolBox`
- Git remote: `https://github.com/LoveDoLove/LDLWinToolBox.git`
- Current branch at scan time: `lovedolove`
- License: Apache License 2.0
- Primary executable: `LDLWinToolBox.bat`
- Primary docs: `README.md`, `ANALYSIS.md`, `PROMPT_GUIDE.md`
- GitHub metadata: `.github/FUNDING.yml`, `.github/ISSUE_TEMPLATE/bug-report---.md`, `.github/ISSUE_TEMPLATE/feature-request---.md`
- Asset: `images/logo.png`
- Ignored local template observed: `BLANK_README.md`

## Current Repository Logic

`LDLWinToolBox.bat` is a standalone menu-driven Windows Batch script. It initializes delayed expansion, checks for Administrator access, relaunches with UAC through PowerShell `Start-Process -Verb RunAs` when needed, switches to the script directory, and creates a timestamped log file named `LDLWinToolBox_yyMMddHHmmss.log`.

Implemented menu behavior:

1. Advanced System Cleanup: calculates free space before and after cleanup, stops `wuauserv` and `bits`, deletes Windows/user temp files, Prefetch, SoftwareDistribution downloads, Event Viewer log files, and root driver folders such as `AMD`, `NVIDIA`, and `INTEL`; rebuilds temp directories; restarts services; reports MB freed.
2. System Integrity Repair: asks confirmation, runs `sfc /scannow`, then `DISM /Online /Cleanup-Image /RestoreHealth`.
3. Windows Component Store Cleanup: asks confirmation, runs `DISM.exe /Online /Cleanup-Image /StartComponentCleanup`.
4. Update All Installed Apps: asks confirmation, runs `winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements`.
5. Complete Network Reset: asks confirmation, runs `netsh winsock reset`, `netsh int ip reset`, and `ipconfig /flushdns`; tells user to restart.
6. Clear Event Viewer Logs: enumerates all logs with `wevtutil.exe el` and clears each one with `wevtutil.exe cl`.
7. Manual SSD TRIM: lists volumes with PowerShell `Get-Volume`, sanitizes the entered drive letter, runs `defrag <drive>: /L /V`, displays output, and appends it to the log.
8. Exit: closes the tool.

## Declared Feature Targets

The user listed these as available or planned feature targets, but the current scanned `LDLWinToolBox.bat` implementation does not yet expose them as tools:

- Disable BitLocker `[Plan]`.
- Kill Browser AI using:
  `iwr -useb https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1 | iex`

Treat the remote `iwr | iex` command as high risk. Do not execute it during analysis. If implemented later, add a clear warning, confirmation prompt, and logging.

## Documentation And Prompt Files

- `README.md` describes the app, prerequisites, installation, usage, license, and contact info.
- `ANALYSIS.md` records technical analysis and future prompt rules.
- `PROMPT_GUIDE.md` explains how users should launch, select menu options, and prompt AI for future changes.
- Existing prompt rules emphasize Batch standard, auto-admin preservation, history preservation, input sanitization, clean verbosity, and long-running process warnings.

## Known Gaps And Risks

- Current README says options `1-8` execute tools, but option `8` is currently `Exit`.
- User-declared feature targets `Disable BitLocker` and `Kill Browser AI` are not implemented in the scanned script.
- The current admin-check path in `LDLWinToolBox.bat` should be reviewed before future releases because the line includes `system32%` in the protected path.
- Cleanup deletes Event Viewer log files directly and option 6 also clears logs through `wevtutil`; future changes should keep this behavior intentional and clearly documented.
- `BLANK_README.md` is present locally but ignored by git and appears to be an unused Best-README-Template source file.
- No tracked `.agents/skills/` directory exists at the 2026-06-07 scan; any future repo-local skill installation must clone a public GitHub source and record provenance.

## Persistent Working Rules

- Preserve the app as a single-file Windows Batch tool unless the user explicitly asks for a different architecture.
- Prefer native Windows commands and Batch syntax for implementation.
- Keep PowerShell calls minimal, one-line, and justified by Windows capability gaps.
- Preserve auto-admin behavior and timestamped logs.
- Keep console messages readable and route verbose command output into the log.
- Add `(Y/N)` confirmation for long-running, destructive, privacy-affecting, or remote-execution operations.
- Keep prompt/history updates append-friendly and date-stamped.

