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

### Phase 2: Safety & Clarity (Next)

1. Add progress hints for long-running tasks (`[1/N]` markers where missing)
2. Make cleanup operations more conservative by default

### Phase 3: New Feature Modules

1. System information summary
2. Windows Update status check
3. Defender status check and quick scan entry
4. Service health check for common Windows services

### Phase 4: Diagnostics & Reporting

1. Disk health and SMART summary
2. Driver inventory and version view
3. Network before/after snapshot
4. Log export and archive bundle
5. Exportable report of actions and results

### Phase 5: Efficiency & Maintenance

1. Reduce redundant PowerShell calls
2. Add a read-only mode for status checks
3. Version and update check for the toolbox itself

### Phase 6: Advanced Features

1. Selective cleanup instead of fixed cleanup sets
2. Custom exclusion list for cleanup targets
3. Safe Mode or recovery entry helpers

## New Features

- System information summary
- Windows Update status check
- Driver inventory and version view
- Service health check for common Windows services
- Disk health and SMART summary
- Log export and archive bundle
- Network before/after snapshot
- Defender status check and quick scan entry
- Safe Mode or recovery entry helpers
- Selective cleanup instead of fixed cleanup sets
- Custom exclusion list for cleanup targets
- Exportable report of actions and results
- Version and update check for the toolbox itself

## Optimizations

- Reduce redundant PowerShell calls
- Improve error handling and user-facing failure messages
- Add progress hints for long-running tasks
- Make cleanup operations more conservative by default
- Add a read-only mode for status checks
- Maintain a lightweight verification checklist after changes
- Keep README, memory, and task notes synchronized
