# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec — Windows build (run: python -m PyInstaller WindSnowCalc.spec)
import os
from PyInstaller.utils.hooks import collect_all

SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))
ICON = os.path.join(SPEC_DIR, "assets", "app.ico")

block_cipher = None

datas = [
    ("index.html", "."),
    ("data/cities.js", "data"),
    ("data/global.js", "data"),
    ("data/meta.js", "data"),
    ("data/world-map.svg", "data"),
    ("js/app.js", "js"),
]

hiddenimports = []
binaries = []

try:
    tmp = collect_all("webview")
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]
except Exception:
    hiddenimports.append("webview")

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="WindSnowCalc",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version="version_info.txt",
    icon=ICON if os.path.isfile(ICON) else None,
)
