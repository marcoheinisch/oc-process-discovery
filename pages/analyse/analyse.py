import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash_interactive_graphviz import DashInteractiveGraphviz as dig

from layout.processMining.sidebar import sidebar as pm_sidebar


pm_page_content = html.Div([
        html.H1("Process Analysis"),
        html.Hr(),
        html.Div(
                    [
                        dig(
                            id="process-model",
                        )
                    ]
                )
    ],
    id="pm-page-content",    
)

layout = html.Div([
    pm_page_content,
    pm_sidebar
])