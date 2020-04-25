# pylint: disable=C0103
"""
Common shared text strings, formatting defaults and lookup tables.
"""

import os
from datetime import datetime
import pandas as pd
import plotly.io as pio

# Core page components
title = "Alaska Community Daily Precipitation"
url = "http://snap.uaf.edu/tools/demo"
preview = "http://snap.uaf.edu/tools/demo/assets/preview.png"
description = "This app lets you explore historical precipitation for places in Alaska."
gtag_id = os.getenv("GTAG_ID", default="")
index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={gtag_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{gtag_id}');
        </script>
        {{%metas%}}
        <title>{{%title%}}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Schema.org markup for Google+ -->
        <meta itemprop="name" content="{title}">
        <meta itemprop="description" content="{description}">
        <meta itemprop="image" content="{preview}">

        <!-- Twitter Card data -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@SNAPandACCAP">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">
        <meta name="twitter:creator" content="@SNAPandACCAP">
        <!-- Twitter summary card with large image must be at least 280x150px -->
        <meta name="twitter:image:src" content="{preview}">

        <!-- Open Graph data -->
        <meta property="og:title" content="{title}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{url}" />
        <meta property="og:image" content="{preview}" />
        <meta property="og:description" content="{description}" />
        <meta property="og:site_name" content="{title}" />

        <link rel="alternate" hreflang="en" href="{url}" />
        <link rel="canonical" href="{url}"/>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# Other app values
communities = pd.read_csv("data/stations.csv", index_col=False)
precip_types = {"pcpt": "Precipitation", "snow": "Snowfall"}
months = {}
for i in range(1, 13):
    months.update({i: datetime(2020, i, 1).strftime("%B")})

# Plotly format template
plotly_template = pio.templates["simple_white"]
axis_configs = {
    "automargin": True,
    "showgrid": False,
    "showline": False,
    "ticks": "",
    "title": {"standoff": 0},
    "zeroline": False,
    "fixedrange": True,
}
xaxis_config = {**axis_configs, **{"tickformat": "%B"}}
plotly_template.layout.xaxis = xaxis_config
plotly_template.layout.yaxis = axis_configs

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
