from module.data.entities import BarGraphData, PieGraphData, ScatterGraphData
from module.data.entities.balance import Balance
from module.data.manager.analysis import AnalysisGraphData
from module.data.manager.balance_graph import BalanceGraphData


def test_analysis_graph_data_apply_state_count():
    data_manager = AnalysisGraphData()
    # tp_sl: list of tuples (state_index, count)
    tp_sl = [(0, 5), (1, 10)]  # Let's say state 0 has 5, state 1 has 10
    open_data = [(3,)]  # 3 open transactions

    data_manager.apply_state_count(tp_sl, open_data)

    assert isinstance(data_manager.STATE_COUNT, PieGraphData)
    assert data_manager.STATE_COUNT.VALUES == [5, 10, 3]
    assert len(data_manager.STATE_COUNT.NAMES) == 3


def test_analysis_graph_data_apply_direction_count():
    data_manager = AnalysisGraphData()
    short_long = [(0, 15), (1, 20)]

    data_manager.apply_direction_count(short_long)

    assert isinstance(data_manager.DIRECTION_COUNT, PieGraphData)
    assert data_manager.DIRECTION_COUNT.VALUES == [15, 20]
    assert len(data_manager.DIRECTION_COUNT.NAMES) == 2


def test_analysis_graph_data_apply_strategy_count():
    data_manager = AnalysisGraphData()
    strategy = [("Breakout", 8), ("MeanReversion", 12)]

    data_manager.apply_strategy_count(strategy)

    assert isinstance(data_manager.STRATEGY_COUNT, PieGraphData)
    assert data_manager.STRATEGY_COUNT.VALUES == [8, 12]
    assert data_manager.STRATEGY_COUNT.NAMES == ["Breakout", "MeanReversion"]


def test_analysis_graph_data_apply_platform_count():
    data_manager = AnalysisGraphData()
    platform = [("Binance", 14), ("OKX", 6)]

    data_manager.apply_platform_count(platform)

    assert isinstance(data_manager.PLATFORM_COUNT, PieGraphData)
    assert data_manager.PLATFORM_COUNT.VALUES == [14, 6]
    assert data_manager.PLATFORM_COUNT.NAMES == ["Binance", "OKX"]


def test_analysis_graph_data_apply_result():
    data_manager = AnalysisGraphData()
    result = [(1, 100), (2, -50), (3, 200)]

    data_manager.apply_result(result)

    assert isinstance(data_manager.RESULT, BarGraphData)
    assert data_manager.RESULT.X == [1, 2, 3]
    assert data_manager.RESULT.Y == [100, -50, 200]


def test_analysis_graph_data_apply_rr():
    data_manager = AnalysisGraphData()
    rr = [(1, 2.5), (2, 1.5)]

    data_manager.apply_rr(rr)

    assert isinstance(data_manager.RR, BarGraphData)
    assert data_manager.RR.X == [1, 2]
    assert data_manager.RR.Y == [2.5, 1.5]


def test_balance_graph_data_apply():
    data_manager = BalanceGraphData()

    # Create dummy Balance entities
    b1 = Balance(1, 101, 10, 1500.0, 1480.0)
    b2 = Balance(2, 102, 10, 1600.0, 1590.0)

    data_manager.apply_balance_data([b1, b2])

    assert isinstance(data_manager.balance, ScatterGraphData)
    assert isinstance(data_manager.estimated, ScatterGraphData)
    assert data_manager.balance.X == [101, 102]
    assert data_manager.balance.Y == [1500.0, 1600.0]
    assert data_manager.estimated.X == [101, 102]
    assert data_manager.estimated.Y == [1480.0, 1590.0]
    assert data_manager.size_id == 10


def test_balance_graph_data_apply_empty():
    data_manager = BalanceGraphData()
    data_manager.apply_balance_data([])

    assert isinstance(data_manager.balance, ScatterGraphData)
    assert isinstance(data_manager.estimated, ScatterGraphData)
    assert data_manager.balance.X == []
    assert data_manager.balance.Y == []
    assert data_manager.estimated.X == []
    assert data_manager.estimated.Y == []
    assert data_manager.size_id is None


def test_analysis_graph_data_apply_state_count_empty_open():
    data_manager = AnalysisGraphData()
    data_manager.apply_state_count([], [])

    assert isinstance(data_manager.STATE_COUNT, PieGraphData)
    assert data_manager.STATE_COUNT.VALUES == [0]
    assert len(data_manager.STATE_COUNT.NAMES) == 1
