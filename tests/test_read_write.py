import json

import pytest

from module.tools.file.read_write import ReadWrite


def test_json_write_and_read(tmp_path):
    file_path = str(tmp_path / "subdir" / "test.json")
    data = {"key": "value", "list": [1, 2, 3], "nested": {"a": 1}}

    # Write data (should automatically create 'subdir')
    ReadWrite.json_write(file_path, data)

    # Read data back
    result = ReadWrite.json_read(file_path)

    assert result == data


def test_json_read_non_existent(tmp_path):
    file_path = str(tmp_path / "non_existent.json")
    result = ReadWrite.json_read(file_path)
    assert result is None


def test_json_read_empty_file(tmp_path):
    file_path = str(tmp_path / "empty.json")
    with open(file_path, "w"):
        pass  # Create empty file

    result = ReadWrite.json_read(file_path)
    assert result is None


def test_json_read_invalid_format(tmp_path):
    file_path = str(tmp_path / "invalid.json")
    with open(file_path, "w") as f:
        f.write("{invalid json}")

    with pytest.raises(json.JSONDecodeError):
        ReadWrite.json_read(file_path)
