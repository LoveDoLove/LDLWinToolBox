from __future__ import annotations

import json
import platform
import shutil
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from toolbox_base import (
    MENU_LOGO,
    Logger,
    clear_screen,
    prompt_yes_no,
    run_and_log,
)

VIVE_REPO = "thebookisclosed/ViVe"
VIVE_TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools" / "vivetool"
LOW_LATENCY_IDS = ["58989092", "60716524", "61391826"]
LOW_LATENCY_DESC = {
    "58989092": "Core Low Latency Profile",
    "60716524": "Core low latency mode for background operations",
    "61391826": "Optimizes application launch speed",
}


def detect_architecture() -> str:
    machine = platform.machine().lower()
    return "SnapdragonArm64" if machine in ("arm64", "aarch64") else "IntelAmd"


def _fetch_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": "LDLWinToolBox/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        OSError,
        json.JSONDecodeError,
    ):
        return None


def _download_file(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "LDLWinToolBox/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            with dest.open("wb") as f:
                shutil.copyfileobj(resp, f)
        return True
    except (urllib.error.URLError, OSError):
        return False


def ensure_vivetool(logger: Logger) -> Path | None:
    VIVE_TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    exe = VIVE_TOOLS_DIR / "ViVeTool.exe"
    ver_file = VIVE_TOOLS_DIR / "version.txt"
    cached_ver = ver_file.read_text(encoding="utf-8").strip() if ver_file.exists() else ""

    arch = detect_architecture()
    logger.log_only("INFO", f"Detected architecture: {arch}")

    release = _fetch_json(f"https://api.github.com/repos/{VIVE_REPO}/releases/latest")
    if release is not None:
        tag = release["tag_name"]
        if tag != cached_ver:
            logger.log("INFO", f"Downloading ViVeTool {tag}...")
            suffix = f"{arch}.zip"
            asset = next(
                (a for a in release["assets"] if a["name"].endswith(suffix)),
                None,
            )
            if asset is None:
                logger.log("ERROR", f"No ViVeTool asset for {arch}.")
                return exe if exe.exists() else None
            zip_path = VIVE_TOOLS_DIR / asset["name"]
            logger.log("INFO", f"  Source: {asset['browser_download_url']}")
            if not _download_file(asset["browser_download_url"], zip_path):
                logger.log("ERROR", "Download failed.")
                zip_path.unlink(missing_ok=True)
                return exe if exe.exists() else None
            logger.log("INFO", "Extracting...")
            try:
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(VIVE_TOOLS_DIR)
            except zipfile.BadZipFile:
                logger.log("ERROR", "Corrupted download.")
                zip_path.unlink(missing_ok=True)
                return exe if exe.exists() else None
            zip_path.unlink(missing_ok=True)
            ver_file.write_text(tag, encoding="utf-8")
            logger.log("INFO", f"ViVeTool {tag} ready.")
        else:
            logger.log("INFO", f"ViVeTool {tag} is up to date.")
    elif exe.exists():
        logger.log("WARN", "Could not check for updates. Using cached ViVeTool.")
    else:
        logger.log(
            "ERROR",
            "ViVeTool not found and could not be downloaded.",
        )
        return None
    return exe if exe.exists() else None


def low_latency_mode(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("            LOW LATENCY MODE")
    print(MENU_LOGO)
    print("This feature uses ViVeTool to manage Windows low")
    print("latency feature flags for better system responsiveness.")
    print()
    print("Feature IDs:")
    for fid in LOW_LATENCY_IDS:
        print(f"  {fid} — {LOW_LATENCY_DESC[fid]}")
    print(MENU_LOGO)
    logger.section("Low Latency Mode")

    arch = detect_architecture()
    logger.log_only("INFO", f"Detected architecture: {arch}")

    vivetool = ensure_vivetool(logger)
    if vivetool is None:
        input("Press Enter to continue...")
        return

    while True:
        clear_screen()
        print(MENU_LOGO)
        print("            LOW LATENCY MODE")
        print(MENU_LOGO)
        print(f"Architecture : {arch}")
        print(f"ViVeTool     : {vivetool}")
        ver_path = VIVE_TOOLS_DIR / "version.txt"
        current_ver = (
            ver_path.read_text(encoding="utf-8").strip() if ver_path.exists() else "unknown"
        )
        print(f"Version      : {current_ver}")
        print(MENU_LOGO)
        print("[1] Check Status")
        print("[2] Enable Low Latency Mode")
        print("[3] Disable Low Latency Mode")
        print("[4] Return to Main Menu")
        print(MENU_LOGO)
        choice = input("Select an option: ").strip()
        logger.log_only("INFO", f"Low Latency Mode sub-menu selection: {choice}")

        if choice == "1":
            logger.section("Low Latency Mode — Status Check")
            result = run_and_log(
                logger,
                [
                    str(vivetool),
                    "/query",
                    f"/id:{','.join(LOW_LATENCY_IDS)}",
                ],
                "vivetool /query",
            )
            if result.stdout:
                logger.write_raw(result.stdout)
                print(result.stdout)
            input("Press Enter to continue...")
        elif choice == "2":
            clear_screen()
            print(MENU_LOGO)
            print("            LOW LATENCY MODE")
            print(MENU_LOGO)
            print("WARNING: This enables system-wide low latency")
            print("features to improve responsiveness.")
            print("-> A reboot may be required to take effect.")
            print("-> Can be safely reverted by disabling.")
            print(MENU_LOGO)
            logger.section("Low Latency Mode — Enable")
            if not prompt_yes_no(
                logger,
                "Enable Low Latency Mode? (Y/N): ",
                "Low Latency Mode Enable",
            ):
                continue
            result = run_and_log(
                logger,
                [
                    str(vivetool),
                    "/enable",
                    f"/id:{','.join(LOW_LATENCY_IDS)}",
                ],
                "vivetool /enable",
            )
            if result.stdout:
                logger.write_raw(result.stdout)
                print(result.stdout)
            input("Press Enter to continue...")
        elif choice == "3":
            clear_screen()
            print(MENU_LOGO)
            print("            LOW LATENCY MODE")
            print(MENU_LOGO)
            print("WARNING: This disables low latency features,")
            print("restoring default system behavior.")
            print("-> A reboot may be required to take effect.")
            print(MENU_LOGO)
            logger.section("Low Latency Mode — Disable")
            if not prompt_yes_no(
                logger,
                "Disable Low Latency Mode? (Y/N): ",
                "Low Latency Mode Disable",
            ):
                continue
            result = run_and_log(
                logger,
                [
                    str(vivetool),
                    "/disable",
                    f"/id:{','.join(LOW_LATENCY_IDS)}",
                ],
                "vivetool /disable",
            )
            if result.stdout:
                logger.write_raw(result.stdout)
                print(result.stdout)
            input("Press Enter to continue...")
        elif choice == "4":
            logger.log("INFO", "Low Latency Mode returned to main menu.")
            return
        else:
            logger.log(
                "WARN",
                f"Invalid Low Latency Mode selection: {choice}",
            )
