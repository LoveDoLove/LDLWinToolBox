@C:\Users\LoveDoLove\.codex\RTK.md

# AGENTS.md - LDLWinToolBox

## Agent Role

You are the AI maintainer for `LDLWinToolBox`, a Python-first Windows utility with a thin Batch launcher for administrative cleanup, repair, update, network reset, log clearing, SSD TRIM, and low-latency configuration workflows.

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
- Console output should stay concise and user-readable; raw command output is routed through the Logger to the structured log file.
- Logs should include a session header, feature sections, user cancellation notes, command start/end markers, and exit codes for key system commands.
- Runtime logs are ignored by git through the existing `*.log` ignore rule.
- Long-running or risky operations must warn the user, explain interrupt safety, and ask for `(Y/N)` confirmation.
- Sanitize user input for every new menu feature that accepts values.
- Keep existing documentation and analysis history intact. If `ANALYSIS.md` or `PROMPT_GUIDE.md` exists, append updates instead of replacing historical context.

## Project Architecture (Production)

The project follows a modular file-per-feature architecture:

- `ldlwintoolbox.py` — thin entry point with admin logic and colored main menu dispatch
- `LDLWinToolBox.bat` — thin launcher invoking `uv run -- python ldlwintoolbox.py`
- `toolbox_base.py` — shared infrastructure (Logger, CommandResult, Color, cprint, Spinner, run/command/prompt helpers)
- `features/` — one file per feature, each importing only from `toolbox_base`
- `scripts/check.ps1` — unified ruff lint + format check runner
- `LDLWinToolBox.spec` — PyInstaller spec for EXE packaging; version via `str(vers)` not `repr(vers)` (see below)
- `.github/workflows/ci.yml` — CI (ruff on push/PR)
- `.github/workflows/release.yml` — Release (PyInstaller build on tag)
- `README.md` — project documentation written using the `BLANK_README.md` (Best-README-Template) format, covering all 23 menu features, architecture, and production build info
- Zero external dependencies; all imports from Python stdlib; ANSI colors for UX
- `TOOLBOX_VERSION` read dynamically from `pyproject.toml` via `tomllib`

### PyInstaller Spec: Version File Serialization

In `LDLWinToolBox.spec`, the version info `VSVersionInfo` object is serialized to `build/version_info.txt` using `str(vers)`, then loaded by `EXE(version=str(vers_file))`. **Must use `str()` not `repr()`** — `repr(vers)` produces qualified names (`versioninfo.VSVersionInfo(...)`) that cannot be `eval()`'d inside PyInstaller's `versioninfo.py` module scope, while `str(vers)` produces unqualified names (`VSVersionInfo(...)`) that match the `pyi-grab_version` format and deserialize correctly.

## Current Implemented Features

### System Cleanup (1-3)

1. Advanced System Cleanup in `features/system_cleanup.py` with Y/N confirmation, optional restore point, free-space calculator, Windows/user temp cleanup, `Prefetch`, `SoftwareDistribution\Download`, and vendor driver root cleanup.
2. Windows Component Store Cleanup in `features/winsxs_cleanup.py` with Y/N confirmation and optional restore point using `DISM /StartComponentCleanup`.
3. Clear Event Viewer Logs in `features/event_log_clear.py` with Y/N confirmation and optional restore point using `wevtutil`.

### System Repair & Update (4-5)

4. System Integrity Repair in `features/system_repair.py` with Y/N confirmation and optional restore point using `sfc /scannow` and `DISM /RestoreHealth`.
5. Update all installed apps in `features/winget_upgrade.py` with Y/N confirmation and optional restore point using `winget upgrade --all`.

### Network (6)

6. Complete Network Reset in `features/network_reset.py` with Y/N confirmation and optional restore point using Winsock, TCP/IP reset, and DNS flush.

### Performance (7-8)

7. Manual SSD TRIM in `features/ssd_trim.py` with Y/N confirmation after drive selection and optional restore point using `defrag /L /V`.
8. Low Latency Mode in `features/low_latency_mode.py` using ViVeTool (architecture detection, auto-download, sub-menu for query/enable/disable for feature IDs 58989092, 60716524, 61391826).

### Security & Privacy (9-10)

9. Disable BitLocker in `features/bitlocker_disable.py` using `manage-bde -status`, drive validation, optional restore point, `DISABLE` confirmation, and guarded `manage-bde -off <drive>:`.
10. Kill Browser AI in `features/browser_ai_killer.py` using the configured remote PowerShell script.

### Recovery (11)

11. Recovery & Safe Mode Tools in `features/recovery_tools.py` with bcdedit boot config, safe mode (minimal/networking/cmd-prompt), WinRE status/enable/disable, restore normal boot.

### Diagnostics (12-19)

12. System Information in `features/system_info.py` (OS, CPU, RAM, disk, uptime via ctypes+winreg).
13. Windows Update Status in `features/windows_update.py` (service state, registry config, UsoClient scan).
14. Defender Status & Quick Scan in `features/defender_tools.py` (Get-MpComputerStatus, MpCmdRun update, Start-MpQuickScan).
15. Service Health Check in `features/service_health.py` (20 critical services via Get-Service/sc query).
16. Disk Health & SMART Summary in `features/disk_health.py` (Get-PhysicalDisk + Get-StorageReliabilityCounter).
17. Driver Inventory in `features/driver_inventory.py` (driverquery /FO CSV parsing).
18. Network Snapshot in `features/network_snapshot.py` (ipconfig/route/netsh/netstat capture + diff).
19. Export Logs & Report in `features/export_report.py` (session report + log ZIP archive).

### Tools (20-22)

20. View Log History in `features/log_viewer.py` using a read-only paged console viewer for the newest `logs\LDLWinToolBox_*.log` files.
21. Check for Updates in `features/self_update.py` (GitHub releases API comparison).
22. Cleanup Exclusion List in `features/cleanup_config.py` (JSON-based exclusion manager).

23. Exit with Y/N confirmation.

### Production Version Additions
- `Color` class + `cprint()` for ANSI colored console output (zero deps)
- `Spinner` context manager for long-running task progress indication (thread-based, zero deps)
- `TOOLBOX_VERSION` dynamically read from `pyproject.toml` via `tomllib`
- `scripts/check.ps1` — unified ruff linter + formatter runner
- `LDLWinToolBox.spec` — PyInstaller spec for EXE packaging
- `.github/workflows/ci.yml` — CI workflow (ruff on push/PR)
- `.github/workflows/release.yml` — Release workflow (PyInstaller build on version tag)

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
