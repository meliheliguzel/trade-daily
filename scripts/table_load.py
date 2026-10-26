from module.tools.ui.table import (
    CenterAlignDelegate,
    DailyModel,
    StateInfoModel,
    StateInfoTabelData,
)
from windows.protokol.isection import ISectionProtokol


def daily_table_load(self: ISectionProtokol, data: list, count: int) -> DailyModel:

    table_model = DailyModel(data, count)
    self._base.ui.tableView_daily.setModel(table_model)
    delegate = CenterAlignDelegate(self._base.ui.tableView_daily)
    self._base.ui.tableView_daily.setItemDelegate(delegate)
    self._base.ui.tableView_daily.resizeRowsToContents()

    return table_model


def state_info_table_load(self: ISectionProtokol, data: StateInfoTabelData) -> StateInfoModel:

    table_model = StateInfoModel(data)
    self._base.ui.tableView_daily_state_info.setModel(table_model)
    delegate = CenterAlignDelegate(self._base.ui.tableView_daily_state_info)
    self._base.ui.tableView_daily_state_info.setItemDelegate(delegate)
    self._base.ui.tableView_daily.resizeRowsToContents()

    return table_model

