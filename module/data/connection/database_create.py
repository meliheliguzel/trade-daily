import os
import sqlite3

from config.query import DataBaseQuery


def create_new_user_db(location: str) -> None:
    """Creates a new user database at the specified location and initializes schema tables."""
    os.makedirs(os.path.dirname(location), exist_ok=True)
    conn = sqlite3.connect(location)
    try:
        cursor = conn.cursor()
        try:
            for table_sql in DataBaseQuery.TABLE_LIST:
                cursor.execute(table_sql)
            conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()


