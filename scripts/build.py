#!/usr/bin/env python3
"""
Cross-Platform Build and Packaging Script for TradeDaily.
Supports building standalone bundles for Linux, Windows, and macOS using PyInstaller.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Returns the absolute path to the project root directory."""
    return Path(__file__).resolve().parent.parent


def ensure_icons(root: Path) -> None:
    """Ensures application icons (PNG and ICO) are extracted and present in assets/."""
    assets_dir = root / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    png_path = assets_dir / "icon.png"
    ico_path = assets_dir / "icon.ico"

    if not png_path.exists() or not ico_path.exists():
        print("Extracting application icons from compiled Qt resources...")
        try:
            from PySide6.QtGui import QPixmap
            from PySide6.QtWidgets import QApplication

            import rc_icons  # noqa: F401

            _ = QApplication.instance() or QApplication([])
            pixmap = QPixmap(":/icons/td_icon_2.jpg")
            if not pixmap.isNull():
                if not png_path.exists():
                    pixmap.save(str(png_path), "PNG")
                    print(f"  [+] Saved: {png_path}")
                if not ico_path.exists():
                    pixmap.save(str(ico_path), "ICO")
                    print(f"  [+] Saved: {ico_path}")
            else:
                print("  [!] Warning: Could not load td_icon_2.jpg from Qt resources.")
        except Exception as e:
            print(f"  [!] Warning while extracting icons: {e}")


def clean_build_dirs(root: Path) -> None:
    """Removes previous build and dist directories."""
    print("Cleaning previous build artifacts...")
    for folder in ["build", "dist"]:
        folder_path = root / folder
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"  [-] Removed: {folder_path}")


def create_linux_desktop_file(root: Path, dist_bin: Path) -> None:
    """Creates a standard FreeDesktop .desktop entry file for Linux distribution."""
    desktop_content = """[Desktop Entry]
Type=Application
Name=TradeDaily
Comment=Modern Desktop Trading Journal & Analytics
Exec=TradeDaily
Icon=TradeDaily
Terminal=false
Categories=Office;Finance;
StartupWMClass=TradeDaily
"""
    desktop_path = root / "dist" / "TradeDaily.desktop"
    desktop_path.write_text(desktop_content, encoding="utf-8")
    desktop_path.chmod(0o755)
    print(f"  [+] Created Linux desktop launcher: {desktop_path}")


def run_build(onefile: bool = False, clean: bool = False, skip_build: bool = False) -> int:
    """Executes the PyInstaller build process."""
    root = get_project_root()
    os.chdir(root)

    current_os = platform.system().lower()
    print("=" * 60)
    print("TradeDaily Cross-Platform Build Tool")
    print(f"Operating System: {platform.system()} ({platform.machine()})")
    print(f"Python Version:   {platform.python_version()}")
    print(f"Packaging Mode:   {'One-File (Single Binary)' if onefile else 'One-Directory (Recommended Bundle)'}")
    print("=" * 60)

    if clean:
        clean_build_dirs(root)

    ensure_icons(root)

    spec_file = root / "TradeDaily.spec"
    if not spec_file.exists():
        print(f"[!] Error: Specification file not found at {spec_file}")
        return 1

    if skip_build:
        print("[*] Skipping actual compilation (--skip-build set).")
        return 0

    cmd = [sys.executable, "-m", "PyInstaller"]

    if clean:
        cmd.append("--clean")

    if onefile:
        # Build onefile directly with essential flags
        icon_path = root / "assets" / ("icon.ico" if current_os == "windows" else "icon.png")
        cmd.extend([
            "main.py",
            "--name=TradeDaily",
            "--noconsole",
            "--onefile",
            f"--icon={icon_path}",
            "--collect-data=plotly",
            "--copy-metadata=plotly",
            "--copy-metadata=narwhals",
            "--add-data=assets:assets",
            "--hidden-import=PySide6.QtWebEngineWidgets",
            "--hidden-import=PySide6.QtWebEngineCore",
            "--hidden-import=PySide6.QtPrintSupport",
            "--hidden-import=PySide6.QtSvg",
            "--hidden-import=plotly.express",
            "--hidden-import=plotly.graph_objects",
            "--hidden-import=plotly.io",
            "--hidden-import=rc_icons",
            "--exclude-module=tkinter",
            "--exclude-module=matplotlib",
            "--exclude-module=scipy",
            "--exclude-module=pytest",
        ])
    else:
        # Use TradeDaily.spec for clean, fully configured onedir / macOS bundle
        cmd.append(str(spec_file))

    print(f"Running build command: {' '.join(cmd)}\n")
    proc = subprocess.run(cmd)

    if proc.returncode != 0:
        print(f"\n[!] Build failed with exit code: {proc.returncode}")
        return proc.returncode

    dist_dir = root / "dist"
    print("\n" + "=" * 60)
    print("BUILD SUCCESSFUL!")
    print("=" * 60)

    if current_os == "windows":
        exe_path = dist_dir / ("TradeDaily.exe" if onefile else "TradeDaily/TradeDaily.exe")
        print(f"Windows Executable: {exe_path}")
    elif current_os == "darwin":
        app_path = dist_dir / "TradeDaily.app"
        print(f"macOS Application Bundle: {app_path}")
    else:
        bin_path = dist_dir / ("TradeDaily" if onefile else "TradeDaily/TradeDaily")
        print(f"Linux Binary: {bin_path}")
        if bin_path.exists():
            create_linux_desktop_file(root, bin_path)

    return 0


def main():
    parser = argparse.ArgumentParser(description="Build and package TradeDaily for distribution.")
    parser.add_argument("--clean", action="store_true", help="Clean build directories before compilation.")
    parser.add_argument("--onefile", action="store_true", help="Compile into a single standalone executable file.")
    parser.add_argument("--skip-build", action="store_true", help="Prepare assets and validate without running PyInstaller.")
    args = parser.parse_args()

    sys.exit(run_build(onefile=args.onefile, clean=args.clean, skip_build=args.skip_build))


if __name__ == "__main__":
    main()
