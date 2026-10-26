from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QRadioButton,
    QTableView,
    QTextBrowser,
    QWidget,
)

from config.query.data_base import DataBaseQuery
from config.query.parity import ParityQuery
from config.query.platform import PlatformQuery
from config.query.record import RecordQuery
from module.data.connection.sql_lite import SQLite
from windows.main.data_display import DataDisplay


class DummyDisplayBase(QWidget):
    def __init__(self, db):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self._status_bar_message = MagicMock()

        self.ui = MagicMock()
        self.ui.tableView_daily = QTableView(self)
        self.ui.tableView_daily_state_info = QTableView(self)
        self.ui.radioButton_display_time_down = QRadioButton(self)
        self.ui.radioButton_display_time_up = QRadioButton(self)

        self.ui.label_daily_display_trn_no = QLabel(self)
        self.ui.label_daily_date_of_entry = QLabel(self)
        self.ui.label_daily_platform = QLabel(self)
        self.ui.label_daily_parity = QLabel(self)
        self.ui.label_daily_rr_ratio = QLabel(self)
        self.ui.label_daily_size = QLabel(self)
        self.ui.label_daily_direction = QLabel(self)
        self.ui.label_daily_state = QLabel(self)
        self.ui.label_daily_date_of_exit = QLabel(self)
        self.ui.label_daily_result = QLabel(self)
        self.ui.label_daily_exit_price = QLabel(self)
        self.ui.label_daily_enter_price = QLabel(self)
        self.ui.label_daily_target_price = QLabel(self)
        self.ui.label_daily_stop_price = QLabel(self)

        self.ui.textBrowser_daily_not = QTextBrowser(self)
        self.ui.listWidget_daily_chart_link = QListWidget(self)
        self.ui.listWidget_daily_strategy = QListWidget(self)
        self.ui.listWidget_daily_chart_image = QListWidget(self)


@pytest.fixture
def display_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_display.db")
    SQLite.reset()
    db = SQLite(db_path)
    for q in DataBaseQuery.TABLE_LIST:
        db.create_table(q)

    # Insert test platform, parity and transaction
    db.insert(PlatformQuery.ADD, ("Binance",))
    db.insert(ParityQuery.ADD, ("BTCUSDT", 1))

    # Insert 1 open transaction and 1 closed transaction
    t1_id = db.insert(RecordQuery.TRANSACTION_INSERT, (1, 1, "2026-10-20 12:00:00", 1, 2.0, 100.0))
    db.insert(RecordQuery.DETAIL_OPEN_INSERT, (t1_id, 50000.0, 52000.0, 49000.0))
    db.insert(RecordQuery.NOTE_INSERT, (t1_id, "Test note 1"))

    t2_id = db.insert(RecordQuery.TRANSACTION_INSERT, (1, 1, "2026-10-21 14:00:00", 0, 1.5, 200.0))
    db.insert(RecordQuery.CLOSING_INSERT, (t2_id, "2026-10-21 16:00:00", 1, 300.0))
    db.insert(RecordQuery.DETAIL_CLOSING_INSERT, (t2_id, 48000.0))

    base = DummyDisplayBase(db)
    qtbot.addWidget(base)
    display = DataDisplay(base)

    yield base, display

    db.close_connection()
    SQLite.reset()


def test_display_reload_and_state_info(display_fixture):
    base, display = display_fixture

    display.reload()
    assert base.ui.tableView_daily.model() is not None
    assert base.ui.tableView_daily_state_info.model() is not None


def test_display_time_sort(display_fixture):
    base, display = display_fixture

    base.ui.radioButton_display_time_up.setChecked(True)
    display.time_sort(True)

    base.ui.radioButton_display_time_down.setChecked(True)
    display.time_sort(True)


def test_display_external_data_load(display_fixture):
    base, display = display_fixture

    display.reload()
    base.ui.tableView_daily.selectRow(0)
    display.external_data_load(None)

    assert base.ui.label_daily_platform.text() == "Binance"
    assert base.ui.label_daily_parity.text() == "BTCUSDT"
    assert base.ui.label_daily_rr_ratio.text() == "2.0"


def test_display_chart_link_display(display_fixture):
    from PySide6.QtWidgets import QListWidgetItem
    _base, display = display_fixture

    item = QListWidgetItem("https://tradingview.com/chart/1")
    display.chart_link_display(item)

    assert len(display._child_windows) == 1


def test_display_chart_image_display_invalid(display_fixture):
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QListWidgetItem
    base, display = display_fixture

    item = QListWidgetItem("img1")
    item.setData(Qt.ItemDataRole.UserRole, b"not_a_valid_image")
    display.chart_image_display(item)

    base._status_bar_message.show_warning_message.assert_called()


def test_display_state_info_filter(display_fixture):
    base, display = display_fixture

    display.reload()
    model = base.ui.tableView_daily_state_info.model()
    # Click first state row (e.g., Open or Total)
    idx = model.index(0, 0)
    display.state_info_doubleClicked(idx)
    assert base.ui.tableView_daily.model() is not None


def test_display_load_more(display_fixture):
    base, display = display_fixture
    display.reload()
    display._DataDisplay__daily_table_load_more()
    assert base.ui.tableView_daily.model() is not None
