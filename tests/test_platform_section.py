from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QMessageBox, QPushButton, QWidget

from config.query.data_base import DataBaseQuery
from module.data.connection.sql_lite import SQLite
from windows.main.platform import Platform


class DummyPlatformBase(QWidget):
    def __init__(self, db):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self.letters_numbers_val = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9]+"))
        self._status_bar_message = MagicMock()

        self.ui = MagicMock()
        self.ui.lineEdit_record_platform_name = QLineEdit(self)
        self.ui.comboBox_record_platform_edit = QComboBox(self)
        self.ui.comboBox_record_daily_platform = QComboBox(self)
        self.ui.pushButton_record_platform_save = QPushButton(self)


@pytest.fixture
def platform_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_platform.db")
    SQLite.reset()
    db = SQLite(db_path)
    db.create_table(DataBaseQuery.PLATFORM)
    db.create_table(DataBaseQuery.PARITY)
    db.create_table(DataBaseQuery.TRANSACTION)

    base = DummyPlatformBase(db)
    qtbot.addWidget(base)
    section = Platform(base)
    yield base, section

    db.close_connection()
    SQLite.reset()


def test_platform_add_and_load(platform_fixture):
    base, section = platform_fixture

    base.ui.lineEdit_record_platform_name.setText("Binance")
    section.save()

    # Index 0 is "New", Index 1 is "Binance"
    assert base.ui.comboBox_record_platform_edit.count() == 2
    assert base.ui.comboBox_record_daily_platform.count() == 1
    assert base.ui.comboBox_record_daily_platform.itemText(0) == "Binance"


def test_platform_duplicate_warning(platform_fixture):
    base, section = platform_fixture

    base.ui.lineEdit_record_platform_name.setText("Bybit")
    section.save()

    # Try adding same again (index 0 is "New")
    section.edit_load(0)
    base.ui.lineEdit_record_platform_name.setText("Bybit")
    section.save()

    base._status_bar_message.show_warning_message.assert_called()


def test_platform_edit_update(platform_fixture):
    base, section = platform_fixture

    base.ui.lineEdit_record_platform_name.setText("Coinbase")
    section.save()

    # Index 0 is "New", Index 1 is "Coinbase"
    section.edit_load(1)
    assert base.ui.lineEdit_record_platform_name.text() == "Coinbase"

    # Rename
    base.ui.lineEdit_record_platform_name.setText("CoinbasePro")
    section.save()

    section.edit_load(1)
    assert base.ui.lineEdit_record_platform_name.text() == "CoinbasePro"


def test_platform_remove_confirmed(platform_fixture, monkeypatch):
    base, section = platform_fixture

    base.ui.lineEdit_record_platform_name.setText("OKX")
    section.save()
    assert base.ui.comboBox_record_daily_platform.count() == 1

    section.edit_load(1)
    # Mock confirmation to Yes
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.Yes)
    section.remove()

    assert base.ui.comboBox_record_daily_platform.count() == 0


def test_platform_remove_cancelled(platform_fixture, monkeypatch):
    base, section = platform_fixture

    base.ui.lineEdit_record_platform_name.setText("Kraken")
    section.save()

    section.edit_load(1)
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.No)
    section.remove()

    assert base.ui.comboBox_record_daily_platform.count() == 1
