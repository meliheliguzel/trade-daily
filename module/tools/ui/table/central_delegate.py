from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyledItemDelegate


class CenterAlignDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):

        option.displayAlignment = Qt.AlignCenter
        super().paint(painter, option, index)
