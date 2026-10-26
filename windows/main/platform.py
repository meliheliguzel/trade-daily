from PySide6.QtWidgets import QMessageBox

from config import PlatformConfig
from config.query import PlatformQuery
from module.data.entities import PlatformEntity
from module.data.manager import get_data
from module.tools.ui import change_border, comboBox_data_load, input_control
from scripts import ExceptState, except_work

from .i_section import ISection


class Platform(ISection):

    def __init__(self, base):

        super().__init__(base)
        self._base.ui.lineEdit_record_platform_name.setValidator(
            self._base.letters_numbers_val
        )
        self.__select_data: PlatformEntity = None
        self.load()

    @except_work(ExceptState.CRITICAL)
    def save(self):

        data = self.__get_data()
        if not data:
            return

        if self.__select_data:
            dup_count = self._base._data_base.select(
                PlatformQuery.NAME_CONTROL_UPDATE, (data, self.__select_data.primary_key)
            )[0][0]
        else:
            dup_count = self._base._data_base.select(
                PlatformQuery.NAME_CONTROL, (data,)
            )[0][0]

        if dup_count != 0:
            self._base._status_bar_message.show_warning_message(
                PlatformConfig.ADD_WARNING_MESSAGE
            )
            change_border(
                self._base.ui.lineEdit_record_platform_name,
                duration=PlatformConfig.ADD_BORDER_DURATION,
            )
            return

        self._base.ui.pushButton_record_platform_save.setDisabled(True)
        if self.__select_data:
            self.update(data)
        else:
            self.add(data)
        self.load()
        self.__clear_edit()
        self._base.ui.pushButton_record_platform_save.setDisabled(False)

    @except_work(ExceptState.ERROR)
    def add(self, data: str):

        self._base._data_base.insert(PlatformQuery.ADD, (data,))
        self._base._status_bar_message.show_success_message(
            PlatformConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.ERROR)
    def update(self, data: str):

        self._base._data_base.update(
            PlatformQuery.UPDATE,
            (data, self.__select_data.primary_key),
        )
        self._base._status_bar_message.show_success_message(
            PlatformConfig.ADD_SUCCES_MESSAGE
        )

    @except_work(ExceptState.CRITICAL)
    def remove(self):

        if self.__select_data:

            msg_box = QMessageBox(self._base)
            msg_box.setWindowTitle(PlatformConfig.REMOVE_MESSAGE_BOX_TITLE)
            msg_box.setText(PlatformConfig.REMOVE_MESSAGE_BOX_TEXT)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            if msg_box.exec() == QMessageBox.Yes:
                id = self.__select_data.primary_key
                if (
                    self._base._data_base.select(PlatformQuery.DEL_CONTROL, (id,))[0][0]
                    == 0
                ):
                    self._base._data_base.delete(PlatformQuery.REMOVE, id)
                    self._base._status_bar_message.show_success_message(
                        PlatformConfig.REMOVE_SUCCES_MESSAGE
                    )
                else:
                    self._base._status_bar_message.show_warning_message(
                        PlatformConfig.REMOVE_WARNING_MESSAGE
                    )
                self.load()
                self.__clear_edit()

            else:
                self._base._status_bar_message.show_info_message(
                    PlatformConfig.REMOVE_INFO_CANCEL
                )

        else:
            self._base._status_bar_message.show_notice_message(
                PlatformConfig.REMOVE_NOTICE_NOT_SELECT
            )

    @except_work(ExceptState.ERROR)
    def load(self):

        data = get_data(self._base._data_base, PlatformEntity, PlatformQuery.LOAD)
        if type(data) == list:
            platform = {i.name: i for i in data}
        else:
            raise data
        comboBox_data_load(self._base.ui.comboBox_record_daily_platform, platform)
        comboBox_data_load(self._base.ui.comboBox_record_platform_edit, platform, True)
        comboBox_data_load(self._base.ui.comboBox_record_parity_edit_platform, platform)
        self._base.ui.comboBox_record_daily_parity.clear()
        self._base.ui.comboBox_record_parity_edit.clear()

    @except_work(ExceptState.ERROR)
    def edit_load(self, index):

        data: PlatformEntity = self._base.ui.comboBox_record_platform_edit.itemData(
            index
        )
        if data:
            self._base.ui.lineEdit_record_platform_name.setText(data.name)
            self.__select_data = data
        else:
            self.__select_data = None
            self._base.ui.lineEdit_record_platform_name.clear()

    def __get_data(self) -> str | None:
        "result -> name"

        if input_control(
            [
                self._base.ui.lineEdit_record_platform_name,
            ],duration=PlatformConfig.INPUT_DURATION
        ):
            return self._base.ui.lineEdit_record_platform_name.text()
        else:
            self._base._status_bar_message.show_warning_message(
                PlatformConfig.GET_DATA_WARNING_MESSAGE
            )
            return None

    def __clear_edit(self):
        self._base.ui.lineEdit_record_platform_name.clear()
        self.__select_data = None
        self._base.ui.comboBox_record_platform_edit.setCurrentIndex(0)
