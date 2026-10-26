
import pytest
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QLineEdit,
    QPlainTextEdit,
    QRadioButton,
    QTextEdit,
    QWidget,
)

from module.tools.ui.input_control import (
    BorderColors,
    _get_widget_style,
    _validate_qcheckbox,
    _validate_qcombobox,
    _validate_qgroupbox,
    _validate_qlineedit,
    _validate_text_edit,
    border_reset,
    change_border,
    input_control,
)


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app



@pytest.fixture
def test_widget(qapp):
    widget = QLineEdit()
    widget.setObjectName("test_widget")
    yield widget
    widget.deleteLater()


def test_validate_qlineedit(qapp):
    widget = QLineEdit()
    widget.setText("   ")
    assert not _validate_qlineedit(widget)
    widget.setText("valid")
    assert _validate_qlineedit(widget)


def test_validate_text_edit(qapp):
    for widget_cls in [QTextEdit, QPlainTextEdit]:
        widget = widget_cls()
        widget.setPlainText("   ")
        assert not _validate_text_edit(widget)
        widget.setPlainText("valid")
        assert _validate_text_edit(widget)


def test_validate_qcombobox(qapp):
    # Editable, empty
    combo = QComboBox()
    combo.setEditable(True)
    combo.lineEdit().setText("   ")
    assert not _validate_qcombobox(combo)

    # Editable, valid
    combo.lineEdit().setText("valid")
    assert _validate_qcombobox(combo)

    # Non-editable, no items
    combo.setEditable(False)
    combo.clear()
    assert not _validate_qcombobox(combo)

    # Non-editable, items but invalid index
    combo.addItems(["item1", "item2"])
    combo.setCurrentIndex(-1)
    assert not _validate_qcombobox(combo)

    # Non-editable, valid index
    combo.setCurrentIndex(0)
    assert _validate_qcombobox(combo)


def test_validate_qgroupbox(qapp):
    group = QGroupBox()
    # No radios → valid
    assert _validate_qgroupbox(group)

    # Add radios, none checked
    radio = QRadioButton(group)
    assert not _validate_qgroupbox(group)

    # Check a radio
    radio.setChecked(True)
    assert _validate_qgroupbox(group)


def test_validate_qcheckbox(qapp):
    cb = QCheckBox()
    assert not _validate_qcheckbox(cb)
    cb.setChecked(True)
    assert _validate_qcheckbox(cb)


def test_change_border_no_duration(qapp, mocker):
    mock_timer = mocker.patch.object(QTimer, "singleShot")
    widget = QLineEdit()
    change_border(widget, duration=None)
    assert "border: 2px solid red" in widget.styleSheet()
    mock_timer.assert_not_called()


def test_border_reset(qapp):
    widget = QLineEdit()
    change_border(widget, duration=None)
    border_reset(widget)
    assert "border: 2px solid red" not in widget.styleSheet()


def test_border_reset_with_existing_style(qapp):
    widget = QLineEdit()
    widget.setStyleSheet("color: white;")
    change_border(widget, duration=None)
    border_reset(widget, BorderColors.RED)
    assert widget.styleSheet() == "color: white;"


def test_input_control_single_valid(qapp):
    widget = QLineEdit()
    widget.setText("valid")
    assert input_control(widget)


def test_input_control_single_invalid(qapp):
    widget = QLineEdit()
    assert not input_control(widget)
    assert "border: 2px solid red" in widget.styleSheet()


def test_input_control_mixed_widgets(qapp):
    valid = QLineEdit(text="valid")
    invalid = QLineEdit()
    assert not input_control([valid, invalid])
    assert "border" not in valid.styleSheet()
    assert "border: 2px solid red" in invalid.styleSheet()


def test_input_control_unknown_widget(qapp):
    widget = QWidget()  # Not in validation handlers
    assert not input_control(widget)
    assert "border: 2px solid red" in widget.styleSheet()


def test_get_widget_style_without_name():
    widget = QLineEdit()
    assert (
        _get_widget_style(widget, "green") == "QLineEdit { border: 2px solid green; }"
    )


def test_get_widget_style_with_name():
    widget = QLineEdit()
    widget.setObjectName("myWidget")
    assert _get_widget_style(widget, "cyan") == "#myWidget { border: 2px solid cyan; }"


def test_groupbox_without_radios(qapp):
    group = QGroupBox()
    group.setCheckable(True)
    group.setChecked(False)
    assert _validate_qgroupbox(group)  # No radios → considered valid




def test_change_border_appends_style(qapp, mocker):
    """Checks whether to keep the current style and add the new style"""
    widget = QLineEdit()
    widget.setStyleSheet("color: white;")

    change_border(widget, BorderColors.BLUE, 10)

    expected_style = _get_widget_style(widget,BorderColors.BLUE)
    assert  expected_style in  widget.styleSheet()
    assert  "color: white;" in  widget.styleSheet()



def test_change_border_with_zero_duration(qapp, mocker):
    """If the duration is given as 0, the timer will not start."""
    mock_timer = mocker.patch.object(QTimer, "singleShot")
    widget = QLineEdit()

    change_border(widget, duration=0)

    mock_timer.assert_not_called()


def test_border_reset_with_multiple_styles(qapp):
    """Removes only the relevant style when there are multiple styles"""
    widget = QLineEdit()
    delete_style = _get_widget_style(widget, BorderColors.RED)
    widget.setStyleSheet(
        f"""
        {delete_style}
        QLineEdit {{
            border: 3px dashed blue;
            background: yellow;
        }}
    """
    )

    border_reset(widget, BorderColors.RED)

    assert delete_style not in widget.styleSheet()
    assert "border: 3px dashed blue" in widget.styleSheet()
    assert "background: yellow" in widget.styleSheet()




def test_change_border_immediate_effect(test_widget):
    # No borders at the beginning
    assert "border" not in test_widget.styleSheet()

    change_border(test_widget, BorderColors.RED, duration=1)

    # The style should be applied immediately
    assert "border: 2px solid red" in test_widget.styleSheet()


def test_border_reset_mechanism(test_widget):

    test_widget.setStyleSheet("#test_widget { border: 2px solid red; }")

    border_reset(test_widget, BorderColors.RED)

    assert "border: 2px solid red" not in test_widget.styleSheet()


def test_duration_reset_with_mocked_timer(test_widget, mocker):
    mock_timer = mocker.patch("PySide6.QtCore.QTimer.singleShot")

    change_border(test_widget, BorderColors.BLUE, duration=5)

    mock_timer.assert_called_once_with(5000, mocker.ANY)

    args = mock_timer.call_args[0]
    timeout_callback = args[1]
    timeout_callback()

    assert "border: 2px solid blue" not in test_widget.styleSheet()


def test_zero_duration(test_widget):
    change_border(test_widget, BorderColors.GREEN, duration=0)

    assert "border: 2px solid green" in test_widget.styleSheet()


def test_no_duration(test_widget):
    change_border(test_widget, BorderColors.CYAN, duration=None)

    assert "border: 2px solid cyan" in test_widget.styleSheet()


def test_input_control_duration(test_widget, mocker):

    mock_timer = mocker.patch("PySide6.QtCore.QTimer.singleShot")
    input_control(test_widget, duration=2)
    args = mock_timer.call_args[0]
    timeout_callback = args[1]
    timeout_callback()
    assert (
        _get_widget_style(test_widget, BorderColors.RED) not in test_widget.styleSheet()
    )
