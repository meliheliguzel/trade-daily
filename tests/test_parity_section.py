from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QPushButton, QWidget

from config.parity import ParityConfig
from config.query.data_base import DataBaseQuery
from config.query.platform import PlatformQuery
from module.data.connection.sql_lite import SQLite
from module.data.entities import PlatformEntity
from windows.main.parity import Parity


class DummyBase(QWidget):
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
def base_and_parity(qtbot, tmp_path):
    db_path = str(tmp_path / "test.db")
    SQLite.reset()
    db = SQLite(db_path)
    db.create_table(DataBaseQuery.platform)
    db.create_table(DataBaseQuery.parity)
    db.create_table(DataBaseQuery.transaction)

    # Insert a test platform
    db.insert(PlatformQuery.ADD, ("Binance",))
    platform_entity = PlatformEntity(1, "Binance")

    base = DummyBase(db)
    qtbot.addWidget(base)
    base.ui.comboBox_record_parity_edit_platform.addItem("Binance", platform_entity)
    base.ui.comboBox_record_daily_platform.addItem("Binance", platform_entity)

    parity_section = Parity(base)
    # Connect signals as done in main.py
    base.ui.comboBox_record_parity_edit_platform.currentIndexChanged.connect(parity_section.load)
    base.ui.comboBox_record_parity_edit.currentIndexChanged.connect(parity_section.edit_load)

    # Initial load
    parity_section.load(0)

    yield base, parity_section

    parity_section._thread_work.stop()
    db.close_connection()
    SQLite.reset()


def test_add_multiple_parities_without_reselecting_platform(base_and_parity):
    base, parity_section = base_and_parity

    # Add first parity: BTCUSDT
    base.ui.lineEdit_record_parity_name.setText("BTCUSDT")
    parity_section.save()

    base._status_bar_message.show_success_message.assert_called_with(
        ParityConfig.ADD_SUCCES_MESSAGE
    )

    # Verify combobox now has "New" and "BTCUSDT"
    assert base.ui.comboBox_record_parity_edit.count() == 2
    assert base.ui.comboBox_record_parity_edit.itemText(0) == "New"
    assert base.ui.comboBox_record_parity_edit.itemText(1) == "BTCUSDT"

    # User does NOT touch platform combobox (it remains on Binance)
    # User types second parity: ETHUSDT
    base._status_bar_message.reset_mock()
    base.ui.lineEdit_record_parity_name.setText("ETHUSDT")
    parity_section.save()

    # Verify second save succeeds without error!
    base._status_bar_message.show_success_message.assert_called_with(
        ParityConfig.ADD_SUCCES_MESSAGE
    )

    # Verify both parities are in combobox
    assert base.ui.comboBox_record_parity_edit.count() == 3
    items = [base.ui.comboBox_record_parity_edit.itemText(i) for i in range(3)]
    assert "New" in items
    assert "BTCUSDT" in items
    assert "ETHUSDT" in items


def test_parity_duplicate_warning(base_and_parity):
    base, parity_section = base_and_parity

    # Add first parity
    base.ui.lineEdit_record_parity_name.setText("BTCUSDT")
    parity_section.save()

    # Try adding BTCUSDT again on same platform
    base._status_bar_message.reset_mock()
    base.ui.lineEdit_record_parity_name.setText("BTCUSDT")
    parity_section.save()

    # Should warn that parity already exists
    base._status_bar_message.show_warning_message.assert_called_with(
        ParityConfig.ADD_WARNING_MESSAGE
    )


def test_parity_edit_existing(base_and_parity):
    base, parity_section = base_and_parity

    # Add BTCUSDT
    base.ui.lineEdit_record_parity_name.setText("BTCUSDT")
    parity_section.save()

    # Select BTCUSDT in combobox (index 1)
    base.ui.comboBox_record_parity_edit.setCurrentIndex(1)
    assert base.ui.lineEdit_record_parity_name.text() == "BTCUSDT"

    # Save without changing name: should succeed (no self-conflict)
    base._status_bar_message.reset_mock()
    parity_section.save()
    base._status_bar_message.show_success_message.assert_called_with(
        ParityConfig.ADD_SUCCES_MESSAGE
    )

    # Change name to BTCUSD and save
    base.ui.comboBox_record_parity_edit.setCurrentIndex(1)
    base.ui.lineEdit_record_parity_name.setText("BTCUSD")
    base._status_bar_message.reset_mock()
    parity_section.save()
    base._status_bar_message.show_success_message.assert_called_with(
        ParityConfig.ADD_SUCCES_MESSAGE
    )

    items = [base.ui.comboBox_record_parity_edit.itemText(i) for i in range(base.ui.comboBox_record_parity_edit.count())]
    assert "BTCUSD" in items


def test_parity_empty_name_warning(base_and_parity):
    base, parity_section = base_and_parity

    base.ui.lineEdit_record_parity_name.setText("")
    parity_section.save()

    base._status_bar_message.show_warning_message.assert_called_with(
        ParityConfig.GET_DATA_WARNING_MESSAGE
    )
