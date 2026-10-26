from typing import Protocol


class AnalysisProtokol(Protocol):

    def graph_display(self) -> None: ...

    def garph_display(self) -> None: ...

    def draw_graph(self) -> None: ...
