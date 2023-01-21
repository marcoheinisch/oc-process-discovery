import datetime

from dash import Dash, dcc, html
from dash_extensions.enrich import Output, Input, State
from dms.dms import DataManagementSystem
from app import app

import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# https://dash.plotly.com/dash-core-components/markdown


# load markdown file and display it in the app
markdown_content = open('README.md', 'r').read()

chapter_title= "Setup"
pattern = f"(^# {chapter_title}\n.+)(.*\n)*"
match = re.search(pattern, markdown_content, re.MULTILINE)
if match:
    pass
    #markdown_content = markdown_content.replace(match.group(1),"")

layout = html.Div(dcc.Markdown(markdown_content, dangerously_allow_html = True))


app = Dash(__name__, external_stylesheets=external_stylesheets)