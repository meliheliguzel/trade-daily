from config import RecordConfig
from config.query import RecordQuery
from module.data.entities import TransactionUpdateData
from scripts import ExceptState, except_work
from windows.protokol.isection import ISectionProtokol

from .data_control import DataControl
from .get_data import GetData


class DataOperations:

    def __init__(self, section: ISectionProtokol):

        self.__section: ISectionProtokol = section
        self.__data_control = DataControl(section)
        self.__get_data = GetData(section)
        self._base = section._base

    @except_work(ExceptState.CRITICAL)
    def update(self, data: TransactionUpdateData) -> bool:

        if self.__data_control.control():

            transaction_id = data.ORIGINAL_DATA.transaction.primary_key
            self.__update_transaction(transaction_id)
            self.__update_closing(transaction_id)
            self.__update_note(transaction_id)
            self.__update_detail_open(transaction_id)
            self.__update_detail_closing(transaction_id)
            self.__update_image(transaction_id, data)
            self.__update_link(transaction_id, data)
            self.__update_strategy(transaction_id, data)
            return True

        else:
            self.__section._base._status_bar_message.show_warning_message(
                RecordConfig.MISSING_AREA
            )
            return False

    @except_work(ExceptState.CRITICAL)
    def add(self) -> bool:

        if self.__data_control.control():
            t_id = self.__add_transaction()
            self.__add_closing(t_id)
            self.__add_detail_closing(t_id)
            self.__add_detail_open(t_id)
            self.__add_image(t_id)
            self.__add_link(t_id)
            self.__add_note(t_id)
            self.__add_strategy(t_id)
            self.__section._base._status_bar_message.show_success_message(
                f"{t_id} - {RecordConfig.TRANSACTION_ADD_SUCCES_MESSAGE}"
            )
            return True

        else:
            self.__section._base._status_bar_message.show_warning_message(
                RecordConfig.MISSING_AREA
            )
            return False

    def border_reset(self):
        self.__data_control.widget_border_reset()

    @except_work(ExceptState.ERROR)
    def __update_transaction(self, t_id: int):

        data = self.__get_data.transaction_data(t_id)
        self.__section._base._data_base.update(
            RecordQuery.TRANSACTION_UPDATE,
            (
                data.platform_id,
                data.parity_id,
                data.date_of_entry,
                data.long_short,
                data.rr,
                data.size,
                t_id,
            ),
        )

    @except_work(ExceptState.ERROR)
    def __update_closing(self, t_id: int):

        closing = self.__get_data.closing_data(t_id)
        if self.__section._base._data_base.select(RecordQuery.CLOSING_CONTROL, (t_id,))[0][0]:
            if closing:
                self.__section._base._data_base.update(
                    RecordQuery.CLOSING_UPDATE,
                    (
                        closing.date_of_exit,
                        closing.tp_sl,
                        closing.result,
                        t_id,
                    ),
                )
            else:
                self.__section._base._data_base.delete(RecordQuery.CLOSING_DELETE, t_id)
        elif closing:
            self.__add_closing(t_id)

    @except_work(ExceptState.ERROR)
    def __update_note(self, t_id: int):

        note = self.__get_data.note_data(t_id)
        if self.__section._base._data_base.select(RecordQuery.NOTE_CONTROL, (t_id,))[0][0]:
            if note:
                self.__section._base._data_base.update(
                    RecordQuery.NOTE_UPDATE,
                    (
                        note.note_text,
                        t_id,
                    ),
                )
            else:
                self.__section._base._data_base.delete(RecordQuery.NOTE_DELETE, t_id)
        elif note:
            self.__add_note(t_id)

    @except_work(ExceptState.ERROR)
    def __update_detail_open(self, t_id: int):

        detail_open = self.__get_data.detail_open_data(t_id)

        if self.__section._base._data_base.select(
            RecordQuery.DETAIL_OPEN_CONTROL, (t_id,)
        )[0][0]:
            if detail_open:
                self.__section._base._data_base.update(
                    RecordQuery.DETAIL_OPEN_UPDATE,
                    (
                        detail_open.entry_price,
                        detail_open.target_price,
                        detail_open.stop_price,
                        t_id,
                    ),
                )
            else:
                self.__section._base._data_base.delete(
                    RecordQuery.DETAIL_OPEN_DELETE, t_id
                )
        elif detail_open:
            self.__add_detail_open(t_id)

    @except_work(ExceptState.ERROR)
    def __update_detail_closing(self, t_id: int):

        detail_close = self.__get_data.detail_closing_data(t_id)
        if self.__section._base._data_base.select(
            RecordQuery.DETAIL_CLOSING_CONTROL, (t_id,)
        )[0][0]:
            if detail_close:
                self.__section._base._data_base.update(
                    RecordQuery.DETAIL_CLOSING_UPDATE, (detail_close.exit_price, t_id)
                )
            else:
                self.__section._base._data_base.delete(
                    RecordQuery.DETAIL_CLOSING_DELETE, t_id
                )
        elif detail_close:
            self.__add_detail_closing(t_id)

    @except_work(ExceptState.ERROR)
    def __update_image(self, t_id: int, data: TransactionUpdateData):

        self.__add_image(t_id)

        if data.CHART_IMAGE_REMOVE_IDS:
            for i in data.CHART_IMAGE_REMOVE_IDS:
                self.__section._base._data_base.delete(RecordQuery.IMAGE_DELETE_ONE, i)

    @except_work(ExceptState.ERROR)
    def __update_link(self, t_id: int, data: TransactionUpdateData):

        self.__add_link(t_id)

        if data.CHART_LINK_REMOVE_IDS:
            for i in data.CHART_LINK_REMOVE_IDS:
                self.__section._base._data_base.delete(RecordQuery.LINK_DELETE_ONE, i)

    @except_work(ExceptState.ERROR)
    def __update_strategy(self, t_id: int, data: TransactionUpdateData):

        self.__add_strategy(t_id)

        if data.STRATEGY_REMOVE_IDS:
            for i in data.STRATEGY_REMOVE_IDS:
                self.__section._base._data_base.delete(
                    RecordQuery.STRATEGY_DELETE_ONE, i
                )

    @except_work(ExceptState.ERROR)
    def __add_transaction(self) -> int | None:

        data = self.__get_data.transaction_data()
        return self.__section._base._data_base.insert(
            RecordQuery.TRANSACTION_INSERT,
            (
                data.platform_id,
                data.parity_id,
                data.date_of_entry,
                data.long_short,
                data.rr,
                data.size,
            ),
        )

    @except_work(ExceptState.ERROR)
    def __add_closing(self, t_id: int):

        closing = self.__get_data.closing_data(t_id)
        if closing:
            self.__section._base._data_base.insert(
                RecordQuery.CLOSING_INSERT,
                (
                    closing.transaction_id,
                    closing.date_of_exit,
                    closing.tp_sl,
                    closing.result,
                ),
            )

    @except_work(ExceptState.ERROR)
    def __add_note(self, t_id: int):

        note = self.__get_data.note_data(t_id)
        if note:
            self.__section._base._data_base.insert(
                RecordQuery.NOTE_INSERT, (note.transaction_id, note.note_text)
            )

    @except_work(ExceptState.ERROR)
    def __add_detail_open(self, t_id: int):

        detail_open = self.__get_data.detail_open_data(t_id)
        if detail_open:
            self.__section._base._data_base.insert(
                RecordQuery.DETAIL_OPEN_INSERT,
                (
                    detail_open.transaction_id,
                    detail_open.entry_price,
                    detail_open.target_price,
                    detail_open.stop_price,
                ),
            )

    @except_work(ExceptState.ERROR)
    def __add_detail_closing(self, t_id: int):

        detail_close = self.__get_data.detail_closing_data(t_id)
        if detail_close:
            self.__section._base._data_base.insert(
                RecordQuery.DETAIL_CLOSING_INSERT,
                (detail_close.transaction_id, detail_close.exit_price),
            )

    @except_work(ExceptState.ERROR)
    def __add_image(self, t_id: int):

        images = self.__get_data.image_data(t_id)
        if images:
            for i in images:
                self.__section._base._data_base.insert(
                    RecordQuery.IMAGE_INSERT, (t_id, i.image, i.extension)
                )

    @except_work(ExceptState.ERROR)
    def __add_link(self, t_id: int):

        link = self.__get_data.link_data(t_id)
        if link:
            for i in link:
                self.__section._base._data_base.insert(
                    RecordQuery.LINK_INSERT, (i.transaction_id, i.link)
                )

    @except_work(ExceptState.ERROR)
    def __add_strategy(self, t_id: int):

        strategy = self.__get_data.strategy_data(t_id)
        if strategy:
            for i in strategy:
                self.__section._base._data_base.insert(
                    RecordQuery.STRATEGY_INSERT, (i.transaction_id, i.strategy_id)
                )
