import os
from pathlib import Path

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QSizePolicy

from config import AnalysisConfig
from config.global_var import Locations
from config.query import AnalysisQuery
from module.data.manager import AnalysisGraphData
from module.tools.charts.analysis import analysis_graphics_create
from module.tools.ui import clearLayout
from scripts import ExceptState, except_work

from .i_section import ISection


class Analysis(ISection):

    def __init__(self, base):
        super().__init__(base)
        self._thread_work.signals.finished.connect(self.graph_display)
        self.__web_view = None

        if (
            Path(self._base._user_loc.ANALYSIS_GRAPH).is_file()
            and os.path.getsize(self._base._user_loc.ANALYSIS_GRAPH) > 0
        ):
            QTimer.singleShot(10, self.graph_display)
        else:
            self.draw_graph()

    @property
    def web_view(self) -> QWebEngineView | None:
        return self.__web_view

    @except_work(ExceptState.ERROR)
    def graph_display(self):

        if (
            Path(self._base._user_loc.ANALYSIS_GRAPH).is_file()
            and os.path.getsize(self._base._user_loc.ANALYSIS_GRAPH) > 0
        ):

            clearLayout(self._base.ui.verticalLayout_analaysis)

            self.__web_view = QWebEngineView()
            self._base.ui.verticalLayout_analaysis.addWidget(self.__web_view)

            self.__web_view.load(QUrl.fromLocalFile(self._base._user_loc.ANALYSIS_GRAPH))

            self.__web_view.sizePolicy().setHorizontalPolicy(
                QSizePolicy.Policy.Expanding
            )
            self.__web_view.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
            self.__web_view.page().profile().downloadRequested.connect(
                self.__on_downloadRequested
            )
        else:
            clearLayout(self._base.ui.verticalLayout_analaysis)
            self.__web_view = None
            self._base._status_bar_message.show_warning_message(
                AnalysisConfig.NOT_FOUND_GRAPH_MESSAGE
            )

    @except_work(ExceptState.CRITICAL)
    def draw_graph(self):
        count_res = self._base._data_base.select('SELECT COUNT(*) FROM "Transaction";')
        if not count_res or count_res[0][0] == 0:
            if os.path.exists(self._base._user_loc.ANALYSIS_GRAPH):
                try:
                    os.remove(self._base._user_loc.ANALYSIS_GRAPH)
                except Exception:
                    pass
            clearLayout(self._base.ui.verticalLayout_analaysis)
            self.__web_view = None
            self._base._status_bar_message.show_warning_message(
                AnalysisConfig.NOT_FOUND_GRAPH_MESSAGE
            )
            return

        data = self.__get_data()
        self._thread_work.add_work(
            analysis_graphics_create, [data, self._base._user_loc.ANALYSIS_GRAPH]
        )


    @except_work(ExceptState.ERROR)
    def __on_downloadRequested(self, download: QWebEngineDownloadRequest):

        download.setDownloadDirectory(Locations.DOWNLOAD)
        download.accept()
        self._base._status_bar_message.show_info_message(
            download.downloadFileName()+AnalysisConfig.IMAGE_DOWNLOAD_MESSAGE
        )

    @except_work(ExceptState.CRITICAL)
    def __get_data(self):

        long_short = self._base._data_base.select(AnalysisQuery.LONG_SHORT_COUNT)
        open = self._base._data_base.select(AnalysisQuery.OPEN_COUNT)
        tp_sl = self._base._data_base.select(AnalysisQuery.TP_SL_COUNT)
        strategy_count = self._base._data_base.select(AnalysisQuery.STRATEGY_COUNT)
        t_result = self._base._data_base.select(AnalysisQuery.RESULT)
        rr = self._base._data_base.select(AnalysisQuery.RR)
        platform = self._base._data_base.select(AnalysisQuery.PLATFORM_COUNT)

        result = AnalysisGraphData()
        result.apply_direction_count(long_short)
        result.apply_state_count(tp_sl, open)
        result.apply_strategy_count(strategy_count)
        result.apply_rr(rr)
        result.apply_result(t_result)
        result.apply_platform_count(platform)

        return result
