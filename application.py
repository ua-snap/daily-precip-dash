# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import numpy as np
from scipy.interpolate import UnivariateSpline
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
app.index_string = luts.index_string
app.title = luts.title
app.layout = layout


def get_title_components(years, community, precip_type):
    year_min = str(years.min())
    year_max = str(years.max())
    community_name = str(
        luts.communities.loc[luts.communities["stid"] == int(community)]["name"].values[
            0
        ]
    )
    precip_name = luts.precip_types[precip_type]
    return (year_min, year_max, community_name, precip_name)


@app.callback(
    Output("precip-scatter", "figure"),
    [Input("communities-dropdown", "value"), Input("precip_type", "value")],
)
def update_scatter(community, precip_type):
    """ Generate precipitation scatter chart """

    std = fetch_data(community)

    # Daily mean
    daily_mean = (
        std.drop(columns=["month", "year"])
        .groupby(["unified_year"])
        .mean()
        .round(4)
        .reset_index()
    )

    (year_min, year_max, community_name, precip_name) = get_title_components(
        std["year"], community, precip_type
    )

    title = (
        "Average Daily "
        + precip_name
        + ", "
        + community_name
        + ", "
        + year_min
        + "-"
        + year_max
    )

    return go.Figure(
        data=[
            go.Scatter(
                x=daily_mean["unified_year"], y=daily_mean[precip_type], mode="markers"
            )
        ],
        layout=go.Layout(
            template=luts.plotly_template,
            title=dict(text=title),
            yaxis=dict(title=precip_name + " (in)"),
        ),
    )


@app.callback(
    Output("precip-box", "figure"),
    [Input("communities-dropdown", "value"), Input("precip_type", "value")],
)
def update_boxes(community, precip_type):
    """ Generate precipitation scatter chart """

    std = fetch_data(community)

    # TODO can this be made to show year/month on hover
    # for outliers??
    # Daily mean
    monthly_daily_means = (
        std.drop(columns=["year"])
        .groupby(["month", "unified_year"])
        .mean()
        .round(4)
        .reset_index()
    )

    (year_min, year_max, community_name, precip_name) = get_title_components(
        std["year"], community, precip_type
    )

    title = (
        "Average Daily "
        + precip_name
        + " Per Month, "
        + community_name
        + ", "
        + year_min
        + "-"
        + year_max
    )

    return go.Figure(
        data=[
            go.Box(
                name=precip_type,
                x=monthly_daily_means["month"],
                y=monthly_daily_means[precip_type],
            )
        ],
        layout=go.Layout(
            template=luts.plotly_template,
            title=dict(text=title),
            xaxis=dict(
                tickvals=list(luts.months.keys()), ticktext=list(luts.months.values())
            ),
        ),
    )


@app.callback(
    Output("precip-bubble", "figure"),
    [Input("communities-dropdown", "value"), Input("precip_type", "value")],
)
def update_bubble(community, precip_type):
    """ Generate large bubble chart of precip info """

    std = fetch_data(community)

    # Smaller than this isn't visible or meaningful
    # to display here.
    std = std.loc[std[precip_type] > 0.1]

    s = std[precip_type]  # temp assign for clearer line below
    std = std.assign(bubble_size=np.interp(s, (s.min(), s.max()), (3, 75)))

    (year_min, year_max, community_name, precip_name) = get_title_components(
        std["year"], community, precip_type
    )

    title = (
        "Daily "
        + precip_name
        + ", "
        + community_name
        + ", "
        + year_min
        + "-"
        + year_max
    )

    return go.Figure(
        data=[
            go.Scatter(
                x=std["unified_year"],
                y=std["year"],
                mode="markers",
                marker=dict(size=std["bubble_size"], line=dict(width=0)),
                customdata=std[precip_type],
                hovertemplate="%{x}, %{y}: %{customdata} inches<extra></extra>",
            )
        ],
        layout=go.Layout(
            template=luts.plotly_template,
            title=title,
            yaxis=dict(
                showgrid=True,
                tickvals=(list(range(std["year"].min(), std["year"].max() + 1))),
            ),
            margin=dict(t=25, b=25),
            height=1600,
        ),
    )


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
