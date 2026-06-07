# memory/tasks.md

Last updated: 2026-06-07

## Pending

- [ ] Review the remote `kill_ai.ps1` gist source when it is reachable, and keep the `KILL` confirmation unless a trusted local implementation replaces it.
- [ ] If repo-local skills are needed, clone public GitHub open-source skills into `.agents/skills/<skill-name>/` and record URL, commit or tag, and license.

## Completed

- [x] 2026-06-07: Scanned current repository logic, docs, prompt files, Git metadata, and issue templates.
- [x] 2026-06-07: Created `AGENTS.md`, `MEMORY.md`, `memory/tasks.md`, and daily work log to restore AI identity and project state in future sessions.
- [x] 2026-06-07: Fixed admin privilege check by replacing the malformed `cacls` protected-path check with `fltmc`.
- [x] 2026-06-07: Implemented `Disable BitLocker (Plan)` with status display, drive validation, `DISABLE` confirmation, and `manage-bde -off`.
- [x] 2026-06-07: Implemented `Kill Browser AI` with source warning, `KILL` confirmation, and logged PowerShell execution.
- [x] 2026-06-07: Hardened SSD TRIM drive input validation and stopped direct Event Viewer log deletion from cleanup.
- [x] 2026-06-07: Improved logging with `logs\`, session headers, log helper labels, feature sections, user cancellation records, command start/end markers, and exit codes.
- [x] 2026-06-07: Added read-only `View Log History` menu option for recent `logs\LDLWinToolBox_*.log` files.
