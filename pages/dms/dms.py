from datetime import date
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dms.dms import DataManagementSystem
from app import app
import base64


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
                html.A('Upload .jsonocel files')
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
            multiple=True,
            # Only allow files with the .jsonocel extension to be selected
            accept=".jsonocel"

        ),
        html.Div(id='output-jsonocel-upload'),
    ], style={'padding': '10px'}),
    
    # Data management component
    html.Div([
        html.H6("View and delete files"),
        html.Div(
             html.Div([
            html.Div(html.B("Your files")),
            dcc.Checklist(id='uploaded-files-checklist', options=[]),
            # Delete button
            html.Button(id='delete-file-button', children='Delete'),
            # Download button
           html.Button("Download", id="download-button", n_clicks=0),
           dcc.Download(id="download-file")
        ], style={'width': '25%', 'display': 'inline-block'}),
        style={'color': 'grey', 'height': '300px', 'width': '300%', 'display': 'flex', 'justify-content': 'left'}),
        
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}),
    ])
    


# Callback function to store the contents of the uploaded file
@app.callback(Output('output-jsonocel-upload', 'children'),
              [Input('upload-jsonocel', 'contents')],
              [State('upload-jsonocel', 'filename'),
               State('upload-jsonocel', 'last_modified')])
#store the contents of an uploaded file and display a message indicating the file was successfully uploaded
def parse_contents(contents, filename, date): #date is not used yet
    DataManagementSystem.store('filename', contents)
    return html.Div([
        'File {} successfully uploaded'.format(filename)
    ])



#list of uploaded files
@app.callback(Output('uploaded-files-checklist', 'options'),
              [Input('upload-jsonocel', 'filename')],
              [State('uploaded-files-checklist', 'options')])
def update_checklist_options(filenames, existing_options):
    if filenames is not None:
        # Append the filename of the most recently uploaded file to the existing options
        updated_options = existing_options + [{'label': filename, 'value': filename} for filename in filenames]
        return updated_options
    return existing_options


# Download selected files DOES NOT WORK YET
@app.callback(
    [Output("download-file", "data"), Output("download-file", "filename")],
    [Input("download-button", "n_clicks"),
     Input("uploaded-files-checklist", "value")]
)
def download_selected_files(n_clicks, selected_files):
    # Retrieve the data for the selected files from the SingletonClass object
    data = [DataManagementSystem.load(file) for file in selected_files]
    # Encode the data as base64
    data = [base64.b64encode(d).decode('utf-8') for d in data]
    # Return the data and the filename for each selected file as a dictionary
    return [data, selected_files]

#delete selected files
"""@app.callback("""


if __name__ == '__main__': #only run if this file is called directly
    app.run_server(debug=True) #enables debug mode