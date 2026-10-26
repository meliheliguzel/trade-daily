import os
from pathlib import Path

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMessageBox, QSizePolicy

from config import BalanceConfig
from config.global_var import Locations
from config.query import BalanceQuery
from module.data.entities import Balance, BalanceSize
from module.data.manager import BalanceGraphData, get_data
from module.tools.charts.balance import balance_graphics_create
from module.tools.ui import change_border, clearLayout, comboBox_data_load, input_control
from scripts import ExceptState, except_work

from .i_section import ISection


class BalanceRecord(ISection):

    def __init__(self, base):
        super().__init__(base)
        self._base.ui.lineEdit_record_balance_size.setValidator(self._base.float_val)
        self.__select_data = None
        self.load()
        self._thread_work.signals.finished.connect(self.graph_display)
        self.__web_view = None
        QTimer.singleShot(10, self.graph_display)

    @property
    def web_view(self) -> QWebEngineView | None:
        return self.__web_view

    @except_work(ExceptState.CRITICAL)
    def save(self):

        data = self.__get_data()
        if data:

            self._base.ui.widget_record_balance.setDisabled(True)
            if self.__select_data:
                self.update(data)
            else:
                self.add(data)
            self.load()
            self.__clear_edit()
            self._base.ui.widget_record_balance.setDisabled(False)

        else:
            self.__clear_edit()
            self._base._status_bar_message.show_warning_message(
                BalanceConfig.ADD_WARNING_MESSAGE
            )
            change_border(
                self._base.ui.lineEdit_record_balance_size,
                duration=BalanceConfig.ADD_BORDER_DURATION,
            )

    @except_work(ExceptState.ERROR)
    def add(self, data: BalanceSize):

        data.primary_key = self._base._data_base.insert(
            BalanceQuery.SIZE_ADD, (data.size, data.state)
        )
        self.__calculate(data)
        self.draw_graph()
        self._base._status_bar_message.show_success_message(
            BalanceConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.ERROR)
    def update(self, data: BalanceSize):

        data.primary_key = self.__select_data.primary_key
        self._base._data_base.update(
            BalanceQuery.SIZE_UPDATE,
            (data.size, data.state, data.primary_key),
        )
        self.__calculate(data)
        self.draw_graph()
        self._base._status_bar_message.show_success_message(
            BalanceConfig.UPDATE_SUCCES_MESSAGE
        )

    @except_work(ExceptState.CRITICAL)
    def remove(self):

        if self.__select_data:

            msg_box = QMessageBox(self._base)
            msg_box.setWindowTitle(BalanceConfig.REMOVE_MESSAGE_BOX_TITLE)
            msg_box.setText(BalanceConfig.REMOVE_MESSAGE_BOX_TEXT)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            if msg_box.exec() == QMessageBox.Yes:
                id = self.__select_data.primary_key

                self._base._data_base.delete(BalanceQuery.DEL_BALANCE, id)
                self._base._data_base.delete(BalanceQuery.SIZE_DEL, id)
                self._base._status_bar_message.show_success_message(
                    BalanceConfig.REMOVE_SUCCES_MESSAGE
                )
                self.load()
                self.__clear_edit()
                self.draw_graph()

            else:  # ? cancel
                self._base._status_bar_message.show_info_message(
                    BalanceConfig.REMOVE_INFO_CANCEL
                )

        else:  # ? not select
            self._base._status_bar_message.show_notice_message(
                BalanceConfig.REMOVE_NOTICE_NOT_SELECT
            )

    @except_work(ExceptState.ERROR)
    def load(self):
        self._base.ui.comboBox_record_balance.blockSignals(True)
        data = get_data(self._base._data_base, BalanceSize, BalanceQuery.LOAD)
        if type(data) == list:
            size = {str(i.size): i for i in data}
        else:
            raise data
        comboBox_data_load(self._base.ui.comboBox_record_balance, size)
        self._base.ui.comboBox_record_balance.blockSignals(False)

        if data:
            self._base.ui.comboBox_record_balance.setCurrentIndex(0)
            self.edit_load(0)
        else:
            self._base.ui.comboBox_record_balance.setCurrentIndex(-1)
            self.__clear_edit()

    @except_work(ExceptState.ERROR)
    def edit_load(self, index):

        data: BalanceSize = self._base.ui.comboBox_record_balance.itemData(index)
        if data:
            self._base.ui.lineEdit_record_balance_size.setText(str(data.size))
            if data.state == 0:
                self._base.ui.radioButton_record_balance_close.setChecked(True)
            else:
                self._base.ui.radioButton_record_balance_open.setChecked(True)
            self.__select_data = data
        else:
            self.__clear_edit()

    @except_work(ExceptState.ERROR)
    def __get_data(self) -> BalanceSize | None:
        "result -> name"

        if input_control(
            [
                self._base.ui.lineEdit_record_balance_size,
            ],
            duration=BalanceConfig.INPUT_DURATION,
        ):
            size = float(self._base.ui.lineEdit_record_balance_size.text())
            if self._base.ui.radioButton_record_balance_close.isChecked():
                state = 0
            else:
                state = 1
            return BalanceSize(0, size, state)
        else:
            self._base._status_bar_message.show_warning_message(
                BalanceConfig.GET_DATA_WARNING_MESSAGE
            )
            return None

    @except_work(ExceptState.ERROR)
    def __clear_edit(self):

        self.__select_data = None
        self._base.ui.lineEdit_record_balance_size.clear()
        self._base.ui.radioButton_record_balance_open.setChecked(True)

    @except_work(ExceptState.ERROR)
    def __calculate(self, data: BalanceSize):

        if data.state == 1:
            self._base._data_base.delete(BalanceQuery.DEL_BALANCE, data.primary_key)
            rows = self._base._data_base.select(
                BalanceQuery.CALCULATE, (data.size, data.primary_key)
            )
            if rows:
                self._base._data_base.insert_many(BalanceQuery.ADD, rows)

    @except_work(ExceptState.ERROR)
    def graph_display(self):

        if (
            Path(self._base._user_loc.BALANCE_GRAPH).is_file()
            and os.path.getsize(self._base._user_loc.BALANCE_GRAPH) > 0
        ):

            clearLayout(self._base.ui.verticalLayout_balance)

            self.__web_view = QWebEngineView()
            self._base.ui.verticalLayout_balance.addWidget(self.__web_view)

            self.__web_view.load(QUrl.fromLocalFile(self._base._user_loc.BALANCE_GRAPH))

            self.__web_view.sizePolicy().setHorizontalPolicy(
                QSizePolicy.Policy.Expanding
            )
            self.__web_view.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
            self.__web_view.page().profile().downloadRequested.connect(
                self.__on_downloadRequested
            )
        else:
            clearLayout(self._base.ui.verticalLayout_balance)
            self.__web_view = None
            self._base._status_bar_message.show_warning_message(
                BalanceConfig.NOT_FOUND_GRAPH_MESSAGE
            )

    @except_work(ExceptState.CRITICAL)
    def draw_graph(self):
        balance_ids = self._base._data_base.select(BalanceQuery.SIZE_IDS)
        count_res = self._base._data_base.select('SELECT COUNT(*) FROM Balance;')
        if not balance_ids or not count_res or count_res[0][0] == 0:
            if os.path.exists(self._base._user_loc.BALANCE_GRAPH):
                try:
                    os.remove(self._base._user_loc.BALANCE_GRAPH)
                except Exception:
                    pass
            clearLayout(self._base.ui.verticalLayout_balance)
            self.__web_view = None
            self._base._status_bar_message.show_warning_message(
                BalanceConfig.NOT_FOUND_GRAPH_MESSAGE
            )
            return

        data = self.__get_graph_data()
        if not data:
            if os.path.exists(self._base._user_loc.BALANCE_GRAPH):
                try:
                    os.remove(self._base._user_loc.BALANCE_GRAPH)
                except Exception:
                    pass
            clearLayout(self._base.ui.verticalLayout_balance)
            self.__web_view = None
            self._base._status_bar_message.show_warning_message(
                BalanceConfig.NOT_FOUND_GRAPH_MESSAGE
            )
            return

        self._thread_work.add_work(
            balance_graphics_create, [data, self._base._user_loc.BALANCE_GRAPH]
        )


    @except_work(ExceptState.ERROR)
    def __on_downloadRequested(self, download: QWebEngineDownloadRequest):

        download.setDownloadDirectory(Locations.DOWNLOAD)
        download.accept()
        self._base._status_bar_message.show_info_message(
            download.downloadFileName() + BalanceConfig.IMAGE_DOWNLOAD_MESSAGE
        )

    @except_work(ExceptState.ERROR)
    def __get_graph_data(self) -> list[BalanceGraphData]:

        result = []
        balance_ids = self._base._data_base.select(BalanceQuery.SIZE_IDS)

        for i in balance_ids:
            data = get_data(self._base._data_base, Balance, BalanceQuery.BALANCE_GET, i)
            if not data:
                continue
            graph_data = BalanceGraphData()
            graph_data.apply_balance_data(data)
            result.append(graph_data)

        return result

    @except_work(ExceptState.ERROR)
    def recalculation(self):
        for i in get_data(self._base._data_base, BalanceSize, BalanceQuery.LOAD):
            self.__calculate(i)
        self.draw_graph()


