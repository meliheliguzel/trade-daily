import pytest
from PySide6.QtCore import QDateTime
import datetime
from module.utils.time_convert import str_to_qDateTime, current_time


def test_str_to_qDateTime_slashes():
    dt = str_to_qDateTime("27/5/2026 13:45")
    assert isinstance(dt, QDateTime)
    assert dt.date().year() == 2026
    assert dt.date().month() == 5
    assert dt.date().day() == 27
    assert dt.time().hour() == 13
    assert dt.time().minute() == 45


def test_str_to_qDateTime_dots():
    dt = str_to_qDateTime("27.5.2026 13:45")
    assert isinstance(dt, QDateTime)
    assert dt.date().year() == 2026
    assert dt.date().month() == 5
    assert dt.date().day() == 27
    assert dt.time().hour() == 13
    assert dt.time().minute() == 45


def test_str_to_qDateTime_invalid():
    dt = str_to_qDateTime("2026-05-27 13:45")
    assert dt is None


def test_current_time():
    now_qdt = current_time()
    now_sys = datetime.datetime.now()

    assert isinstance(now_qdt, QDateTime)
    assert now_qdt.date().year() == now_sys.year
    assert now_qdt.date().month() == now_sys.month
    assert now_qdt.date().day() == now_sys.day
    assert now_qdt.time().hour() == now_sys.hour
    assert now_qdt.time().minute() == now_sys.minute
