from dash import html
from dash import dcc

from layout.sidebar.sidebar import sidebar


content = html.Div(id="page-content")

layout = html.Div([dcc.Location(id="url"), sidebar, content])