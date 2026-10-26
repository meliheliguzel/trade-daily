from PySide6.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from module.tools.ui import (
    get_extra_data_from_list_widget,
    list_widget_image_load,
    list_widget_items_load,
    widget_list_item_add,
)


def generate_valid_image_bytes() -> bytes:
    """Generates a valid PNG image as bytes using QPixmap."""
    pixmap = QPixmap(10, 10)
    pixmap.fill(QColor(255, 0, 0))  # Red color
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    return bytes(byte_array.data())

def test_create_list_item_text_and_data(qtbot):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    add_data = {"key": "value"}
    widget_list_item_add(add_data=add_data, text="Test Item", icon=None, list_widget=list_widget)

    assert list_widget.count() == 1
    item = list_widget.item(0)
    assert item.text() == "Test Item"
    assert item.data(Qt.ItemDataRole.UserRole) == add_data
    assert item.icon().isNull()

def test_create_list_item_icon_and_add_label(qtbot):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    pixmap = QPixmap(10, 10)
    icon = QIcon(pixmap)
    add_label = "extra_label"

    widget_list_item_add(
        add_data=None,
        text=None,
        icon=icon,
        list_widget=list_widget,
        add_label=add_label
    )

    assert list_widget.count() == 1
    item = list_widget.item(0)
    assert item.text() == ""
    assert not item.icon().isNull()
    assert item.data(Qt.ItemDataRole.UserRole + 1) == add_label

def test_list_widget_image_load_valid_list(qtbot, mocker):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    mock_error_func = mocker.Mock()
    valid_bytes = generate_valid_image_bytes()
    images_data = [valid_bytes]

    list_widget_image_load(images_data, mock_error_func, list_widget)

    assert list_widget.count() == 1
    item = list_widget.item(0)
    assert not item.icon().isNull()
    assert item.data(Qt.ItemDataRole.UserRole) == valid_bytes
    mock_error_func.assert_not_called()

def test_list_widget_image_load_invalid_list(qtbot, mocker):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    mock_error_func = mocker.Mock()
    images_data = [b'invalid_image_data']

    list_widget_image_load(images_data, mock_error_func, list_widget)

    assert list_widget.count() == 0
    mock_error_func.assert_called_once_with("Image could not be loaded.")

def test_list_widget_image_load_dict(qtbot, mocker):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    mock_error_func = mocker.Mock()
    valid_bytes = generate_valid_image_bytes()
    metadata = {"meta": "data"}
    images_data = {valid_bytes: metadata}

    list_widget_image_load(images_data, mock_error_func, list_widget)

    assert list_widget.count() == 1
    item = list_widget.item(0)
    assert item.data(Qt.ItemDataRole.UserRole) == metadata
    mock_error_func.assert_not_called()

def test_list_widget_items_load(qtbot):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    data = {"Item1": 1, "Item2": 2}

    list_widget_items_load(data, list_widget)

    assert list_widget.count() == 2
    for i in range(2):
        item = list_widget.item(i)
        assert item.text() in data.keys()
    # Check UserRole data is None
    assert list_widget.item(0).data(Qt.ItemDataRole.UserRole) == 1

def test_get_extra_data_from_list_widget(qtbot):
    list_widget = QListWidget()
    qtbot.addWidget(list_widget)
    datas = [123, "abc", {"key": "value"}]

    for data in datas:
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, data)
        list_widget.addItem(item)

    result = get_extra_data_from_list_widget(list_widget)
    assert result == datas
