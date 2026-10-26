from dataclasses import dataclass

from PySide6.QtCore import QAbstractTableModel, Qt

from config import StateInfoTableConfig, StateInfoTableRowConfig


@dataclass
class StateInfoTabelData:
    open_count: int
    tp_count: int
    sl_count: int
    long_count: int
    short_count: int
    total_count: int

    def get_dict(self):
        return {
            StateInfoTableRowConfig.OPEN: self.open_count,
            StateInfoTableRowConfig.TP: self.tp_count,
            StateInfoTableRowConfig.SL: self.sl_count,
            StateInfoTableRowConfig.LONG: self.long_count,
            StateInfoTableRowConfig.SHORT: self.short_count,
            StateInfoTableRowConfig.TOTAL: self.total_count,
        }


class StateInfoModel(QAbstractTableModel):
    def __init__(self, data: StateInfoTabelData):
        super().__init__()
        self._data: dict = data.get_dict()

    def rowCount(self, parent=None):
        return StateInfoTableConfig.ROW_COUNT

    def columnCount(self, parent=None):
        return StateInfoTableConfig.COLUMN_COUNT

    def data(self, index, role):

        row_info = list(self._data.keys())[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == StateInfoTableConfig.STATE_NUMBER:
                return row_info
            elif index.column() == StateInfoTableConfig.AMOUNT_NUMBER:
                return self._data[row_info]

        elif role == Qt.ItemDataRole.BackgroundRole:
            return StateInfoTableConfig.PALETTE[row_info]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == StateInfoTableConfig.STATE_NUMBER:
                    return StateInfoTableConfig.STATE
                elif section == StateInfoTableConfig.AMOUNT_NUMBER:
                    return StateInfoTableConfig.AMOUNT
        return None

