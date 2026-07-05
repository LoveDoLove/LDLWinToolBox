# memory/tasks.md

Last updated: 2026-07-05

## Pending

- [ ] Phase 2+: System information summary, progress hints, Windows Update check, Defender check, service health, SMART summary, driver inventory, network snapshot, reduced PS calls, export report, self-update, selective cleanup, safe mode, read-only mode

## Completed

- [x] 2026-07-05: Phase 2: Added progress hints `[1/1]` to WinSxS / Winget, `[1/2][2/2]` to SFC+DISM; made vendor driver root deletion opt-in (Y/N) for conservative cleanup.
- [x] 2026-07-05: Added optional restore point via `create_restore_point()` to features 1-7 and 9.
- [x] 2026-07-05: Added missing Y/N confirmation prompts to features 1, 3, 7, and 12.
- [x] 2026-07-05: Reorganized main menu into logical groups (Cleanup / Repair & Update / Network / Performance / Security & Privacy / Tools).
- [x] 2026-07-05: Refactored monolithic `ldlwintoolbox.py` into `toolbox_base.py` + `features/` (one file per feature).
- [x] 2026-07-05: Implemented Low Latency Mode with architecture detection, auto ViVeTool download/extraction, and sub-menu (query/enable/disable).
- [x] 2026-06-17: Replaced the Log History `more` viewer with an internal paged console viewer so CMD stays open while browsing logs.
- [x] 2026-06-16: Rescanned the current repository against the Python-first implementation and refreshed AGENTS.md, MEMORY.md, and memory history with the latest commit and guarded remote-script details.
- [x] 2026-06-07: Scanned current repository logic, docs, prompt files, Git metadata, and issue templates.
- [x] 2026-06-07: Created `AGENTS.md`, `MEMORY.md`, `memory/tasks.md`, and daily work log to restore AI identity and project state in future sessions.
- [x] 2026-06-07: Fixed admin privilege check by replacing the malformed `cacls` protected-path check with `fltmc`.
- [x] 2026-06-07: Implemented `Disable BitLocker (Plan)` with status display, drive validation, `DISABLE` confirmation, and `manage-bde -off`.
- [x] 2026-06-07: Implemented `Kill Browser AI` with source warning, `KILL` confirmation, and logged PowerShell execution.
- [x] 2026-06-07: Hardened SSD TRIM drive input validation and stopped direct Event Viewer log deletion from cleanup.
- [x] 2026-06-07: Improved logging with `logs\`, session headers, log helper labels, feature sections, user cancellation records, command start/end markers, and exit codes.
- [x] 2026-06-07: Added read-only `View Log History` menu option for recent `logs\LDLWinToolBox_*.log` files.
- [x] 2026-06-09: Rescanned current repository logic and updated `AGENTS.md`, `MEMORY.md`, and memory history.
- [x] 2026-06-13: Restored session state, rescanned repository facts, retrieved and reviewed the remote `kill_ai.ps1` gist source, and confirmed no repo-local skills were needed for current work.
- [x] 2026-06-13: Added shared Batch helpers for command preflight checks, confirmation prompts, and drive selection; refactored confirmation-driven menu actions to use them.
- [x] 2026-06-13: Fixed empty-drive propagation in the BitLocker and SSD TRIM flows after the `":" was not understood` error surfaced.
- [x] 2026-06-13: Reworked the project into a Python-first utility with `ldlwintoolbox.py`, `pyproject.toml`, and a thin `LDLWinToolBox.bat` launcher.
- [x] 2026-06-13: Updated README, AGENTS, MEMORY, and the daily work log to describe the Python/uv entry point.
- [x] 2026-06-13: Replaced the old Batch core with a Python implementation while keeping the launcher, logging, confirmations, and guarded remote command flow.
