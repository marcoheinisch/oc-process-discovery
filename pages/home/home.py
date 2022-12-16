import datetime

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dms.dms import DataManagementSystem
from app import app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#layout = html.Div(html.P("This is the content of the Home page!"))

#app = Dash(__name__, external_stylesheets=external_stylesheets)

layout = html.Div([
    dcc.Upload(
        id='upload-jsonocel',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-jsonocel-upload'),
])

def parse_contents(contents, filename, date):
    DataManagementSystem.store(contents)
    if 'jsonocel' in filename: 
        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            html.H6('File successfully imported.'),
            html.Hr(),
        ])
    else:
        return html.Div(['Please upload a valid .jsonocel file.'])

@app.callback(Output('output-jsonocel-upload', 'children'),
              Input('upload-jsonocel', 'contents'),
              State('upload-jsonocel', 'filename'),
              State('upload-jsonocel', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)