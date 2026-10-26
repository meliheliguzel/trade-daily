import os
from unittest.mock import MagicMock, patch

from module.data.manager import AnalysisGraphData
from module.tools.charts.analysis import analysis_graphics_create, graphics_fig_create
from windows.main.analysis import Analysis


def test_graphics_fig_create():
    data = AnalysisGraphData()
    data.apply_direction_count([(0, 5), (1, 10)])
    data.apply_state_count([(0, 2), (1, 8)], [(5,)])
    data.apply_strategy_count([("Trend", 7)])
    data.apply_platform_count([("Binance", 12)])
    data.apply_result([(1, 100), (2, -50)])
    data.apply_rr([(1, 2.0), (2, 1.5)])

    figs = graphics_fig_create(data)
    assert len(figs) == 6


def test_analysis_graphics_create(tmp_path):
    data = AnalysisGraphData()
    data.apply_direction_count([(0, 5), (1, 10)])
    data.apply_state_count([(0, 2), (1, 8)], [(5,)])
    data.apply_strategy_count([("Trend", 7)])
    data.apply_platform_count([("Binance", 12)])
    data.apply_result([(1, 100), (2, -50)])
    data.apply_rr([(1, 2.0), (2, 1.5)])

    out_file = str(tmp_path / "analysis_graph.html")
    analysis_graphics_create(data, out_file)

    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


@patch("windows.main.analysis.clearLayout")
@patch("windows.main.analysis.QWebEngineView")
def test_analysis_init_draws_graph_if_missing(mock_web_view, mock_clear, tmp_path):
    new_file = tmp_path / "analysis_graph.html"

    mock_base = MagicMock()
    mock_base._user_loc.ANALYSIS_GRAPH = str(new_file)
    mock_base._data_base.select.return_value = [(0,)]

    analysis = Analysis(mock_base)

    assert not new_file.is_file()
    analysis._thread_work.stop()


@patch("windows.main.analysis.clearLayout")
@patch("windows.main.analysis.QWebEngineView")
def test_analysis_draw_graph_no_transactions(mock_web_view, mock_clear, tmp_path):
    graph_file = tmp_path / "analysis_graph.html"
    graph_file.write_text("dummy")

    mock_base = MagicMock()
    mock_base._user_loc.ANALYSIS_GRAPH = str(graph_file)
    mock_base._data_base.select.return_value = [(0,)]

    analysis = Analysis(mock_base)
    analysis.draw_graph()

    assert not graph_file.exists()
    mock_base._status_bar_message.show_warning_message.assert_called()
    analysis._thread_work.stop()


@patch("windows.main.analysis.clearLayout")
@patch("windows.main.analysis.QWebEngineView")
def test_analysis_draw_graph_with_transactions(mock_web_view, mock_clear, tmp_path):
    graph_file = tmp_path / "analysis_graph.html"
    graph_file.write_text("existing content")

    mock_base = MagicMock()
    mock_base._user_loc.ANALYSIS_GRAPH = str(graph_file)
    mock_base._data_base.select.side_effect = [
        [(5,)],        # count
        [(0, 2), (1, 3)],  # long_short
        [(1,)],        # open
        [(0, 1), (1, 3)],  # tp_sl
        [("S1", 4)],   # strategy
        [(1, 50)],     # result
        [(1, 2.0)],    # rr
        [("P1", 5)],   # platform
    ]

    analysis = Analysis(mock_base)
    with patch.object(analysis._thread_work, "add_work") as mock_add_work:
        analysis.draw_graph()
        mock_add_work.assert_called_once()
        args = mock_add_work.call_args[0]
        assert args[0] == analysis_graphics_create
        assert args[1][1] == str(graph_file)
    analysis._thread_work.stop()
