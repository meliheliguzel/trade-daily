# urllineedit.py
import pytest
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit


class UrlLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter URL (http:// or https://)")

        # URL validation regular expression
        url_pattern = (
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$"
        )

        reg_exp = QRegularExpression(url_pattern, QRegularExpression.CaseInsensitiveOption)
        validator = QRegularExpressionValidator(reg_exp, self)
        self.setValidator(validator)

        # Set up style for validation feedback
        self.textChanged.connect(self._update_style)

    def _update_style(self):
        if self.hasAcceptableInput():
            self.setStyleSheet("background-color: white;")
        else:
            self.setStyleSheet("background-color: #FFC0CB;")




@pytest.fixture
def url_line_edit(qtbot):
    widget = UrlLineEdit()
    qtbot.addWidget(widget)
    return widget

VALID_URLS = [
    "http://example.com",
    "https://www.example.com",
    "http://localhost:8080",
    "http://192.168.1.1",
    "https://example.com/path?query=param#fragment",
]

INVALID_URLS = [
    "example.com",
    "ftp://example.com",
    "http://",
    "https://example space.com",
    "just a string",
]

@pytest.mark.parametrize("url", VALID_URLS)
def test_valid_urls(url_line_edit, url):
    url_line_edit.setText(url)
    assert url_line_edit.hasAcceptableInput()

@pytest.mark.parametrize("url", INVALID_URLS)
def test_invalid_urls(url_line_edit, url):
    url_line_edit.setText(url)
    assert not url_line_edit.hasAcceptableInput()

def test_empty_input(url_line_edit):
    url_line_edit.setText("")
    assert not url_line_edit.hasAcceptableInput()
