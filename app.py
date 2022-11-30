import dash
import dash_bootstrap_components as dbc
#from dash.long_callback import DiskcacheLongCallbackManager
from flask_caching import Cache

from utils.external_assets import FONT_AWSOME, CUSTOM_STYLE
from layout.layout import layout

import flask


server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=False,
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

#long_callback_manager = DiskcacheLongCallbackManager(cache)

app.layout = layout

server = app.server