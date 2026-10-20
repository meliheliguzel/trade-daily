from collections import deque
from collections.abc import Callable

from PySide6.QtCore import QObject, QThread, Signal


class ThreadWorkerSignals(QObject):
    """Signals for the worker."""
    finished = Signal()
    error = Signal(str)

class ThreadWorker(QThread):
    def __init__(self):
        super().__init__()
        self.signals = ThreadWorkerSignals()
        self.work_queue: deque[tuple[Callable[..., None], list]] = deque()
        self.is_running = False
        self.is_paused = False  # Durum bilgisi ekledik

    def add_work(self, function: Callable[..., None], parameters: list | None = None) -> None:
        """Add new work to the queue."""
        self.work_queue.append((function, parameters or []))
        if not self.is_running:
            self.is_running = True
            self.start()

    def run(self) -> None:
        """Run the queued tasks sequentially."""
        while self.is_running and self.work_queue:
            if self.is_paused:
                self.msleep(100)  # Wait briefly if paused
                continue

            function, parameters = self.work_queue.popleft()
            try:
                function(*parameters)
                if not self.is_running:
                    break
                self.signals.finished.emit()
            except Exception as e:
                if not self.is_running:
                    break
                error_message: str = f"Error in function {function.__name__}: {e!s}"
                self.signals.error.emit(error_message)
        self.is_running = False

    def pause(self) -> None:
        """Pause the worker."""
        self.is_paused = True

    def resume(self) -> None:
        """Resume the worker."""
        self.is_paused = False

    def stop(self) -> None:
        """Stop the worker."""
        self.work_queue.clear()  # Clear work queue
        self.is_paused = True
        self.is_running = False

