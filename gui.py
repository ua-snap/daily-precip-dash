# pylint: disable=C0103,C0301
"""
GUI for app
"""

import os
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
import luts
import data

# For hosting
path_prefix = os.getenv("REQUESTS_PATHNAME_PREFIX") or "/"

# Used to make the chart exports nice
fig_download_configs = dict(
    filename="Daily_Precipitation", width="1000", height="650", scale=2
)
fig_configs = dict(
    displayModeBar=True,
    showSendToCloud=False,
    toImageButtonOptions=fig_download_configs,
    modeBarButtonsToRemove=[
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "hoverClosestPie",
        "hoverClosest3d",
        "hoverClosestGl2d",
        "hoverClosestGeo",
        "toggleHover",
        "toggleSpikelines",
    ],
    displaylogo=False,
)


# Helper functions
def wrap_in_section(content, section_classes="", container_classes="", div_classes=""):
    """
    Helper function to wrap sections.
    Accepts an array of children which will be assigned within
    this structure:
    <section class="section">
        <div class="container">
            <div>[children]...
    """
    return html.Section(
        className="section " + section_classes,
        children=[
            html.Div(
                className="container " + container_classes,
                children=[html.Div(className=div_classes, children=content)],
            )
        ],
    )


header = ddsih.DangerouslySetInnerHTML(
    f"""
<div class="container">
<nav class="navbar" role="navigation" aria-label="main navigation">

  <div class="navbar-brand">
    <a class="navbar-item" href="https://www.snap.uaf.edu">
      <img src="{path_prefix}assets/SNAP_acronym_color_square.svg">
    </a>

    <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div class="navbar-menu">

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-primary">
            <strong>Feedback</strong>
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</div>
"""
)

communities_dropdown_field = html.Div(
    className="field dropdown-selector",
    children=[
        html.Label("Choose a location", className="label"),
        html.Div(
            className="control",
            children=[
                dcc.Dropdown(
                    id="communities-dropdown",
                    options=[
                        {"label": row["name"], "value": row["stid"]}
                        for index, row in luts.communities.iterrows()
                    ],
                    value="26411",  # Fairbanks
                )
            ],
        ),
    ],
)

about = wrap_in_section(
    [
        ddsih.DangerouslySetInnerHTML(
            f"""
<h1 class="title is-3">{luts.title}</h1>
<p>These charts show daily precipitation records for Alaska weather stations.</p>
<p class="camera-icon">Click the <span>
<svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg>
</span> icon in the upper&ndash;right of each chart to download it.</p>
<p>Data provided by the the <a href="http://www.rcc-acis.org">Applied Climate Information System (ACIS)</a>.</p>
<p>Get started by choosing a community.</p>
            """
        ),
        communities_dropdown_field
    ],
    div_classes="content is-size-5",
)




# Daily Precip as a scatterplot + mean line
scatter_graph = wrap_in_section(
    [
        html.H3("Daily precipitation", className="title is-4"),
        html.P(
            """
Placeholder
    """,
            className="content is-size-5",
        ),
        dcc.Graph(id="precip-scatter", config=fig_configs),
    ],
    section_classes="graph",
)

# Daily precip as a daily bubble chart
bubble_graph = wrap_in_section(
    [
        html.H3("Daily precipitation TBD Title What", className="title is-4"),
        html.P(
            """
TBD Placeholder
""",
            className="content is-size-5",
        ),
        html.Div(
            className="graph", children=[dcc.Graph(id="precip-bubble", config=fig_configs)]
        ),
    ],
    section_classes="graph",
)


footer = html.Footer(
    className="footer has-text-centered",
    children=[
        html.Div(
            children=[
                html.A(
                    href="https://snap.uaf.edu",
                    className="snap",
                    children=[html.Img(src=path_prefix + "assets/SNAP_color_all.svg")],
                ),
                html.A(
                    href="https://uaf.edu/uaf/",
                    children=[html.Img(src=path_prefix + "assets/UAF.svg")],
                ),
            ]
        ),
        ddsih.DangerouslySetInnerHTML(
            """
<p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.
<br><a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
            """
        ),
    ],
)

layout = html.Div(children=[header, about, scatter_graph, bubble_graph, footer])
