from dash import html


layout = html.Div([
    html.H1("Dataset Management"),
    html.Hr(),
    html.Button('Extract from SAP', id='btn-extract', n_clicks=0),
    html.Div(id='container-feedback-text')
])