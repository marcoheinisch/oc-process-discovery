import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

from utils.constants import home_page_location, dms_page_location, analyse_page_location

from layout.processMining.apdas import apdas


# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-dark navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="pm-sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
        dbc.Col(
            html.H2(
                "Options",
                className="display-4",
                style={
                    "color": "#f8f9fa",
                    "text-align": "left",
                },
            )
        ),
    ]
)
options = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Label(
                    "Choose your process discovery algorithm:",
                ),
                dcc.Dropdown(
                    id="apda-option",
                    options=[
                        {"label": row[0], "value": row[1]} for row in apdas
                    ],
                    value="AM",
                    clearable=False,
                    optionHeight=80,
                    searchable=True,

                ),
            ],
        ),
    ],
    body=True,
    id="apda-dropdown",
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(
                    style={
                        "border-top": "solid white"
                    },
                    id="pm-hr"
                ),
            ],
            id="pm-blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            options,
            id="pm-collapse",
        ),
    ],
    id="pm-sidebar",
)