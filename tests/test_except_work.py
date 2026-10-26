from collections.abc import Callable
from unittest.mock import Mock

import pytest

from scripts import ExceptState, except_work
from scripts.except_works import ExceptRun


LoggerFunc = Callable[[str, str], None]
StatusBarFunc = Callable[[str], None]


class Logger:
    def warning(self, message: str, location: str) -> None: ...
    def debug(self, message: str, location: str) -> None: ...
    def error(self, message: str, location: str) -> None: ...
    def critical(self, message: str, location: str) -> None: ...
    def info(self, message: str, location: str) -> None: ...

class StatusbarMessage:
    def show_warning_message(self, message: str) -> None: ...
    def show_error_message(self, message: str) -> None: ...
    def show_critical_message(self, message: str) -> None: ...


# Pytest Tests
class TestExceptRun:
    def test_initialization_and_mappings(self) -> None:
        mock_logger = Mock(spec=Logger)
        mock_status_bar = Mock(spec=StatusbarMessage)
        except_run = ExceptRun(mock_logger, mock_status_bar)

        # Check logger method mappings
        assert except_run.logger[ExceptState.WARNING] == mock_logger.warning
        assert except_run.logger[ExceptState.DEBUG] == mock_logger.debug
        assert except_run.logger[ExceptState.ERROR] == mock_logger.error
        assert except_run.logger[ExceptState.CRITICAL] == mock_logger.critical

        # Check status bar method mappings
        assert except_run.status_bar[ExceptState.WARNING] == mock_status_bar.show_warning_message
        assert except_run.status_bar[ExceptState.DEBUG] == mock_status_bar.show_warning_message
        assert except_run.status_bar[ExceptState.ERROR] == mock_status_bar.show_error_message
        assert except_run.status_bar[ExceptState.CRITICAL] == mock_status_bar.show_critical_message

class TestExceptWorkDecorator:
    @pytest.fixture
    def mock_self(self):
        mock_self = Mock()
        mock_self._base._logger = Mock(spec=Logger)
        mock_self._base._status_bar_message = Mock(spec=StatusbarMessage)
        return mock_self

    def test_logs_and_updates_status_on_exception(self, mock_self):
        state = ExceptState.ERROR

        @except_work(state)
        def func(self) :
            raise ValueError("Test error")

        result = func(mock_self)

        assert result is None
        error = "Test error"
        expected_location: str = f"{func.__module__} {func.__qualname__}"
        expected_message: str = f"{error!s} {expected_location}"
        mock_self._base._logger.error.assert_called_once_with(error, expected_location)
        mock_self._base._status_bar_message.show_error_message.assert_called_once_with(expected_message)

    def test_all_states_trigger_correct_methods(self, mock_self):
        test_cases: list[tuple[ExceptState, str, str]] = [
            (ExceptState.WARNING, 'warning', 'show_warning_message'),
            (ExceptState.DEBUG, 'debug', 'show_warning_message'),  # DEBUG maps to show_warning
            (ExceptState.ERROR, 'error', 'show_error_message'),
            (ExceptState.CRITICAL, 'critical', 'show_critical_message'),
        ]

        for state, logger_method, status_method in test_cases:
            @except_work(state)
            def func(self):
                raise Exception("Test")

            func(mock_self)

            getattr(mock_self._base._logger, logger_method).assert_called()
            getattr(mock_self._base._status_bar_message, status_method).assert_called()
            mock_self._base._logger.reset_mock()
            mock_self._base._status_bar_message.reset_mock()

    def test_integer_state(self, mock_self):
        @except_work(3)  # CRITICAL is 3
        def func(self):
            raise Exception("Test")

        func(mock_self)

        mock_self._base._logger.critical.assert_called()
        mock_self._base._status_bar_message.show_critical_message.assert_called()

    def test_no_exception_no_logs(self, mock_self):
        @except_work(ExceptState.WARNING)
        def func(self) :
            return "success"

        result = func(mock_self)

        assert result == "success"
        mock_self._base._logger.warning.assert_not_called()
        mock_self._base._status_bar_message.show_warning_message.assert_not_called()

    def test_metadata_preserved(self):
        def sample_func(self):
            """Sample docstring."""
            pass

        decorated_func = except_work(ExceptState.WARNING)(sample_func)

        assert decorated_func.__name__ == "sample_func"
        assert decorated_func.__doc__ == "Sample docstring."

    def test_invalid_state_raises_key_error(self, mock_self):
        @except_work(99)  # Invalid state
        def func(self):
            raise Exception("Test")

        with pytest.raises(KeyError):
            func(mock_self)


