import pytest

from config.global_var import Locations
from module.data.connection.sql_lite import SQLite
from windows.main.main import MainWindow


@pytest.fixture
def isolated_main_window(qtbot, tmp_path):
    old_main = Locations.MAIN
    old_app_data = Locations.APP_DATA
    old_setup = Locations.USER_SETUP

    app_path = tmp_path / "app_main_test"
    Locations.set_app_data(str(app_path))
    Locations.set_main(str(app_path))
    SQLite.reset()

    window = MainWindow()
    qtbot.addWidget(window)

    yield window

    window._data_base.close_connection()
    window._logger.close()
    if window._info_window:
        window._info_window.close()
    SQLite.reset()

    Locations.set_app_data(old_app_data)
    Locations.MAIN = old_main
    Locations.USER_SETUP = old_setup


def test_main_window_init(isolated_main_window):
    window = isolated_main_window
    assert window.windowTitle() == "TradeDaily"
    assert window._user_setup is not None
    assert window._user_setup.data.CURRENT_USER == "main"
    assert window.comboBox_accounts.currentText() == "main"


def test_main_window_open_info(isolated_main_window):
    window = isolated_main_window
    window.open_info()
    assert window._info_window is not None
    assert window._info_window.isVisible()


def test_main_window_tab_changed(isolated_main_window):
    window = isolated_main_window
    # Change to analysis tab
    analysis_index = window.ui.tabWidget_main.indexOf(window.ui.tab_analaysis)
    window.tab_changed(analysis_index)

    # Change to balance tab
    balance_index = window.ui.tabWidget_main.indexOf(window.ui.tab_balance)
    window.tab_changed(balance_index)


def test_main_window_reload_all_sections(isolated_main_window):
    window = isolated_main_window
    # Should run smoothly without raising errors
    window.reload_all_sections()


def test_main_window_user_change(isolated_main_window):
    window = isolated_main_window

    # Add a second profile
    window._user_setup.add("second_profile")
    window._accounts._Accounts__load()

    # Trigger user change via comboBox_accounts
    index = window.comboBox_accounts.findText("second_profile")
    assert index >= 0
    window.comboBox_accounts.setCurrentIndex(index)

    assert window._user_setup.data.CURRENT_USER == "second_profile"
    assert window._data_base is not None
