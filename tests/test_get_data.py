from unittest.mock import Mock

from module.data.entities.base_entity import DbEntity
from module.data.manager.get_data import get_data


class DummyEntity(DbEntity):
    def __init__(self, id_val, name_val):
        self.id = id_val
        self.name = name_val


def test_get_data_success():
    # Setup mock connection
    mock_conn = Mock()
    mock_conn.select.return_value = [
        (1, "Alice"),
        (2, "Bob"),
    ]

    # Run get_data
    result = get_data(mock_conn, DummyEntity, "SELECT * FROM users", (10,))

    # Assertions
    mock_conn.select.assert_called_once_with("SELECT * FROM users", (10,))
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], DummyEntity)
    assert result[0].id == 1
    assert result[0].name == "Alice"
    assert isinstance(result[1], DummyEntity)
    assert result[1].id == 2
    assert result[1].name == "Bob"


def test_get_data_exception():
    # Setup mock connection to raise an error
    mock_conn = Mock()
    forced_exception = RuntimeError("Database query timed out")
    mock_conn.select.side_effect = forced_exception

    # Run get_data
    result = get_data(mock_conn, DummyEntity, "SELECT * FROM users")

    # Assertions
    mock_conn.select.assert_called_once_with("SELECT * FROM users", None)
    assert isinstance(result, Exception)
    assert result is forced_exception
