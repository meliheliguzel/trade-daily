from pathlib import Path

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


def test_users_manager_save_load_cycle(tmp_app_data):
    # Initialize first manager -> creates default 'main'
    manager1 = UsersManager()
    assert manager1.data.CURRENT_USER == "main"
    assert manager1.data.USER_LIST == ["main"]

    # Add users and change current user
    manager1.add("user_a")
    manager1.add("user_b")
    manager1.set_current_user("user_a")
    manager1.save()

    # Initialize second manager to load persisted data from the same file
    manager2 = UsersManager()
    assert manager2.data.CURRENT_USER == "user_a"
    assert "user_b" in manager2.data.USER_LIST
    assert len(manager2.data.USER_LIST) == 3


def test_users_manager_corrupted_json_recovery(tmp_app_data):
    # Setup corrupted JSON file
    user_setup_path = Path(Locations.USER_SETUP)
    user_setup_path.parent.mkdir(parents=True, exist_ok=True)
    with open(user_setup_path, "w") as f:
        f.write("{invalid json: corrupt}")

    # Initializing manager on corrupted JSON should fall back gracefully and recreate 'main'
    manager = UsersManager()
    assert manager.data.CURRENT_USER == "main"
    assert manager.data.USER_LIST == ["main"]
    assert (tmp_app_data / "main").is_dir()
