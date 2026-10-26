from config import RrConfig
from module.tools.ui import input_control
from module.utils import rr_standart_calculate
from scripts import ExceptState, except_work

from .i_section import ISection


class Rr(ISection):

    def __init__(self, base):
        super().__init__(base)
        self._base.ui.lineEdit_rr_lever.setValidator(self._base.positive_float_val)
        self._base.ui.lineEdit_rr_r.setValidator(self._base.positive_float_val)
        self._base.ui.lineEdit_rr_stop.setValidator(self._base.positive_float_val)

    @except_work(ExceptState.CRITICAL)
    def standart_calculate(self):

        self._base.ui.pushButton_rr_calculate.setDisabled(True)
        if input_control(
            [
                self._base.ui.lineEdit_rr_stop,
                self._base.ui.lineEdit_rr_r,
                self._base.ui.lineEdit_rr_lever,
            ],duration=RrConfig.INPUT_DURATION
        ):
            stop = float(self._base.ui.lineEdit_rr_stop.text())
            r_ratio = float(self._base.ui.lineEdit_rr_r.text())
            lever = float(self._base.ui.lineEdit_rr_lever.text())

            rslt = rr_standart_calculate(stop, r_ratio, lever)
            self._base.ui.lcdNumber_rr_result.display(rslt)

            if self._base.ui.checkBox_rr_clear.isChecked():
                self._base.ui.lineEdit_rr_stop.clear()
                self._base.ui.lineEdit_rr_r.clear()
                self._base.ui.lineEdit_rr_lever.clear()

        self._base.ui.pushButton_rr_calculate.setDisabled(False)
