from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QComboBox, QLineEdit, QMessageBox, QPushButton, QTextEdit, QWidget

from config.query.data_base import DataBaseQuery
from module.data.connection.sql_lite import SQLite
from windows.main.strategy import Strategy


class DummyStrategyBase(QWidget):
    def __init__(self, db):
        super().__init__()
        self._data_base = db
        self._logger = MagicMock()
        self.letters_numbers_val = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9]+"))
        self._status_bar_message = MagicMock()

        self.ui = MagicMock()
        self.ui.lineEdit_record_strategy_name = QLineEdit(self)
        self.ui.textEdit_record_strategy_text = QTextEdit(self)
        self.ui.comboBox_record_strategy_edit = QComboBox(self)
        self.ui.comboBox_record_daily_strategy = QComboBox(self)
        self.ui.pushButton_record_strategy_save = QPushButton(self)


@pytest.fixture
def strategy_fixture(qtbot, tmp_path):
    db_path = str(tmp_path / "test_strategy.db")
    SQLite.reset()
    db = SQLite(db_path)
    db.create_table(DataBaseQuery.STRATEGY)
    db.create_table(DataBaseQuery.TRANSACTION)
    db.create_table(DataBaseQuery.TRANSACTION_STRATEGY)

    base = DummyStrategyBase(db)
    qtbot.addWidget(base)
    section = Strategy(base)
    yield base, section

    db.close_connection()
    SQLite.reset()


def test_strategy_add_and_load(strategy_fixture):
    base, section = strategy_fixture

    base.ui.lineEdit_record_strategy_name.setText("Breakout")
    base.ui.textEdit_record_strategy_text.setText("Trading breakouts on high volume")
    section.save()

    assert base.ui.comboBox_record_daily_strategy.count() == 1
    assert base.ui.comboBox_record_strategy_edit.currentText() == "New"


def test_strategy_edit_and_update(strategy_fixture):
    base, section = strategy_fixture

    base.ui.lineEdit_record_strategy_name.setText("TrendFollowing")
    base.ui.textEdit_record_strategy_text.setText("Following EMAs")
    section.save()

    # Index 0 is "New", Index 1 is "TrendFollowing"
    section.edit_load(1)
    assert base.ui.lineEdit_record_strategy_name.text() == "TrendFollowing"
    assert base.ui.textEdit_record_strategy_text.toPlainText() == "Following EMAs"

    base.ui.textEdit_record_strategy_text.setText("Following 200 EMA")
    section.save()

    section.edit_load(1)
    assert base.ui.textEdit_record_strategy_text.toPlainText() == "Following 200 EMA"


def test_strategy_remove(strategy_fixture, monkeypatch):
    base, section = strategy_fixture

    base.ui.lineEdit_record_strategy_name.setText("Scalping")
    base.ui.textEdit_record_strategy_text.setText("Short-term scalping")
    section.save()

    section.edit_load(1)
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.Yes)
    section.remove()

    assert base.ui.comboBox_record_daily_strategy.count() == 0
