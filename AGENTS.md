@C:\Users\LoveDoLove\.codex\RTK.md

# AGENTS.md - LDLWinToolBox

## Agent Role

You are the AI maintainer for `LDLWinToolBox`, a Python-first Windows utility with a thin Batch launcher for administrative cleanup, repair, update, network reset, log clearing, and SSD TRIM workflows.

Work from repository facts first. Preserve existing history and project decisions unless the user explicitly asks to replace them.

## Startup Order

On every new session:

1. Read `AGENTS.md` and `MEMORY.md`.
2. Analyze the project source and repository structure first, especially `LDLWinToolBox.bat`, `README.md`, `.github/`, and tracked metadata.
3. Only after project analysis, analyze prompt/history files if present: `ANALYSIS.md`, `PROMPT_GUIDE.md`, `memory/tasks.md`, and `memory/YYYY-MM-DD.md`.
4. Continue from the stored rules and tasks while keeping prior history intact.
5. When updating history, append dated notes or update status clearly; do not delete older decisions unless the user explicitly requests cleanup.

## Command Rules

- Follow `C:\Users\LoveDoLove\.codex\RTK.md`: prefix shell commands with `rtk`.
- Prefer Windows BAT/Command standard commands through `rtk cmd /c ...`.
- Project implementation must remain centered on `ldlwintoolbox.py` with `LDLWinToolBox.bat` as a thin launcher, using Python standard library code and standard Windows commands where appropriate.
- Use PowerShell only as a narrow one-line bridge where Python or native Windows tooling lacks the required Windows capability, matching current patterns such as UAC `RunAs`, timestamp generation, disk free-space queries, or volume enumeration.
- Avoid destructive commands during development unless they are scoped, reviewed, and explicitly requested.

## Project Rules

- Main executable: `LDLWinToolBox.bat` launcher for `ldlwintoolbox.py`.
- Keep the app menu-driven and suitable for Windows 10/11.
- The script must auto-check Administrator permission and auto-request elevation with UAC before system-level operations.
- Preserve timestamped structured logging under `logs\LDLWinToolBox_yyMMddHHmmss.log`.
- Console output should stay concise and user-readable; raw command output should go to `!LOGFILE!`.
- Logs should include a session header, feature sections, user cancellation notes, command start/end markers, and exit codes for key system commands.
- Runtime logs are ignored by git through the existing `*.log` ignore rule.
- Long-running or risky operations must warn the user, explain interrupt safety, and ask for `(Y/N)` confirmation.
- Sanitize user input for every new menu feature that accepts values.
- Keep existing documentation and analysis history intact. If `ANALYSIS.md` or `PROMPT_GUIDE.md` exists, append updates instead of replacing historical context.

## Current Implemented Features

Current `ldlwintoolbox.py` menu implementation:

1. Advanced System Cleanup with space calculator.
2. System Integrity Repair using `sfc /scannow` and `DISM /RestoreHealth`.
3. Windows Component Store Cleanup using `DISM /StartComponentCleanup`.
4. Update all installed apps using `winget upgrade --all`.
5. Complete Network Reset using Winsock, TCP/IP reset, and DNS flush.
6. Clear Event Viewer Logs using `wevtutil`.
7. Manual SSD TRIM using `defrag /L /V`.
8. Disable BitLocker `(Plan)` using `manage-bde -status` and guarded `manage-bde -off <drive>:`.
9. Kill Browser AI using the user-specified command:
  `iwr -useb https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1 | iex`
10. View Log History using a read-only paged console viewer for recent `logs\LDLWinToolBox_*.log` files.
11. Exit.

Remote script execution is high risk. Do not run this command during development. If it is implemented as a menu feature, add an explicit warning and confirmation before execution.

## Skill Rules

- Before coding, reviewing, or refactoring, check for applicable local skills under `.agents/skills/`.
- Repository-local skill packages must be cloned from public GitHub open-source skills. Do not hand-write custom skill packages in this repo.
- For every installed repo-local skill, preserve upstream provenance: source URL, commit or tag, and license.
- Current scan on 2026-06-09 found no tracked `.agents/skills/` directory in this repository.
- The session-level `karpathy-guidelines` skill exists outside this repo and may be used for disciplined coding behavior, but it is not currently a repo-local cloned skill asset.

## Memory Files

- `MEMORY.md`: long-term user preferences, project goals, stable constraints, and project snapshot.
- `memory/tasks.md`: cross-session todo and progress.
- `memory/YYYY-MM-DD.md`: daily AI work log, decisions, and notes.
