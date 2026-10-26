from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow


class WebWindow(QMainWindow):
    def __init__(self, url: QUrl,title:str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        self.web_view.load(url)
        self.resize(1000, 625)
