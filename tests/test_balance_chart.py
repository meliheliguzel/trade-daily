import os

from module.data.entities import Balance
from module.data.manager import BalanceGraphData
from module.tools.charts.balance import balance_graphics_create, graphics_fig_create


def test_balance_graphics_empty():
    assert graphics_fig_create([]) == []


def test_balance_graphics_create_success(tmp_path):
    bgd = BalanceGraphData()
    bgd.apply_balance_data([
        Balance(primary_key=1, transaction_id=1, size_id=1, value=1000.0, estimated=1000.0),
        Balance(primary_key=2, transaction_id=2, size_id=1, value=1150.0, estimated=1100.0),
    ])

    out_file = str(tmp_path / "balance_test.html")
    balance_graphics_create([bgd], out_file, dark_mode=True)

    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0

    with open(out_file, encoding="utf-8") as f:
        html = f.read()

    assert "dark-mode" in html
    assert "Balance Status 1" in html

    # Also test light mode
    out_light = str(tmp_path / "balance_light.html")
    balance_graphics_create([bgd], out_light, dark_mode=False)
    assert os.path.exists(out_light)


def test_balance_graphics_create_empty_list(tmp_path):
    out_file = str(tmp_path / "empty.html")
    balance_graphics_create([], out_file)
    assert not os.path.exists(out_file)
