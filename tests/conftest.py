import pytest
from PySide6.QtWidgets import QApplication

from module.data.connection import SQLite


@pytest.fixture(scope="session")
def qapp():
    """Single QApplication instance for the entire test suite."""
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singletons after every test."""
    yield
    SQLite.reset()


@pytest.fixture
def tmp_db(tmp_path):
    """Isolated temporary database fixture."""
    SQLite.reset()
    db_path = str(tmp_path / "test.db")
    db = SQLite(db_path)
    yield db
    db.close_connection()
    SQLite.reset()
