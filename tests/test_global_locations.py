
from config.global_var import FileNames, GlobalConfig, Locations, UserLocations


def test_locations_defaults():
    assert GlobalConfig.VERSION == "1.0"
    assert GlobalConfig.APP_NAME == "Trade_Daily"
    assert FileNames.LOG_FILE == "app.log"
    assert FileNames.DATA_BASE == "default.db"

    assert Locations.APP_DATA is not None
    assert Locations.MAIN is not None
    assert Locations.USER_SETUP.endswith(FileNames.USER_SETUP)


def test_locations_setters(tmp_path):
    orig_main = Locations.MAIN
    orig_app_data = Locations.APP_DATA
    orig_setup = Locations.USER_SETUP

    custom_main = str(tmp_path / "custom_main")
    Locations.set_main(custom_main)
    assert Locations.MAIN == custom_main
    assert Locations.USER_SETUP == f"{custom_main}/{FileNames.USER_SETUP}"

    custom_app_data = str(tmp_path / "custom_app_data")
    Locations.set_app_data(custom_app_data)
    assert Locations.APP_DATA == custom_app_data

    custom_setup = str(tmp_path / "custom_setup.json")
    Locations.set_user_setup(custom_setup)
    assert Locations.USER_SETUP == custom_setup

    # Reset
    Locations.set_main(orig_main)
    Locations.set_app_data(orig_app_data)
    Locations.set_user_setup(orig_setup)


def test_user_locations():
    user = "alice"
    loc = UserLocations(user)
    assert loc.LOG == f"{Locations.MAIN}/{user}/{FileNames.LOG_FILE}"
    assert loc.DATA_BASE == f"{Locations.MAIN}/{user}/{FileNames.DATA_BASE}"
    assert loc.ANALYSIS_GRAPH == f"{Locations.MAIN}/{user}/{FileNames.ANALYSIS_GRAPH}"
    assert loc.BALANCE_GRAPH == f"{Locations.MAIN}/{user}/{FileNames.BALANCE_GRAPH}"
