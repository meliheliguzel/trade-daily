import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    _instance: Optional["Logger"] = None
    _log_file: str | None = None
    logger: logging.Logger = None

    def __new__(cls, log_file: str = "app.log") -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize_logger(log_file)
        elif log_file and cls._log_file != log_file:
            cls.set_log_file(log_file)
        return cls._instance

    @classmethod
    def _initialize_logger(cls, log_file: str) -> None:
        cls.logger = logging.getLogger("AppLogger")
        cls.logger.setLevel(logging.DEBUG)
        cls.set_log_file(log_file)

    @classmethod
    def set_log_file(cls, log_file: str) -> None:
        """Switch active log destination, safely closing previous handlers."""
        cls._log_file = log_file

        dir_name = os.path.dirname(log_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        cls.close()

        if cls.logger is None:
            cls.logger = logging.getLogger("AppLogger")
            cls.logger.setLevel(logging.DEBUG)

        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        cls.logger.addHandler(file_handler)

    @classmethod
    def close(cls) -> None:
        """Close and flush all open handlers to release file locks."""
        if hasattr(cls, "logger") and cls.logger:
            for handler in list(cls.logger.handlers):
                try:
                    handler.flush()
                    handler.close()
                except Exception:
                    pass
                cls.logger.removeHandler(handler)

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance and close handlers."""
        cls.close()
        cls._instance = None
        cls._log_file = None

    def set_log_level(self, level: str) -> None:
        level_dict: dict[str, int] = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        self.logger.setLevel(level_dict.get(level, logging.DEBUG))

    def set_log_format(self, format_string: str) -> None:
        formatter = logging.Formatter(format_string)
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    def _format_message(self, message: str, extra: str | None = None) -> str:
        if extra is not None:
            text = f"{message} - {extra}"
        else:
            text = str(message)
        return text.replace("\n", " ")

    def debug(self, message: str, extra: str | None = None) -> None:
        self.logger.debug(self._format_message(message, extra))

    def info(self, message: str, extra: str | None = None) -> None:
        self.logger.info(self._format_message(message, extra))

    def warning(self, message: str, extra: str | None = None) -> None:
        self.logger.warning(self._format_message(message, extra))

    def error(self, message: str, extra: str | None = None) -> None:
        self.logger.error(self._format_message(message, extra))

    def critical(self, message: str, extra: str | None = None) -> None:
        self.logger.critical(self._format_message(message, extra))
