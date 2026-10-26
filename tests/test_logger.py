import pytest

from module.tools.logger import Logger


@pytest.fixture(autouse=True)
def cleanup_logger():
    Logger.reset()
    yield
    Logger.reset()


def test_logger_singleton(tmp_path):
    log_file_1 = tmp_path / "user1" / "app.log"
    logger1 = Logger(str(log_file_1))
    logger2 = Logger(str(log_file_1))

    assert logger1 is logger2


def test_logger_writes_to_file(tmp_path):
    log_file = tmp_path / "user1" / "app.log"
    logger = Logger(str(log_file))
    logger.info("Test message", "LocationA")
    logger.warning("Warning message")

    with open(log_file, encoding="utf-8") as f:
        content = f.read()

    assert "Test message - LocationA" in content
    assert "Warning message" in content


def test_logger_switch_account_log_file(tmp_path):
    log_user1 = tmp_path / "user1" / "app.log"
    log_user2 = tmp_path / "user2" / "app.log"

    logger = Logger(str(log_user1))
    logger.info("Message for user1")

    # Switch to user2
    logger.set_log_file(str(log_user2))
    logger.info("Message for user2")

    with open(log_user1, encoding="utf-8") as f:
        content1 = f.read()

    with open(log_user2, encoding="utf-8") as f:
        content2 = f.read()

    # user1 log should only have user1 message
    assert "Message for user1" in content1
    assert "Message for user2" not in content1

    # user2 log should only have user2 message
    assert "Message for user2" in content2
    assert "Message for user1" not in content2


def test_logger_reinstantiation_redirects_log_file(tmp_path):
    log_user1 = tmp_path / "user1" / "app.log"
    log_user2 = tmp_path / "user2" / "app.log"

    logger1 = Logger(str(log_user1))
    logger1.info("Init user 1")

    # Calling Logger with a different file should switch destination
    logger2 = Logger(str(log_user2))
    assert logger1 is logger2

    logger2.info("Init user 2")

    with open(log_user1, encoding="utf-8") as f:
        content1 = f.read()
    with open(log_user2, encoding="utf-8") as f:
        content2 = f.read()

    assert "Init user 1" in content1
    assert "Init user 2" not in content1
    assert "Init user 2" in content2


def test_logger_reset(tmp_path):
    log_file = tmp_path / "app.log"
    Logger(str(log_file))
    Logger.reset()

    assert Logger._instance is None
    assert Logger._log_file is None
