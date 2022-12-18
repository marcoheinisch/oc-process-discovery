
from dash.dependencies import Input, Output
from dash import html, ctx
import time

from app import app
from extraction.extraction import extract_ocel


@app.callback(
    prevent_initial_call=True,
    output=Output("paragraph_id", "children"),
    inputs=Input("button_id", "n_clicks"),
    background=True,
    running=[
        (Output("button_id", "children"), "...", "Extract from SAP"),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
)
def update_clicks(n_clicks):
    msg = ""
    msg = extract_ocel()
    return [msg]
