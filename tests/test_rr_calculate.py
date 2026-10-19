import pytest
from module.utils.rr_calculate import rr_standart_calculate


def test_rr_calculate_normal():
    # Example: stop = 2.0, r = 10.0, lever = 5.0 -> (10.0 / (2.0 * 5.0)) * 100 = (10.0 / 10.0) * 100 = 100.0
    result = rr_standart_calculate(2.0, 10.0, 5.0)
    assert result == 100.0


def test_rr_calculate_zero_stop():
    with pytest.raises(ZeroDivisionError):
        rr_standart_calculate(0.0, 10.0, 5.0)


def test_rr_calculate_zero_lever():
    with pytest.raises(ZeroDivisionError):
        rr_standart_calculate(2.0, 10.0, 0.0)


def test_rr_calculate_negative_values():
    # stop = -2.0, r = 10.0, lever = 5.0 -> (10.0 / (-2.0 * 5.0)) * 100 = -100.0
    result = rr_standart_calculate(-2.0, 10.0, 5.0)
    assert result == -100.0
