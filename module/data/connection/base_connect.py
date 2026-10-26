from abc import ABCMeta
from typing import Any

from ...utils import SingletonMeta


class Connect(metaclass=SingletonMeta):
    __metaclass__: type[ABCMeta] = ABCMeta

    def __init__(self, db_name: str, retries: int = 3) -> None: ...

    def create_connection(self) -> None:
        """Establish a connection to the database and return the connection object"""
        ...

    def get_cursor(self) -> None:
        """Create and manage cursor objects"""
        ...

    def query(self, sql:str,values: tuple[Any, ...] = ()) -> None:
        ...

    def insert(self, insert_sql: str, values: tuple[Any, ...]) -> int|None:
        """Add new data to database"""
        ...

    def insert_many(self, insert_sql: str, seq_of_values: list[tuple[Any, ...]]) -> None:
        """Batch insert data into database"""
        ...

    def update(self, update_sql: str, values: tuple[Any, ...]) -> None:
        """Update data in database"""
        ...

    def delete(self, delete_sql: str, value: Any) -> None:
        """Delete data from database"""
        ...

    def select(self, select_sql: str, values: tuple[Any, ...] | None = None) -> list[tuple[Any, ...]]:
        """Select and return data from database"""
        ...

    def backup(self,backup_db_name:str) -> None:
        ...

    def close_connection(self) -> None:
        """Close database connection"""
        ...

