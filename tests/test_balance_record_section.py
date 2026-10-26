from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QRadioButton, QVBoxLayout, QWidget

from config.balance_record import BalanceConfig
from config.query.data_base import DataBaseQuery
from module.data.connection.sql_lite import SQLite
from windows.main.balance_record import BalanceRecord


class DummyBalanceBase(QWidget):
    def __init__(self, db, tmp_path):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self.float_val = QDoubleValidator()
        self._status_bar_message = MagicMock()

        self._user_loc = MagicMock()
        self._user_loc.BALANCE_GRAPH = str(tmp_path / "balance_graph.html")

        self.ui = MagicMock()
        self.ui.lineEdit_record_balance_size = QLineEdit(self)
        self.ui.comboBox_record_balance = QComboBox(self)
        self.ui.radioButton_record_balance_close = QRadioButton(self)
        self.ui.radioButton_record_balance_open = QRadioButton(self)
        self.ui.widget_record_balance = QWidget(self)
        self.ui.verticalLayout_balance = QVBoxLayout(self)


@pytest.fixture
def balance_section(qtbot, tmp_path):
    db_path = str(tmp_path / "test.db")
    SQLite.reset()
    db = SQLite(db_path)
    db.create_table(DataBaseQuery.BALANCE_SIZE)
    db.create_table(DataBaseQuery.BALANCE)
    db.create_table(DataBaseQuery.TRANSACTION)
    db.create_table(DataBaseQuery.TRANSACTION_CLOSING)

    base = DummyBalanceBase(db, tmp_path)
    qtbot.addWidget(base)

    section = BalanceRecord(base)
    yield base, section

    section._thread_work.stop()
    db.close_connection()
    SQLite.reset()


def test_add_balance_in_empty_account_does_not_crash(balance_section):
    base, section = balance_section

    # In a fresh account with 0 transactions, enter 1000.0
    base.ui.lineEdit_record_balance_size.setText("1000.0")
    base.ui.radioButton_record_balance_open.setChecked(True)

    section.save()

    # Verify save succeeded
    base._status_bar_message.show_success_message.assert_called_with(
        BalanceConfig.ADD_SUCCES_MESSAGE
    )

    # Verify Balance_Size record was created in database
    sizes = base._data_base.select("SELECT size, state FROM Balance_Size;")
    assert len(sizes) == 1
    assert sizes[0][0] == 1000.0
    assert sizes[0][1] == 1


def test_balance_draw_graph_with_no_balance_rows(balance_section):
    base, section = balance_section

    # Directly call draw_graph when there are no balance rows
    section.draw_graph()

    # Should safely display not found warning without exceptions
    base._status_bar_message.show_warning_message.assert_called_with(
        BalanceConfig.NOT_FOUND_GRAPH_MESSAGE
    )
