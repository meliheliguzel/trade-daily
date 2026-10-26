from typing import Protocol


class BalanceRecordProtokol(Protocol):

    def recalculation(self) -> None:
        ...

    def draw_graph(self) -> None:
        ...
