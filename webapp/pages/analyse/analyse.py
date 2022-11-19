import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

from webapp.pages.analyse.analyse_data import dataframe

from webapp.components.table import make_dash_table


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

layout = dbc.Container(
    [
        html.H1("Analyse"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
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