# PyInstaller spec for LDLWinToolBox

import tomllib
from pathlib import Path

from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)

here = Path.cwd()
pyproject = here / "pyproject.toml"
data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
app_ver = data["project"]["version"]

ver_parts = tuple(int(x) for x in app_ver.split("."))
while len(ver_parts) < 4:
    ver_parts += (0,)

vers = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=ver_parts,
        prodvers=ver_parts,
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        StringFileInfo([
            StringTable(
                "040904B0",
                [
                    StringStruct("FileDescription", "LDL Windows ToolBox"),
                    StringStruct("FileVersion", app_ver),
                    StringStruct("InternalName", "LDLWinToolBox"),
                    StringStruct("LegalCopyright", ""),
                    StringStruct("OriginalFilename", "LDLWinToolBox.exe"),
                    StringStruct("ProductName", "LDL Windows ToolBox"),
                    StringStruct("ProductVersion", app_ver),
                ],
            )
        ]),
        VarFileInfo([VarStruct("Translation", [0x0409, 1200])]),
    ],
)

vers_file = here / "build" / "version_info.txt"
vers_file.parent.mkdir(parents=True, exist_ok=True)
vers_file.write_text(repr(vers), encoding="utf-8")

a = Analysis(  # noqa: F821
    ["ldlwintoolbox.py"],
    pathex=[],
    binaries=[],
    datas=[("features", "features"), ("pyproject.toml", ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter", "idlelib", "turtle", "test", "distutils",
        "unittest", "pdb", "pyparsing", "matplotlib",
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)  # noqa: F821

exe = EXE(  # noqa: F821
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="LDLWinToolBox",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=str(vers_file),
)
