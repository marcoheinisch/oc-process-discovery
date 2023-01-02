from dash.dependencies import Input, Output, State
import copy
import os
import dash
from dash import html, dcc
import math
import re
import pm4py
from pm4py.objects.ocel.obj import OCEL

from app import app
from app import log_management


def get_path():
    return log_management.load_selected()


def get_ocel() -> OCEL:
    return pm4py.read_ocel(get_path())


def get_new_path_name():
    log_paths = log_management.get_filter_steps()
    length = len(log_paths)
    if length == 1:
        return 'test/filtered_ocel.json'
    else:
        return 'test/filtered_ocel{}.json'.format(length - 1)

def save_filtered_ocel(ocel):
    path = get_new_path_name()
    pm4py.write_ocel(ocel, path)
    log_paths = log_management.get_filter_steps()
    log_paths.append(path)


# panel components
filtering_label = html.Label(
    id='filtering-label',
    hidden="hidden",
    children='Filtering has been succesfully applied!'
)


# Filter on Event Attributes
event_attribute_label = html.Label(
    id='event-attribute-label',
    hidden="hidden",
    children='Filtering on Event Attributes has been succesfully applied!'
)

event_attribute_dropdown = dcc.Dropdown(
    id='event-attribute-dropdown',
    options=[{'label': attr, 'value': attr} for attr in get_ocel().events.columns.tolist()],
    value=[],
    multi=True
)

# create checkboxes for selecting elements
event_attribute_checkboxes = html.Div(
    id='event-attribute-checkboxes',
    children=[]
)

# create radio buttons for setting "Positive" flag
event_attribute_positive_radio = dcc.RadioItems(
    id='event-attribute-positive-radio',
    options=[{'label': 'positive', 'value': True}, {'label': 'negative', 'value': False}],
    value=True,  # default value
    labelStyle={'display': 'inline-block'}
)

# Filter on Object Attributes
object_attribute_dropdown = dcc.Dropdown(
    id='object-attribute-dropdown',
    options=[{'label': attr, 'value': attr} for attr in get_ocel().objects.columns.tolist()],
    value=[],
    multi=True
)

# create checkboxes for selecting elements
object_attribute_checkboxes = html.Div(
    id='object-attribute-checkboxes',
    children=[]
)

# create radio buttons for setting "Positive" flag
object_attribute_positive_radio = dcc.RadioItems(
    id='object-attribute-positive-radio',
    options=[{'label': 'positive', 'value': True}, {'label': 'negative', 'value': False}],
    value=True,  # default value
    labelStyle={'display': 'inline-block'}
)


# callbacks
# Filter on Event Attributes callbacks
# define callback for updating element checkboxes
@app.callback(
    Output('event-attribute-checkboxes', 'children'),
    [Input('event-attribute-dropdown', 'value')],
    State('event-attribute-checkboxes', 'children')
)
def update_event_attribute_checkboxes(keys, children):
    selected_values = {}
    for child in children:
        key = child['props']['children'][0]['props']['id'].rsplit('-', 1)[0]
        value = child['props']['children'][0]['props']['value']
        selected_values[key] = value

    checkboxes = []
    for key in keys:
        if key not in selected_values:
            selected_values[key] = []

        checkboxes.append(html.Div(
            children=[
                dcc.Checklist(
                    id=f'{key}-checklist',
                    options=[{'label': element, 'value': element} for element in sorted(set(get_ocel().events[key]))],
                    value=selected_values[key]
                )
            ]
        ))
    return checkboxes


# define callback for updating "Positive" flag
@app.callback(
    Output('event-attribute-positive-flag', 'children'),
    [Input('event-attribute-positive-radio', 'value')]
)
def update_event_attribute_positive_flag(value):
    return value


# Filter on Object Attributes callbacks
# define callback for updating element checkboxes
@app.callback(
    Output('object-attribute-checkboxes', 'children'),
    [Input('object-attribute-dropdown', 'value')],
    State('object-attribute-checkboxes', 'children')
)
def update_object_attribute_checkboxes(keys, children):
    selected_values = {}
    for child in children:
        print(child)
        key = child['props']['children'][0]['props']['id'].rsplit('-', 1)[0]
        value = child['props']['children'][0]['props']['value']
        print(key)
        selected_values[key] = value
        print(value)

    checkboxes = []
    for key in keys:
        s = set(get_ocel().objects[key])
        elements = copy.copy(s)

        def is_real_number(x):
            pattern1 = r'^[+-]?\d*\.?\d+$'
            pattern2 = r'^0+[1-9]\d*\.?\d*$'
            return bool(re.match(pattern1, x)) and not bool(re.match(pattern2, x))

        are_real_numbers = True
        for x in s:
            if not is_real_number(x):
                are_real_numbers = False
                break
        if are_real_numbers:
            elements = sorted(filter(lambda y: not math.isnan(y), s))

        if key not in selected_values:
            selected_values[key] = []

        checkboxes.append(html.Div(
            children=[
                dcc.Checklist(
                    id=f'{key}-checklist',
                    options=[{'label': element, 'value': element} for element in elements],
                    value=selected_values[key]
                )
            ]
        ))
    return checkboxes


# define callback for updating "Positive" flag
@app.callback(
    Output('object-attribute-positive-flag', 'children'),
    [Input('object-attribute-positive-radio', 'value')]
)
def update_object_attribute_positive_flag(value):
    return value


"""# define callback for rollback
@app.callback(
    [
        Output('event-attribute-dropdown', 'value'),
        Output('event-attribute-checkboxes', 'value'),
        Output('event-attribute-positive-radio', 'value'),
        Output('object_attribute_dropdown', 'value'),
        Output('object-attribute-checkboxes', 'value'),
        Output('object-attribute-positive-radio', 'value'),
    ],
    Input('rollback-button', 'n_clicks')
)
def rollback(n_clicks):
    path = get_path()
    # don't do the rollback if no filtering has been done
    if path == original_path:
        return
    # delete current filtered ocel file
    os.remove(get_path())
    del log_paths[len(log_paths) - 1]

    # update the current ocel
    global ocel
    ocel = pm4py.read_ocel(get_path())

    # reset filtering options to default values
    return [], [], True, [], [], True"""


@app.callback(
    Output('filter-trigger-1', 'n-clicks'),
    Input('filter-button', 'n_clicks'),
)
def apply_filtering(button_clicks):
    return button_clicks


@app.callback(
    Output('event-attribute-label', 'hidden'),
    Output('filter-trigger-2', 'n-clicks'),
    Input('filter-trigger-1', 'n-clicks'),
    State('uploaded-files-checklist', 'value'),
    State('event-attribute-dropdown', 'value'),
    State('event-attribute-checkboxes', 'children'),
    State('event-attribute-positive-radio', 'value')

)
def filter_on_event_attributes(button_clicks, filename, keys, children, positive):
    if button_clicks is None or button_clicks == 0:
        return 'hidden', 0

    path = log_management.load_version_control(filename)
    # log_management.store_version_control(filename, filtered)
    return None, button_clicks



# create layout
filtering_panel = [
        # initialize filtering triggers
        html.Button(
            id='filter-trigger-1',
            n_clicks=0,
            hidden=True
        ),
        html.Button(
            id='filter-trigger-2',
            n_clicks=0,
            hidden=True
        ),
        event_attribute_label,
        event_attribute_dropdown,
        event_attribute_checkboxes,
        event_attribute_positive_radio,
        object_attribute_dropdown,
        object_attribute_checkboxes,
        object_attribute_positive_radio,
        html.Button(
            'Filter', id='filter-button',
            n_clicks=0,
        ),
        html.Button('Rollback', id='rollback-button'),
        html.Button('Rollback all', id='rollback-all-button')
]
