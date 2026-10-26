from enum import Enum

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QStatusBar


class MessageType(Enum):
    INFO = "blue"  # Dark and light theme friendly color
    ERROR = "red"
    WARNING = "orange"
    SUCCESS = "green"
    CRITICAL = "purple"
    NOTICE = "cyan"

class MessageTimeout:

    WARNING: int
    INFO: int
    ERROR: int
    SUCCESS: int
    CRITICAL: int
    NOTICE: int

class StatusbarMessage:

    def __init__(self, status_bar: QStatusBar,message_timeout:MessageTimeout):
        self.__status_bar = status_bar
        self.__timeout:MessageTimeout = message_timeout

    def __show_message(self, message: str, message_type: MessageType, time_out: int = 0):
        """Show message with specified type and timeout."""
        self.__status_bar.setStyleSheet(f"QStatusBar {{ color: {message_type.value}; }}")
        if time_out > 0:
            self.__status_bar.showMessage(message, time_out * 1000)
        else:
            self.__status_bar.showMessage(message)

        if time_out > 0:
            QTimer.singleShot(time_out * 1000, self.reset_status_bar)

    def show_info_message(self, message: str):
        """Show info message."""
        self.__show_message(message, MessageType.INFO, self.__timeout.INFO)

    def show_error_message(self, message: str):
        """Show error message. Text color red."""
        self.__show_message(message, MessageType.ERROR, self.__timeout.ERROR)

    def show_warning_message(self, message: str):
        """Show warning message. Text color orange."""
        self.__show_message(message, MessageType.WARNING, self.__timeout.WARNING)

    def show_success_message(self, message: str):
        """Show success message. Text color green."""
        self.__show_message(message, MessageType.SUCCESS, self.__timeout.SUCCESS)

    def show_critical_message(self, message: str):
        """Show critical message. Text color purple."""
        self.__show_message(message, MessageType.CRITICAL, self.__timeout.CRITICAL)

    def show_notice_message(self, message: str):
        """Show notice message. Text color cyan."""
        self.__show_message(message, MessageType.NOTICE, self.__timeout.NOTICE)

    def reset_status_bar(self):
        """Reset the status bar text color to default."""
        self.__status_bar.setStyleSheet("")
        self.__status_bar.showMessage("")

