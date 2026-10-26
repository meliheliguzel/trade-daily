import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.build import (
    clean_build_dirs,
    create_linux_desktop_file,
    ensure_icons,
    get_project_root,
    main,
    run_build,
)


def test_get_project_root():
    root = get_project_root()
    assert isinstance(root, Path)
    assert (root / "main.py").exists()


def test_clean_build_dirs(tmp_path):
    build_dir = tmp_path / "build"
    dist_dir = tmp_path / "dist"
    build_dir.mkdir()
    dist_dir.mkdir()

    assert build_dir.exists()
    assert dist_dir.exists()

    clean_build_dirs(tmp_path)

    assert not build_dir.exists()
    assert not dist_dir.exists()


def test_create_linux_desktop_file(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    dist_bin = dist_dir / "TradeDaily"
    dist_bin.touch()

    create_linux_desktop_file(tmp_path, dist_bin)

    desktop_file = dist_dir / "TradeDaily.desktop"
    assert desktop_file.exists()
    content = desktop_file.read_text(encoding="utf-8")
    assert "[Desktop Entry]" in content
    assert "Exec=" in content
    assert "StartupWMClass=TradeDaily" in content


def test_ensure_icons_existing(tmp_path):
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    png = assets_dir / "icon.png"
    ico = assets_dir / "icon.ico"
    png.write_text("fake_png")
    ico.write_text("fake_ico")

    # Should not re-extract if both exist
    ensure_icons(tmp_path)
    assert png.read_text() == "fake_png"
    assert ico.read_text() == "fake_ico"


def test_run_build_skip_build():
    # Calling run_build with skip_build=True should validate and return 0
    code = run_build(clean=True, skip_build=True)
    assert code == 0


@patch("subprocess.run")
def test_run_build_mocked_success(mock_sub):
    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_sub.return_value = mock_proc

    # Test onedir build
    code_onedir = run_build(onefile=False, clean=False, skip_build=False)
    assert code_onedir == 0

    # Test onefile build
    code_onefile = run_build(onefile=True, clean=False, skip_build=False)
    assert code_onefile == 0


@patch("subprocess.run")
def test_run_build_mocked_failure(mock_sub):
    mock_proc = MagicMock()
    mock_proc.returncode = 42
    mock_sub.return_value = mock_proc

    code = run_build(onefile=False, clean=False, skip_build=False)
    assert code == 42


def test_build_main_cli(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["tradedaily-build", "--skip-build"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
