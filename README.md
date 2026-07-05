<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->

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
    A cohesive, menu-driven Windows utility that safely automates system cleanup, integrity repair, component updates, network reset, BitLocker decryption planning, browser AI cleanup, SSD TRIM, and low-latency configuration workflows.
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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

The LDL Windows ToolBox is a Python-first Windows utility powered by `uv`, with `LDLWinToolBox.bat` acting as a thin launcher for `ldlwintoolbox.py`. It combines administrative privilege elevation, system cleanup, repair flows, network reset, BitLocker decryption planning, browser AI cleanup, SSD TRIM optimization, and low-latency configuration into a single cohesive menu-driven interface.

The project follows a modular architecture:
- `ldlwintoolbox.py` — thin entry point with admin logic and main menu dispatch
- `toolbox_base.py` — shared infrastructure (Logger, CommandResult, run/command/prompt helpers)
- `features/` — one file per feature, each importing only from `toolbox_base`

All operations are safely logged with comprehensive timestamped records under `logs\LDLWinToolBox_yyMMddHHmmss.log`. The tool uses only Python standard library and built-in Windows commands; zero external dependencies are required.

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
- Administrator rights (the tool automatically requests elevation via UAC if launched without them)
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

Upon launching, the interactive menu provides numbered options organized into logical groups:

**System Cleanup**
- **[1] Advanced System Cleanup**: Deeply cleans temporary system data, prefetch, SoftwareDistribution downloads, vendor driver roots; calculates space freed (MB).
- **[2] Windows Component Store Cleanup (WinSxS)**: Removes superseded Windows Update install files using DISM.
- **[3] Clear Event Viewer Logs**: Flushes system, security, and application logs via wevtutil.

**System Repair & Update**
- **[4] System Integrity Repair (SFC + DISM)**: Scans and repairs corrupt OS files with SFC and DISM RestoreHealth.
- **[5] Update All Installed Apps**: Silently updates all winget-installed applications.

**Network**
- **[6] Complete Network Reset**: Resets Winsock, TCP/IP stack, and DNS cache entirely.

**Performance**
- **[7] Manual SSD TRIM**: Triggers manual SSD re-trim using the Windows defrag utility.
- **[8] Low Latency Mode (ViVeTool)**: Auto-detects CPU architecture (Intel/AMD or Snapdragon ARM64), downloads ViVeTool, and manages Windows low-latency feature flags (IDs 58989092, 60716524, 61391826) with query/enable/disable sub-menu.

**Security & Privacy**
- **[9] Disable BitLocker (Plan)**: Shows BitLocker status, validates a selected drive, then starts decryption after typing `DISABLE`.
- **[10] Kill Browser AI**: Executes a configured remote PowerShell cleanup command to disable on-device browser AI features after typing `KILL`.

**Tools**
- **[11] View Log History**: Lists recent toolbox logs and opens the selected log with paged console viewing.
- **[12] Exit**: Closes the toolbox.

Each run writes a structured log under `logs\` with a session header, environment summary, section markers, user cancellations, command start/end markers, and exit codes for key system commands.

_For AI maintenance context and persistent project rules, refer to [AGENTS.md](AGENTS.md), [MEMORY.md](MEMORY.md), and [memory/tasks.md](memory/tasks.md)._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

See the [open issues](https://github.com/LoveDoLove/LDLWinToolBox/issues) for a full list of proposed features (and known issues).

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

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
