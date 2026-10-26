import os
from pathlib import Path

from module.tools.file.tool import control_file_create, file_check


def test_file_check_current_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello")

    assert file_check("sample.txt") is True
    assert file_check("non_existent.txt") is False


def test_file_check_custom_dir(tmp_path):
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    target_file = sub_dir / "target.dat"
    target_file.write_text("data")

    assert file_check("target.dat", str(sub_dir)) is True
    assert file_check("missing.dat", str(sub_dir)) is False


def test_control_file_create_no_enter(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    folder_name = "test_dir_no_enter"

    control_file_create(folder_name, go_inside=False)
    assert (tmp_path / folder_name).is_dir()
    assert Path(os.getcwd()) == tmp_path

    # Calling again should not raise error if exists
    control_file_create(folder_name, go_inside=False)
    assert (tmp_path / folder_name).is_dir()


def test_control_file_create_with_enter(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    folder_name = "test_dir_enter"

    control_file_create(folder_name, go_inside=True)
    assert Path(os.getcwd()) == (tmp_path / folder_name)
