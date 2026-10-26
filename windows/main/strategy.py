from PySide6.QtWidgets import QMessageBox

from config import StrategyConfig
from config.query import StrategyQuery
from module.data.entities import StrategyEntity
from module.data.manager import get_data
from module.tools.ui import change_border, comboBox_data_load, input_control
from scripts import ExceptState, except_work

from .i_section import ISection


class Strategy(ISection):

    def __init__(self, base):

        super().__init__(base)
        self._base.ui.lineEdit_record_strategy_name.setValidator(
            self._base.letters_numbers_val
        )
        self.load()
        self.__select_data: StrategyEntity = None

    @except_work(ExceptState.CRITICAL)
    def save(self):

        data = self.__get_data()
        if not data:
            return

        name = data[0]
        if self.__select_data:
            dup_count = self._base._data_base.select(
                StrategyQuery.NAME_CONTROL_UPDATE,
                (name, self.__select_data.primary_key),
            )[0][0]
        else:
            dup_count = self._base._data_base.select(
                StrategyQuery.NAME_CONTROL,
                (name,),
            )[0][0]

        if dup_count != 0:
            self._base._status_bar_message.show_warning_message(
                StrategyConfig.ADD_WARNING_MESSAGE
            )
            change_border(
                self._base.ui.lineEdit_record_strategy_name,
                duration=StrategyConfig.ADD_BORDER_DURATION,
            )
            return

        self._base.ui.pushButton_record_strategy_save.setDisabled(True)
        if self.__select_data:
            self.update(data)
        else:
            self.add(data)
        self.load()
        self.__clear_edit()
        self._base.ui.pushButton_record_strategy_save.setDisabled(False)

    @except_work(ExceptState.ERROR)
    def add(self, data: tuple[str, str]):

        self._base._data_base.insert(StrategyQuery.ADD, data)
        self._base._status_bar_message.show_success_message(
            StrategyConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.ERROR)
    def update(self, data: tuple[str, str]):

        self._base._data_base.update(
            StrategyQuery.UPDATE,
            (data[0], data[1], self.__select_data.primary_key),
        )
        self._base._status_bar_message.show_success_message(
            StrategyConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.CRITICAL)
    def remove(self):

        if self.__select_data:

            msg_box = QMessageBox(self._base)
            msg_box.setWindowTitle(StrategyConfig.REMOVE_MESSAGE_BOX_TITLE)
            msg_box.setText(StrategyConfig.REMOVE_MESSAGE_BOX_TEXT)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            if msg_box.exec() == QMessageBox.Yes:
                id = self.__select_data.primary_key
                if (
                    self._base._data_base.select(StrategyQuery.DEL_CONTROL, (id,))[0][0]
                    == 0
                ):
                    self._base._data_base.delete(StrategyQuery.REMOVE, id)
                    self._base._status_bar_message.show_success_message(
                        StrategyConfig.REMOVE_SUCCES_MESSAGE
                    )

                else:  
                    self._base._status_bar_message.show_warning_message(
                        StrategyConfig.REMOVE_WARNING_MESSAGE
                    )
                self.load()
                self.__clear_edit()

            else:  
                self._base._status_bar_message.show_info_message(
                    StrategyConfig.REMOVE_INFO_CANCEL
                )

        else:  
            self._base._status_bar_message.show_notice_message(
                StrategyConfig.REMOVE_NOTICE_NOT_SELECT
            )

    @except_work(ExceptState.ERROR)
    def edit_load(self, index):

        data: StrategyEntity = self._base.ui.comboBox_record_strategy_edit.itemData(
            index
        )
        if data:
            self.__select_data = data
            self._base.ui.lineEdit_record_strategy_name.setText(data.name)
            self._base.ui.textEdit_record_strategy_text.setText(
                self.__select_data.description
            )
        else:
            self.__select_data = None
            self._base.ui.lineEdit_record_strategy_name.clear()
            self._base.ui.textEdit_record_strategy_text.clear()

    @except_work(ExceptState.ERROR)
    def load(self):

        data = get_data(self._base._data_base, StrategyEntity, StrategyQuery.LOAD)
        if type(data) == list:
            strategy = {i.name: i for i in data}
        else:
            raise data
        comboBox_data_load(self._base.ui.comboBox_record_daily_strategy, strategy)
        comboBox_data_load(self._base.ui.comboBox_record_strategy_edit, strategy, True)

    def __clear_edit(self):

        self._base.ui.lineEdit_record_strategy_name.clear()
        self._base.ui.textEdit_record_strategy_text.clear()
        self.__select_data = None
        self._base.ui.comboBox_record_strategy_edit.setCurrentIndex(0)

    def __get_data(self) -> tuple[str, str] | None:
        "result -> name,description"

        if input_control(
            [
                self._base.ui.lineEdit_record_strategy_name,
                self._base.ui.textEdit_record_strategy_text,
            ],duration=StrategyConfig.INPUT_DURATION
        ):

            name = self._base.ui.lineEdit_record_strategy_name.text()
            description = self._base.ui.textEdit_record_strategy_text.toPlainText()

            return (name, description)
        else:
            self._base._status_bar_message.show_warning_message(
                StrategyConfig.GET_DATA_WARNING_MESSAGE
            )
            return None
