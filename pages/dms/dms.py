import datetime
from dash import dash, dcc, html
from dash.dependencies import Input, Output, State
from dms.dms import DataManagementSystem
from app import app



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#start_time_str = dcc.Input(id="start-time", type="text", placeholder="Start time (hh:mm:ss)")
#end_time_str = dcc.Input(id="end-time", type="text", placeholder="End time (hh:mm:ss)")




# Layout for the file upload component
layout = html.Div([
    # Header
    html.H1("Dataset Management"),
    html.Hr(),
    
    # Extract from SAP button
    html.Div([
        html.Button('Extract from SAP', id='btn-extract', n_clicks=0),
        html.Div(id='container-feedback-text')
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    
    # File upload component
    html.Div([
        dcc.Upload(
            id='upload-jsonocel',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '15%',
                'height': '40px',
                'lineHeight': '40px',
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
    ], style={'padding': '10px'}),
    
    # Data management component
    html.Div([
        html.H6("View and delete files"),
        html.Div(
             html.Div([
            html.Div(html.B("Uploaded Files")),
            dcc.Checklist(id='uploaded-files-checklist', options=[])
        ], style={'width': '25%', 'display': 'inline-block'}),
        style={'color': 'grey', 'height': '300px', 'width': '300%', 'display': 'flex', 'justify-content': 'left'}),
        html.Div([
            html.Div([
                html.Div(html.B("Objects"), style={'width': '25%', 'display': 'inline-block'}),
                dcc.Checklist(
                    options=[
                        {'label': 'Option 1', 'value': 'option-1'},
                        {'label': 'Option 2', 'value': 'option-2'},
                        {'label': 'Option 3', 'value': 'option-3'},
                        ],
                        value=['option-1', 'option-3'],
                        labelStyle={'display': 'block'}
                    ),
                ], style={'width': '25%', 'display': 'inline-block'}),
                html.Div([
                    html.Div(html.B("Activities"), style={'width': '25%', 'display': 'inline-block'}),
                    dcc.Checklist(
                        options=[
                            {'label': 'Option A', 'value': 'option-a'},
                            {'label': 'Option B', 'value': 'option-b'},
                            {'label': 'Option C', 'value': 'option-c'}
                        ],
                        value=['option-a', 'option-c'],
                        labelStyle={'display': 'block'}
                    ),
                ], style={'width': '25%', 'display': 'inline-block'}),

            html.Hr(),

                html.Div([
                    html.B("Timestamp"),
                    dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    
                    )],
        )
                
            ])
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}),
    ])


# Callback function to store the contents of the uploaded file
@app.callback(Output('output-jsonocel-upload', 'children'),
              [Input('upload-jsonocel', 'contents')],
              [State('upload-jsonocel', 'filename'),
               State('upload-jsonocel', 'last_modified')])
def parse_contents(contents, filename, date):
    # Store the contents of the uploaded file
    DataManagementSystem.store(contents)
    return html.Div([
        'File {} successfully uploaded'.format(filename)
    ])


def update_output(list_of_contents, list_of_names, list_of_dates):
    # Check if a file was uploaded
    if list_of_contents is not None:
        # Initialize an list called children
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#list of uploaded files
@app.callback(Output('uploaded-files-checklist', 'options'),
              [Input('upload-jsonocel', 'filename')])
def update_checklist_options(filenames):
    if filenames is not None:
        return [{'label': filename, 'value': filename} for filename in filenames]
    return []




if __name__ == '__main__': #only run if this file is called directly
    app.run_server(debug=True) #enables debug mode