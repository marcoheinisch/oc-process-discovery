import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

from pages.analyse.analyse_data import dataframe

from components.table import make_dash_table

from layout.processMining.sidebar import sidebar as pm_sidebar


controls = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in dataframe().columns
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in dataframe().columns
                    ],
                    value="sepal width (cm)",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

container = dbc.Container(
    [
        html.H1("Process Mining"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=6),
            ],
            align="center",
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col(make_dash_table(dataframe()), width={"size": 8, "offset": 3}),
            align="center",
        )
    ],
    fluid=True,
)

pm_page_content = html.Div(
    container,
    id="pm-page-content",
)

layout = html.Div([dcc.Location(id="pm-content"), pm_page_content, pm_sidebar])