from enum import IntEnum, StrEnum

from PySide6.QtCore import QStandardPaths

from module.tools.ui import MessageTimeout


class GlobalConfig(StrEnum):
    VERSION = "1.0"
    APP_NAME = "Trade_Daily"


class FileNames(StrEnum):

    LOG_FILE = "app.log"
    DATA_BASE = "default.db"
    ANALYSIS_GRAPH = "analysis_graph.html"
    BALANCE_GRAPH = "balance_graph.html"
    USER_SETUP = "user_setup.json"


class Locations:
    APP_DATA: str = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppDataLocation
    )
    DOWNLOAD: str = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.DownloadLocation
    )
    MAIN: str = f"{APP_DATA}/{GlobalConfig.APP_NAME}"

    USER_SETUP: str = f"{MAIN}/{FileNames.USER_SETUP}"

    @staticmethod
    def set_app_data(path: str) -> None:
        Locations.APP_DATA = path

    @staticmethod
    def set_user_setup(path: str) -> None:
        Locations.USER_SETUP = path

    @staticmethod
    def set_main(path: str) -> None:
        Locations.MAIN = path
        Locations.USER_SETUP = f"{path}/{FileNames.USER_SETUP}"


class UserLocations:

    def __init__(self, user_name: str):

        self.LOG: str = f"{Locations.MAIN}/{user_name}/{FileNames.LOG_FILE}"
        self.DATA_BASE: str = f"{Locations.MAIN}/{user_name}/{FileNames.DATA_BASE}"
        self.ANALYSIS_GRAPH: str = (
            f"{Locations.MAIN}/{user_name}/{FileNames.ANALYSIS_GRAPH}"
        )
        self.BALANCE_GRAPH: str = (
            f"{Locations.MAIN}/{user_name}/{FileNames.BALANCE_GRAPH}"
        )


class StatusBarTimeOut(MessageTimeout, IntEnum):  #

    WARNING = 5
    INFO = 5
    ERROR = 7
    SUCCESS = 5
    CRITICAL = 15
    NOTICE = 5
