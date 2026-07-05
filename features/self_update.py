from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

from toolbox_base import MENU_LOGO, TOOLBOX_VERSION, Logger, clear_screen, run_command


def _parse_tag(tag: str) -> tuple[int, ...]:
    clean = tag.lstrip("v").lstrip("V")
    parts = re.split(r"[._\-]", clean)
    result: list[int] = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            break
    return tuple(result)


def _is_newer(remote_tag: str, local_ver: str) -> bool:
    remote_parts = _parse_tag(remote_tag)
    local_parts = _parse_tag(local_ver)
    if not remote_parts:
        return False
    if not local_parts:
        return True
    return remote_parts > local_parts


def self_update(logger: Logger) -> None:
    clear_screen()
    print(MENU_LOGO)
    print("              CHECK FOR UPDATES")
    print(MENU_LOGO)
    logger.section("Check for Updates")

    print(f"  Local version : {TOOLBOX_VERSION}")
    logger.log_only("INFO", f"Local version: {TOOLBOX_VERSION}")

    remote_url = "https://api.github.com/repos/LoveDoLove/LDLWinToolBox/releases/latest"
    print(f"  Checking      : {remote_url}")
    logger.log_only("INFO", f"Querying GitHub API: {remote_url}")

    try:
        req = urllib.request.Request(
            remote_url,
            headers={"User-Agent": "LDLWinToolBox/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        logger.log("WARN", f"GitHub API returned HTTP {e.code}")
        print(f"  GitHub API error: HTTP {e.code}")
        input("Press Enter to continue...")
        return
    except (urllib.error.URLError, OSError, ValueError) as e:
        logger.log("WARN", f"Failed to reach GitHub: {e}")
        print(f"  Network error: {e}")
        input("Press Enter to continue...")
        return

    remote_tag = data.get("tag_name", "")
    remote_name = data.get("name", "")
    remote_body = data.get("body", "")
    remote_url_page = data.get("html_url", "")

    if not remote_tag:
        logger.log("WARN", "No tag_name found in response.")
        input("Press Enter to continue...")
        return

    print(f"  Remote version: {remote_tag}")
    logger.log_only("INFO", f"Remote version: {remote_tag} ({remote_name})")

    if _is_newer(remote_tag, TOOLBOX_VERSION):
        print()
        print(f"  >>> A new version is available: {remote_tag}")
        print(f"  >>> {remote_url_page}")
        print()
        if remote_body:
            short = remote_body.strip()[:500]
            print(f"  Release notes:")
            for line in short.splitlines()[:10]:
                print(f"    {line}")
        print()
        from urllib.request import urlopen
        try:
            req_check = urllib.request.Request(
                remote_url_page,
                method="HEAD",
            )
            with urllib.request.urlopen(req_check, timeout=5):
                pass
            if prompt_yes_no(
                logger,
                "Open download page in browser? (Y/N): ",
                "Open Download Page",
            ):
                import webbrowser
                webbrowser.open(remote_url_page)
                logger.log_only("INFO", f"Browser opened to {remote_url_page}")
        except Exception:
            print(f"  Download: {remote_url_page}")
    else:
        print()
        print("  >>> You are on the latest version.")
        logger.log_only("INFO", "Up to date.")

    logger.log_only("INFO", "UPDATE CHECK COMPLETE")
    input("Press Enter to continue...")
