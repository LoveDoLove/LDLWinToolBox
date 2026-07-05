from __future__ import annotations

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, run_command


def _run_ps(script: str) -> str:
    if not command_exists("powershell"):
        return ""
    result = run_command(
        ["powershell", "-NoProfile", "-Command", script],
        capture=True,
    )
    if result.code != 0:
        return ""
    return result.stdout.strip()


def _fmt_bytes(n: int | float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def disk_health(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("           DISK HEALTH & SMART SUMMARY")
    print(MENU_LOGO)
    logger.section("Disk Health & SMART")

    ps = (
        "$d=Get-PhysicalDisk | ForEach-Object {"
        "$f=$_;"
        "$rel=$_ | Get-StorageReliabilityCounter -ErrorAction SilentlyContinue;"
        "$w=if($rel -and $rel.WearPercentage -ge 0){$rel.WearPercentage.ToString()+'%'}else{'N/A'};"
        "$t=if($rel -and $rel.Temperature -ne 0){$rel.Temperature.ToString()+'C'}else{'N/A'};"
        "$re=if($rel){$rel.ReadErrorsTotal}else{'N/A'};"
        "$we=if($rel){$rel.WriteErrorsTotal}else{'N/A'};"
        "Write-Output ($f.FriendlyName+'|'+$f.MediaType+'|'+$f.HealthStatus+'|'+"
        "[math]::Round($f.Size/1GB,1).ToString()+'GB|'+$f.OperationalStatus+'|'+$f.BusType+'|'+"
        "$t+'|'+$w+'|'+$re+'|'+$we)"
        "};"
        "if(-not $d){Write-Output 'NO_DATA'}"
    )

    raw = _run_ps(ps)
    if not raw or raw.strip() == "NO_DATA":
        logger.log("INFO", "No physical disk data available via PowerShell.")
        print("No physical disk data returned. Try running as Administrator.")
        print()
        print("  Fallback: Volume-level info from Get-PSDrive:")
        ps2 = (
            "Get-PSDrive -PSProvider FileSystem "
            "| Where-Object {$_.Root -match '^[A-Z]:\\\\$'} "
            "| ForEach-Object {Write-Output ($_.Root+'|'+[math]::Round($_.Used/1GB,1).ToString()+'/'+"
            "[math]::Round(($_.Used+$_.Free)/1GB,1).ToString()+'GB|'+[math]::Round($_.Free/1GB,1).ToString()+'GB')}"
        )
        raw2 = _run_ps(ps2)
        if raw2:
            print(f"  {'Drive':<8} {'Used/Total':<22} {'Free':<10}")
            print(f"  {'-'*8} {'-'*22} {'-'*10}")
            for line in raw2.splitlines():
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    print(f"  {parts[0]:<8} {parts[1]:<22} {parts[2]:<10}")
                    logger.log_only("INFO", f"Disk: {parts[0]} {parts[1]} free={parts[2]}")
        input("Press Enter to continue...")
        return

    print(f"  {'Name':<30} {'Type':<12} {'Health':<12} {'Size':<10} {'Status':<14} {'Bus':<10} {'Temp':<8} {'Wear':<8} {'ReadErr':<8} {'WriteErr':<8}")
    print(f"  {'-'*30} {'-'*12} {'-'*12} {'-'*10} {'-'*14} {'-'*10} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")

    for line in raw.splitlines():
        parts = line.strip().split("|")
        if len(parts) >= 10:
            name, media, health, size, op_status, bus, temp, wear, re, we = parts[:10]
            print(f"  {name:<30} {media:<12} {health:<12} {size:<10} {op_status:<14} {bus:<10} {temp:<8} {wear:<8} {re:<8} {we:<8}")
            logger.log_only("INFO", f"Disk: {name} health={health} wear={wear} temp={temp}")

    print()
    logger.section("Volume Summary")
    ps_vol = (
        "Get-Volume | Where-Object {$_.DriveType -eq 'Fixed' -and $_.DriveLetter} "
        "| ForEach-Object {Write-Output ($_.DriveLetter+':|'+$_.FileSystem+'|'+$_.HealthStatus+'|'+$_.SizeRemaining+'|'+$_.Size)}"
    )
    raw_vol = _run_ps(ps_vol)
    if raw_vol:
        print(f"  {'Volume':<8} {'FS':<8} {'Health':<12} {'Free':<12} {'Total':<12}")
        print(f"  {'-'*8} {'-'*8} {'-'*12} {'-'*12} {'-'*12}")
        for line in raw_vol.splitlines():
            parts = line.strip().split("|")
            if len(parts) >= 5:
                vol, fs, h, free_s, total_s = parts[:5]
                free_b = int(free_s) if free_s.isdigit() else 0
                total_b = int(total_s) if total_s.isdigit() else 0
                free_fmt = _fmt_bytes(free_b) if free_b else free_s
                total_fmt = _fmt_bytes(total_b) if total_b else total_s
                print(f"  {vol:<8} {fs:<8} {h:<12} {free_fmt:<12} {total_fmt:<12}")
                logger.log_only("INFO", f"Volume: {vol} {h} free={free_fmt} of {total_fmt}")

    print()
    logger.section("SMART Reliability Counters")
    ps_smart = (
        "Get-PhysicalDisk | Get-StorageReliabilityCounter -ErrorAction SilentlyContinue "
        "| ForEach-Object {Write-Output ($_.DeviceId+'|'+$_.Temperature+'|'+"
        "$_.WearPercentage+'|'+$_.ReadErrorsTotal+'|'+$_.WriteErrorsTotal+'|'+"
        "$_.ReadLatencyMax+'|'+$_.WriteLatencyMax+'|'+$_.FlushLatencyMax)}"
    )
    raw_smart = _run_ps(ps_smart)
    if raw_smart:
        print(f"  {'Disk#':<8} {'Temp(C)':<10} {'Wear%':<8} {'ReadErr':<10} {'WriteErr':<10} {'RdLat(ms)':<12} {'WrLat(ms)':<12} {'FlLat(ms)':<12}")
        print(f"  {'-'*8} {'-'*10} {'-'*8} {'-'*10} {'-'*10} {'-'*12} {'-'*12} {'-'*12}")
        for line in raw_smart.splitlines():
            parts = line.strip().split("|")
            if len(parts) >= 8:
                did, temp, wear, re, we, rl, wl, fl = parts[:8]
                print(f"  {did:<8} {temp:<10} {wear:<8} {re:<10} {we:<10} {rl:<12} {wl:<12} {fl:<12}")

    logger.log_only("INFO", "DISK HEALTH CHECK COMPLETE")
    input("Press Enter to continue...")
