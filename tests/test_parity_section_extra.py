from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QMessageBox, QPushButton, QWidget

from config.query.data_base import DataBaseQuery
from config.query.platform import PlatformQuery
from module.data.connection.sql_lite import SQLite
from module.data.entities import PlatformEntity
from windows.main.parity import Parity


class DummyParityBase(QWidget):
    def __init__(self, db):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self.letters_numbers_val = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9]+"))
        self._status_bar_message = MagicMock()

        self.ui = MagicMock()
        self.ui.lineEdit_record_parity_name = QLineEdit(self)
        self.ui.comboBox_record_parity_edit_platform = QComboBox(self)
        self.ui.comboBox_record_parity_edit = QComboBox(self)
        self.ui.comboBox_record_daily_platform = QComboBox(self)
        self.ui.comboBox_record_daily_parity = QComboBox(self)
        self.ui.pushButton_record_parity_save = QPushButton(self)


@pytest.fixture
def parity_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_parity.db")
    SQLite.reset()
    db = SQLite(db_path)
    db.create_table(DataBaseQuery.PLATFORM)
    db.create_table(DataBaseQuery.PARITY)
    db.create_table(DataBaseQuery.TRANSACTION)

    db.insert(PlatformQuery.ADD, ("Binance",))
    platform_entity = PlatformEntity(1, "Binance")

    base = DummyParityBase(db)
    qtbot.addWidget(base)
    base.ui.comboBox_record_parity_edit_platform.addItem("Binance", platform_entity)
    base.ui.comboBox_record_daily_platform.addItem("Binance", platform_entity)

    section = Parity(base)
    yield base, section

    db.close_connection()
    SQLite.reset()


def test_parity_remove_confirmed_and_cancel(parity_fixture, monkeypatch):
    base, section = parity_fixture

    base.ui.lineEdit_record_parity_name.setText("BTCUSDT")
    section.save()
    assert base.ui.comboBox_record_daily_parity.count() == 1

    section.edit_load(1)

    # Cancel remove
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.No)
    section.remove()
    assert base.ui.comboBox_record_daily_parity.count() == 1

    # Confirm remove
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.Yes)
    section.remove()
    assert base.ui.comboBox_record_daily_parity.count() == 0


def test_parity_daily_load(parity_fixture):
    base, section = parity_fixture

    base.ui.lineEdit_record_parity_name.setText("ETHUSDT")
    section.save()

    section.daily_load(0)
    assert base.ui.comboBox_record_daily_parity.count() == 1
    assert base.ui.comboBox_record_daily_parity.currentText() == "ETHUSDT"
