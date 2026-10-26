
from ..entities import Balance, ScatterGraphData


class BalanceGraphData:

    def __init__(self) -> None:

        self.balance:ScatterGraphData = None
        self.estimated:ScatterGraphData = None
        self.size_id:int = None

    def apply_balance_data(self,data:list[Balance]) -> None:
        x: list = []
        balance: list = []
        estimated: list = []
        for i in data:
            x.append(i.transaction_id)
            balance.append(i.value)
            estimated.append(i.estimated)
        self.estimated = ScatterGraphData(x,estimated)
        self.balance = ScatterGraphData(x,balance)
        self.size_id = data[0].size_id if data else None
