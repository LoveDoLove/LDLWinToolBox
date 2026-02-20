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
    A cohesive, menu-driven Windows Batch utility that safely automates advanced system cleanup, integrity repair, components update, and NVMe SSD optimizations.
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

The LDL Windows ToolBox is a standalone Windows Batch script (`LDLWinToolBox.bat`) that effectively combines administrative privileges checks, system garbage collection, script verifications, and SSD TRIM optimization into a single, cohesive menu-driven interface.

It safely automates otherwise tedious system administration tasks while maintaining comprehensive, timestamped logs (`LDLWinToolBox_yyMMddHHmmss.log`) of all actions to ensure complete historical records and safety.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Windows Batch][Batch-shield]][Batch-url]
- [![PowerShell][PowerShell-shield]][PowerShell-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Windows 10 or Windows 11
- Administrator rights (the script will automatically securely request this using `RunAs` if launched without it)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/LoveDoLove/LDLWinToolBox.git
   ```
2. Double-click on `LDLWinToolBox.bat` to launch the interactive menu.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Upon launching, the interactive menu provides numerical options (1-8) to execute tools:

- **[1] Advanced System Cleanup**: Deeply cleans temporary system data, calculates Space Freed (MB).
- **[2] System Integrity Repair**: Executes `SFC` and `DISM` to scan and repair corrupt OS files.
- **[3] Windows Component Store Cleanup**: Removes superseded Windows Update install files (WinSxS).
- **[4] Update All Installed Apps**: Silently updates all `winget`-installed apps.
- **[5] Complete Network Reset**: Resets Winsock, TCP/IP, and DNS cache entirely.
- **[6] Clear Event Viewer Logs**: Flushes system, security, and application logs.
- **[7] Manual SSD TRIM**: Optimized for NVMe drives, triggers manual SSD re-trim using Windows defrag.

_For more detailed background checks on each process, please refer to [ANALYSIS.md](ANALYSIS.md) and [PROMPT_GUIDE.md](PROMPT_GUIDE.md)_

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
- [RunAs PowerShell Module](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-7.2)
- [Winget Tool](https://docs.microsoft.com/en-us/windows/package-manager/winget/)

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
[Batch-shield]: https://img.shields.io/badge/Windows_Batch-0078D6?style=for-the-badge&logo=windows&logoColor=white
[Batch-url]: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands
[PowerShell-shield]: https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white
[PowerShell-url]: https://docs.microsoft.com/en-us/powershell/
