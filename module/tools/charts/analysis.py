import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from module.data.manager import AnalysisGraphData

from .tool import fig_to_html


def graphics_fig_create(data: AnalysisGraphData, dark_mode: bool = True) -> list:

    if dark_mode:
        pio.templates.default = "plotly_dark"
    else:
        pio.templates.default = "plotly_white"

    fig_4 = go.Figure(
        data=[
            go.Bar(
                x=data.RR.X,
                y=data.RR.Y,
                marker=dict(
                    color=data.RR.Y,
                    colorscale=px.colors.diverging.Tropic_r,
                    line=dict(color="white", width=0.05),
                ),
                # customdata=list(zip(Transaction_result, Parity, Long_short)),
                # hovertemplate=
                # "Transaction Result: %{customdata[0]}<br>" +
                # "Parity: %{customdata[1]}<br>" +
                #  "Long/Short: %{customdata[2]}<br>" +
                #  "Position size: %{y}<extra></extra>"
            )
        ]
    )
    fig_4.update_layout(
        title="Rr",
        xaxis_title="Transaction id",
        yaxis_title="rr",
    )
    fig_3 = go.Figure(
        data=[
            go.Bar(
                x=data.RESULT.X,
                y=data.RESULT.Y,
                marker=dict(
                    color=data.RESULT.Y,
                    colorscale=px.colors.diverging.BrBG,
                    line=dict(color="white", width=0.1),
                ),
                # customdata=list(zip(Transaction_result, Parity, Long_short, Psize)),
                # hovertemplate=
                # "Transaction Result: %{customdata[0]}<br>" +
                # "Parity: %{customdata[1]}<br>" +
                # "Long/Short: %{customdata[2]}<br>" +
                # "Position size: %{customdata[3]}<extra></extra>"
            )
        ]
    )
    fig_3.update_layout(
        title="Balance Status Resulting from the Transaction",
        xaxis_title="Transaction id",
        yaxis_title="Transaction Result",
    )

    aggrnyl_colors: list[str] = px.colors.sequential.Aggrnyl

    fig_2 = go.Figure(
        data=[
            go.Pie(
                labels=data.DIRECTION_COUNT.NAMES,
                values=data.DIRECTION_COUNT.VALUES,
                marker=dict(
                    colors=aggrnyl_colors[: len(data.DIRECTION_COUNT.NAMES)],
                    line=dict(color="#ffffff", width=0.3),
                ),
                hoverinfo="label+percent",
            )
        ]
    )
    fig_2.update_layout(
        title="Direction",
    )

    rdBu_colors: list[str] = px.colors.sequential.RdBu

    fig_1 = go.Figure(
        data=[
            go.Pie(
                labels=data.STATE_COUNT.NAMES,
                values=data.STATE_COUNT.VALUES,
                marker=dict(
                    colors=rdBu_colors[: len(data.STATE_COUNT.NAMES)],
                    line=dict(color="#ffffff", width=0.3),
                ),
                hoverinfo="label+percent",
            )
        ]
    )
    fig_1.update_layout(
        title="State",
    )

    blues_r: list[str] = px.colors.sequential.Blues_r

    fig_0 = go.Figure(
        data=[
            go.Pie(
                labels=data.STRATEGY_COUNT.NAMES,
                values=data.STRATEGY_COUNT.VALUES,
                marker=dict(
                    colors=blues_r[: len(data.STRATEGY_COUNT.NAMES)],
                    line=dict(color="#ffffff", width=0.3),
                ),
                hoverinfo="label+percent",
            )
        ]
    )
    fig_0.update_layout(
        title="Strategy",
    )


    bupu: list[str] = px.colors.sequential.BuPu

    fig_5 = go.Figure(
        data=[
            go.Pie(
                labels=data.PLATFORM_COUNT.NAMES,
                values=data.PLATFORM_COUNT.VALUES,
                marker=dict(
                    colors=bupu[: len(data.PLATFORM_COUNT.NAMES)],
                    line=dict(color="#ffffff", width=0.3),
                ),
                hoverinfo="label+percent",
            )
        ]
    )
    fig_5.update_layout(
        title="Platform",
    )

    return [fig_0, fig_1, fig_2, fig_3, fig_4, fig_5]

def analysis_graphics_create(data: AnalysisGraphData, file_path, dark_mode: bool = True):

    if dark_mode:
        tema = '"dark-mode"'
    else:
        tema = '"light-mode"'
    fig_list: list = graphics_fig_create(data, dark_mode)
    html_list: list[str] = fig_to_html(fig_list)

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
        .plot2 {{
            position: static;
            width: 49.5%;

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
    <div class="container">
        <div class="plot2">{html_list[2]}</div>
        <div class="plot2">{html_list[1]}</div>
    </div>
    <div class="container">
        <div class="plot2">{html_list[0]}</div>
        <div class="plot2">{html_list[5]}</div>
    </div>
    <div class="container">
        <div class="plot">{html_list[3]}</div>
    </div>
    <div class="container">
        <div  class="plot">{html_list[4]}</div>
    </div>

</body>
</html>
"""

    with open(file_path, encoding="utf-8", mode="w") as f:
        f.write(html_page)
