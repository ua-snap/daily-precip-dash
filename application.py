# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import numpy as np
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import luts
from gui import layout
from data import fetch_data


app = dash.Dash(__name__)

# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server

# Customize this layout to include Google Analytics
gtag_id = os.getenv("GTAG_ID", default="")
app.index_string = f"""
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
        <meta itemprop="name" content="{luts.title}">
        <meta itemprop="description" content="{luts.description}">
        <meta itemprop="image" content="{luts.preview}">

        <!-- Twitter Card data -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@SNAPandACCAP">
        <meta name="twitter:title" content="{luts.title}">
        <meta name="twitter:description" content="{luts.description}">
        <meta name="twitter:creator" content="@SNAPandACCAP">
        <!-- Twitter summary card with large image must be at least 280x150px -->
        <meta name="twitter:image:src" content="{luts.preview}">

        <!-- Open Graph data -->
        <meta property="og:title" content="{luts.title}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{luts.url}" />
        <meta property="og:image" content="{luts.preview}" />
        <meta property="og:description" content="{luts.description}" />
        <meta property="og:site_name" content="{luts.title}" />

        <link rel="alternate" hreflang="en" href="{luts.url}" />
        <link rel="canonical" href="{luts.url}"/>
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

app.title = luts.title
app.layout = layout



@app.callback(Output("precip-scatter", "figure"), [Input("communities-dropdown", "value")])
def update_tally(community):
    """ Generate precipitation scatter chart """

    std = fetch_data(community)
    return go.Figure(
        data=[
            go.Scatter(
                name="pcpt",
                x=std["doy"],
                y=std["pcpt"],
                mode="markers",
                marker=dict(line_width=1),
            )
        ],
        layout=go.Layout(title="<b>Daily Precipitiation, [date range] (Anchorage)</b>"),
    )


@app.callback(
    Output("precip-bubble", "figure"),
    [Input("communities-dropdown", "value")],
)
def update_tally_zone(community):
    """ Generate large bubble chart of precip info """

    std = fetch_data(community)
    std["bubble_size"] = np.interp(std["pcpt"], (std["pcpt"].min(), std["pcpt"].max()), (0, 50))
    std = std.loc[(std["bubble_size"] > 0)]
    print(std)
    return go.Figure(
        data=[
            go.Scatter(
                x=std["doy"],
                y=std["year"],
                mode="markers+text",
                marker=dict(
                    size=std["bubble_size"]
                )
            ),
        ],
        layout=go.Layout(title="<b>Daily Precipitiation, [date range] (Anchorage)</b>"),
    )


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
