import sqlite3

import pytest

from module.data.connection import SQLite, SQLiteConnectionError, SQLiteQueryError


# pytest fixture for setting up and tearing down the database
@pytest.fixture
def db():
    SQLite.reset()
    db_name = ':memory:'
    sql = SQLite(db_name)
    yield sql
    sql.close_connection()
    SQLite.reset()

def test_create_connection(db:SQLite):
    assert isinstance(db.connection, sqlite3.Connection)

def test_create_connection_error(monkeypatch):
    def mock_connect(*args, **kwargs):
        raise sqlite3.Error("Mock connection error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)
    with pytest.raises(SQLiteConnectionError):
        SQLite(':memory:')

def test_insert(db:SQLite):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    db.insert("INSERT INTO test (name) VALUES (?)", ("Test Name",))
    result = db.select("SELECT * FROM test")
    assert len(result) == 1
    assert result[0][1] == "Test Name"

@pytest.mark.parametrize("initial_name, updated_name", [
    ("Test Name", "Updated Name"),
    ("Another Name", "Another Updated Name")
])
def test_update(db:SQLite, initial_name, updated_name):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    db.insert("INSERT INTO test (name) VALUES (?)", (initial_name,))
    db.update("UPDATE test SET name = ? WHERE id = ?", (updated_name, 1))
    result = db.select("SELECT name FROM test WHERE id = ?", (1,))
    assert result[0][0] == updated_name

@pytest.mark.parametrize("initial_name", [
    ("Test Name",),
    ("Another Name",)
])
def test_delete(db:SQLite, initial_name):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    db.insert("INSERT INTO test (name) VALUES (?)", initial_name)
    db.delete("DELETE FROM test WHERE id = ?", 1)
    result = db.select("SELECT * FROM test")
    assert len(result) == 0

def test_select(db:SQLite):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    db.insert("INSERT INTO test (name) VALUES (?)", ("Test Name",))
    result = db.select("SELECT * FROM test WHERE id = ?", (1,))
    assert len(result) == 1
    assert result[0][1] == "Test Name"

def test_backup(db:SQLite, tmpdir):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    db.insert("INSERT INTO test (name) VALUES (?)", ("Test Name",))
    backup_db_path = tmpdir / "backup.db"
    db.backup(str(backup_db_path))
    backup_sql = SQLite(str(backup_db_path))
    result = backup_sql.select("SELECT * FROM test")
    assert len(result) == 1
    assert result[0][1] == "Test Name"
    backup_sql.close_connection()

# Test exception handling
def test_insert_error(db:SQLite):
    with pytest.raises(SQLiteQueryError):
        db.insert("INSERT INTO non_existing_table (name) VALUES (?)", ("Test Name",))

def test_update_error(db:SQLite):
    with pytest.raises(SQLiteQueryError):
        db.update("UPDATE non_existing_table SET name = ? WHERE id = ?", ("Updated Name", 1))

def test_delete_error(db:SQLite):
    with pytest.raises(SQLiteQueryError):
        db.delete("DELETE FROM non_existing_table WHERE id = ?", 1)

def test_select_error(db:SQLite):
    with pytest.raises(SQLiteQueryError):
        db.select("SELECT * FROM non_existing_table WHERE id = ?", (1,))

def test_insert_many(db: SQLite):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    rows = [("Item 1",), ("Item 2",), ("Item 3",)]
    db.insert_many("INSERT INTO test (name) VALUES (?)", rows)
    result = db.select("SELECT name FROM test ORDER BY id")
    assert len(result) == 3
    assert [r[0] for r in result] == ["Item 1", "Item 2", "Item 3"]

def test_insert_many_empty(db: SQLite):
    create_table_sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    db.query(create_table_sql)
    db.insert_many("INSERT INTO test (name) VALUES (?)", [])
    result = db.select("SELECT * FROM test")
    assert len(result) == 0

if __name__ == "__main__":
    pytest.main()




