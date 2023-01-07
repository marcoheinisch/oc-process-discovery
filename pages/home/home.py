import datetime

from dash import Dash, dcc, html
from dash_extensions.enrich import Output, Input, State
from dms.dms import DataManagementSystem
from app import app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

layout = html.Div(html.P("This is the content of the Home page!"))

app = Dash(__name__, external_stylesheets=external_stylesheets)