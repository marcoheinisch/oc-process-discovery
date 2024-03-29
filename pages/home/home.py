import datetime

from dash import Dash, dcc, html
from dash_extensions.enrich import Output, Input, State
from dms.dms import DataManagementSystem
from app import app

import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# https://dash.plotly.com/dash-core-components/markdown

def get_redme_markdown():
    markdown_content = open('README.md', 'r').read()
    from_chapter= "# Quick setup"
    to_chapter = "# Usage"
       
    markdown_content = markdown_content.replace(f"""
- [Quick setup](#quick-setup)
  - [Python setup](#python-setup)
  - [Docker setup](#docker-setup)""", "")
    

    markdown_content = markdown_content.replace(
        f"""(#further-information)""",
        f"""(#further-information)
- [Quick setup](#quick-setup)
  - [Python setup](#python-setup)
  - [Docker setup](#docker-setup)""")

    
    match = re.search(
        f"({from_chapter}.*?)({to_chapter})", 
        markdown_content, 
        re.DOTALL)
    if match:
        text = match.group(1)
        markdown_content = markdown_content.replace(text,"") + "\n" + text
    return markdown_content

markdown_content = get_redme_markdown()

layout = html.Div([
    html.H1("Documentation"),
    html.Hr(),
    dcc.Markdown(
        markdown_content, 
        dedent = False,
        dangerously_allow_html = True,
        id = 'markdown-content',
        style = {'max-width': ' 50em'}
    )])


#app = Dash(__name__, external_stylesheets=external_stylesheets)


