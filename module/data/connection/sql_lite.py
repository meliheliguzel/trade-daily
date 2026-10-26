import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from .base_connect import Connect


class SQLiteConnectionError(Exception):
    """SQLite connection error"""
    pass

class SQLiteQueryError(Exception):
    """SQLite query error"""
    pass

class SQLite(Connect):
    def __init__(self, db_name: str, retries: int = 3) -> None:
        self.db_name = db_name
        self.retries = retries
        self.connection: sqlite3.Connection | None = self.create_connection()

    def create_connection(self) -> sqlite3.Connection:
        retry_count = 0
        while retry_count < self.retries:
            try:
                connection: sqlite3.Connection = sqlite3.connect(self.db_name)
                return connection
            except sqlite3.Error as e:
                retry_count += 1
                if retry_count >= self.retries:
                    raise SQLiteConnectionError(
                        f"Error establishing database connection: {e}"
                    )

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        if self.connection is None:
            self.connection = self.create_connection()
        cursor: sqlite3.Cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            raise SQLiteQueryError(f"Error while running query: {e}")
        finally:
            cursor.close()

    def query(self, sql: str, values: tuple[Any, ...] = ()) -> None:
        with self.get_cursor() as cursor:
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)

    def create_table(self,table_sql:str):
        self.query(table_sql)

    def insert(self, insert_sql: str, values: tuple[Any, ...]) -> int|None:
        with self.get_cursor() as cursor:
            cursor.execute(insert_sql, values)
            return cursor.lastrowid

    def insert_many(self, insert_sql: str, seq_of_values: list[tuple[Any, ...]]) -> None:
        if not seq_of_values:
            return
        with self.get_cursor() as cursor:
            cursor.executemany(insert_sql, seq_of_values)

    def update(self, update_sql: str, values: tuple[Any, ...]) -> None:
        self.query(update_sql, values)

    def delete(self, delete_sql: str, value: Any) -> None:
        self.query(delete_sql, (value,))

    def select(self, select_sql: str, values: tuple[Any, ...] | None = None) -> list[tuple[Any, ...]]:
        with self.get_cursor() as cursor:
            if values:
                cursor.execute(select_sql, values)
            else:
                cursor.execute(select_sql)
            return cursor.fetchall()

    def backup(self, backup_db_name: str) -> None:
        with sqlite3.connect(backup_db_name) as backup_connection:
            self.connection.backup(backup_connection)

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
