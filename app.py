import dash
import dash_bootstrap_components as dbc
import diskcache
from flask_caching import Cache
from dash import DiskcacheManager

from dms.dms import DataManagementSystem
from utils.external_assets import FONT_AWSOME, CUSTOM_STYLE
from layout.layout import layout
from uuid import uuid4

import flask


server = flask.Flask(__name__) # define flask app.server

callback_cache = diskcache.Cache("./cache-directory/callback_cache")
background_callback_manager = DiskcacheManager(
    callback_cache, cache_by=[lambda: uuid4()], expire=60
)

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    background_callback_manager=background_callback_manager,
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
log_management.register("example-sap.jsonocel", "data/uploads/example-sap.jsonocel")
log_management.select("example-sap.jsonocel")

app.layout = layout

server = app.server