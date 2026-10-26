from typing import Any

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QLabel, QListWidgetItem, QMainWindow

from config import DataDisplayConfig
from config.query import DataDisplayQuery
from module.data.entities import (
    DbEntity,
    Transaction,
    TransactionDirection,
    TransactionFullData,
    TransactionState,
)
from module.data.manager import all_transaction_data, get_data
from module.tools.ui import list_widget_image_load
from module.tools.ui.table import DailyModel, StateInfoModel, StateInfoTabelData
from scripts import ExceptState, daily_table_load, except_work, state_info_table_load

from .i_section import ISection


class DataDisplay(ISection):
    # ? testler

    def __init__(self, base):

        super().__init__(base)
        self.__daily_table_model: DailyModel = None
        self.__daily_info_tabel_model: StateInfoModel = None
        self._child_windows: list[QMainWindow] = []
        QTimer.singleShot(10,self.reload)

    @except_work(ExceptState.CRITICAL)
    def daily_table_load(self, select_sql: str, values: tuple[Any, ...] | None = None):

        load = self.__get_data(Transaction, select_sql, values)
        if load is not None:
            self.__daily_table_model = daily_table_load(
                self,
                load,
                DataDisplayConfig.DAILY_TABLE_LOAD_START_COUNT,
            )
            self.__clear_externat_data()
            if load:
                self._base._status_bar_message.show_success_message(
                    DataDisplayConfig.DAILY_TABLE_LOAD_SUCCESS_MESSAGE,
                )
        else:
            self.__clear_externat_data()

    @except_work(ExceptState.CRITICAL)
    def daily_table_check_scroll(self, _):

        if (
            self._base.ui.tableView_daily.verticalScrollBar().value()
            == self._base.ui.tableView_daily.verticalScrollBar().maximum()
        ):
            self.__daily_table_load_more()

    @except_work(ExceptState.CRITICAL)
    def external_data_load(self,_):

        data:TransactionFullData = self.selected_data()
        self.__clear_externat_data()

        self._base.ui.label_daily_display_trn_no.setText(
            str(data.transaction.primary_key)
        )
        self._base.ui.label_daily_date_of_entry.setText(data.transaction.date_of_entry)
        self._base.ui.label_daily_platform.setText(data.transaction.platform)
        self._base.ui.label_daily_parity.setText(data.transaction.parity)
        self._base.ui.label_daily_rr_ratio.setText(str(data.transaction.rr))
        self._base.ui.label_daily_size.setText(str(data.transaction.size))
        self._base.ui.label_daily_direction.setText(
            TransactionDirection.direction_read[data.transaction.long_short]
        )
        self._base.ui.label_daily_state.setText(
            TransactionState.state_read_show[data.transaction.tp_sl]
        )

        if data.transaction.tp_sl is not None:
            self._base.ui.label_daily_date_of_exit.setText(data.closing.date_of_exit)
            self._base.ui.label_daily_result.setText(str(data.closing.result))
            if data.detail_closing:
                self._base.ui.label_daily_exit_price.setText(
                    str(data.detail_closing.exit_price)
                )

        if data.detail_open:
            self._base.ui.label_daily_enter_price.setText(
                str(data.detail_open.entry_price)
            )
            self._base.ui.label_daily_target_price.setText(
                str(data.detail_open.target_price)
            )
            self._base.ui.label_daily_stop_price.setText(
                str(data.detail_open.stop_price)
            )

        if data.note:
            self._base.ui.textBrowser_daily_not.setText(data.note.note_text)

        if data.chart_links:
            self._base.ui.listWidget_daily_chart_link.addItems(
                [i.link for i in data.chart_links]
            )

        if data.strategy:
            self._base.ui.listWidget_daily_strategy.addItems(
                [i.name for i in data.strategy]
            )

        if data.chart_images:
            list_widget_image_load(
                [i.image for i in data.chart_images],
                self.__image_load_error,
                self._base.ui.listWidget_daily_chart_image,
                str(data.transaction.primary_key),
            )

    @except_work(ExceptState.CRITICAL)
    def chart_image_display(self, item: QListWidgetItem):

        data = item.data(Qt.ItemDataRole.UserRole)
        pixmap = QPixmap()
        if not pixmap.loadFromData(data):
            self._base._status_bar_message.show_warning_message(
                DataDisplayConfig.CHART_IMAGE_DISPLAY_WARNING_MESSAGE
            )
            return

        child_window = QMainWindow(self._base)
        self._child_windows.append(child_window)
        child_window.setWindowTitle(
            f"{DataDisplayConfig.CHART_IMAGE_DISPLAY_WINDOWS_TITLE} {item.data(Qt.ItemDataRole.UserRole+1)}"
        )
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        child_window.setCentralWidget(label)
        child_window.resize(pixmap.size())
        child_window.show()

    @except_work(ExceptState.ERROR)
    def chart_link_display(self, item: QListWidgetItem):

        child_window = QMainWindow(self._base)
        self._child_windows.append(child_window)
        web_view = QWebEngineView()
        child_window.setCentralWidget(web_view)
        web_view.load(QUrl(item.text()))
        child_window.resize(*DataDisplayConfig.CHART_LINK_DISPLAY_WINDOWS_SIZE)
        child_window.setWindowTitle(item.text())
        web_view.show()
        child_window.show()

    @except_work(ExceptState.ERROR)
    def selected_data(self) -> TransactionFullData:

        transaction = self.__daily_table_model.get_selected_item(
            self._base.ui.tableView_daily
        )
        return all_transaction_data(self._base._data_base, transaction)

    @except_work(ExceptState.ERROR)
    def state_info_table_load(self):

        data = StateInfoTabelData(
            self._base._data_base.select(DataDisplayQuery.DATA_STATE_COUNT_OPEN)[0][0],
            self._base._data_base.select(DataDisplayQuery.DATA_STATE_COUNT_TP)[0][0],
            self._base._data_base.select(DataDisplayQuery.DATA_STATE_COUNT_SL)[0][0],
            self._base._data_base.select(DataDisplayQuery.DATA_STATE_COUNT_LONG)[0][0],
            self._base._data_base.select(DataDisplayQuery.DATA_STATE_COUNT_SHORT)[0][0],
            self._base._data_base.select(DataDisplayQuery.DATA_STATE_COUNT_TOTAL)[0][0],
        )
        self.__daily_info_tabel_model = state_info_table_load(self, data)

    @except_work(ExceptState.ERROR)
    def state_info_doubleClicked(self, index):

        if self.__daily_info_tabel_model:
            state = self.__daily_info_tabel_model.data(
                index.sibling(index.row(), 0),
                Qt.ItemDataRole.DisplayRole,
            )
            self.daily_table_load(DataDisplayQuery.STATE_LOAD[state])

    @except_work(ExceptState.CRITICAL)
    def reload(self):

        self.daily_table_load(DataDisplayQuery.LOAD)
        self.state_info_table_load()

    def time_sort(self,_):
        self.reload()

    def __clear_externat_data(self):

        self._base.ui.textBrowser_daily_not.clear()
        self._base.ui.listWidget_daily_chart_link.clear()
        self._base.ui.listWidget_daily_strategy.clear()
        self._base.ui.label_daily_exit_price.clear()
        self._base.ui.label_daily_date_of_exit.clear()
        self._base.ui.label_daily_result.clear()
        self._base.ui.label_daily_enter_price.clear()
        self._base.ui.label_daily_target_price.clear()
        self._base.ui.label_daily_stop_price.clear()
        self._base.ui.listWidget_daily_chart_image.clear()

    def __daily_table_load_more(self):

        self.__daily_table_model.load_more(DataDisplayConfig.DAILY_TABLE_LOAD_COUNT)
        self._base.ui.tableView_daily.resizeRowsToContents()

    @except_work(ExceptState.ERROR)
    def __get_data(
        self, entity: DbEntity, select_sql: str, values: tuple[Any, ...] | None = None
    ) -> list[DbEntity] | Exception:

        data = get_data(self._base._data_base, entity, select_sql, values)
        if type(data) == list:
            if self._base.ui.radioButton_display_time_up.isChecked():
                data.reverse()
            return data
        else:
            raise data

    def __image_load_error(self, message: str):

        self._base._status_bar_message.show_warning_message(message)
