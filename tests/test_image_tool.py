from module.tools.file.image import image_data


def test_image_data_valid(tmp_path):
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

    result = image_data(str(img))
    assert result is not None
    data, ext = result
    assert data == b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    assert ext == ".png"


def test_image_data_empty_file(tmp_path):
    img = tmp_path / "empty.jpg"
    img.touch()

    result = image_data(str(img))
    assert result is None


def test_image_data_non_existent(tmp_path):
    result = image_data(str(tmp_path / "not_found.png"))
    assert result is None
