from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox

from config import RecordConfig
from config.query import RecordQuery
from module.data.entities import TransactionFullData, TransactionUpdateData
from module.data.manager import all_transaction_data
from module.tools.file import image_data
from module.tools.ui import (
    DataRole,
    list_widget_image_load,
    list_widget_items_load,
    widget_list_item_add,
)
from module.utils import current_time, str_to_qDateTime
from scripts import ExceptState, except_work
from scripts.record import DataOperations

from .i_section import ISection


class Record(ISection):

    def __init__(self, base):
        super().__init__(base)

        self._base.ui.lineEdit_record_daily_transaction_id.setValidator(
            self._base.int_val
        )
        self._base.ui.lineEdit_record_daily_size.setValidator(
            self._base.positive_float_val
        )
        self._base.ui.lineEdit_record_daily_rr.setValidator(
            self._base.positive_float_val
        )
        self._base.ui.lineEdit_record_daily_result.setValidator(self._base.float_val)
        self._base.ui.lineEdit_record_daily_enter_price.setValidator(
            self._base.positive_float_val
        )
        self._base.ui.lineEdit_record_daily_target_price.setValidator(
            self._base.positive_float_val
        )
        self._base.ui.lineEdit_record_daily_stop_price.setValidator(
            self._base.positive_float_val
        )
        self._base.ui.lineEdit_record_daily_exit_price.setValidator(
            self._base.positive_float_val
        )
        self.open_transaction()
        self.__time_reload()
        self.__update_data: TransactionUpdateData = None
        self.__data_operation: DataOperations = DataOperations(self)

    def save(self):

        self._base.ui.widget_record_transaction.setDisabled(True)
        if self.__update_data:
            result = self.__data_operation.update(self.__update_data)
        else:
            result = self.__data_operation.add()
        if result:
            self._base._balance_record.recalculation()
            self._clear_all()
            self.open_transaction()
            self._base._data_display.reload()
            self._base._analysis.draw_graph()
        self._base.ui.widget_record_transaction.setDisabled(False)

    @except_work(ExceptState.CRITICAL)
    def remove(self):

        if self.__update_data:

            msg_box = QMessageBox(self._base)
            msg_box.setWindowTitle(RecordConfig.REMOVE_WARNING_TITLE)
            msg_box.setText(RecordConfig.REMOVE_WARNING_TEXT)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            if msg_box.exec() == QMessageBox.Yes:
                id = self.__update_data.ORIGINAL_DATA.transaction.primary_key
                if self._base._data_base.select(RecordQuery.INDEX_CONTROL, (id,))[0][0]:
                    self._base._data_base.delete(RecordQuery.CLOSING_DELETE, id)
                    self._base._data_base.delete(RecordQuery.DETAIL_OPEN_DELETE, id)
                    self._base._data_base.delete(RecordQuery.DETAIL_CLOSING_DELETE, id)
                    self._base._data_base.delete(RecordQuery.NOTE_DELETE, id)
                    self._base._data_base.delete(RecordQuery.STRATEGY_DELETE_ALL, id)
                    self._base._data_base.delete(RecordQuery.LINK_DELETE_ALL, id)
                    self._base._data_base.delete(RecordQuery.IMAGE_DELETE_ALL, id)
                    self._base._data_base.delete(RecordQuery.TRANSACTION_DELETE, id)
                    self._base._data_base.delete(RecordQuery.BALANCE_DELTE, id)

                    self._clear_all()
                    self.open_transaction()
                    self._base._analysis.draw_graph()
                    self._base._balance_record.draw_graph()
                    self._base._status_bar_message.show_success_message(
                        RecordConfig.REMOVE_SUCCES_MESSAGE
                    )
                else:  # ? is being used
                    self._base._status_bar_message.show_warning_message(
                        RecordConfig.REMOVE_WARNING_MESSAGE
                    )

            else:  # ? cancel
                self._base._status_bar_message.show_info_message(
                    RecordConfig.REMOVE_CANCEL_MESSAGE
                )
        else:
            self._base._status_bar_message.show_error_message(
                RecordConfig.REMOVE_ERROR_MESSAGE
            )

    @except_work(ExceptState.ERROR)
    def open_transaction(self):

        self._base.ui.comboBox_record_daily_open_trn.blockSignals(True)
        self._base.ui.comboBox_record_daily_open_trn.clear()
        open_trn = [
            str(i[0])
            for i in self._base._data_base.select(RecordQuery.OPEN_TRANSACTION)
        ]
        if open_trn:
            self._base.ui.comboBox_record_daily_open_trn.addItems(open_trn)
        self._base.ui.comboBox_record_daily_open_trn.setCurrentIndex(-1)
        self._base.ui.comboBox_record_daily_open_trn.blockSignals(False)

    @except_work(ExceptState.ERROR)
    def open_transaction_load(self, _):

        primary_key = self._base.ui.comboBox_record_daily_open_trn.currentText()
        if primary_key:
            self._base.ui.lineEdit_record_daily_transaction_id.setText(primary_key)
            data = all_transaction_data(
                self._base._data_base,
                int(primary_key),
            )
            self.__data_load(data)

    @except_work(ExceptState.ERROR)
    def update_data_load_table(self):
        self.__data_load(self._base._data_display.selected_data())
        self._base.ui.tabWidget_main.setCurrentWidget(self._base.ui.tab_record)

    @except_work(ExceptState.ERROR)
    def update_data_load(self):

        id = self._base.ui.lineEdit_record_daily_transaction_id.text()
        if id != "":
            id = int(id)
            if self._base._data_base.select(RecordQuery.INDEX_CONTROL, (id,))[0][0]:
                self.__data_load(all_transaction_data(self._base._data_base, id))
            elif not id:
                self._clear_all()
            else:
                self._base._status_bar_message.show_notice_message(
                    RecordConfig.UPDATE_DATA_LOAD_NOTICE_MESSAGE
                )

    @except_work(ExceptState.ERROR)
    def strategy_add(self, index):

        if index != -1:

            strategy = self._base.ui.comboBox_record_daily_strategy.itemData(index)
            if not self._base.ui.listWidget_record_daily_strategy.findItems(
                strategy.name, Qt.MatchFlag.MatchExactly
            ):
                widget_list_item_add(
                    strategy,
                    strategy.name,
                    None,
                    self._base.ui.listWidget_record_daily_strategy,
                    RecordConfig.NEW,
                )
            else:
                self._base._status_bar_message.show_notice_message(
                    RecordConfig.STRATEGY_ADD_NOTICE_MESSAGE
                )
            self._base.ui.comboBox_record_daily_strategy.setCurrentIndex(-1)

    @except_work(ExceptState.ERROR)
    def strategy_remove(self):

        current_row = self._base.ui.listWidget_record_daily_strategy.currentRow()
        if current_row != -1:
            removed_item = self._base.ui.listWidget_record_daily_strategy.takeItem(
                current_row
            )
            if self.__update_data:
                if removed_item.data(DataRole.LABEL) != RecordConfig.NEW:
                    self.__update_data.STRATEGY_REMOVE_IDS.append(
                        removed_item.data(DataRole.DATA).primary_key
                    )
            del removed_item
            self._base._status_bar_message.show_success_message(
                RecordConfig.STRATEGY_REMOVE_SUCCES_MESSAGE
            )
        else:
            self._base._status_bar_message.show_warning_message(
                RecordConfig.STRATEGY_REMOVE_WARNING_MESSAGE
            )

    @except_work(ExceptState.ERROR)
    def image_add(self):

        file_paths, _ = QFileDialog.getOpenFileNames(
            self._base, RecordConfig.IMAGE_ADD_TITLE, "", RecordConfig.IMAGE_ADD_FILTER
        )

        if file_paths:
            images_data = {}
            for path in file_paths:
                data = image_data(path)
                if data:
                    images_data[data[0]] = data
            list_widget_image_load(
                images_data,
                self.__imge_load_error,
                self._base.ui.listWidget_record_daily_chart_image,
                RecordConfig.NEW,
            )
            self._base._status_bar_message.show_success_message(
                RecordConfig.IMAGE_ADD_SUCCES_MESSAGE
            )
        else:
            self._base._status_bar_message.show_warning_message(
                RecordConfig.IMAGE_ADD_WARNING_MESSAGE
            )

    @except_work(ExceptState.ERROR)
    def image_remove(self):

        current_row = self._base.ui.listWidget_record_daily_chart_image.currentRow()
        if current_row != -1:
            removed_item = self._base.ui.listWidget_record_daily_chart_image.takeItem(
                current_row
            )
            if self.__update_data:
                if removed_item.data(DataRole.LABEL) != RecordConfig.NEW:
                    self.__update_data.CHART_IMAGE_REMOVE_IDS.append(
                        removed_item.data(DataRole.DATA).primary_key
                    )
            del removed_item
            self._base._status_bar_message.show_success_message(
                RecordConfig.IMAGE_REMOVE_SUCCES_MESSAGE
            )
        else:
            self._base._status_bar_message.show_warning_message(
                RecordConfig.IMAGE_REMOVE_WARNING_MESSAGE
            )

    @except_work(ExceptState.ERROR)
    def link_add(self):

        link = self._base.ui.lineEdit_record_daily_chart_link.text()
        widget_list_item_add(
            link,
            link,
            None,
            self._base.ui.listWidget_record_daily_chart_link,
            RecordConfig.NEW,
        )
        self._base.ui.lineEdit_record_daily_chart_link.clear()

    @except_work(ExceptState.ERROR)
    def link_remove(self):

        current_row = self._base.ui.listWidget_record_daily_chart_link.currentRow()
        if current_row != -1:
            removed_item = self._base.ui.listWidget_record_daily_chart_link.takeItem(
                current_row
            )
            if self.__update_data:
                if removed_item.data(DataRole.LABEL) != RecordConfig.NEW:
                    self.__update_data.CHART_LINK_REMOVE_IDS.append(
                        removed_item.data(DataRole.DATA).primary_key
                    )
            del removed_item
            self._base._status_bar_message.show_success_message(
                RecordConfig.LINK_REMOVE_SUCCES_MESSAGE
            )
        else:
            self._base._status_bar_message.show_warning_message(
                RecordConfig.LINK_REMOVE_WARNING_MESSAGE
            )

    def _clear_all(self):

        self.__data_operation.border_reset()
        self._base.ui.lineEdit_record_daily_chart_link.clear()
        self._base.ui.lineEdit_record_daily_enter_price.clear()
        self._base.ui.lineEdit_record_daily_exit_price.clear()
        self._base.ui.lineEdit_record_daily_result.clear()
        self._base.ui.lineEdit_record_daily_rr.clear()
        self._base.ui.lineEdit_record_daily_size.clear()
        self._base.ui.lineEdit_record_daily_stop_price.clear()
        self._base.ui.lineEdit_record_daily_target_price.clear()
        self._base.ui.lineEdit_record_daily_transaction_id.clear()
        self._base.ui.textEdit_record_daily_note.clear()
        self._base.ui.listWidget_record_daily_chart_image.clear()
        self._base.ui.listWidget_record_daily_chart_link.clear()
        self._base.ui.listWidget_record_daily_strategy.clear()
        self._base.ui.comboBox_record_daily_parity.clear()

        self._base.ui.comboBox_record_daily_open_trn.setCurrentIndex(-1)
        self._base.ui.comboBox_record_daily_platform.setCurrentIndex(-1)
        self._base.ui.comboBox_record_daily_strategy.setCurrentIndex(-1)

        self._base.ui.radioButton_record_daily_open.setChecked(True)
        self.__update_data = None
        self.__time_reload()

    @except_work(ExceptState.CRITICAL)
    def __data_load(self, data: TransactionFullData):

        self._clear_all()

        self.__update_data = TransactionUpdateData(data, [], [], [])
        self._base.ui.lineEdit_record_daily_transaction_id.setText(
            str(data.transaction.primary_key)
        )
        self._base.ui.lineEdit_record_daily_rr.setText(str(data.transaction.rr))
        self._base.ui.lineEdit_record_daily_size.setText(str(data.transaction.size))
        self._base.ui.dateTimeEdit_record_daily_entry.setDateTime(
            str_to_qDateTime(data.transaction.date_of_entry)
        )

        if data.note:
            self._base.ui.textEdit_record_daily_note.setText(data.note.note_text)

        if data.detail_open:
            self._base.ui.lineEdit_record_daily_enter_price.setText(
                str(data.detail_open.entry_price)
            )
            self._base.ui.lineEdit_record_daily_stop_price.setText(
                str(data.detail_open.stop_price)
            )
            self._base.ui.lineEdit_record_daily_target_price.setText(
                str(data.detail_open.target_price)
            )
            if data.transaction.tp_sl is not None:
                self._base.ui.lineEdit_record_daily_exit_price.setText(
                    str(data.detail_closing.exit_price)
                )

        if data.transaction.tp_sl is not None:
            self._base.ui.lineEdit_record_daily_result.setText(str(data.closing.result))
            self._base.ui.dateTimeEdit_record_daily_exit.setDateTime(
                str_to_qDateTime(data.closing.date_of_exit)
            )

        if data.transaction.long_short:
            self._base.ui.radioButton_record_daily_long.setChecked(True)
        else:
            self._base.ui.radioButton_record_daily_short.setChecked(True)

        if data.transaction.tp_sl is None:
            self._base.ui.radioButton_record_daily_open.setChecked(True)
        elif data.transaction.tp_sl:
            self._base.ui.radioButton_record_daily_tp.setChecked(True)
        else:
            self._base.ui.radioButton_record_daily_sl.setChecked(True)

        if data.chart_images:
            list_widget_image_load(
                {i.image: i for i in data.chart_images},
                self.__imge_load_error,
                self._base.ui.listWidget_record_daily_chart_image,
                data.transaction.primary_key,
            )

        if data.chart_links:
            list_widget_items_load(
                {i.link: i for i in data.chart_links},
                self._base.ui.listWidget_record_daily_chart_link,
                data.transaction.primary_key,
            )

        if data.strategy:
            list_widget_items_load(
                {i.name: i for i in data.strategy},
                self._base.ui.listWidget_record_daily_strategy,
                data.transaction.primary_key,
            )

        index_platform = self._base.ui.comboBox_record_daily_platform.findText(
            data.transaction.platform
        )
        if index_platform != -1:
            self._base.ui.comboBox_record_daily_platform.setCurrentIndex(index_platform)
        else:
            msg = RecordConfig.PLATFORM_NOT_FOUND_MESSAGE.format(data.transaction.platform)
            self._base._status_bar_message.show_warning_message(msg)
            self._base._logger.warning(msg)

        index_parity = self._base.ui.comboBox_record_daily_parity.findText(
            data.transaction.parity
        )
        if index_parity != -1:
            self._base.ui.comboBox_record_daily_parity.setCurrentIndex(index_parity)
        else:
            msg = RecordConfig.PARITY_NOT_FOUND_MESSAGE.format(data.transaction.parity)
            self._base._status_bar_message.show_warning_message(msg)
            self._base._logger.warning(msg)


    def __imge_load_error(self, message: str):
        self._base._status_bar_message.show_warning_message(message)
        self._base._logger.debug(message)

    def __time_reload(self):

        self._base.ui.dateTimeEdit_record_daily_entry.setDateTime(current_time())
        self._base.ui.dateTimeEdit_record_daily_exit.setDateTime(current_time())
