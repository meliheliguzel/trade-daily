from typing import LiteralString

import plotly.graph_objects as go
import plotly.io as pio

from module.data.manager import BalanceGraphData

from .tool import fig_to_html


def graphics_fig_create(
    data: list[BalanceGraphData], dark_mode: bool = True
) -> list[go.Figure]:

    if not data:
        return []

    if dark_mode:
        pio.templates.default = "plotly_dark"
    else:
        pio.templates.default = "plotly_white"

    result: list = []

    for i in data:
        if not i or not i.balance or len(i.balance.X) == 0:
            continue

        fig: go.Figure = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=i.estimated.X,
                y=i.estimated.Y,
                mode="lines+markers",
                name="Estimated Balance",
                line=dict(color="magenta", width=2),
                marker=dict(color="magenta", size=8),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=i.balance.X,
                y=i.balance.Y,
                mode="lines+markers",
                name="Current Balance",
                line=dict(color="#00CED1", width=2),
                marker=dict(color="#00CED1", size=8),
            )
        )
        #fig.update_yaxes(rangemode="tozero")
        fig.update_layout(
            title=f"Balance Status {i.size_id}",
            xaxis_title="Transaction index",
            yaxis_title="Balance",
        )
        result.append(fig)
    return result


def balance_graphics_create(
    data: list[BalanceGraphData], file_path: str, dark_mode: bool = True
) -> None:

    if not data:
        return

    if dark_mode:
        tema = '"dark-mode"'
    else:
        tema = '"light-mode"'
    fig_list: list = graphics_fig_create(data, dark_mode)
    if not fig_list:
        return
    html_list: list[str] = fig_to_html(fig_list)
    result: list[LiteralString] = []
    for i in html_list:
        result.append(
            f"""
    <div class="container">
        <div class="plot">{i}</div>
    </div>"""
        )
    html_page: str = f"""
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .container {{
            display: flex;
        }}
        .plot {{
            position: static;
            width: 99%;
        }}

        .dark-mode{{
            background-color: black;
            color: white;
        }}
         .light-mode {{
            background-color: white;
            color: black;
        }}
    </style>
</head>
<body class={tema}>

    {"\n".join(result)}

</body>
</html>
"""
    with open(file_path, encoding="utf-8", mode="w") as f:
        f.write(html_page)
