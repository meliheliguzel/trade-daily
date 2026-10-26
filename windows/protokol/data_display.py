from typing import Protocol

from module.data.entities import TransactionFullData


class DataDisplayProtokol(Protocol):

    def reload(self) -> None: ...

    def selected_data(self) -> TransactionFullData: ...
