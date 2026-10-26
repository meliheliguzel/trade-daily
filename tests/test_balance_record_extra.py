from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QMessageBox, QRadioButton, QVBoxLayout, QWidget

from config.query.data_base import DataBaseQuery
from module.data.connection.sql_lite import SQLite
from windows.main.balance_record import BalanceRecord


class DummyBalanceExtraBase(QWidget):
    def __init__(self, db, tmp_path):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self._status_bar_message = MagicMock()
        self.float_val = QDoubleValidator(-1e9, 1e9, 6, self)

        self._user_loc = MagicMock()
        self._user_loc.BALANCE_GRAPH = str(tmp_path / "balance_extra.html")

        self.ui = MagicMock()
        self.ui.lineEdit_record_balance_size = QLineEdit(self)
        self.ui.comboBox_record_balance = QComboBox(self)
        self.ui.radioButton_record_balance_close = QRadioButton(self)
        self.ui.radioButton_record_balance_open = QRadioButton(self)
        self.ui.widget_record_balance = QWidget(self)
        self.ui.verticalLayout_balance = QVBoxLayout(self)


@pytest.fixture
def balance_extra_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_balance_extra.db")
    SQLite.reset()
    db = SQLite(db_path)
    for q in DataBaseQuery.TABLE_LIST:
        db.create_table(q)

    base = DummyBalanceExtraBase(db, tmp_path)
    qtbot.addWidget(base)
    section = BalanceRecord(base)
    yield base, section

    section._thread_work.stop()
    db.close_connection()
    SQLite.reset()


def test_balance_add_update_remove(balance_extra_fixture, monkeypatch):
    base, section = balance_extra_fixture

    # 1. Add balance
    base.ui.lineEdit_record_balance_size.setText("10000.0")
    base.ui.radioButton_record_balance_open.setChecked(True)
    section.save()

    assert base.ui.comboBox_record_balance.count() == 1

    # 2. Update balance
    section.edit_load(0)
    assert base.ui.lineEdit_record_balance_size.text() == "10000.0"
    base.ui.lineEdit_record_balance_size.setText("25000.0")
    section.save()

    section.load()
    assert base.ui.comboBox_record_balance.currentText() == "25000.0"

    # 3. Recalculation
    section.recalculation()

    # 4. Remove balance (cancel)
    section.edit_load(0)
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.No)
    section.remove()
    assert base.ui.comboBox_record_balance.count() == 1

    # 5. Remove balance (confirm)
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.Yes)
    section.remove()
    assert base.ui.comboBox_record_balance.count() == 0
