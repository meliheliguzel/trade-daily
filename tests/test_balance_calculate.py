import pytest

from config.query.balance import BalanceQuery
from module.data.connection import SQLite
from module.data.connection.database_create import create_new_user_db


@pytest.fixture
def test_db(tmp_path):
    SQLite.reset()
    db_path = str(tmp_path / "test_user.db")
    create_new_user_db(db_path)
    db = SQLite(db_path)
    yield db
    db.close_connection()
    SQLite.reset()


def test_balance_calculate_with_open_positions(test_db):
    # Insert required foreign key rows
    test_db.insert("INSERT INTO Platform (name) VALUES (?);", ("Binance",))
    test_db.insert("INSERT INTO Parity (platform_id, name) VALUES (?, ?);", (1, "BTC/USDT"))
    test_db.insert("INSERT INTO Balance_Size (size, state) VALUES (?, ?);", (1000.0, 1))

    # Transaction 1: Closed with Take Profit (tp_sl = 1, result = 200.0)
    test_db.insert(
        "INSERT INTO \"Transaction\" (platform_id, parity_id, date_of_entry, long_short, rr, size) VALUES (?, ?, ?, ?, ?, ?);",
        (1, 1, "2026-01-01 10:00:00", 1, 2.0, 100.0),
    )
    test_db.insert(
        "INSERT INTO Transaction_Closing (transaction_id, date_of_exit, tp_sl, result) VALUES (?, ?, ?, ?);",
        (1, "2026-01-01 12:00:00", 1, 200.0),
    )

    # Transaction 2: OPEN trade (No Transaction_Closing entry!)
    test_db.insert(
        "INSERT INTO \"Transaction\" (platform_id, parity_id, date_of_entry, long_short, rr, size) VALUES (?, ?, ?, ?, ?, ?);",
        (1, 1, "2026-01-02 10:00:00", 0, 1.5, 100.0),
    )

    # Transaction 3: Closed with Stop Loss (tp_sl = 0, result = -50.0)
    test_db.insert(
        "INSERT INTO \"Transaction\" (platform_id, parity_id, date_of_entry, long_short, rr, size) VALUES (?, ?, ?, ?, ?, ?);",
        (1, 1, "2026-01-03 10:00:00", 1, 3.0, 50.0),
    )
    test_db.insert(
        "INSERT INTO Transaction_Closing (transaction_id, date_of_exit, tp_sl, result) VALUES (?, ?, ?, ?);",
        (3, "2026-01-03 14:00:00", 0, -50.0),
    )

    # Execute CALCULATE with initial balance 1000.0 and size_id 1
    rows = test_db.select(BalanceQuery.CALCULATE, (1000.0, 1))
    assert len(rows) == 3

    # Row 1 (TP): start 1000 + 200 = 1200
    t1_id, size_id, res1, est1 = rows[0]
    assert t1_id == 1
    assert size_id == 1
    assert res1 == 1200.0
    assert est1 == 1200.0

    # Row 2 (OPEN): should NOT be penalized as a loss. It should remain 1200.0!
    t2_id, _, res2, est2 = rows[1]
    assert t2_id == 2
    assert res2 == 1200.0
    assert est2 == 1200.0

    # Row 3 (SL): 1200 - 50 = 1150
    t3_id, _, res3, est3 = rows[2]
    assert t3_id == 3
    assert res3 == 1150.0
    assert est3 == 1150.0
