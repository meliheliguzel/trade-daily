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

def test_initialization_no_existing_data(tmp_app_data):
    manager = UsersManager()
    assert manager.data.CURRENT_USER == "main"
    assert manager.data.USER_LIST == ["main"]
    assert (tmp_app_data / "main").is_dir()

def test_add_user(tmp_app_data):
    manager = UsersManager()
    initial_user_count = len(manager.data.USER_LIST)
    manager.add("test_user")
    assert "test_user" in manager.data.USER_LIST
    assert len(manager.data.USER_LIST) == initial_user_count + 1
    assert (tmp_app_data / "test_user").is_dir()

def test_add_duplicate_user(tmp_app_data):
    manager = UsersManager()
    initial_users = manager.data.USER_LIST.copy()
    manager.add("main")
    assert manager.data.USER_LIST == initial_users

def test_update_success(tmp_app_data):
    manager = UsersManager()
    manager.add("old_user")
    manager.update("old_user", "new_user")
    assert "new_user" in manager.data.USER_LIST
    assert "old_user" not in manager.data.USER_LIST
    assert (tmp_app_data / "new_user").is_dir()
    assert not (tmp_app_data / "old_user").exists()

def test_update_non_existent(tmp_app_data):
    manager = UsersManager()
    result = manager.update("nonexistent", "new_user")
    assert not result
    assert "new_user" not in manager.data.USER_LIST

def test_remove(tmp_app_data):
    manager = UsersManager()
    manager.add("test_user")
    manager.remove("test_user")
    assert "test_user" not in manager.data.USER_LIST
    assert not (tmp_app_data / "test_user").exists()

def test_remove_current_user_switches_to_next(tmp_app_data):
    manager = UsersManager()
    manager.add("user2")
    manager.add("user3")
    manager.set_current_user("user2")
    manager.remove("user2")
    assert "user2" not in manager.data.USER_LIST
    assert manager.data.CURRENT_USER == "main"
    assert (tmp_app_data / "user3").is_dir()
    assert not (tmp_app_data / "user2").exists()

def test_remove_last_user_re_adds_main(tmp_app_data):
    manager = UsersManager()
    manager.remove("main")
    assert "main" in manager.data.USER_LIST
    assert manager.data.CURRENT_USER == "main"

def test_set_current_user_valid(tmp_app_data):
    manager = UsersManager()
    manager.add("user2")
    result = manager.set_current_user("user2")
    assert result
    assert manager.data.CURRENT_USER == "user2"

def test_set_current_user_invalid(tmp_app_data):
    manager = UsersManager()
    result = manager.set_current_user("invalid_user")
    assert not result
    assert manager.data.CURRENT_USER == "main"

def test_data_persistence(tmp_app_data):
    # This test may fail due to save/load issues in the original code
    manager1 = UsersManager()
    manager1.add("persisted_user")
    manager1.set_current_user("persisted_user")

    # Simulate restart by creating a new manager
    manager2 = UsersManager()

    assert "persisted_user" in manager2.data.USER_LIST
    assert manager2.data.CURRENT_USER == "persisted_user"
