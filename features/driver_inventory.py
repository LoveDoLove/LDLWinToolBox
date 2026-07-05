from __future__ import annotations

from toolbox_base import MENU_LOGO, Logger, clear_screen, command_exists, run_command


def driver_inventory(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              DRIVER INVENTORY")
    print(MENU_LOGO)
    logger.section("Driver Inventory")

    if not command_exists("driverquery"):
        logger.log("ERROR", "driverquery.exe is required but not found.")
        input("Press Enter to continue...")
        return

    logger.log_only("INFO", "Querying drivers via driverquery /FO CSV /V ...")
    result = run_command(
        ["driverquery", "/FO", "CSV", "/V"],
        capture=True,
    )
    if result.code != 0:
        logger.log("ERROR", "driverquery failed.")
        input("Press Enter to continue...")
        return

    lines = result.stdout.splitlines()
    if len(lines) < 2:
        logger.log("INFO", "No driver data returned.")
        input("Press Enter to continue...")
        return

    import csv
    import io

    reader = csv.reader(io.StringIO(result.stdout))
    all_rows = list(reader)
    if len(all_rows) < 2:
        logger.log("INFO", "No driver data parsed.")
        input("Press Enter to continue...")
        return

    headers = all_rows[0]
    data_rows = all_rows[1:]

    try:
        name_idx = headers.index("Module Name")
        type_idx = headers.index("Driver Type")
        date_idx = headers.index("Link Date")
    except ValueError:
        name_idx = headers.index("Module Name") if "Module Name" in headers else 0
        type_idx = 3 if len(headers) > 3 else 1
        date_idx = 4 if len(headers) > 4 else 2

    total = len(data_rows)
    type_counts: dict[str, int] = {}
    print()
    print(f"  Total drivers: {total}")
    print()
    print(f"  {'Driver Name':<35} {'Type':<18} {'Date':<20}")
    print(f"  {'-' * 35} {'-' * 18} {'-' * 20}")

    for row in data_rows:
        name = row[name_idx] if len(row) > name_idx else "?"
        d_type = row[type_idx] if len(row) > type_idx else "?"
        date = row[date_idx] if len(row) > date_idx else "?"
        type_counts[d_type] = type_counts.get(d_type, 0) + 1
        print(f"  {name:<35} {d_type:<18} {date:<20}")
        logger.log_only("INFO", f"Driver: {name} type={d_type} date={date}")

    print()
    print("  --- Driver Type Summary ---")
    for d_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"    {d_type:<25} {count:>5}")
    print(f"    {'TOTAL':<25} {total:>5}")

    logger.log_only("INFO", f"Drivers: {total} total, {len(type_counts)} types")
    logger.log_only("INFO", "DRIVER INVENTORY COMPLETE")
    input("Press Enter to continue...")
