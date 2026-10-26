from PySide6.QtWidgets import QStatusBar

from config.global_var import StatusBarTimeOut
from module.tools.ui.status_bar_message import MessageType, StatusbarMessage


def test_statusbar_message(qtbot):
    bar = QStatusBar()
    qtbot.addWidget(bar)

    sb_msg = StatusbarMessage(bar, StatusBarTimeOut)

    sb_msg.show_info_message("Info test")
    assert bar.currentMessage() == "Info test"
    assert MessageType.INFO.value in bar.styleSheet()

    sb_msg.show_error_message("Error test")
    assert bar.currentMessage() == "Error test"
    assert MessageType.ERROR.value in bar.styleSheet()

    sb_msg.show_warning_message("Warning test")
    assert bar.currentMessage() == "Warning test"
    assert MessageType.WARNING.value in bar.styleSheet()

    sb_msg.show_success_message("Success test")
    assert bar.currentMessage() == "Success test"
    assert MessageType.SUCCESS.value in bar.styleSheet()

    sb_msg.show_critical_message("Critical test")
    assert bar.currentMessage() == "Critical test"
    assert MessageType.CRITICAL.value in bar.styleSheet()

    sb_msg.show_notice_message("Notice test")
    assert bar.currentMessage() == "Notice test"
    assert MessageType.NOTICE.value in bar.styleSheet()

    sb_msg.reset_status_bar()
    assert bar.currentMessage() == ""
    assert bar.styleSheet() == ""
