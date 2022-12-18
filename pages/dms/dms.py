from dash import html, ctx, dcc
from dash.dependencies import Input, Output
import time

from app import app
from extraction.extraction import extract_ocel


layout = html.Div([
    html.H1("Dataset Management"),
    html.Hr(),
    dcc.Loading(
        id="loading-1",
        children=[
            html.Div([html.P(id="paragraph_id", children=[])]),
        ],
    ),
    html.Button(id="button_id", children="Extract from SAP"),
    html.Button(id="cancel_button_id", children="Stop!"),
])


