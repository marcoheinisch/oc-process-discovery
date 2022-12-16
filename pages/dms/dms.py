from dash import html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


start_time_str = dcc.Input(id="start-time", type="text", placeholder="Start time (hh:mm:ss)")
end_time_str = dcc.Input(id="end-time", type="text", placeholder="End time (hh:mm:ss)")




layout = html.Div([
    html.H1("Dataset Management"),
    html.Hr(),
    html.Div([
        html.Div([
            html.Button('Extract from SAP', id='btn-extract', n_clicks=0),
            html.Div(id='container-feedback-text')
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.H6("Preview and Filter"),
            html.Div(
                "Preview dataset information and metrics",
            style={'color': 'grey', 'height': '300px', 'display': 'flex', 'justify-content': 'center'}),
            html.Div([
                html.Div([
                    html.Div(html.B("Objects"), style={'width': '25%', 'display': 'inline-block'}),
                    dcc.Checklist(
                        options=[
                            {'label': 'Option 1', 'value': 'option-1'},
                            {'label': 'Option 2', 'value': 'option-2'},
                            {'label': 'Option 3', 'value': 'option-3'}
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

            

                html.Div([
                    html.B("Timestamp"),
                    start_time_str,
                    end_time_str
                ], style={'width': '25%', 'display': 'inline-block'}),

                
            ])
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'})
    ])
])

