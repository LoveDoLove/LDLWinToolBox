# MEMORY.md

Last updated: 2026-06-16

## User Preferences

- User prefers Chinese-language collaboration when discussing work, while repository documentation may remain English if that matches the existing files.
- Always analyze the current project first, then analyze prompt/history files, then apply future rules while preserving history.
- Use Python as the primary implementation language for this project, with Windows command-line tools where appropriate.
- Follow RTK command discipline from `C:\Users\LoveDoLove\.codex\RTK.md`; in this PowerShell environment, use `rtk cmd /c ...` for standard Windows commands.
- Keep changes surgical and verifiable. Do not refactor unrelated code.
- Skill packages under `.agents/skills/` must be cloned from public GitHub open-source skills, not authored manually in this repository.

## Project Snapshot

- App name: `LDLWinToolBox`
- Repository path: `D:\Projects\WinProjects\LDLWinToolBox`
- Git remote: `https://github.com/LoveDoLove/LDLWinToolBox.git`
- Current branch at scan time: `lovedolove`
- Latest scanned commit: `ae4ad2e Rewrite tool as Python uv launcher`
- License: Apache License 2.0
- Primary executable: `LDLWinToolBox.bat` thin launcher for `ldlwintoolbox.py` via `uv run -- python`
- Packaging metadata: `pyproject.toml`, `uv.lock`
- Primary docs: `README.md`, `AGENTS.md`, `MEMORY.md`, `memory/tasks.md`
- Backlog notes: `memory/feature-ideas.md`
- Prompt/history docs observed as absent at the latest scan: `ANALYSIS.md`, `PROMPT_GUIDE.md`
- GitHub metadata: `.github/FUNDING.yml`, `.github/ISSUE_TEMPLATE/bug-report---.md`, `.github/ISSUE_TEMPLATE/feature-request---.md`
- Asset: `images/logo.png`
- Ignored local template observed: `BLANK_README.md`
- Runtime logs observed under `logs\`; `*.log` is ignored by `.gitignore`.

## Current Repository Logic

`LDLWinToolBox.bat` is now a thin launcher that invokes `uv run -- python ldlwintoolbox.py`. The Python entry point initializes the menu, checks for Administrator access, relaunches with UAC when needed, prefers `uv` when available and falls back to `sys.executable`, switches to the script directory, and creates a timestamped structured log file named `logs\LDLWinToolBox_yyMMddHHmmss.log`.

Logging behavior:

- Creates `logs\` automatically and falls back to the script directory if the log directory cannot be created.
- Writes a session header with script path, working directory, user, computer, OS, system root, temp path, and log path.
- Uses helper labels for `INFO`, `WARN`, `ERROR`, `CMD`, and `OK` log entries.
- Records feature section boundaries, menu selections, user cancellations, key command starts, command exit codes, and major completion messages.
- Keeps raw command output in the same log file while keeping console output concise.
- Provides a read-only Log History viewer that lists recent logs newest-first, caps the picker at the latest 9 entries, and opens a selected file with `more`.

Implemented menu behavior:

1. Advanced System Cleanup: calculates free space before and after cleanup, stops `wuauserv` and `bits`, deletes Windows/user temp files, Prefetch, SoftwareDistribution downloads, and root driver folders such as `AMD`, `NVIDIA`, and `INTEL`; rebuilds temp directories; restarts services; reports MB freed. Event Viewer logs are intentionally handled by option 6 instead of direct file deletion.
2. System Integrity Repair: asks confirmation, runs `sfc /scannow`, then `DISM /Online /Cleanup-Image /RestoreHealth`.
3. Windows Component Store Cleanup: asks confirmation, runs `DISM.exe /Online /Cleanup-Image /StartComponentCleanup`.
4. Update All Installed Apps: asks confirmation, runs `winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements`.
5. Complete Network Reset: asks confirmation, runs `netsh winsock reset`, `netsh int ip reset`, and `ipconfig /flushdns`; tells user to restart.
6. Clear Event Viewer Logs: enumerates all logs with `wevtutil.exe el` and clears each one with `wevtutil.exe cl`.
7. Manual SSD TRIM: lists volumes with PowerShell `Get-Volume`, sanitizes and validates a single drive letter, confirms the drive exists, runs `defrag <drive>: /L /V`, displays output, and appends it to the log.
8. Disable BitLocker `(Plan)`: shows current BitLocker status, validates a selected drive letter, displays selected drive status, requires typing `DISABLE`, then starts `manage-bde -off <drive>:` and logs updated status.
9. Kill Browser AI: warns that it downloads and executes a remote PowerShell script, requires typing `KILL`, then runs the configured gist command and logs the result.
10. View Log History: lists the newest toolbox logs in `logs\`, lets the user choose one of the latest 9 entries, and opens it with paged console viewing.
11. Exit: closes the tool.

## Implemented Feature Targets

The user-listed feature targets below were implemented in `LDLWinToolBox.bat` on 2026-06-07:

- Disable BitLocker `[Plan]` with status display, drive validation, and `DISABLE` confirmation.
- Kill Browser AI using:
  `iwr -useb https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1 | iex`

Treat the remote `iwr | iex` command as high risk. Do not execute it during analysis. The menu feature requires a clear warning, `KILL` confirmation, and logging.

## Documentation And Prompt Files

- `README.md` describes the app, prerequisites, installation, usage, license, and contact info.
- `AGENTS.md` records AI working rules, startup order, project rules, and current feature inventory.
- `MEMORY.md` records long-term user preferences, repository facts, current logic, risks, and persistent rules.
- `memory/tasks.md` tracks cross-session work.
- `ANALYSIS.md` and `PROMPT_GUIDE.md` were not present in the latest working tree scan; if restored later, preserve their history and append updates.
- Existing prompt rules emphasize auto-admin preservation, history preservation, input sanitization, clean verbosity, and long-running process warnings.

## Known Gaps And Risks

- The current Python launcher/elevation flow uses `IsUserAnAdmin()` plus `ShellExecuteW(..., "runas", ...)`; keep both the `uv` and `sys.executable` launch paths working.
- Cleanup no longer deletes Event Viewer log files directly; option 6 remains the safe `wevtutil` path for clearing logs.
- The remote `kill_ai.ps1` gist was retrieved and reviewed on 2026-06-13; it disables Chrome and Edge on-device AI by applying registry policy keys and locking the `OptGuideOnDeviceModel` folders, but it still remains high risk and must not be executed automatically during analysis.
- `BLANK_README.md` is present locally but ignored by git and appears to be an unused Best-README-Template source file.
- No tracked `.agents/skills/` directory exists at the 2026-06-16 scan; any future repo-local skill installation must clone a public GitHub source and record provenance.

## Persistent Working Rules

- Preserve the app as a Python-first Windows utility with a thin Batch launcher unless the user explicitly asks for a different architecture.
- Prefer Python standard library calls and native Windows commands for implementation.
- Keep PowerShell calls minimal, one-line, and justified by Windows capability gaps.
- Preserve auto-admin behavior and structured timestamped logs under `logs\`.
- Keep console messages readable and route verbose command output into the log.
- Add `(Y/N)` confirmation for long-running, destructive, privacy-affecting, or remote-execution operations.
- Keep prompt/history updates append-friendly and date-stamped.
- Keep future enhancement ideas in `memory/feature-ideas.md` so they can be reread and prioritized later.
- Treat the `Suggested Priority Order` section in `memory/feature-ideas.md` as the default implementation roadmap until the user asks to reorder it.
