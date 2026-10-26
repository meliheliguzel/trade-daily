from typing import Any

from PySide6.QtWidgets import QComboBox


def comboBox_data_load(comboBox:QComboBox,data:dict[str,Any]|None,new:bool=False):
    comboBox.clear()
    if new:
        comboBox.addItem("New",None)
    for i in data.keys():
        comboBox.addItem(i, data[i])

