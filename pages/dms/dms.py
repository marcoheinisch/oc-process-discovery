import dash
import os

from dash import dash_table
import numpy as np
import pm4py
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, ctx
from dash_extensions.enrich import Output, Input, State
from datetime import date

import dms
from app import log_management
from app import app
from utils.constants import UPLOAD_DIRECTORY
from extraction.extraction import extract_ocel
from filtering.filtering import filtering_panel
import copy
import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#start_time_str = dcc.Input(id="start-time", type="text", placeholder="Start time (hh:mm:ss)")
#end_time_str = dcc.Input(id="end-time", type="text", placeholder="End time (hh:mm:ss)")


# Layout for the file upload component
layout = html.Div([
    # Header
    html.H1("Data Management"),
    html.Hr(),
    
    html.Div([
        # Extract from SAP button
        html.H6("Upload or extract log"),
        dcc.Loading(id='loading-extract', children=[
            html.Div([
                html.Button('Extract from SAP', id='btn-extract', n_clicks=0, style={'width': '70%'}),
                html.Button("Config", id="con_config_button", n_clicks=0, style={'width': '30%'}),
                html.Div(id='container-feedback-text', style={'color': 'gray'})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '10px'}),
        ], type='default'),
        
        # File upload component
        html.Div([
            dcc.Upload(
                id='upload-jsonocel',
                children=html.Div([
                    html.A('Upload .jsonocel files')
                ]),
                style={
                    'width': '100%',
                    'height': '40px',
                    'lineHeight': '40px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
                # Allow multiple files to be uploaded
                multiple=True,
                # Only allow files with the .jsonocel extension to be selected
                accept=".jsonocel"
            ),
            html.Div(id='output-jsonocel-upload', style={'width': '100%','color': 'gray'}),
        ], style={'width': '100%', 'padding': '10px'}),
        
        # Data management component
        html.Div([
            html.Hr(style={}),
            html.H6("View and select File for analysis"),
            #html.Div(html.B("Your files")),
            dcc.RadioItems(id='uploaded-files-checklist', options=[], style={'width': '100%'}),
            # Delete button
            html.Button(id='delete-file-button', children='Delete', style={'width': '50%'}, n_clicks=0),
            # Download button
            html.Button("Download", id="download-button", n_clicks=0, style={'width': '50%'}),
            dcc.Download(id="download-file", base64=True),
            html.Button(
                'Clear all',
                id='clear-button',
                n_clicks=0,
                style={
                    'width': '100%',
                },
            ),
        ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        html.Div([
            html.H6("Filter Data"),
        ] + filtering_panel ),

        # Modal for SAP connection configuration
        html.Div([
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("SAP connection configuration")),
                dbc.ModalBody([
                    html.P("1. Select a parameter to be modified and enter its new value below."),
                    dcc.Dropdown(['user', 'passwd', 'ashost', 'saprouter', 'msserv', 'sysid', 'group', 'client', 'lang', 'trace'], 'user', id='param-dropdown'),
                    html.Div(id='dd-output-container', style={'color': 'gray'}),
                    html.Div([
                        dbc.Input(id="input", placeholder="Enter new value.", type="text"),
                        html.P(id="output", style={'color': 'gray'}),
                    ]),
                    html.Button(
                        "Save", id="save", n_clicks=0
                    ),
                    html.Div(id='save-output', style={'color': 'gray'}),
                    html.Hr(style={"margin-top":"0.5rem", "margin-bottom":"0.5rem"}),
                    html.P("2. Select the daterange of the data to be extracted:"),
                    html.Div([
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=date(1995, 8, 5),
                            max_date_allowed=date.today(),
                            start_date=log_management.extraction_config['from_date'],
                            end_date=log_management.extraction_config['to_date'],
                            persistence=False,
                            #display_format='DD.MM.YYYY'
                        ),
                        html.Div(id='output-container-date-picker-range', style={'color': 'gray'})
                    ]),
                    html.Hr(style={"margin-top":"0.5rem", "margin-bottom":"0.5rem"}),
                    dcc.Checklist(id="options_checklist", options=['Use SQLite3 database instead SAP']),
                    html.Div(id='options_checklist_output', style={"display":"none",'color': 'gray'}),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="con_config_modal",
            is_open=False,),
        ])
    # Global dms div
    ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'}),
    html.Div([
            html.H6(
                "Statistics of your event log",
            ),
            html.Label(
                id='log-statistics-label',
                children='Select a log first!'
            ),
            html.Hr(),
            dash_table.DataTable(
                id='log-statistics-table'
            ),
        ],
        style=
            {
            'width': '60%',
            'display': 'inline-block',
            'padding': '10px',
            'float': 'right',
            'margin': '20rm',
        },

    ),

])



@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        log_management.extraction_config['from_date'] = start_date_object
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        log_management.extraction_config['to_date'] = end_date_object
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


# Callback function to store the contents of the uploaded file
@app.callback(Output('output-jsonocel-upload', 'children'),
              Output('uploaded-files-checklist', 'value'),
              [Input('upload-jsonocel', 'contents')],
              [State('upload-jsonocel', 'filename'),
               State('upload-jsonocel', 'last_modified'),
               State('uploaded-files-checklist', 'value')])
#store the contents of an uploaded file(s) and display a message indicating the file(s) was successfully uploaded
def parse_contents(contents, filename, date, selected): #date is not used yet
    if contents is None:
        return "No files uploaded", selected
    for i in range(len(contents)):
        filename[i] = log_management.get_a_unique_filename(filename[i])
        log_management.store(filename[i], contents[i])
    if len(contents) == 1:
        selected = filename[0]
    return html.Div([
        'File {} successfully uploaded'.format(filename)
    ]), selected


# Callback function to mark a file for the analysis
@app.callback(Output('uploaded-files-checklist', 'children'), 
              [Input('uploaded-files-checklist', 'value')])
def select_checklist_options(value):
    log_management.select(value)
    return '  You have selected "{}" for analysis'.format(value)


# Callback function to open the modal
@app.callback(
    Output("con_config_modal", "is_open"),
    [Input("con_config_button", "n_clicks"), Input("close", "n_clicks")],
    [State("con_config_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback to display selected parameter in options_checklist
@app.callback(
    Output('options_checklist_output', 'children'),
    Output('btn-extract', "children"),
    Input('options_checklist', 'value'),
)
def update_config(value):
    selected = value and (len(value) > 0)
    log_management.use_sqlite = selected
    button_value = "Extract from SAP" if not selected else "Extract from SQLite"
    return value, button_value

# Callback to save input given in modal
@app.callback(
    Output('save-output', 'children'),
    Input('save', 'n_clicks'),
    State('param-dropdown', 'value'),
    State("input", "value")
)
def change_sap_config(save_btn, selected_param, new_value):
    msg = "Not saved."
    if "save" == ctx.triggered_id:
        log_management.sap_config[selected_param] = new_value
        msg = f"New value for {selected_param} saved successfully."
    return html.Div(msg)


#list of uploaded files
@app.callback(Output('uploaded-files-checklist', 'options'),
              Input('container-feedback-text', 'children'),
              [Input('output-jsonocel-upload', 'children')],
              [State('uploaded-files-checklist', 'options')])
def update_checklist_options(v, children, existing_options):
    options = log_management.all_upload_keys()
    if options is None:
        options = []
    updated_options =  [{'label': str(filename), 'value': str(filename)} for filename in options]
    return updated_options


# Download selected files DOES NOT WORK YET
"""@app.callback(
    [Output("download-file", "data"), Output("download-file", "filename")],
    [Input("download-button", "n_clicks"),
     Input("uploaded-files-checklist", "value")]
)
def download_selected_files(n_clicks, selected_files):
    # Retrieve the data for the selected files from the SingletonClass object
    data = [log_management.load(file) for file in selected_files]
    # Encode the data as base64
    data = [base64.b64encode(d).decode('utf-8') for d in data]
    # Return the data and the filename for each selected file as a dictionary
    return [data, selected_files]"""
#delete selected files
"""@app.callback("""


@app.callback(
    Output('container-feedback-text', 'children'),
    Input('btn-extract', 'n_clicks')
)
def extract_from_sap(btn1):
    msg = ""
    if 'btn-extract' == ctx.triggered_id and btn1 is not None and btn1 > 0:
        msg = extract_ocel()
    return html.Div(msg)

if __name__ == '__main__': #only run if this file is called directly
    app.run_server(debug=True) #enables debug mode

@app.callback(
    Output("download-file", 'data'),
    Input("download-button", 'n_clicks'),
    State('uploaded-files-checklist', 'value'),
)
def download(button_clicks, filename):
    if button_clicks is None or button_clicks == 0:
        return dash.no_update
    ocel = log_management.get_ocel()
    singleton_instance = dms.dms.SingletonClass()
    key = singleton_instance.selected
    filename = os.path.join(UPLOAD_DIRECTORY, key.rpartition('.jsonocel')[0] + '_downloaded.jsonocel')
    pm4py.write_ocel(ocel, filename)
    return dcc.send_file(filename)

@app.callback(Output('log-statistics-label', 'children'),
    Output('log-statistics-table', 'data'),
    Input('uploaded-files-checklist', 'children'),
    Input('filter-trigger-4', 'n-clicks'),)
def set_statistics(value1, value2):
    ocel = log_management.get_ocel()
    df = ocel.get_extended_table()
    # df.rename(columns=lambda x: re.sub(r'\W+', '_', x), inplace=True)
    df.replace({np.nan: 'N/A'}, inplace=True)
    def flatten_lists(val):
        if isinstance(val, list):
            return ','.join(val)
        return val

    df = df.applymap(flatten_lists)
    columns = [{'name': col, 'id': col} for col in df.columns]
    print(df)
    print(df.to_dict('records')[0])
    message = str(ocel).replace("Please use <THIS>.get_extended_table() to get a dataframe representation of the events related to the objects.", "")
    return message, df.to_dict('records')
