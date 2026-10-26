from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QTableView

from config import DailyTableConfig
from module.data.entities import Transaction, TransactionDirection


class DailyModel(QAbstractTableModel):

    def __init__(self, data: dict, count: int = DailyTableConfig.DATA_LOAD_NUMBER):

        super().__init__()
        self._data: list[Transaction] = data
        self._row_count = 0

        self.load_more(count)

    def rowCount(self, parent=QModelIndex()):
        return self._row_count

    def columnCount(self, parent=QModelIndex()):
        return DailyTableConfig.COLUMN_COUNT

    def data(self, index, role):

        row_info: Transaction = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == DailyTableConfig.ID_NUMBER:
                return row_info.primary_key
            elif index.column() == DailyTableConfig.DATE_OF_ENTRY_NUMBER:
                return row_info.date_of_entry
            elif index.column() == DailyTableConfig.LONG_SHORT_NUMBER:
                return TransactionDirection.direction_read[row_info.long_short]
            elif index.column() == DailyTableConfig.PLATFORM_NUMBER:
                return row_info.platform
            elif index.column() == DailyTableConfig.PARITY_NUMBER:
                return row_info.parity
            elif index.column() == DailyTableConfig.SIZE_NUMBER:
                return row_info.size
            elif index.column() == DailyTableConfig.RR_NUMBER:
                return row_info.rr

        elif role == Qt.ItemDataRole.ForegroundRole:
            return DailyTableConfig.STATE_PALETTE[row_info.tp_sl]
        elif role == Qt.ItemDataRole.BackgroundRole:
            return DailyTableConfig.BACKGROUND_COLOR
        return None

    def headerData(self, section, orientation, role):

        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == DailyTableConfig.ID_NUMBER:
                    return DailyTableConfig.ID
                elif section == DailyTableConfig.DATE_OF_ENTRY_NUMBER:
                    return DailyTableConfig.DATE_OF_ENTRY
                elif section == DailyTableConfig.LONG_SHORT_NUMBER:
                    return DailyTableConfig.LONG_SHORT
                elif section == DailyTableConfig.PLATFORM_NUMBER:
                    return DailyTableConfig.PLATFORM
                elif section == DailyTableConfig.PARITY_NUMBER:
                    return DailyTableConfig.PARITY
                elif section == DailyTableConfig.SIZE_NUMBER:
                    return DailyTableConfig.SIZE
                elif section == DailyTableConfig.RR_NUMBER:
                    return DailyTableConfig.RR
        return None

    def load_more(self, count: int = 100):

        if self._row_count >= len(self._data):
            return

        start = self._row_count
        end = min(start + count, len(self._data))

        self.beginInsertRows(QModelIndex(), start, end - 1)
        self._row_count += end - start
        self.endInsertRows()

    def get_selected_item(self, table_view: QTableView) -> Transaction | None:

        selected_index = table_view.currentIndex()
        if selected_index.isValid():
            return self._data[selected_index.row()]
        return None
