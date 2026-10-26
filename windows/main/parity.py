from PySide6.QtWidgets import QMessageBox

from config import ParityConfig
from config.query import ParityQuery
from module.data.entities import ParityEntity, PlatformEntity
from module.data.manager import get_data
from module.tools.ui import change_border, comboBox_data_load, input_control
from scripts import ExceptState, except_work

from .i_section import ISection


class Parity(ISection):

    def __init__(self, base):
        super().__init__(base)

        self._base.ui.lineEdit_record_parity_name.setValidator(
            self._base.letters_numbers_val
        )
        self.__select_data: ParityEntity = None
        self.__select_platform: PlatformEntity = None

    @except_work(ExceptState.CRITICAL)
    def save(self):

        data = self.__get_data()
        if not data:
            return

        name, platform_id = data
        if self.__select_data:
            dup_count = self._base._data_base.select(
                ParityQuery.NAME_CONTROL_UPDATE,
                (name, platform_id, self.__select_data.primary_key),
            )[0][0]
        else:
            dup_count = self._base._data_base.select(
                ParityQuery.NAME_CONTROL,
                (name, platform_id),
            )[0][0]

        if dup_count != 0:
            self._base._status_bar_message.show_warning_message(
                ParityConfig.ADD_WARNING_MESSAGE
            )
            change_border(
                self._base.ui.lineEdit_record_parity_name,
                duration=ParityConfig.ADD_BORDER_DURATION,
            )
            return

        self._base.ui.pushButton_record_parity_save.setDisabled(True)
        if self.__select_data:
            self.update(data)
        else:
            self.add(data)
        self.__comboBox_reload()
        self.__clear_edit()
        self._base.ui.pushButton_record_parity_save.setDisabled(False)

    @except_work(ExceptState.ERROR)
    def add(self, data: tuple[str, int]):

        self._base._data_base.insert(ParityQuery.ADD, data)
        self._base._status_bar_message.show_success_message(
            ParityConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.ERROR)
    def update(self, data: tuple[str, int]):

        self._base._data_base.update(
            ParityQuery.UPDATE,
            (*data, self.__select_data.primary_key),
        )
        self._base._status_bar_message.show_success_message(
            ParityConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.CRITICAL)
    def remove(self):

        if self.__select_data:

            msg_box = QMessageBox(self._base)
            msg_box.setWindowTitle(ParityConfig.REMOVE_MESSAGE_BOX_TITLE)
            msg_box.setText(ParityConfig.REMOVE_MESSAGE_BOX_TEXT)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            if msg_box.exec() == QMessageBox.Yes:
                id = self.__select_data.primary_key
                if (
                    self._base._data_base.select(ParityQuery.DEL_CONTROL, (id,))[0][0]
                    == 0
                ):
                    self._base._data_base.delete(ParityQuery.REMOVE, id)
                    self._base._status_bar_message.show_success_message(
                        ParityConfig.REMOVE_SUCCES_MESSAGE
                    )
                else:  # ? is being used
                    self._base._status_bar_message.show_warning_message(
                        ParityConfig.REMOVE_WARNING_MESSAGE
                    )
                self.__comboBox_reload()
                self.__clear_edit()

            else:  # ? cancel
                self._base._status_bar_message.show_info_message(
                    ParityConfig.REMOVE_INFO_CANCEL
                )

        else:  # ? not select
            self._base._status_bar_message.show_notice_message(
                ParityConfig.REMOVE_NOTICE_NOT_SELECT
            )

    @except_work(ExceptState.ERROR)
    def daily_load(self, index):

        platform: PlatformEntity = (
            self._base.ui.comboBox_record_daily_platform.itemData(index)
        )
        if platform:
            data = self.__get_parity(platform.primary_key)
            if data:
                parity = {i.name: i for i in data}
                comboBox_data_load(self._base.ui.comboBox_record_daily_parity, parity)
            else:
                self._base.ui.comboBox_record_daily_parity.clear()
        else:
            self._base.ui.comboBox_record_daily_parity.clear()

    @except_work(ExceptState.ERROR)
    def load(self, index):

        platform: PlatformEntity = (
            self._base.ui.comboBox_record_parity_edit_platform.itemData(index)
        )
        self.__select_platform = platform
        if platform:
            data = self.__get_parity(platform.primary_key)
            parity = {i.name: i for i in data} if data else {}
            comboBox_data_load(self._base.ui.comboBox_record_parity_edit, parity, True)
        else:
            self._base.ui.comboBox_record_parity_edit.clear()

    @except_work(ExceptState.ERROR)
    def edit_load(self, index):

        data: ParityEntity = self._base.ui.comboBox_record_parity_edit.itemData(index)
        if data:
            self._base.ui.lineEdit_record_parity_name.setText(data.name)
            self.__select_data = data
        else:
            self.__select_data = None
            self._base.ui.lineEdit_record_parity_name.clear()

    @except_work(ExceptState.ERROR)
    def __get_parity(self, platform_id: int):

        data = get_data(
            self._base._data_base, ParityEntity, ParityQuery.LOAD, (platform_id,)
        )
        if type(data) == list:
            return data
        else:
            raise data

    @except_work(ExceptState.ERROR)
    def __get_data(self) -> tuple[str, int] | None:
        "result -> name,platform_id"

        platform = (
            self.__select_platform
            or self._base.ui.comboBox_record_parity_edit_platform.currentData()
        )
        has_name = input_control(
            [self._base.ui.lineEdit_record_parity_name],
            duration=ParityConfig.INPUT_DURATION,
        )
        if not platform:
            change_border(
                self._base.ui.comboBox_record_parity_edit_platform,
                duration=ParityConfig.GET_DATA_DURATION,
            )
            self._base._status_bar_message.show_warning_message(
                ParityConfig.GET_DATA_WARNING_MESSAGE
            )
            return None

        if not has_name:
            self._base._status_bar_message.show_warning_message(
                ParityConfig.GET_DATA_WARNING_MESSAGE
            )
            return None

        self.__select_platform = platform
        return (
            self._base.ui.lineEdit_record_parity_name.text(),
            platform.primary_key,
        )

    def __clear_edit(self):

        self._base.ui.lineEdit_record_parity_name.clear()
        self.__select_data = None
        self._base.ui.comboBox_record_parity_edit.setCurrentIndex(0)

    def __comboBox_reload(self):

        self.load(self._base.ui.comboBox_record_parity_edit_platform.currentIndex())
        if self._base.ui.comboBox_record_daily_platform.currentIndex() != -1:
            self.daily_load(self._base.ui.comboBox_record_daily_platform.currentIndex())
