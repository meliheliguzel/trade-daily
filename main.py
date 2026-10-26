import atexit
import sys

from PySide6.QtWidgets import QApplication

from windows.main import MainWindow


def run() -> None:
    app = QApplication(sys.argv)
    widget = MainWindow()

    @atexit.register
    def closed():
        widget._data_base.close_connection()
        widget._logger.close()

    widget.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()



