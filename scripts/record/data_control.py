from module.tools.ui import input_control
from module.tools.ui.input_control import border_reset
from windows.protokol.isection import ISectionProtokol


class DataControl:

    def __init__(self, base: ISectionProtokol):

        self.__section: ISectionProtokol = base

    def control(self) -> bool:

        self.widget_border_reset()
        transaction = self.__transaction_control()
        detail = self.__detail_control()
        closing = self.__closing_control()

        if not (transaction and detail and closing):
            return False

        return True

    def widget_border_reset(self):

        widget_list = [
            self.__section._base.ui.lineEdit_record_daily_rr,
            self.__section._base.ui.lineEdit_record_daily_size,
            self.__section._base.ui.comboBox_record_daily_platform,
            self.__section._base.ui.comboBox_record_daily_parity,
            self.__section._base.ui.lineEdit_record_daily_enter_price,
            self.__section._base.ui.lineEdit_record_daily_stop_price,
            self.__section._base.ui.lineEdit_record_daily_target_price,
            self.__section._base.ui.lineEdit_record_daily_exit_price,
            self.__section._base.ui.lineEdit_record_daily_result,
        ]
        for i in widget_list:
            border_reset(i)

    def __transaction_control(self) -> bool:

        return input_control(
            [
                self.__section._base.ui.lineEdit_record_daily_rr,
                self.__section._base.ui.lineEdit_record_daily_size,
                self.__section._base.ui.comboBox_record_daily_platform,
                self.__section._base.ui.comboBox_record_daily_parity,
            ]
        )

    def __detail_control(self) -> bool:

        detail_open_list = [
            self.__section._base.ui.lineEdit_record_daily_enter_price,
            self.__section._base.ui.lineEdit_record_daily_stop_price,
            self.__section._base.ui.lineEdit_record_daily_target_price,
        ]
        if not self.__section._base.ui.radioButton_record_daily_open.isChecked():
            detail_open_list.append(
                self.__section._base.ui.lineEdit_record_daily_exit_price
            )
            if (
                detail_open_list[0].text()
                or detail_open_list[1].text()
                or detail_open_list[2].text()
                or detail_open_list[3].text()
            ):
                return input_control(detail_open_list)

        if (
            detail_open_list[0].text()
            or detail_open_list[1].text()
            or detail_open_list[2].text()
        ):
            return input_control(detail_open_list)

        return True

    def __closing_control(self) -> bool:

        if not self.__section._base.ui.radioButton_record_daily_open.isChecked():

            return input_control(self.__section._base.ui.lineEdit_record_daily_result)
        return True
