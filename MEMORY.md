# MEMORY.md

Last updated: 2026-07-05

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
- Latest scanned commit: `fbb2701 Refactor into modular architecture + add Low Latency Mode + reorganize menu`
- Latest repository scan: `2026-07-05`.
- License: Apache License 2.0
- Primary executable: `LDLWinToolBox.bat` thin launcher for `ldlwintoolbox.py` via `uv run -- python`
- Packaging metadata: `pyproject.toml`, `uv.lock`
- Primary docs: `README.md`, `AGENTS.md`, `MEMORY.md`, `memory/tasks.md`
- Backlog notes: `memory/feature-ideas.md`
- Prompt/history docs observed as absent at the latest scan: `ANALYSIS.md`, `PROMPT_GUIDE.md`
- GitHub metadata: `.github/FUNDING.yml`, `.github/ISSUE_TEMPLATE/bug-report---.md`, `.github/ISSUE_TEMPLATE/feature-request---.md`
- Asset: `images/logo.png`
- Ignored local template observed: `BLANK_README.md`
- Runtime logs observed under `logs\`; `*.log` is ignored by `.gitignore`. Downloaded binaries in `tools/` are also git-ignored.

## Current Repository Logic

`LDLWinToolBox.bat` is now a thin launcher that invokes `uv run -- python ldlwintoolbox.py`. The Python entry point initializes the menu, checks for Administrator access, relaunches with UAC when needed, prefers `uv` when available and falls back to `sys.executable`, switches to the script directory, and creates a timestamped structured log file named `logs\LDLWinToolBox_yyMMddHHmmss.log`.

The project has been refactored into a modular structure:
- `ldlwintoolbox.py` — thin entry point with admin logic and main menu dispatch
- `toolbox_base.py` — shared infrastructure (Logger, CommandResult, run/command/prompt helpers)
- `features/` — one file per feature, each importing only from `toolbox_base`

Logging behavior:

- Creates `logs\` automatically and falls back to the script directory if the log directory cannot be created.
- Writes a session header with script path, working directory, user, computer, OS, system root, temp path, and log path.
- Uses helper labels for `INFO`, `WARN`, `ERROR`, `CMD`, and `OK` log entries.
- Records feature section boundaries, menu selections, user cancellations, key command starts, command exit codes, and major completion messages.
- Keeps raw command output in the same log file while keeping console output concise.
- Provides a read-only Log History viewer that lists recent logs newest-first, caps the picker at the latest 9 entries, and opens a selected file with an internal paged console viewer.

Implemented menu behavior (each feature in its own `features/*.py` file), grouped into logical categories:

**System Cleanup (1-3):**

1. Advanced System Cleanup: asks Y/N confirmation, optional restore point; calculates free space before and after cleanup, stops `wuauserv` and `bits`, deletes Windows/user temp files, Prefetch, SoftwareDistribution downloads; **optionally** removes vendor driver roots (`AMD`, `NVIDIA`, `INTEL`) via separate Y/N prompt; rebuilds temp directories; restarts services; reports MB freed. Event Viewer logs are intentionally handled by option 3 instead of direct file deletion.
2. Windows Component Store Cleanup: asks Y/N confirmation and optional restore point, runs `DISM.exe /Online /Cleanup-Image /StartComponentCleanup` with `[1/1]` progress hint.
3. Clear Event Viewer Logs: asks Y/N confirmation and optional restore point; enumerates all logs with `wevtutil.exe el` and clears each one with `wevtutil.exe cl`.

**System Repair & Update (4-5):**

4. System Integrity Repair: asks confirmation and optional restore point, runs `sfc /scannow` then `DISM /Online /Cleanup-Image /RestoreHealth` with `[1/2] [2/2]` progress hints.
5. Update All Installed Apps: asks confirmation and optional restore point, runs `winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements` with `[1/1]` progress hint.

**Network (6):**

6. Complete Network Reset: asks confirmation and optional restore point, runs `netsh winsock reset`, `netsh int ip reset`, and `ipconfig /flushdns`; tells user to restart.

**Performance (7-8):**

7. Manual SSD TRIM: lists volumes with PowerShell `Get-Volume`, sanitizes and validates a single drive letter, confirms the drive exists, asks Y/N confirmation and optional restore point, runs `defrag <drive>: /L /V`, displays output, and appends it to the log.
8. Low Latency Mode: auto-detects CPU architecture (Intel/AMD x64 or Snapdragon ARM64), fetches the latest ViVeTool release from GitHub via API, downloads and extracts the matching ZIP to `tools/vivetool/`, and provides a sub-menu to query/enable/disable feature IDs 58989092, 60716524, and 61391826. Version caching avoids redundant downloads.

**Security & Privacy (9-10):**

9. Disable BitLocker `(Plan)`: shows current BitLocker status, validates a selected drive letter, displays selected drive status, optional restore point, requires typing `DISABLE`, then starts `manage-bde -off <drive>:` and logs updated status.
10. Kill Browser AI: warns that it downloads and executes a remote PowerShell script, requires typing `KILL`, then launches PowerShell with `-ExecutionPolicy Bypass` and a guarded `try/catch` wrapper around the configured gist command so the result is logged.

**Recovery (11):**

11. Recovery & Safe Mode Tools: sub-menu for bcdedit boot config, safe mode (minimal/networking/cmd-prompt), WinRE status/enable/disable, restore normal boot, restart to recovery.

**Tools (20-22):**

20. View Log History: lists the newest toolbox logs in `logs\`, lets the user choose one of the latest 9 entries, and opens it with paged console viewing.
21. Check for Updates: queries GitHub releases API, compares with local version (1.0.3), opens browser for download if newer.
22. Cleanup Exclusion List: manage JSON-based exclusion list in `config/exclusions.json`; paths matching exclusions are skipped during cleanup.

23. Exit: asks Y/N confirmation, then closes the tool.

**Diagnostics (11-18):**

11. System Information: read-only summary of OS, CPU, RAM, disk, uptime using stdlib + ctypes + winreg.
12. Windows Update Status: queries wuauserv, Auto Update registry config, last install/search dates; runs UsoClient scan.
13. Defender Status & Quick Scan: displays Get-MpComputerStatus fields, optional MpCmdRun signature update, optional Start-MpQuickScan.
14. Service Health Check: checks 20 critical services via PowerShell Get-Service, shows Running/Stopped summary.
15. Disk Health & SMART: Get-PhysicalDisk + Get-StorageReliabilityCounter for health, wear, temp, errors; volume summary.
16. Driver Inventory: parses driverquery /FO CSV output, shows all drivers with type/date summary.
17. Network Snapshot: captures ipconfig/route/netsh/netstat state to file and log; optional diff against previous snapshot.
18. Export Logs & Report: generates a plain-text session report (features run, commands, warnings) and archives all logs to ZIP.
19. System Cleanup: now supports selective target sub-menu (Windows Temp, User Temp, Prefetch, SoftDist, Vendor Roots) with exclusion list integration.

## Implemented Feature Targets

The user-listed feature targets below were implemented:

### 2026-06-07 (Batch)

- Disable BitLocker `[Plan]` with status display, drive validation, and `DISABLE` confirmation.
- Kill Browser AI using:
  `powershell -NoProfile -ExecutionPolicy Bypass -Command "try { iwr -useb https://gist.githubusercontent.com/raw/d08347a1f1083e4e3d29daf17f86223c/kill_ai.ps1 | iex; exit 0 } catch { Write-Error $_; exit 1 }"`

Treat the remote `iwr | iex` command as high risk. Do not execute it during analysis. The menu feature requires a clear warning, `KILL` confirmation, and logging.

### 2026-07-05 (Python)

- Modular refactor: split monolithic `ldlwintoolbox.py` into `toolbox_base.py` + `features/` (one file per feature).
- Low Latency Mode: auto-detects `platform.machine()` → `IntelAmd` (AMD64/x86) or `SnapdragonArm64` (ARM64), fetches latest ViVe release from `api.github.com/repos/thebookisclosed/ViVe/releases/latest`, downloads matching ZIP via `urllib.request`, extracts with `zipfile` to `tools/vivetool/`, caches version in `version.txt`, provides sub-menu for `/query`, `/enable`, `/disable` on IDs 58989092, 60716524, 61391826.
- Menu reorganization into logical groups: System Cleanup, Repair & Update, Network, Performance, Security & Privacy, Tools.

## Documentation And Prompt Files

- `README.md` describes the app, prerequisites, installation, usage, license, and contact info.
- `AGENTS.md` records AI working rules, startup order, project rules, and current feature inventory.
- `MEMORY.md` records long-term user preferences, repository facts, current logic, risks, and persistent rules.
- `memory/tasks.md` tracks cross-session work.
- `ANALYSIS.md` and `PROMPT_GUIDE.md` were not present in the latest working tree scan; if restored later, preserve their history and append updates.
- Existing prompt rules emphasize auto-admin preservation, history preservation, input sanitization, clean verbosity, and long-running process warnings.

## New Feature Details

### Low Latency Mode (Menu 8)

**Architecture detection:**
- `platform.machine()` → `AMD64` → Intel/AMD x64
- `platform.machine()` → `ARM64` → Snapdragon ARM64

**ViVeTool management:**
- Stores tool in `tools/vivetool/` under script directory
- Caches version in `version.txt` to skip redundant downloads
- Falls back to cached binary when GitHub API is unavailable

**Sub-menu:**
1. Check Status — runs `ViVeTool.exe /query /id:58989092,60716524,61391826`
2. Enable — runs `ViVeTool.exe /enable /id:58989092,60716524,61391826` (with Y/N confirmation)
3. Disable — runs `ViVeTool.exe /disable /id:58989092,60716524,61391826` (with Y/N confirmation)
4. Return to Main Menu

**Risks:**
- Downloads binaries from GitHub; requires internet on first run
- Feature ID changes in future Windows builds may require updates
- Reboot may be required after changing low latency features

## Restore Point Feature

`create_restore_point(logger, description)` in `toolbox_base.py` creates a system restore point before destructive operations. Key behaviors:

- Uses `Checkpoint-Computer` via single-line PowerShell
- Asks user `(Y/N)` before attempting
- Failure (e.g. System Restore disabled) logs WARN and continues — never blocks the feature
- Known error `0x80070422` detected and shown with a helpful message
- Integrated into features 1-7 and 9 (all except read-only/remote features)

## Known Gaps And Risks

- The current Python launcher/elevation flow uses `IsUserAnAdmin()` plus `ShellExecuteW(..., "runas", ...)`; keep both the `uv` and `sys.executable` launch paths working.
- Cleanup no longer deletes Event Viewer log files directly; option 3 (Clear Event Viewer Logs) remains the safe `wevtutil` path for clearing logs.
- No circular dependencies; each feature imports only from `toolbox_base`
- The remote `kill_ai.ps1` gist was retrieved and reviewed on 2026-06-13; it disables Chrome and Edge on-device AI by applying registry policy keys and locking the `OptGuideOnDeviceModel` folders, but it still remains high risk and is only executed through the guarded PowerShell wrapper after explicit `KILL` confirmation.
- `BLANK_README.md` is present locally but ignored by git and appears to be an unused Best-README-Template source file.
- No tracked `.agents/skills/` directory exists at the 2026-06-16 scan; any future repo-local skill installation must clone a public GitHub source and record provenance.

## New / Changed Files (Production Version)

- `pyproject.toml` — added `[tool.ruff]` section for lint/format/isort
- `toolbox_base.py` — added `Color`, `cprint()`, `Spinner`, dynamic `TOOLBOX_VERSION` from pyproject.toml
- `ldlwintoolbox.py` — colored main menu with version display, box-drawing chars
- `scripts/check.ps1` — unified ruff lint + format + import check runner
- `.github/workflows/ci.yml` — CI workflow (Windows + ruff-action)
- `.github/workflows/release.yml` — Release workflow (PyInstaller build + GitHub Release)
- `LDLWinToolBox.spec` — PyInstaller spec for EXE packaging
- `README.md` — rewritten using `BLANK_README.md` (Best-README-Template) format, covering all 23 menu features, architecture, and production build info
- `memory/2026-07-05.md` — updated with Production Version work log

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

## Production Version Plan (2026-07-05)

Four-phase plan to move from feature-complete to production-ready. All phases completed.

### Phase A: Code Hardening
- A1: Ruff lint + format + isort in `pyproject.toml`
- A2: Full type annotations in all `features/*.py` (already complete)
- A3: `scripts/check.ps1` — unified lint/format runner
- A4: `.github/workflows/ci.yml` — run check on every push/PR

### Phase B: UX Polish
- B1: ANSI color constants (`Color` class) + `cprint()` in `toolbox_base.py`, zero dependencies
- B2: `Spinner` context manager for long-running tasks (thread-based, zero deps)
- B3: Colored menu with box-drawing chars, group headers, version display, dimmed log path

### Phase C: Packaging & Release
- C1: PyInstaller `.spec` at project root
- C2: `.github/workflows/release.yml` — auto-build + release on version tag
- C3: Version sourced from `pyproject.toml` via `tomllib` at runtime (`TOOLBOX_VERSION`)
