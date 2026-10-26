from PySide6.QtWidgets import QDialog

from config import InfoConfig
from ui import Ui_info


class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_info()
        self.ui.setupUi(self)
        self.setWindowTitle(InfoConfig.TITLE)
        self.ui.textBrowser.setHtml(InfoConfig.get_html_content())
        self.ui.pushButton.clicked.connect(self.close)
