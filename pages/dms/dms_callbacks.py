
from dash.dependencies import Input, Output
from dash import html, ctx

from app import app
from extraction.extraction import extract_ocel


@app.callback(
    Output('container-feedback-text', 'children'),
    Input('btn-extract', 'n_clicks')
)
def extract_from_sap(btn1):
    msg = ""
    if 'btn-extract' == ctx.triggered_id:
        msg = extract_ocel()
    return html.Div(msg)