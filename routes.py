import dash_bootstrap_components as dbc
from dash import html
from dash_extensions.enrich import Output, Input, State

from app import app

from utils.constants import home_page_location, dms_page_location, analyse_page_location

from pages.home import home
from pages.dms import dms
from pages.analyse import analyse


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == home_page_location:
        return home.layout
    elif pathname == dms_page_location:
        return dms.layout
    elif pathname == analyse_page_location:
        return analyse.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
