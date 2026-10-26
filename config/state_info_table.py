from PySide6.QtGui import QColor


class StateInfoTableRowConfig:

    TOTAL: str = "Total"
    TP: str = "Tp"
    SL: str = "Sl"
    OPEN: str = "Open"
    LONG: str = "Long"
    SHORT: str = "Short"

class StateInfoTableConfig:

    ROW_COUNT: int = 6
    COLUMN_COUNT: int = 2

    STATE: str = "State"
    AMOUNT: str = "Amount"

    STATE_NUMBER: int = 0
    AMOUNT_NUMBER: int = 1

    PALETTE: dict = {
        StateInfoTableRowConfig.OPEN: QColor("#cc921c"),
        StateInfoTableRowConfig.TP: QColor("#00bcd4"),
        StateInfoTableRowConfig.SL: QColor("#ff0088"),
        StateInfoTableRowConfig.LONG: QColor("#59bc47"),
        StateInfoTableRowConfig.SHORT: QColor("#e01fe0"),
        StateInfoTableRowConfig.TOTAL: QColor("#5256ef"),
    }


