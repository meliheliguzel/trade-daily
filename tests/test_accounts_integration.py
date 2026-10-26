import sqlite3

import pytest

from module.data.settings.users import Locations, UsersManager


@pytest.fixture
def tmp_app_data(tmp_path):
    old_main = Locations.MAIN
    old_user_setup = Locations.USER_SETUP
    old_app_data = Locations.APP_DATA

    app_data_path = tmp_path / "appdata"
    Locations.set_app_data(str(app_data_path))
    Locations.set_main(str(app_data_path))

    yield app_data_path

    Locations.set_app_data(old_app_data)
    Locations.MAIN = old_main
    Locations.USER_SETUP = old_user_setup


def test_account_creation_and_db_initialization(tmp_app_data):
    manager = UsersManager()

    # Create new account
    manager.add("test_acc")

    # Verify folder is physically created
    acc_dir = tmp_app_data / "test_acc"
    assert acc_dir.is_dir()

    # Verify default.db is initialized with all tables
    db_path = acc_dir / "default.db"
    assert db_path.is_file()

    with sqlite3.connect(str(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        # Ensure critical tables exist
        assert "Platform" in tables
        assert "Strategy" in tables
        assert "Balance" in tables
        assert "Note" in tables


def test_account_rename(tmp_app_data):
    manager = UsersManager()
    manager.add("old_name")

    # Verify old folder exists
    assert (tmp_app_data / "old_name").is_dir()

    # Rename account
    manager.update("old_name", "new_name")

    # Verify old folder is renamed/moved to new folder name
    assert not (tmp_app_data / "old_name").exists()
    assert (tmp_app_data / "new_name").is_dir()
    assert (tmp_app_data / "new_name" / "default.db").is_file()


def test_account_deletion_and_fallback(tmp_app_data):
    manager = UsersManager()
    manager.add("acc_to_del")

    # Verify acc_to_del exists
    assert (tmp_app_data / "acc_to_del").is_dir()

    # Delete account
    manager.remove("acc_to_del")

    # Verify folder is fully cleaned up
    assert not (tmp_app_data / "acc_to_del").exists()


def test_delete_last_account_recreates_main(tmp_app_data):
    manager = UsersManager()
    # At start, "main" is the only account in user list
    assert manager.data.USER_LIST == ["main"]
    assert (tmp_app_data / "main").is_dir()

    # Remove "main" (the last active account)
    manager.remove("main")

    # Verify "main" folder was recreated and main is re-added
    assert manager.data.USER_LIST == ["main"]
    assert manager.data.CURRENT_USER == "main"
    assert (tmp_app_data / "main").is_dir()
    assert (tmp_app_data / "main" / "default.db").is_file()
