import pytest

from module.data.settings.users import Locations, UsersManager


@pytest.fixture(autouse=True)
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


@pytest.mark.parametrize(
    "name",
    [
        "user1",
        "test_user",
        "my-account",
        "admin",
        "A1",
        "x_y-z",
    ],
)
def test_validate_name_valid(name):
    manager = UsersManager()
    assert manager.validate_name(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "a",  # Too short (1 char)
        "a" * 31,  # Too long (31 chars)
        "user@name",  # Invalid special character
        "user/name",  # Slash
        "user name",  # Space
        "user.name",  # Dot
        "",  # Empty
        "   ",  # Just whitespace
        None,  # None
        123,  # Integer
        ["user"],  # List
    ],
)
def test_validate_name_invalid(name):
    manager = UsersManager()
    assert manager.validate_name(name) is False


@pytest.mark.parametrize(
    "name",
    [
        "CON",
        "con",
        "Con",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "com9",
        "LPT1",
        "lpt9",
    ],
)
def test_validate_name_reserved(name):
    manager = UsersManager()
    assert manager.validate_name(name) is False
