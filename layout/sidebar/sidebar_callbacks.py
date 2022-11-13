from dash.dependencies import Input, Output, State

from app import app


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("pm-sidebar", "className"),
    [Input("pm-sidebar-toggle", "n_clicks")],
    [State("pm-sidebar", "className")],
)
def pm_toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""

@app.callback(
    Output("pm-collapse", "is_open"),
    [Input("pm-navbar-toggle", "n_clicks")],
    [State("pm-collapse", "is_open")],
)
def pm_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open