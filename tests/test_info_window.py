from config.info import InfoConfig
from windows.supplement.info import InfoWindow


def test_info_config_content():
    html = InfoConfig.get_html_content()
    assert "TradeDaily" in html
    assert InfoConfig.VERSION in html
    assert InfoConfig.AUTHOR in html
    assert InfoConfig.LICENSE in html
    assert "Developer's Note:" in html


def test_info_window_initialization(qtbot):
    window = InfoWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == InfoConfig.TITLE
    content = window.ui.textBrowser.toHtml()
    assert "TradeDaily" in content
    assert InfoConfig.VERSION in content

    # Test back button closes window
    window.show()
    assert window.isVisible()
    window.ui.pushButton.click()
    assert not window.isVisible()


def test_main_window_open_info(qtbot, mocker):
    from windows.main.main import MainWindow

    # Mock heavy components to keep unit test isolated
    mocker.patch("windows.main.main.UsersManager")
    mocker.patch("windows.main.main.Logger")
    mocker.patch("windows.main.main.SQLite")
    mocker.patch("windows.main.main.Rr")
    mocker.patch("windows.main.main.DataDisplay")
    mocker.patch("windows.main.main.Record")
    mocker.patch("windows.main.main.Strategy")
    mocker.patch("windows.main.main.Platform")
    mocker.patch("windows.main.main.Parity")
    mocker.patch("windows.main.main.Analysis")
    mocker.patch("windows.main.main.BalanceRecord")
    mocker.patch("windows.main.main.Accounts")

    main_win = MainWindow()
    qtbot.addWidget(main_win)

    assert main_win._info_window is None

    # Trigger action_info
    main_win.ui.action_info.trigger()

    assert main_win._info_window is not None
    qtbot.addWidget(main_win._info_window)
    assert main_win._info_window.isVisible()
    assert main_win._info_window.windowTitle() == InfoConfig.TITLE

    # Close info window
    main_win._info_window.close()
    assert not main_win._info_window.isVisible()
