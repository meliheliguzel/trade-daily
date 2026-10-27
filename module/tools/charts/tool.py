
import plotly.graph_objects as go
import plotly.offline as pyo


def fig_to_html(data:  list[go.Figure]) -> list[str]:

    html_list: list[str] = []

    for i in data:
        title_text = (
            i.layout.title.text
            if hasattr(i.layout, "title") and i.layout.title and getattr(i.layout.title, "text", None)
            else "chart"
        )
        config: dict[str, bool | dict[str, int | str] | list[str]] = {
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "jpeg",  # one of png, svg, jpeg, webp
                "filename": f"{title_text}_image",
                "scale": 1,
            },
            "modeBarButtonsToAdd": [
                "drawline",
                "drawopenpath",
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",
            ],
            "scrollZoom": True,
            "displayModeBar": True,
            "responsive": True,
        }
        html_list.append(pyo.plot(i, output_type="div", include_plotlyjs=True, config=config))

    return html_list
