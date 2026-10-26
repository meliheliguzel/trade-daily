from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QComboBox, QLineEdit, QMessageBox, QWidget

from config.global_var import Locations
from module.data.connection.sql_lite import SQLite
from module.data.settings.users import UsersManager
from windows.main.accounts import Accounts


class DummyAccountsBase(QWidget):
    def __init__(self, tmp_path):
        super().__init__()
        self._user_setup = UsersManager()
        self._user_loc = self._user_setup.get_user_loc()
        self._status_bar_message = MagicMock()
        self._logger = MagicMock()
        self._data_base = SQLite(self._user_loc.DATA_BASE)
        self.reload_all_sections = MagicMock()

        self.comboBox_accounts = QComboBox(self)
        self.ui = MagicMock()
        self.ui.comboBox_record_accounts_default = QComboBox(self)
        self.ui.comboBox_record_accounts_edit = QComboBox(self)
        self.ui.lineEdit_record_accounts_name = QLineEdit(self)


@pytest.fixture
def accounts_fixture(qtbot, tmp_path):
    old_main = Locations.MAIN
    old_app_data = Locations.APP_DATA
    old_setup = Locations.USER_SETUP

    app_path = tmp_path / "accounts_test"
    Locations.set_app_data(str(app_path))
    Locations.set_main(str(app_path))
    SQLite.reset()

    base = DummyAccountsBase(tmp_path)
    qtbot.addWidget(base)
    section = Accounts(base)

    yield base, section

    base._data_base.close_connection()
    SQLite.reset()
    Locations.set_app_data(old_app_data)
    Locations.MAIN = old_main
    Locations.USER_SETUP = old_setup


def test_accounts_add_and_update(accounts_fixture):
    base, section = accounts_fixture

    # Index 0 is "New"
    base.ui.comboBox_record_accounts_edit.setCurrentText("New")
    base.ui.lineEdit_record_accounts_name.setText("prop_firm")
    section.save()

    assert "prop_firm" in base._user_setup.get_user_list()
    assert base.ui.lineEdit_record_accounts_name.text() == ""

    # Rename prop_firm to prop_firm_funded
    base.ui.comboBox_record_accounts_edit.setCurrentText("prop_firm")
    base.ui.lineEdit_record_accounts_name.setText("prop_firm_funded")
    section.save()

    assert "prop_firm_funded" in base._user_setup.get_user_list()
    assert "prop_firm" not in base._user_setup.get_user_list()


def test_accounts_edit_load(accounts_fixture):
    base, section = accounts_fixture

    base.ui.comboBox_record_accounts_edit.setCurrentText("New")
    section.edit_load()
    assert base.ui.lineEdit_record_accounts_name.text() == ""

    base.ui.comboBox_record_accounts_edit.setCurrentText("main")
    section.edit_load()
    assert base.ui.lineEdit_record_accounts_name.text() == "main"


def test_accounts_remove(accounts_fixture, monkeypatch):
    base, section = accounts_fixture

    # Add account to remove
    base.ui.comboBox_record_accounts_edit.setCurrentText("New")
    base.ui.lineEdit_record_accounts_name.setText("temp_acc")
    section.save()

    assert "temp_acc" in base._user_setup.get_user_list()

    # Cancel remove
    base.ui.comboBox_record_accounts_edit.setCurrentText("temp_acc")
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.StandardButton.No)
    section.remove()
    assert "temp_acc" in base._user_setup.get_user_list()

    # Confirm remove
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.StandardButton.Yes)
    section.remove()
    assert "temp_acc" not in base._user_setup.get_user_list()
