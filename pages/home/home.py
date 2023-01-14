import datetime

from dash import Dash, dcc, html
from dash_extensions.enrich import Output, Input, State
from dms.dms import DataManagementSystem
from app import app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# https://dash.plotly.com/dash-core-components/markdown


# load markdown file and display it in the app
markdown_content = open('README.md', 'r').read()
layout = html.Div(dcc.Markdown(markdown_content))


app = Dash(__name__, external_stylesheets=external_stylesheets)