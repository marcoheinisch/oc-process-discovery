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
                html.Span(
                    "What do I see here?",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),
                dbc.Tooltip(
                    html.P("In these Process Graphs you can see the process flow of SAP documents, manly extracted from VBFA, CDHDR, BSAD, VBAK"),
                    target="tooltip-target",
                ),
            ]
        ),
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