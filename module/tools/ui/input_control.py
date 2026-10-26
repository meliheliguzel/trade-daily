

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QLineEdit,
    QPlainTextEdit,
    QRadioButton,
    QTextEdit,
    QWidget,
)


class BorderColors:
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    CYAN = "cyan"


def _get_widget_style(widget: QWidget, border_color: str) -> str:
    """Generates CSS style for the widget."""
    name: str = widget.objectName() or widget.__class__.__name__
    selector: str = f"#{name}" if widget.objectName() else name
    return f"{selector} {{ border: 2px solid {border_color}; }}"


def border_reset(widget: QWidget, border_color: str = BorderColors.RED) -> None:
    """Clears a specific border style from the widget."""
    style_to_remove: str = _get_widget_style(widget, border_color)
    current_style: str = widget.styleSheet()

    if style_to_remove in current_style:
        new_style: str = "\n".join([line for line in current_style.splitlines()
                      if style_to_remove not in line])
        widget.setStyleSheet(new_style)


def change_border(
    widget: QWidget, border_color=BorderColors.RED, duration: int | None = 15
) -> None:
    """
    Changes the border of the provided widget to the specified color.
    After 'duration' seconds (default 15 seconds) the style resets.
    """
    style: str = _get_widget_style(widget, border_color)
    current_style = widget.styleSheet()
    widget.setStyleSheet("\n".join([current_style ,style]))

    if duration:
        QTimer.singleShot(duration * 1000, lambda w=widget, c=border_color: border_reset(w, c))


def _validate_qlineedit(widget: QLineEdit) -> bool:
    return bool(widget.text().strip())


def _validate_text_edit(widget: QTextEdit | QPlainTextEdit) -> bool:
    return bool(widget.toPlainText().strip())


def _validate_qcombobox(widget: QComboBox) -> bool:
    if widget.isEditable():
        return bool(widget.currentText().strip())

    if widget.count() == 0 or widget.currentIndex() < 0:
        return False

    return bool(widget.currentText().strip())


def _validate_qgroupbox(widget: QGroupBox) -> bool:
    radios: list[QRadioButton] = widget.findChildren(QRadioButton)
    return any(rb.isChecked() for rb in radios) if radios else True


def _validate_qcheckbox(widget: QCheckBox) -> bool:
    return widget.isChecked()


_VALIDATION_HANDLERS: list[tuple[type, callable]] = [
    (QLineEdit, _validate_qlineedit),
    (QTextEdit, _validate_text_edit),
    (QPlainTextEdit, _validate_text_edit),
    (QComboBox, _validate_qcombobox),
    (QGroupBox, _validate_qgroupbox),
    (QCheckBox, _validate_qcheckbox),
]


def input_control(
    widget_or_widgets: QWidget | list[QWidget],
    border_color: BorderColors = BorderColors.RED,
    duration: int | None = None,
) -> bool:
    """
    Validates widget input.

    Parameters:
      duration: None -> border is permanent, if an integer is provided it resets after duration seconds.
    """
    widgets: (QWidget & tuple) | list[QWidget] = (
        widget_or_widgets
        if isinstance(widget_or_widgets, (list, tuple))
        else [widget_or_widgets]
    )
    all_valid = True

    for widget in widgets:
        value_valid = False

        for widget_type, validator in _VALIDATION_HANDLERS:
            if isinstance(widget, widget_type):
                value_valid = validator(widget)
                break

        if not value_valid:
            all_valid = False
            change_border(widget, border_color, duration)
        else:
            border_reset(widget, border_color)

    return all_valid

