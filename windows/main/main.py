from pathlib import Path

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QDoubleValidator, QIntValidator, QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow

from config import AccountsConfig, StatusBarTimeOut, UserLocations
from module.data.connection import SQLite
from module.data.settings import UsersManager
from module.tools import Logger
from module.tools.ui import StatusbarMessage
from ui import Ui_Base
from windows.supplement import InfoWindow

from .accounts import Accounts
from .analysis import Analysis
from .balance_record import BalanceRecord
from .data_display import DataDisplay
from .parity import Parity
from .platform import Platform
from .record import Record
from .rr import Rr
from .strategy import Strategy


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Base()
        self.ui.setupUi(self)
        self.setWindowTitle("TradeDaily")

        self._user_setup:UsersManager = UsersManager()
        self._user_loc:UserLocations = self._user_setup.get_user_loc()

        self._status_bar_message: StatusbarMessage = StatusbarMessage(self.ui.statusbar,StatusBarTimeOut)
        self._logger: Logger = Logger(self._user_loc.LOG)
        self._data_base = SQLite(self._user_loc.DATA_BASE)


        self.positive_float_val = QDoubleValidator(0.0, 1e9, 6, self)
        self.float_val = QDoubleValidator(-1e9, 1e9, 6, self)
        self.letters_numbers_val = QRegularExpressionValidator(QRegularExpression(r"^[a-zA-Z0-9/\- ]*$"), self)
        self.int_val = QIntValidator(1, 1e9, self)
        self.comboBox_accounts = QComboBox(self.ui.menubar)
        self.comboBox_accounts.setObjectName("comboBox_accounts")
        self.ui.menubar.setCornerWidget(self.comboBox_accounts, Qt.Corner.TopRightCorner)



        self._rr = Rr(self)
        self.ui.pushButton_rr_calculate.clicked.connect(self._rr.standart_calculate)

        self._data_display = DataDisplay(self)
        self.ui.tableView_daily.verticalScrollBar().valueChanged.connect(self._data_display.daily_table_check_scroll)
        self.ui.tableView_daily.clicked.connect(self._data_display.external_data_load)
        self.ui.listWidget_daily_chart_image.itemDoubleClicked.connect(self._data_display.chart_image_display)
        self.ui.listWidget_daily_chart_link.itemDoubleClicked.connect(self._data_display.chart_link_display)
        self.ui.tableView_daily_state_info.doubleClicked.connect(self._data_display.state_info_doubleClicked)
        self.ui.radioButton_display_time_down.toggled.connect(self._data_display.time_sort)
        self.ui.radioButton_display_time_up.toggled.connect(self._data_display.time_sort)

        self._record = Record(self)
        self.ui.pushButton_transaction_update.clicked.connect(self._record.update_data_load_table)
        self.ui.lineEdit_record_daily_transaction_id.returnPressed.connect(self._record.update_data_load)
        self.ui.toolButton_record_daily_search.clicked.connect(self._record.update_data_load)
        self.ui.pushButton_record_daily_save.clicked.connect(self._record.save)
        self.ui.toolButton_record_daily_delete.clicked.connect(self._record.remove)
        self.ui.toolButton_record_daily_clean.clicked.connect(self._record._clear_all)
        self.ui.comboBox_record_daily_open_trn.currentIndexChanged.connect(self._record.open_transaction_load)

        self.ui.toolButton_record_daily_strategy_del.clicked.connect(self._record.strategy_remove)
        self.ui.comboBox_record_daily_strategy.currentIndexChanged.connect(self._record.strategy_add)

        self.ui.toolButton_record_daily_chart_image_add.clicked.connect(self._record.image_add)
        self.ui.toolButton_record_daily_chart_image_del.clicked.connect(self._record.image_remove)

        self.ui.toolButton_record_daily_chart_link_add.clicked.connect(self._record.link_add)
        self.ui.toolButton_record_daily_chart_link_del.clicked.connect(self._record.link_remove)
        self.ui.lineEdit_record_daily_chart_link.returnPressed.connect(self._record.link_add)

        self._strategy = Strategy(self)
        self.ui.comboBox_record_strategy_edit.currentIndexChanged.connect(self._strategy.edit_load)
        self.ui.pushButton_record_strategy_save.clicked.connect(self._strategy.save)
        self.ui.toolButton_record_strategy_del.clicked.connect(self._strategy.remove)

        self._platform = Platform(self)

        self.ui.comboBox_record_platform_edit.currentIndexChanged.connect(self._platform.edit_load)
        self.ui.pushButton_record_platform_save.clicked.connect(self._platform.save)
        self.ui.toolButton_record_platform_del.clicked.connect(self._platform.remove)

        self._parity = Parity(self)
        self.ui.comboBox_record_parity_edit_platform.currentIndexChanged.connect(self._parity.load)
        self.ui.comboBox_record_daily_platform.currentIndexChanged.connect(self._parity.daily_load)
        self.ui.comboBox_record_parity_edit.currentIndexChanged.connect(self._parity.edit_load)
        self.ui.pushButton_record_parity_save.clicked.connect(self._parity.save)
        self.ui.toolButton_record_parity_del.clicked.connect(self._parity.remove)

        self._analysis = Analysis(self)

        self._balance_record = BalanceRecord(self)
        self.ui.comboBox_record_balance.currentIndexChanged.connect(self._balance_record.edit_load)
        self.ui.pushButton_record_balance_save.clicked.connect(self._balance_record.save)
        self.ui.toolButton_record_balance_del.clicked.connect(self._balance_record.remove)
        self._accounts = Accounts(self)
        self.ui.comboBox_record_accounts_edit.currentIndexChanged.connect(self._accounts.edit_load)
        self.ui.pushButton_record_accounts_save.clicked.connect(self._accounts.save)
        self.ui.toolButton_record_accounts_del.clicked.connect(self._accounts.remove)

        # Account switching (Default account and Menu Bar)
        self.ui.comboBox_record_accounts_default.currentIndexChanged.connect(self.user_change)
        self.comboBox_accounts.currentIndexChanged.connect(self.user_change)

        # Tab switching listener
        self.ui.tabWidget_main.currentChanged.connect(self.tab_changed)

        # Info / About dialog setup
        self._info_window: InfoWindow | None = None
        self.ui.action_info.setText("About TradeDaily")
        self.ui.action_info.setShortcut("F1")
        self.ui.menuinfo.addAction(self.ui.action_info)
        self.ui.action_info.triggered.connect(self.open_info)

    def open_info(self) -> None:
        """Opens the About/Info dialog window."""
        if self._info_window is None:
            self._info_window = InfoWindow(self)
        self._info_window.show()
        self._info_window.raise_()
        self._info_window.activateWindow()

    def user_change(self) -> None:
        sender = self.sender()
        if not sender:
            return
        new_user = sender.currentText()
        if new_user and self._user_setup and new_user != self._user_setup.data.CURRENT_USER:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:
                self._user_setup.set_current_user(new_user)
                self._user_loc = self._user_setup.get_user_loc()

                self._logger.set_log_file(self._user_loc.LOG)

                self._data_base.close_connection()
                SQLite.reset()

                self._data_base = SQLite(self._user_loc.DATA_BASE)

                self.reload_all_sections()

                self._accounts._Accounts__load()

                msg = AccountsConfig.USER_CHANGE_SUCCESS_MESSAGE.format(new_user)
                self._status_bar_message.show_success_message(msg)
                self._logger.info(msg)
            finally:
                QApplication.restoreOverrideCursor()


    def reload_all_sections(self) -> None:
        """Reloads all sections from the new database when the active account changes."""
        self._record._clear_all()
        self._record.open_transaction()
        self._platform.load()
        self._strategy.load()

        self._balance_record.load()
        self._balance_record.recalculation()
        self._data_display.reload()
        self._analysis.draw_graph()

    def tab_changed(self, index: int) -> None:
        """Handles tab change to lazily render or refresh analysis/balance charts if needed."""
        current_widget = self.ui.tabWidget_main.widget(index)
        if current_widget == self.ui.tab_analaysis:
            if not Path(self._user_loc.ANALYSIS_GRAPH).is_file():
                self._analysis.draw_graph()
            elif self._analysis.web_view is None:
                self._analysis.graph_display()
        elif current_widget == self.ui.tab_balance:
            if not Path(self._user_loc.BALANCE_GRAPH).is_file():
                self._balance_record.draw_graph()
            elif self._balance_record.web_view is None:
                self._balance_record.graph_display()
