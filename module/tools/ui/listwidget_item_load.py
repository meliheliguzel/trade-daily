from collections.abc import Callable
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidget, QListWidgetItem

type ErrorFunc = Callable[[str], None]


class DataRole:
    DATA = Qt.ItemDataRole.UserRole
    LABEL: int = Qt.ItemDataRole.UserRole + 1


def widget_list_item_add(
    add_data: Any,
    text: str | None,
    icon: QIcon | None,
    list_widget: QListWidget,
    add_label: str | None = None,
) -> None:
    """Creates a QListWidgetItem with optional text, icon, and additional data."""
    item = QListWidgetItem(text or "")
    if icon is not None:
        item.setIcon(icon)
    if add_label is not None:
        item.setData(DataRole.LABEL, add_label)
    item.setData(DataRole.DATA, add_data)
    list_widget.addItem(item)


def list_widget_image_load(
    images_data: list[bytes] | dict[bytes, Any],
    error_func: ErrorFunc,
    list_widget: QListWidget,
    add_label: str | None = None,
) -> None:
    """Loads images from bytes into a QListWidget with optional metadata."""
    if isinstance(images_data, list):
        for image_bytes in images_data:
            pixmap = QPixmap()
            if not pixmap.loadFromData(image_bytes):
                error_func("Image could not be loaded.")
                continue
            widget_list_item_add(
                image_bytes, None, QIcon(pixmap), list_widget, add_label
            )
    else:
        for image_bytes, metadata in images_data.items():
            pixmap = QPixmap()
            if not pixmap.loadFromData(image_bytes):
                error_func("Image could not be loaded.")
                continue
            widget_list_item_add(metadata, None, QIcon(pixmap), list_widget, add_label)


def list_widget_items_load(
    data: dict[str, Any], list_widget: QListWidget, add_label: str | None = None
) -> None:
    """Loads items from a dictionary into a QListWidget (text and icon only)."""
    for text, data in data.items():
        widget_list_item_add(data, text, None, list_widget, add_label)


def get_extra_data_from_list_widget(
    list_widget: QListWidget, label: bool = False
) -> list[Any] | list[tuple[Any, Any]]:
    """Extracts UserRole data from all items in a QListWidget."""

    if label:
        result: list[tuple[Any, Any]] = []
        for i in range(list_widget.count()):

            data = list_widget.item(i).data(DataRole.DATA)
            label = list_widget.item(i).data(DataRole.LABEL)
            if label:
                result.append((data, label))
            else:
                result.append((data, None))

        return result

    return [list_widget.item(i).data(DataRole.DATA) for i in range(list_widget.count())]
