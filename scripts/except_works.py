from collections.abc import Callable
from enum import IntEnum
from functools import wraps
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from module.tools import Logger
    from module.tools.ui import StatusbarMessage
    from windows.protokol.isection import ISectionProtokol

LoggerFunc = Callable[..., None]
StatusBarFunc = Callable[[str], None]


class ExceptState(IntEnum):
    WARNING = 0
    DEBUG = 1
    ERROR = 2
    CRITICAL = 3


class ExceptRun:
    def __init__(self, logger: "Logger", status_bar: "StatusbarMessage") -> None:
        # Map each state to the corresponding logger method
        self.logger: dict[int, LoggerFunc] = {
            ExceptState.WARNING: logger.warning,
            ExceptState.DEBUG: logger.debug,
            ExceptState.ERROR: logger.error,
            ExceptState.CRITICAL: logger.critical,
        }
        # Map each state to the corresponding status bar method
        self.status_bar: dict[int, StatusBarFunc] = {
            ExceptState.WARNING: status_bar.show_warning_message,
            ExceptState.DEBUG: status_bar.show_warning_message,
            ExceptState.ERROR: status_bar.show_error_message,
            ExceptState.CRITICAL: status_bar.show_critical_message,
        }


def except_work( state: ExceptState | int
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to handle exceptions and log them."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any | None:
            self: ISectionProtokol = args[0]
            location: str = f"{func.__module__} {func.__qualname__}"
            try:
                self._base._logger.info("Function running...",location)
                return func(*args, **kwargs)
            except Exception as e:
                runner = ExceptRun(self._base._logger, self._base._status_bar_message)
                runner.logger[state](str(e), location)
                runner.status_bar[state](f"{e!s} {location}")
                return None

        return wrapper
    return decorator


