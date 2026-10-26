from PySide6.QtGui import QColor

from module.data.entities import TransactionState


class DailyTableConfig:

    COLUMN_COUNT: int = 7
    DATA_LOAD_NUMBER: int = 100

    DATE_OF_ENTRY: str = "Date of entry"
    PLATFORM: str = "Platform"
    PARITY: str = "Parity"
    RR: str = "Rr ratio"
    SIZE: str = "Size"
    LONG_SHORT: str = "Long\\Short"
    ID: str = "id"

    ID_NUMBER: int = 0
    DATE_OF_ENTRY_NUMBER: int = 1
    PLATFORM_NUMBER: int = 2
    PARITY_NUMBER: int = 3
    RR_NUMBER: int = 4
    SIZE_NUMBER: int = 5
    LONG_SHORT_NUMBER: int = 6

    STATE_PALETTE: dict = {
        TransactionState.OPEN: QColor("#cc921c"),
        TransactionState.TP: QColor("#00bcd4"),
        TransactionState.SL: QColor("#ff0088"),
    }
    BACKGROUND_COLOR: QColor = QColor("#000000")

