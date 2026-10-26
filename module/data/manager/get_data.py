from typing import Any

from module.data.connection import Connect
from module.data.entities import DbEntity


def get_data(
    connection: Connect,
    entity: DbEntity,
    select_sql: str,
    values: tuple[Any, ...] | None = None,
) -> list[DbEntity] | Exception:

    try:
        data: list[tuple[Any, ...]] = connection.select(select_sql, values)
        return [entity(*i) for i in data]

    except Exception as e:
        return e
