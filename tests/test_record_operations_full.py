from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QGroupBox,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QRadioButton,
    QTextEdit,
    QWidget,
)

from config.query.data_base import DataBaseQuery
from config.query.parity import ParityQuery
from config.query.platform import PlatformQuery
from config.query.strategy import StrategyQuery
from module.data.connection.sql_lite import SQLite
from module.data.entities import ParityEntity, PlatformEntity, StrategyEntity
from windows.main.record import Record


class DummyRecordFullBase(QWidget):
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

        self.group_state = QGroupBox(self)
        self.ui.radioButton_record_daily_open = QRadioButton(self.group_state)
        self.ui.radioButton_record_daily_tp = QRadioButton(self.group_state)
        self.ui.radioButton_record_daily_sl = QRadioButton(self.group_state)

        self.group_direction = QGroupBox(self)
        self.ui.radioButton_record_daily_long = QRadioButton(self.group_direction)
        self.ui.radioButton_record_daily_short = QRadioButton(self.group_direction)

        self.ui.dateTimeEdit_record_daily_entry = QDateTimeEdit(self)
        self.ui.dateTimeEdit_record_daily_exit = QDateTimeEdit(self)


@pytest.fixture
def full_record_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_full_record.db")
    SQLite.reset()
    db = SQLite(db_path)
    for q in DataBaseQuery.TABLE_LIST:
        db.create_table(q)

    # Insert sample Platform, Parity, Strategy
    db.insert(PlatformQuery.ADD, ("Binance",))
    db.insert(ParityQuery.ADD, ("BTCUSDT", 1))
    db.insert(StrategyQuery.ADD, ("Trend", "Trend Following"))

    plat_entity = PlatformEntity(1, "Binance")
    pari_entity = ParityEntity(1, "BTCUSDT", 1)
    strat_entity = StrategyEntity(1, "Trend", "Trend Following")

    base = DummyRecordFullBase(db)
    qtbot.addWidget(base)

    base.ui.comboBox_record_daily_platform.addItem("Binance", plat_entity)
    base.ui.comboBox_record_daily_parity.addItem("BTCUSDT", pari_entity)
    base.ui.comboBox_record_daily_strategy.addItem("Trend", strat_entity)

    record = Record(base)
    yield base, record

    db.close_connection()
    SQLite.reset()


def test_add_open_transaction(full_record_fixture):
    base, record = full_record_fixture

    base.ui.lineEdit_record_daily_rr.setText("2.0")
    base.ui.lineEdit_record_daily_size.setText("500.0")
    base.ui.lineEdit_record_daily_enter_price.setText("50000.0")
    base.ui.lineEdit_record_daily_stop_price.setText("49000.0")
    base.ui.lineEdit_record_daily_target_price.setText("52000.0")
    base.ui.radioButton_record_daily_open.setChecked(True)
    base.ui.radioButton_record_daily_long.setChecked(True)
    base.ui.textEdit_record_daily_note.setText("Opening long on BTC")

    # Add link and strategy
    base.ui.lineEdit_record_daily_chart_link.setText("https://chart.com/btc")
    record.link_add()
    record.strategy_add(0)

    # Save
    record.save()

    # Verify transaction added to DB
    rows = base._data_base.select('SELECT id, rr, size FROM "Transaction"')
    assert len(rows) == 1
    t_id = rows[0][0]
    assert rows[0][1] == 2.0
    assert rows[0][2] == 500.0

    # Verify detail open and note
    d_rows = base._data_base.select('SELECT enter_price FROM "Transaction_Detail_Open"')
    assert len(d_rows) == 1
    assert d_rows[0][0] == 50000.0

    n_rows = base._data_base.select('SELECT note_text FROM "Note"')
    assert len(n_rows) == 1
    assert n_rows[0][0] == "Opening long on BTC"

    # Verify open transactions list
    assert base.ui.comboBox_record_daily_open_trn.count() == 1

    # Load open transaction back
    base.ui.comboBox_record_daily_open_trn.setCurrentIndex(0)
    record.open_transaction_load(0)
    assert base.ui.lineEdit_record_daily_size.text() == "500.0"

    # Update transaction (close with TP)
    pari_entity = ParityEntity(1, "BTCUSDT", 1)
    base.ui.comboBox_record_daily_parity.addItem("BTCUSDT", pari_entity)
    base.ui.comboBox_record_daily_parity.setCurrentIndex(0)
    base.ui.radioButton_record_daily_tp.setChecked(True)
    base.ui.lineEdit_record_daily_exit_price.setText("52000.0")
    base.ui.lineEdit_record_daily_result.setText("1000.0")
    record.save()

    # Check closing table
    c_rows = base._data_base.select('SELECT tp_sl, result FROM "Transaction_Closing"')
    assert len(c_rows) == 1
    assert c_rows[0][0] == 1  # TP
    assert c_rows[0][1] == 1000.0

    # Delete transaction
    base.ui.lineEdit_record_daily_transaction_id.setText(str(t_id))
    record.update_data_load()
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.Yes)
    record.remove()
    monkeypatch.undo()

    assert len(base._data_base.select('SELECT id FROM "Transaction"')) == 0


def test_add_short_sl_transaction(full_record_fixture):
    base, record = full_record_fixture

    base.ui.lineEdit_record_daily_rr.setText("1.5")
    base.ui.lineEdit_record_daily_size.setText("300.0")
    base.ui.lineEdit_record_daily_enter_price.setText("3000.0")
    base.ui.lineEdit_record_daily_stop_price.setText("3100.0")
    base.ui.lineEdit_record_daily_target_price.setText("2800.0")
    base.ui.lineEdit_record_daily_exit_price.setText("3100.0")
    base.ui.lineEdit_record_daily_result.setText("-150.0")

    base.ui.radioButton_record_daily_short.setChecked(True)
    base.ui.radioButton_record_daily_sl.setChecked(True)

    record.save()

    rows = base._data_base.select('SELECT id, long_short FROM "Transaction"')
    assert len(rows) == 1
    assert rows[0][1] == 0  # Short

    c_rows = base._data_base.select('SELECT tp_sl, result FROM "Transaction_Closing"')
    assert len(c_rows) == 1
    assert c_rows[0][0] == 0  # SL
    assert c_rows[0][1] == -150.0

    # Load back with update_data_load
    base.ui.lineEdit_record_daily_transaction_id.setText(str(rows[0][0]))
    record.update_data_load()
    assert base.ui.radioButton_record_daily_short.isChecked()
    assert base.ui.radioButton_record_daily_sl.isChecked()
