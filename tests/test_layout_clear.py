import pytest
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from module.tools.ui.clearLayout import clearLayout


@pytest.fixture(scope="session", autouse=True)
def app():
    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def countWidgetsInLayout(layout):
    """
    Helper function to count the number of widgets within a given layout, including child layouts.
    """
    count = 0
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item.widget():
            count += 1
        elif item.layout():
            count += countWidgetsInLayout(item.layout())
    return count


def test_clearLayout_single_level():
    # QVBoxLayout test scenario with single-level widgets.
    parent_widget = QWidget()
    layout = QVBoxLayout(parent_widget)

    # Add several widgets to the layout.
    labels = [QLabel(f"Label {i}") for i in range(5)]
    for label in labels:
        layout.addWidget(label)

    # Verify widget counts.
    assert layout.count() == 5
    assert countWidgetsInLayout(layout) == 5

    # Layout count should be 0 after clearLayout is called.
    clearLayout(layout)
    assert layout.count() == 0


def test_clearLayout_nested_layouts():
    # Test scenario with nested layouts.
    parent_widget = QWidget()
    main_layout = QVBoxLayout(parent_widget)

    # Add a widget to the main layout.
    main_layout.addWidget(QLabel("Main Label"))

    # Create a new child layout and add widgets to it.
    nested_layout = QHBoxLayout()
    nested_labels = [QLabel(f"Nested Label {i}") for i in range(3)]
    for label in nested_labels:
        nested_layout.addWidget(label)

    # Add child layout to main layout.
    main_layout.addLayout(nested_layout)

    # Total widget count should be 1 (main widget) + 3 (nested widgets) = 4.
    assert countWidgetsInLayout(main_layout) == 4

    # When clearLayout is executed on the main layout, all widgets should be deleted.
    clearLayout(main_layout)
    assert main_layout.count() == 0


def test_clearLayout_empty_layout():
    # Test for an empty layout.
    parent_widget = QWidget()
    layout = QVBoxLayout(parent_widget)

    # Layout is already empty; calling clearLayout should succeed without issues.
    assert layout.count() == 0
    clearLayout(layout)
    assert layout.count() == 0
