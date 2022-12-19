import dash
import dash_bootstrap_components as dbc

from flask_caching import Cache

from dms.dms import DataManagementSystem
from utils.external_assets import FONT_AWSOME, CUSTOM_STYLE
from layout.layout import layout

import flask


server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        FONT_AWSOME,
        CUSTOM_STYLE
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

log_management = DataManagementSystem()

app.layout = layout

server = app.server