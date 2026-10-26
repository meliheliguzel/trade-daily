from PySide6.QtGui import QDoubleValidator, QIntValidator, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow

from config import UserLocations
from module.data.connection import Connect
from module.data.settings import UsersManager
from module.tools import Logger
from module.tools.ui import StatusbarMessage
from ui import Ui_Base

from .analysis import AnalysisProtokol
from .balance_record import BalanceRecordProtokol
from .data_display import DataDisplayProtokol


class MainWindowProtocol(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui: Ui_Base
        self._status_bar_message: StatusbarMessage
        self._logger: Logger
        self._data_base:Connect
        self._user_setup:UsersManager
        self._user_loc:UserLocations


        self.positive_float_val:QDoubleValidator
        self.float_val:QDoubleValidator
        self.letters_numbers_val:QRegularExpressionValidator
        self.int_val:QIntValidator
        self.url_val:QRegularExpressionValidator

        self._data_display:DataDisplayProtokol
        self._analysis:AnalysisProtokol
        self._balance_record:BalanceRecordProtokol
