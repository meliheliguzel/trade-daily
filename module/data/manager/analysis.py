
from ..entities import BarGraphData, PieGraphData
from ..entities.transaction import TransactionShowData


class AnalysisGraphData:

    def __init__(self) -> None:
        self.RR: BarGraphData = None
        self.RESULT: BarGraphData = None
        self.STATE_COUNT: PieGraphData = None
        self.DIRECTION_COUNT: PieGraphData = None
        self.STRATEGY_COUNT: PieGraphData = None
        self.PLATFORM_COUNT: PieGraphData = None

    def apply_state_count(self, tp_sl: list[tuple[int, int]], open: list[tuple]) -> None:

        values: list = []
        names: list[str] = []
        for i in tp_sl:
            names.append(TransactionShowData.state[i[0]])
            values.append(i[1])
        names.append(TransactionShowData.OPEN)
        open_val = open[0][0] if open and len(open) > 0 and len(open[0]) > 0 else 0
        values.append(open_val)
        self.STATE_COUNT = PieGraphData(values, names)

    def apply_direction_count(self, short_long: list[tuple[int, int]]) -> None:

        values: list = []
        names: list = []
        for i in short_long:
            names.append(TransactionShowData.DIRECTION[i[0]])
            values.append(i[1])
        self.DIRECTION_COUNT = PieGraphData(values, names)

    def apply_strategy_count(self, strategy: list[tuple[int, int]]) -> None:

        values: list = []
        names: list = []
        for i in strategy:
            names.append(i[0])
            values.append(i[1])
        self.STRATEGY_COUNT = PieGraphData(values, names)

    def apply_platform_count(self, platform: list[tuple[int, int]]) -> None:

        values: list = []
        names: list = []
        for i in platform:
            names.append(i[0])
            values.append(i[1])
        self.PLATFORM_COUNT = PieGraphData(values, names)

    def apply_result(self, result: list[tuple[int, int]]) -> None:

        x: list = []
        y: list = []
        for i in result:
            x.append(i[0])
            y.append(i[1])
        self.RESULT = BarGraphData(x, y)

    def apply_rr(self, rr: list[tuple[int, int]]) -> None:

        x: list = []
        y: list = []
        for i in rr:
            x.append(i[0])
            y.append(i[1])
        self.RR = BarGraphData(x, y)
