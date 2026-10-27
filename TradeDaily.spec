# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for TradeDaily.
Supports Linux, Windows, and macOS with standalone directory or application bundle packaging.
"""

import os
import platform
import sys
from PyInstaller.utils.hooks import collect_all, copy_metadata

block_cipher = None

# Collect Plotly and its utilities dynamically (all graph_objs submodules & schemas)
plotly_datas, plotly_binaries, plotly_hidden = collect_all("plotly")
utils_datas, utils_binaries, utils_hidden = collect_all("_plotly_utils")
narwhals_meta = copy_metadata("narwhals")

datas = [
    ("assets", "assets"),
] + plotly_datas + utils_datas + narwhals_meta

binaries = plotly_binaries + utils_binaries

hidden_imports = [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebEngineCore",
    "PySide6.QtPrintSupport",
    "PySide6.QtSvg",
    "PySide6.QtNetwork",
    "sqlite3",
    "rc_icons",
] + plotly_hidden + utils_hidden


excludes = [
    "tkinter",
    "matplotlib",
    "scipy",
    "IPython",
    "ipykernel",
    "notebook",
    "pytest",
    "_pytest",
    "ruff",
]

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

is_windows = sys.platform.startswith("win")
is_darwin = sys.platform == "darwin"

icon_file = "assets/icon.png"
if is_windows:
    icon_file = "assets/icon.ico"
elif is_darwin:
    icon_file = "assets/icon.icns"

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TradeDaily",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file if os.path.exists(icon_file) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="TradeDaily",
)

if is_darwin:
    icns_path = "assets/icon.icns" if os.path.exists("assets/icon.icns") else None
    app = BUNDLE(
        coll,
        name="TradeDaily.app",
        icon=icns_path,
        bundle_identifier="com.meliheliguzel.tradedaily",
        info_plist={
            "CFBundleName": "TradeDaily",
            "CFBundleDisplayName": "TradeDaily",
            "CFBundleGetInfoString": "Modern Desktop Trading Journal & Analytics",
            "CFBundleIdentifier": "com.meliheliguzel.tradedaily",
            "CFBundleVersion": "0.1.0",
            "CFBundleShortVersionString": "0.1.0",
            "NSHumanReadableCopyright": "Copyright © 2026 Melih Eliguzel. MIT License.",
            "NSHighResolutionCapable": True,
        },
    )
