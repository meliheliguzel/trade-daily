from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QLineEdit,
    QListWidget,
    QRadioButton,
    QTextEdit,
    QWidget,
)

from config.query.data_base import DataBaseQuery
from module.data.connection.sql_lite import SQLite
from module.data.entities import StrategyEntity
from windows.main.record import Record


class DummyRecordBase(QWidget):
    def __init__(self, db):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self._status_bar_message = MagicMock()
        self._balance_record = MagicMock()
        self._data_display = MagicMock()
        self._analysis = MagicMock()

        self.positive_float_val = QDoubleValidator(0.0, 1e9, 6, self)
        self.float_val = QDoubleValidator(-1e9, 1e9, 6, self)
        self.int_val = QIntValidator(1, 1e9, self)

        self.ui = MagicMock()
        self.ui.widget_record_transaction = QWidget(self)
        self.ui.lineEdit_record_daily_transaction_id = QLineEdit(self)
        self.ui.lineEdit_record_daily_size = QLineEdit(self)
        self.ui.lineEdit_record_daily_rr = QLineEdit(self)
        self.ui.lineEdit_record_daily_result = QLineEdit(self)
        self.ui.lineEdit_record_daily_enter_price = QLineEdit(self)
        self.ui.lineEdit_record_daily_target_price = QLineEdit(self)
        self.ui.lineEdit_record_daily_stop_price = QLineEdit(self)
        self.ui.lineEdit_record_daily_exit_price = QLineEdit(self)
        self.ui.lineEdit_record_daily_chart_link = QLineEdit(self)

        self.ui.textEdit_record_daily_note = QTextEdit(self)
        self.ui.listWidget_record_daily_chart_image = QListWidget(self)
        self.ui.listWidget_record_daily_chart_link = QListWidget(self)
        self.ui.listWidget_record_daily_strategy = QListWidget(self)

        self.ui.comboBox_record_daily_parity = QComboBox(self)
        self.ui.comboBox_record_daily_open_trn = QComboBox(self)
        self.ui.comboBox_record_daily_platform = QComboBox(self)
        self.ui.comboBox_record_daily_strategy = QComboBox(self)

        self.ui.radioButton_record_daily_open = QRadioButton(self)
        self.ui.radioButton_record_daily_tp = QRadioButton(self)
        self.ui.radioButton_record_daily_sl = QRadioButton(self)
        self.ui.radioButton_record_daily_long = QRadioButton(self)
        self.ui.radioButton_record_daily_short = QRadioButton(self)

        self.ui.dateTimeEdit_record_daily_entry = QDateTimeEdit(self)
        self.ui.dateTimeEdit_record_daily_exit = QDateTimeEdit(self)


@pytest.fixture
def record_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_record.db")
    SQLite.reset()
    db = SQLite(db_path)
    for q in DataBaseQuery.TABLE_LIST:
        db.create_table(q)

    base = DummyRecordBase(db)
    qtbot.addWidget(base)
    record = Record(base)
    yield base, record

    db.close_connection()
    SQLite.reset()


def test_record_strategy_add_and_remove(record_fixture):
    base, record = record_fixture

    strat = StrategyEntity(1, "Trend", "Description")
    base.ui.comboBox_record_daily_strategy.addItem("Trend", strat)

    record.strategy_add(0)
    assert base.ui.listWidget_record_daily_strategy.count() == 1
    assert base.ui.listWidget_record_daily_strategy.item(0).text() == "Trend"

    # Add same strategy again should show notice, not add duplicate
    base.ui.comboBox_record_daily_strategy.addItem("Trend", strat)
    record.strategy_add(0)
    assert base.ui.listWidget_record_daily_strategy.count() == 1
    base._status_bar_message.show_notice_message.assert_called()

    # Remove strategy
    base.ui.listWidget_record_daily_strategy.setCurrentRow(0)
    record.strategy_remove()
    assert base.ui.listWidget_record_daily_strategy.count() == 0


def test_record_link_add_and_remove(record_fixture):
    base, record = record_fixture

    base.ui.lineEdit_record_daily_chart_link.setText("https://tradingview.com/x/12345")
    record.link_add()

    assert base.ui.listWidget_record_daily_chart_link.count() == 1
    assert base.ui.listWidget_record_daily_chart_link.item(0).text() == "https://tradingview.com/x/12345"
    assert base.ui.lineEdit_record_daily_chart_link.text() == ""

    # Remove link
    base.ui.listWidget_record_daily_chart_link.setCurrentRow(0)
    record.link_remove()
    assert base.ui.listWidget_record_daily_chart_link.count() == 0


def test_record_clear_all(record_fixture):
    base, record = record_fixture

    base.ui.lineEdit_record_daily_size.setText("100")
    base.ui.lineEdit_record_daily_rr.setText("2.5")
    base.ui.textEdit_record_daily_note.setText("Some note")
    base.ui.listWidget_record_daily_chart_link.addItem("https://link.com")

    record._clear_all()

    assert base.ui.lineEdit_record_daily_size.text() == ""
    assert base.ui.lineEdit_record_daily_rr.text() == ""
    assert base.ui.textEdit_record_daily_note.toPlainText() == ""
    assert base.ui.listWidget_record_daily_chart_link.count() == 0
    assert base.ui.radioButton_record_daily_open.isChecked()


def test_record_image_add_and_remove(record_fixture, tmp_path, monkeypatch):
    from PySide6.QtGui import QColor, QPixmap
    from PySide6.QtWidgets import QFileDialog
    base, record = record_fixture

    test_img = tmp_path / "chart.png"
    pm = QPixmap(10, 10)
    pm.fill(QColor("red"))
    pm.save(str(test_img), "PNG")

    # 1. Add image via mocked file dialog
    monkeypatch.setattr(QFileDialog, "getOpenFileNames", lambda *args, **kwargs: ([str(test_img)], "Images (*.png)"))
    record.image_add()

    assert base.ui.listWidget_record_daily_chart_image.count() == 1

    # 2. Remove image
    base.ui.listWidget_record_daily_chart_image.setCurrentRow(0)
    record.image_remove()
    assert base.ui.listWidget_record_daily_chart_image.count() == 0

    # 3. Add with cancel dialog
    monkeypatch.setattr(QFileDialog, "getOpenFileNames", lambda *args, **kwargs: ([], ""))
    record.image_add()
    base._status_bar_message.show_warning_message.assert_called()
