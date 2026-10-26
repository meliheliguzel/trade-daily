from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QCheckBox, QLCDNumber, QLineEdit, QPushButton, QWidget

from windows.main.rr import Rr


class DummyRrBase(QWidget):
    def __init__(self):
        super().__init__()
        self._logger = MagicMock()
        self._status_bar_message = MagicMock()
        self.positive_float_val = QDoubleValidator(0.0, 1e9, 6, self)
        self.ui = MagicMock()
        self.ui.lineEdit_rr_lever = QLineEdit(self)
        self.ui.lineEdit_rr_r = QLineEdit(self)
        self.ui.lineEdit_rr_stop = QLineEdit(self)
        self.ui.pushButton_rr_calculate = QPushButton(self)
        self.ui.lcdNumber_rr_result = QLCDNumber(self)
        self.ui.checkBox_rr_clear = QCheckBox(self)


@pytest.fixture
def rr_fixture(qtbot):
    base = DummyRrBase()
    qtbot.addWidget(base)
    rr = Rr(base)
    return base, rr


def test_rr_calculation_success(rr_fixture):
    base, rr = rr_fixture

    base.ui.lineEdit_rr_stop.setText("2.5")
    base.ui.lineEdit_rr_r.setText("1.0")
    base.ui.lineEdit_rr_lever.setText("10.0")
    base.ui.checkBox_rr_clear.setChecked(False)

    rr.standart_calculate()

    # stop=2.5, r=1.0, lever=10 -> rr_standart_calculate(2.5, 1.0, 10.0)
    # result = (100 * 1.0) / (2.5 * 10.0) = 100 / 25 = 4.0
    assert base.ui.lcdNumber_rr_result.value() == 4.0
    assert base.ui.lineEdit_rr_stop.text() == "2.5"


def test_rr_calculation_with_clear(rr_fixture):
    base, rr = rr_fixture

    base.ui.lineEdit_rr_stop.setText("5.0")
    base.ui.lineEdit_rr_r.setText("2.0")
    base.ui.lineEdit_rr_lever.setText("5.0")
    base.ui.checkBox_rr_clear.setChecked(True)

    rr.standart_calculate()

    # result = (100 * 2.0) / (5.0 * 5.0) = 200 / 25 = 8.0
    assert base.ui.lcdNumber_rr_result.value() == 8.0
    assert base.ui.lineEdit_rr_stop.text() == ""
    assert base.ui.lineEdit_rr_r.text() == ""
    assert base.ui.lineEdit_rr_lever.text() == ""


def test_rr_calculation_empty_input(rr_fixture):
    base, rr = rr_fixture

    base.ui.lineEdit_rr_stop.setText("")
    base.ui.lineEdit_rr_r.setText("1.0")
    base.ui.lineEdit_rr_lever.setText("10.0")

    rr.standart_calculate()
    assert base.ui.lcdNumber_rr_result.value() == 0.0
