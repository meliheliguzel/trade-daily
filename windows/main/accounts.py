from PySide6.QtWidgets import QMessageBox

from config import AccountsConfig
from module.data.connection import SQLite
from module.tools.ui import comboBox_data_load, input_control
from scripts import ExceptState, except_work

from .i_section import ISection


class Accounts(ISection):

    def __init__(self, base):
        super().__init__(base)
        self.__load()

    @except_work(ExceptState.ERROR)
    def save(self) -> None:
        user_name = self.__get_data()
        if not user_name:
            return

        current_selection = self._base.ui.comboBox_record_accounts_edit.currentText()
        if current_selection == "New":
            self.add(user_name)
        else:
            self.update(new_name=user_name, old_name=current_selection)

    @except_work(ExceptState.ERROR)
    def add(self, user_name: str) -> None:
        self._base._user_setup.add(user_name)
        self.__load()
        self._base.ui.lineEdit_record_accounts_name.clear()
        self._base._status_bar_message.show_success_message(
            AccountsConfig.ADD_SUCCESS_MESSAGE.format(user_name)
        )
        self._base.comboBox_accounts.setCurrentText(user_name)

    @except_work(ExceptState.ERROR)
    def update(self, new_name: str, old_name: str) -> None:
        if self._base._user_setup.update(old_user=old_name, new_user=new_name):
            self.__load()
            self._base.ui.lineEdit_record_accounts_name.clear()
            self._base._status_bar_message.show_success_message(
                AccountsConfig.UPDATE_SUCCESS_MESSAGE.format(old_name, new_name)
            )

    @except_work(ExceptState.ERROR)
    def remove(self) -> None:
        current_selection = self._base.ui.comboBox_record_accounts_edit.currentText()
        if current_selection and current_selection != "New":
            msg_box = QMessageBox(self._base)
            msg_box.setWindowTitle(AccountsConfig.REMOVE_MESSAGE_BOX_TITLE)
            msg_box.setText(
                AccountsConfig.REMOVE_MESSAGE_BOX_TEXT.format(current_selection)
            )
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if msg_box.exec() == QMessageBox.StandardButton.Yes:
                is_active = (current_selection == self._base._user_setup.data.CURRENT_USER)
                if is_active:
                    self._base._data_base.close_connection()
                    self._base._logger.close()

                if self._base._user_setup.remove(current_selection):
                    if is_active:
                        self._base._user_loc = self._base._user_setup.get_user_loc()
                        self._base._logger.set_log_file(self._base._user_loc.LOG)
                        SQLite.reset()

                        self._base._data_base = SQLite(self._base._user_loc.DATA_BASE)
                        self._base.reload_all_sections()

                    self.__load()
                    self._base.ui.lineEdit_record_accounts_name.clear()
                    self._base._status_bar_message.show_success_message(
                        AccountsConfig.REMOVE_SUCCESS_MESSAGE.format(current_selection)
                    )

    @except_work(ExceptState.ERROR)
    def edit_load(self, index: int = -1) -> None:
        current_selection = self._base.ui.comboBox_record_accounts_edit.currentText()
        if current_selection == "New":
            self._base.ui.lineEdit_record_accounts_name.clear()
        elif current_selection:
            self._base.ui.lineEdit_record_accounts_name.setText(current_selection)

    @except_work(ExceptState.ERROR)
    def __load(self) -> None:

        self._base.ui.comboBox_record_accounts_default.blockSignals(True)
        self._base.ui.comboBox_record_accounts_edit.blockSignals(True)
        self._base.comboBox_accounts.blockSignals(True)

        user_list = self._base._user_setup.get_user_list()

        comboBox_data_load(
            self._base.ui.comboBox_record_accounts_edit,
            {i: i for i in user_list},
            True,
        )

        comboBox_data_load(
            self._base.ui.comboBox_record_accounts_default,
            {i: i for i in user_list},
            False,
        )

        comboBox_data_load(
            self._base.comboBox_accounts,
            {i: i for i in user_list},
            False,
        )

        current_user = self._base._user_setup.data.CURRENT_USER

        index_default = self._base.ui.comboBox_record_accounts_default.findText(current_user)
        if index_default >= 0:
            self._base.ui.comboBox_record_accounts_default.setCurrentIndex(index_default)

        index_menu = self._base.comboBox_accounts.findText(current_user)
        if index_menu >= 0:
            self._base.comboBox_accounts.setCurrentIndex(index_menu)

        self._base.ui.comboBox_record_accounts_default.blockSignals(False)
        self._base.ui.comboBox_record_accounts_edit.blockSignals(False)
        self._base.comboBox_accounts.blockSignals(False)


    @except_work(ExceptState.ERROR)
    def __get_data(self):

        if input_control(
            self._base.ui.lineEdit_record_accounts_name,
            duration=AccountsConfig.INPUT_DURATION,
        ):
            return self._base.ui.lineEdit_record_accounts_name.text()
        else:
            self._base._status_bar_message.show_warning_message(
                AccountsConfig.GET_DATA_WARNING_MESSAGE
            )
            return None

