from PySide6.QtWidgets import QBoxLayout, QLayoutItem


def clearLayout(layout: QBoxLayout) -> None:
    """
    Deletes all widgets and child layouts within the given QBoxLayout.
    If an item is a widget, widget.deleteLater() is called.
    If an item is a child layout, it is recursively cleared.
    """
    while layout.count():
        item: QLayoutItem = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            child_layout = item.layout()
            if child_layout is not None:
                clearLayout(child_layout)

