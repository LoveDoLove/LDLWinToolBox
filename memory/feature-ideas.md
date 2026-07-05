# Feature Ideas Backlog

Last updated: 2026-07-05

This file is a living backlog of future enhancements and maintenance ideas for `LDLWinToolBox`.
Keep entries concise, append-friendly, and aligned with the Python-first, menu-driven design.

## Suggested Priority Order

### Phase 1: Foundation ✅ (Complete)

- [x] Extract shared helper labels and common routines (toolbox_base.py)
- [x] Strengthen input validation for all menu prompts (prompt_drive, select_existing_drive)
- [x] Standardize confirmation flow for risky actions (prompt_yes_no, prompt_keyword)
- [x] Add preflight checks for external commands (command_exists)
- [x] Improve error handling and user-facing failure messages
- [x] Create restore point before risky operations (create_restore_point)

### Phase 2: Safety & Clarity ✅ (Complete)

- [x] Add progress hints for long-running tasks (`[1/N]` markers where missing)
- [x] Make cleanup operations more conservative by default (vendor driver roots now opt-in)

### Phase 3: New Feature Modules ✅ (Complete)

- [x] System information summary (OS, CPU, RAM, disk, uptime via ctypes+winreg)
- [x] Windows Update status check (service, registry config, UsoClient scan)
- [x] Defender status check and quick scan entry (Get-MpComputerStatus, Start-MpQuickScan)
- [x] Service health check for common Windows services (20 critical services)

### Phase 4: Reporting & Export ✅ (Complete)

- [x] Disk health and SMART summary (Get-PhysicalDisk + Get-StorageReliabilityCounter)
- [x] Driver inventory and version view (driverquery /FO CSV parsing)
- [x] Network before/after snapshot (ipconfig/route/netsh/netstat capture + diff)
- [x] Log export and archive bundle (#4+#5 combined: report generation + ZIP archive)

### Phase 5: Efficiency & Maintenance ✅ (Complete)

- [x] Version and update check for the toolbox itself (GitHub releases API)
- [x] Reduce redundant PowerShell calls (disk_health: 3→1 call; remaining calls are non-redundant)
- [x] Add a read-only mode for status checks (diagnostics 12–22 run without admin, 1–11 hidden with [R] restart option)

### Phase 6: Advanced Features ✅ (Complete)

- [x] Selective cleanup instead of fixed cleanup sets (sub-menu in system_cleanup)
- [x] Custom exclusion list for cleanup targets (config/exclusions.json manager)
- [x] Safe Mode or recovery entry helpers (bcdedit/reagentc/shutdown sub-menu)

## New Features

- [x] System information summary
- [x] Windows Update status check
- [x] Driver inventory and version view
- [x] Service health check for common Windows services
- [x] Disk health and SMART summary
- [x] Log export and archive bundle
- [x] Network before/after snapshot
- [x] Defender status check and quick scan entry
- [x] Safe Mode or recovery entry helpers
- [x] Selective cleanup instead of fixed cleanup sets
- [x] Custom exclusion list for cleanup targets
- Exportable report of actions and results
- [x] Version and update check for the toolbox itself

## Optimizations

- [x] Reduce redundant PowerShell calls
- [x] Improve error handling and user-facing failure messages
- [x] Add progress hints for long-running tasks
- [x] Make cleanup operations more conservative by default
- [x] Add a read-only mode for status checks
- Maintain a lightweight verification checklist after changes
- Keep README, memory, and task notes synchronized
