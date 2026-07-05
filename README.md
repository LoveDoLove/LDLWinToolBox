<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License 2.0][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/LoveDoLove/LDLWinToolBox">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">LDL Windows ToolBox</h3>

  <p align="center">
    A cohesive, menu-driven Windows utility for system cleanup, repair, network reset, performance tuning, security management, diagnostics, recovery, and reporting — all in a single Python-first toolbox.
    <br />
    <a href="https://github.com/LoveDoLove/LDLWinToolBox"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/LoveDoLove/LDLWinToolBox">View Demo</a>
    &middot;
    <a href="https://github.com/LoveDoLove/LDLWinToolBox/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/LoveDoLove/LDLWinToolBox/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

The LDL Windows ToolBox is a Python-first Windows utility powered by `uv`, with `LDLWinToolBox.bat` as a thin launcher for `ldlwintoolbox.py`. It combines administrative privilege elevation, system cleanup, repair flows, network reset, BitLocker planning, browser AI cleanup, SSD TRIM, low-latency configuration, recovery tools, diagnostics, and reporting into a single cohesive menu-driven interface.

The project follows a modular architecture:
- `LDLWinToolBox.bat` — thin Batch launcher for the Python entry point
- `ldlwintoolbox.py` — entry point with admin detection, read-only mode, and main menu dispatch
- `toolbox_base.py` — shared infrastructure (Logger, CommandResult, run/command/prompt/restore-point helpers)
- `features/` — one file per feature, each importing only from `toolbox_base`
- `config/exclusions.json` — user-managed exclusion list for cleanup operations
- `logs/` — structured timestamped session logs

The tool runs with zero external dependencies (Python standard library + built-in Windows commands). When launched without administrator privileges, it automatically enters **read-only mode**, hiding destructive features and allowing safe inspection of system information, diagnostics, and logs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][Python-shield]][Python-url]
- [![uv][uv-shield]][uv-url]
- [![PowerShell][PowerShell-shield]][PowerShell-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Windows 10 or Windows 11
- Administrator rights (optional — the tool supports read-only mode without elevation; destructive features auto-request UAC if needed)
- [uv](https://docs.astral.sh/uv/) (recommended) — the launcher falls back to `python` if uv is not available

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/LoveDoLove/LDLWinToolBox.git
   ```
2. Double-click `LDLWinToolBox.bat` to launch the interactive menu, or run:
   ```sh
   uv run -- python ldlwintoolbox.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Upon launching, the interactive menu provides numbered options organized into logical groups. When running without administrator privileges, the tool enters **read-only mode** — admin features (1–11) are hidden and a "[R] Restart as Administrator" shortcut is provided.

### System Cleanup (1–3)
- **[1] Advanced System Cleanup**: Deeply cleans temporary system/user data, Prefetch, SoftwareDistribution downloads; selective target sub-menu with exclusion list integration; calculates space freed (MB).
- **[2] Windows Component Store Cleanup (WinSxS)**: Removes superseded Windows Update install files using DISM.
- **[3] Clear Event Viewer Logs**: Flushes all Windows event logs via wevtutil.

### System Repair & Update (4–5)
- **[4] System Integrity Repair (SFC + DISM)**: Scans and repairs corrupt OS files with SFC /scannow and DISM /RestoreHealth; shows [1/2] [2/2] progress hints.
- **[5] Update All Installed Apps**: Silently updates all winget-installed applications.

### Network (6)
- **[6] Complete Network Reset**: Resets Winsock, TCP/IP stack, and DNS cache; requires restart.

### Performance (7–8)
- **[7] Manual SSD TRIM**: Triggers manual SSD re-trim with `defrag /L /V` on a user-selected volume.
- **[8] Low Latency Mode (ViVeTool)**: Auto-detects CPU architecture (Intel/AMD x64 or Snapdragon ARM64), downloads ViVeTool, and manages Windows feature flags (IDs 58989092, 60716524, 61391826) with a query/enable/disable sub-menu.

### Security & Privacy (9–10)
- **[9] Disable BitLocker (Plan)**: Shows status for all drives, validates selection, then starts `manage-bde -off` after `DISABLE` confirmation.
- **[10] Kill Browser AI**: Executes a remote PowerShell cleanup script to disable on-device browser AI features after `KILL` confirmation.

### Recovery (11)
- **[11] Recovery & Safe Mode Tools**: Sub-menu for boot configuration (bcdedit), Safe Mode (minimal / networking / command prompt), WinRE status & enable/disable, and restore normal boot.

### Diagnostics (12–19)
- **[12] System Information**: OS edition/build, CPU name/logical cores, RAM usage, system drive usage, uptime via ctypes + winreg.
- **[13] Windows Update Status**: wuauserv service state, Auto Update registry config, last install/search dates, runs UsoClient scan.
- **[14] Defender Status & Quick Scan**: Get-MpComputerStatus fields, optional MpCmdRun signature update, optional Start-MpQuickScan.
- **[15] Service Health Check**: Status of 20 critical Windows services (wuauserv, BITS, EventLog, Dhcp, etc.).
- **[16] Disk Health & SMART Summary**: Get-PhysicalDisk with StorageReliabilityCounter (wear, temperature, errors), volume summary, SMART counters.
- **[17] Driver Inventory**: Parses `driverquery /FO CSV` with type/date summary.
- **[18] Network Snapshot**: Captures `ipconfig /all`, `route print`, `netsh interface`, `netstat -ano` to file and log; optional diff with previous snapshot.
- **[19] Export Logs & Report**: Generates a plain-text session report (features run, commands, warnings) and archives all logs to ZIP under `exports/`.

### Tools (20–22)
- **[20] View Log History**: Lists recent toolbox logs and opens the selected file with a paged console viewer.
- **[21] Check for Updates**: Queries the GitHub Releases API, compares with local version (1.0.3), optionally opens browser for download.
- **[22] Cleanup Exclusion List**: Manages a JSON-based exclusion list (`config/exclusions.json`); paths matching exclusions are skipped during cleanup.

Each run writes a structured log under `logs/` with a session header, environment summary, section markers, user cancellations, command start/end markers, and exit codes. Long-running or destructive operations display warnings and require explicit (Y/N) confirmation. Optional system restore points can be created before destructive features.

_For AI maintenance context and persistent project rules, refer to [AGENTS.md](AGENTS.md), [MEMORY.md](MEMORY.md), and [memory/tasks.md](memory/tasks.md)._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

The project has completed all 6 planned development phases:

- **Phase 1**: Foundation — shared helpers, input validation, confirmation flow, restore points
- **Phase 2**: Safety & Clarity — progress hints, conservative cleanup defaults
- **Phase 3**: New Feature Modules — system info, Windows Update, Defender, service health
- **Phase 4**: Reporting & Export — disk SMART, driver inventory, network snapshot, log export
- **Phase 5**: Efficiency & Maintenance — self-update check, read-only mode, PowerShell batching
- **Phase 6**: Advanced Features — recovery tools, selective cleanup, exclusion list

Future improvements are tracked as [open issues](https://github.com/LoveDoLove/LDLWinToolBox/issues) and in [memory/feature-ideas.md](memory/feature-ideas.md).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/LoveDoLove/LDLWinToolBox/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=LoveDoLove/LDLWinToolBox" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->

## License

Distributed under the Apache License 2.0. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

LoveDoLove - [Telegram Channel](https://t.me/lovedoloveofficialchannel) - [Discord](https://discord.com/invite/FyYEmtRCRE)

Project Link: [https://github.com/LoveDoLove/LDLWinToolBox](https://github.com/LoveDoLove/LDLWinToolBox)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [ViVeTool](https://github.com/thebookisclosed/ViVe) by thebookisclosed
- [Windows UAC / ShellExecuteW](https://learn.microsoft.com/windows/win32/api/shellapi/nf-shellapi-shellexecutew)
- [Winget Tool](https://docs.microsoft.com/en-us/windows/package-manager/winget/)
- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/LoveDoLove/LDLWinToolBox.svg?style=for-the-badge
[contributors-url]: https://github.com/LoveDoLove/LDLWinToolBox/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/LoveDoLove/LDLWinToolBox.svg?style=for-the-badge
[forks-url]: https://github.com/LoveDoLove/LDLWinToolBox/network/members
[stars-shield]: https://img.shields.io/github/stars/LoveDoLove/LDLWinToolBox.svg?style=for-the-badge
[stars-url]: https://github.com/LoveDoLove/LDLWinToolBox/stargazers
[issues-shield]: https://img.shields.io/github/issues/LoveDoLove/LDLWinToolBox.svg?style=for-the-badge
[issues-url]: https://github.com/LoveDoLove/LDLWinToolBox/issues
[license-shield]: https://img.shields.io/github/license/LoveDoLove/LDLWinToolBox.svg?style=for-the-badge
[license-url]: https://github.com/LoveDoLove/LDLWinToolBox/blob/master/LICENSE
[Python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[uv-shield]: https://img.shields.io/badge/uv-111111?style=for-the-badge&logo=python&logoColor=white
[uv-url]: https://docs.astral.sh/uv/
[PowerShell-shield]: https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white
[PowerShell-url]: https://docs.microsoft.com/en-us/powershell/
