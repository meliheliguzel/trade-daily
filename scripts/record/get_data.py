
from PySide6.QtCore import Qt

from config import RecordConfig
from module.data.entities import TransactionDataType
from module.data.entities.chart_image import ChartImage
from module.data.entities.chart_link import ChartLink
from module.data.entities.note import Note
from module.data.entities.transaction import WriteTransaction
from module.data.entities.transaction_closing import TransactionClosing
from module.data.entities.transaction_detail_closing import TransactionDetailClosing
from module.data.entities.transaction_detail_open import TransactionDetailOpen
from module.data.entities.transaction_strategy import TransactionStrategy
from module.tools.ui import get_extra_data_from_list_widget
from windows.protokol.isection import ISectionProtokol


class GetData:

    def __init__(self, base: ISectionProtokol):

        self.__section: ISectionProtokol = base

    def transaction_data(self, primary_key: int | None = None) -> WriteTransaction:

        platform = self.__section._base.ui.comboBox_record_daily_platform.currentData(
            Qt.ItemDataRole.UserRole
        ).primary_key
        parity = self.__section._base.ui.comboBox_record_daily_parity.currentData(
            Qt.ItemDataRole.UserRole
        ).primary_key

        entry_date = self.__section._base.ui.dateTimeEdit_record_daily_entry.text()

        if self.__section._base.ui.radioButton_record_daily_long.isChecked():
            long_short = TransactionDataType.LONG
        else:
            long_short = TransactionDataType.SHORT

        rr = float(self.__section._base.ui.lineEdit_record_daily_rr.text())
        size = float(self.__section._base.ui.lineEdit_record_daily_size.text())

        if primary_key:
            return WriteTransaction(
                primary_key, platform, parity, entry_date, long_short, rr, size
            )
        return WriteTransaction(0, platform, parity, entry_date, long_short, rr, size)

    def closing_data(self, transaction_id: int | None = None) -> TransactionClosing | None:

        if not self.__section._base.ui.radioButton_record_daily_open.isChecked():
            if self.__section._base.ui.radioButton_record_daily_tp.isChecked():
                tp_sl = TransactionDataType.TP
            elif self.__section._base.ui.radioButton_record_daily_sl.isChecked():
                tp_sl = TransactionDataType.SL
            result = float(self.__section._base.ui.lineEdit_record_daily_result.text())
            exit_date = self.__section._base.ui.dateTimeEdit_record_daily_exit.text()
            if transaction_id:
                return TransactionClosing(0, transaction_id, exit_date, tp_sl, result)
            return TransactionClosing(0, 0, exit_date, tp_sl, result)
        return None

    def detail_open_data(
        self, transaction_id: int | None = None
    ) -> TransactionDetailOpen | None:

        entry_price = self.__section._base.ui.lineEdit_record_daily_enter_price.text()
        stop_price = self.__section._base.ui.lineEdit_record_daily_stop_price.text()
        target_price = self.__section._base.ui.lineEdit_record_daily_target_price.text()
        if entry_price and stop_price and target_price:
            if transaction_id:
                return TransactionDetailOpen(
                    0, transaction_id, entry_price, target_price, stop_price
                )
            return TransactionDetailOpen(0, 0, entry_price, target_price, stop_price)
        return None

    def detail_closing_data(
        self, transaction_id: int | None = None
    ) -> TransactionDetailClosing | None:

        exit_price = self.__section._base.ui.lineEdit_record_daily_exit_price.text()
        if exit_price and (
            not self.__section._base.ui.radioButton_record_daily_open.isChecked()
        ):
            if transaction_id:
                return TransactionDetailClosing(0, transaction_id, exit_price)
            return TransactionDetailClosing(0, 0, exit_price)
        return None

    def note_data(self, transaction_id: int | None = None) -> Note | None:

        note = self.__section._base.ui.textEdit_record_daily_note.toPlainText()
        if note:
            if transaction_id:
                return Note(0, transaction_id, note)
            return Note(0, 0, note)
        return None

    def strategy_data(
        self, transaction_id: int | None = None
    ) -> list[TransactionStrategy] | None:

        strategy = get_extra_data_from_list_widget(
            self.__section._base.ui.listWidget_record_daily_strategy, True
        )
        if strategy:
            result = []
            for i, label in strategy:
                if label == RecordConfig.NEW:
                    if transaction_id:
                        result.append(
                            TransactionStrategy(
                                0, transaction_id, i.primary_key, i.name
                            )
                        )
                    else:
                        result.append(TransactionStrategy(0, 0, i.primary_key, i.name))
            return result
        return None

    def link_data(self, transaction_id: int | None = None) -> list[ChartLink] | None:

        links = get_extra_data_from_list_widget(
            self.__section._base.ui.listWidget_record_daily_chart_link, True
        )
        if links:
            result = []
            for i, label in links:
                if label == RecordConfig.NEW:
                    if transaction_id:
                        result.append(ChartLink(0, transaction_id, i))
                    else:
                        result.append(ChartLink(0, 0, i))
            return result
        return None

    def image_data(self, transaction_id: int | None = None) -> list[ChartImage] | None:

        images = get_extra_data_from_list_widget(
            self.__section._base.ui.listWidget_record_daily_chart_image, True
        )
        if images:
            result = []
            for i, label in images:
                if label == RecordConfig.NEW:
                    if transaction_id:
                        result.append(ChartImage(0, transaction_id, *i))
                    else:
                        result.append(ChartImage(0, 0, *i))
            return result
        return None
