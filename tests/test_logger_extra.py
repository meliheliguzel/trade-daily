from module.tools.logger import Logger


def test_logger_levels_and_formatting(tmp_path):
    log_file = str(tmp_path / "test_extra.log")
    Logger.reset()
    logger = Logger(log_file)

    logger.set_log_level("INFO")
    logger.set_log_format("%(message)s")

    logger.debug("Debug msg - should be ignored")
    logger.info("Info msg")
    logger.warning("Warning msg", extra="extra_info")
    logger.error("Error msg")
    logger.critical("Critical msg")

    Logger.close()

    with open(log_file, encoding="utf-8") as f:
        content = f.read()

    assert "Info msg" in content
    assert "Warning msg - extra_info" in content
    assert "Error msg" in content
    assert "Critical msg" in content
    assert "Debug msg" not in content

    Logger.reset()
