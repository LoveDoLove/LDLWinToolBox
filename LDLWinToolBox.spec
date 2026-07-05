# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for LDLWinToolBox

import tomllib
from pathlib import Path

here = Path(__file__).parent
pyproject = here / "pyproject.toml"
data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
app_ver = data["project"]["version"]

a = Analysis(
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
pyz = PYZ(a.pure)

exe = EXE(
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
    version=app_ver,
)
