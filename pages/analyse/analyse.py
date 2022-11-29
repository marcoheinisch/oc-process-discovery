import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash_interactive_graphviz import DashInteractiveGraphviz as dig

from layout.processMining.sidebar import sidebar as pm_sidebar

container = dbc.Container(
    [
        html.Div(
            [
                dig(
                    id="process-model",
                )
            ],
        )
    ],
    fluid="True",
    id="pm-container",
)

pm_page_content = html.Div(
    container,
    id="pm-page-content",
    style={
        "display": "grid",
        "grid-template-columns": "repeat(auto-fill, 300px)",
    }
)

layout = html.Div([
    html.H1("Process Mining"),
    html.Hr(),
    pm_page_content,
    pm_sidebar
])