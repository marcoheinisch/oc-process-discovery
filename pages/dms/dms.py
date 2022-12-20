from dash import html
from filtering.filtering import *

layout = html.Div(
    [
    html.H1("Dataset Management"),
    html.Hr(),
    html.Button('Extract from SAP', id='btn-extract', n_clicks=0),
    html.Div(id='container-feedback-text')
] + filtering_panel
)

