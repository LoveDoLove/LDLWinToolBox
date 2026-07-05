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
- Prefer `rtk cmd /c ...` for standard Windows command-line utilities and keep implementation changes aligned with the Python entry point.
- Project implementation must remain centered on `ldlwintoolbox.py` with `LDLWinToolBox.bat` as a thin launcher, using Python standard library code and standard Windows commands where appropriate.
- Use PowerShell only as a narrow one-line bridge where Python or native Windows tooling lacks the required Windows capability, matching current patterns such as UAC `RunAs`, timestamp generation, disk free-space queries, or volume enumeration.
- Avoid destructive commands during development unless they are scoped, reviewed, and explicitly requested.

## Project Rules

- Main executable: `LDLWinToolBox.bat` thin launcher for `ldlwintoolbox.py` via `uv run -- python`.
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

Current modular implementation (`ldlwintoolbox.py` + `toolbox_base.py` + `features/`):

### System Cleanup

1. Advanced System Cleanup with a free-space calculator, Windows/user temp cleanup, `Prefetch`, `SoftwareDistribution\Download`, and vendor driver root cleanup.
2. Windows Component Store Cleanup using `DISM /StartComponentCleanup`.
3. Clear Event Viewer Logs using `wevtutil`.

### System Repair & Update

4. System Integrity Repair using `sfc /scannow` and `DISM /RestoreHealth`.
5. Update all installed apps using `winget upgrade --all`.

### Network

6. Complete Network Reset using Winsock, TCP/IP reset, and DNS flush.

### Performance

7. Manual SSD TRIM using `defrag /L /V`.
8. Low Latency Mode in `features/low_latency_mode.py` using ViVeTool (architecture detection, auto-download, sub-menu for query/enable/disable for feature IDs 58989092, 60716524, 61391826).

### Security & Privacy

9. Disable BitLocker `(Plan)` using `manage-bde -status`, drive validation, `DISABLE` confirmation, and guarded `manage-bde -off <drive>:`.
10. Kill Browser AI using the user-specified command:
  `powershell -NoProfile -ExecutionPolicy Bypass -Command "try { iwr -useb https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1 | iex; exit 0 } catch { Write-Error $_; exit 1 }"`

### Tools

11. View Log History using a read-only paged console viewer for the newest `logs\LDLWinToolBox_*.log` files.

12. Exit.

Remote script execution is high risk. Do not run this command during development. If it is implemented as a menu feature, add an explicit warning and confirmation before execution.

## Skill Rules

- Before coding, reviewing, or refactoring, check for applicable local skills under `.agents/skills/`.
- Repository-local skill packages must be cloned from public GitHub open-source skills. Do not hand-write custom skill packages in this repo.
- For every installed repo-local skill, preserve upstream provenance: source URL, commit or tag, and license.
- Current scan on 2026-06-16 found no tracked `.agents/skills/` directory in this repository.
- The session-level `karpathy-guidelines` skill exists outside this repo and may be used for disciplined coding behavior, but it is not currently a repo-local cloned skill asset.

## Memory Files

- `MEMORY.md`: long-term user preferences, project goals, stable constraints, and project snapshot.
- `memory/tasks.md`: cross-session todo and progress.
- `memory/YYYY-MM-DD.md`: daily AI work log, decisions, and notes.
