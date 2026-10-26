import os

import pytest

from config.query.data_base import DataBaseQuery
from config.query.parity import ParityQuery
from config.query.platform import PlatformQuery
from config.query.strategy import StrategyQuery
from module.data.connection.sql_lite import SQLite
from module.tools.charts.balance import balance_graphics_create, graphics_fig_create


@pytest.fixture
def test_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    SQLite.reset()
    db = SQLite(db_path)
    # Initialize necessary tables
    db.create_table(DataBaseQuery.platform)
    db.create_table(DataBaseQuery.parity)
    db.create_table(DataBaseQuery.strategy)
    db.create_table(DataBaseQuery.balance_size)
    db.create_table(DataBaseQuery.balance)
    yield db
    db.close_connection()
    SQLite.reset()


def test_multiple_parities_same_platform(test_db):
    # Add platform
    test_db.insert(PlatformQuery.ADD, ("Binance",))
    platforms = test_db.select(PlatformQuery.LOAD)
    assert len(platforms) == 1
    platform_id = platforms[0][0]

    # Add first parity
    count1 = test_db.select(ParityQuery.NAME_CONTROL, ("BTCUSDT", platform_id))[0][0]
    assert count1 == 0
    test_db.insert(ParityQuery.ADD, ("BTCUSDT", platform_id))

    # Check first parity exists
    count1_after = test_db.select(ParityQuery.NAME_CONTROL, ("BTCUSDT", platform_id))[0][0]
    assert count1_after == 1

    # Add second parity to the SAME platform
    count2 = test_db.select(ParityQuery.NAME_CONTROL, ("ETHUSDT", platform_id))[0][0]
    assert count2 == 0
    test_db.insert(ParityQuery.ADD, ("ETHUSDT", platform_id))

    # Verify both parities exist for platform_id
    parities = test_db.select(ParityQuery.LOAD, (platform_id,))
    assert len(parities) == 2
    names = [p[2] for p in parities]
    assert "BTCUSDT" in names
    assert "ETHUSDT" in names


def test_parity_name_control_update(test_db):
    test_db.insert(PlatformQuery.ADD, ("Binance",))
    platform_id = test_db.select(PlatformQuery.LOAD)[0][0]

    test_db.insert(ParityQuery.ADD, ("BTCUSDT", platform_id))
    btc_id = test_db.select(ParityQuery.LOAD, (platform_id,))[0][0]

    test_db.insert(ParityQuery.ADD, ("ETHUSDT", platform_id))
    next(p[0] for p in test_db.select(ParityQuery.LOAD, (platform_id,)) if p[2] == "ETHUSDT")

    # Updating BTCUSDT with the same name: should not conflict with itself
    dup = test_db.select(ParityQuery.NAME_CONTROL_UPDATE, ("BTCUSDT", platform_id, btc_id))[0][0]
    assert dup == 0

    # Renaming BTCUSDT to ETHUSDT: should conflict with existing ETHUSDT
    dup_conflict = test_db.select(ParityQuery.NAME_CONTROL_UPDATE, ("ETHUSDT", platform_id, btc_id))[0][0]
    assert dup_conflict == 1


def test_platform_name_control_update(test_db):
    test_db.insert(PlatformQuery.ADD, ("Binance",))
    p1_id = test_db.select(PlatformQuery.LOAD)[0][0]

    test_db.insert(PlatformQuery.ADD, ("Bybit",))
    next(p[0] for p in test_db.select(PlatformQuery.LOAD) if p[1] == "Bybit")

    # Updating Binance without changing name: should not conflict with itself
    dup = test_db.select(PlatformQuery.NAME_CONTROL_UPDATE, ("Binance", p1_id))[0][0]
    assert dup == 0

    # Renaming Binance to Bybit: should conflict
    dup_conflict = test_db.select(PlatformQuery.NAME_CONTROL_UPDATE, ("Bybit", p1_id))[0][0]
    assert dup_conflict == 1


def test_strategy_name_control_update(test_db):
    test_db.insert(StrategyQuery.ADD, ("Breakout", "Description 1"))
    s1_id = test_db.select(StrategyQuery.LOAD)[0][0]

    test_db.insert(StrategyQuery.ADD, ("Trend", "Description 2"))

    # Updating Breakout without changing name: no conflict
    dup = test_db.select(StrategyQuery.NAME_CONTROL_UPDATE, ("Breakout", s1_id))[0][0]
    assert dup == 0

    # Renaming Breakout to Trend: conflict
    dup_conflict = test_db.select(StrategyQuery.NAME_CONTROL_UPDATE, ("Trend", s1_id))[0][0]
    assert dup_conflict == 1


def test_balance_graphics_empty_data(tmp_path):
    # Ensure balance graphics functions do not raise errors when data is None or empty
    assert graphics_fig_create(None) == []
    assert graphics_fig_create([]) == []

    file_path = str(tmp_path / "balance.html")
    # Should safely return without creating file or throwing exception
    balance_graphics_create(None, file_path)
    assert not os.path.exists(file_path)

    balance_graphics_create([], file_path)
    assert not os.path.exists(file_path)
