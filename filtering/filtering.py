from dash_extensions.enrich import Output, Input, State

import copy
import os
import dash
from dash import html, dcc
import math
import re
import pm4py

from app import app
from app import log_management

from utils.constants import UPLOAD_DIRECTORY
import dms.dms
from utils.constants import analyse_page_location, dms_page_location

import pandas as pd


# panel components
save_changes_label = html.Label(
    id='save-changes-label',
    hidden="hidden",
    children='The filtered log has been successfully saved!'
)


filtering_label = html.Label(
    id='filtering-label',
    hidden="hidden",
    children='Filtering has been succesfully applied!'
)

clear_label = html.Label(
    id='clear-label',
    hidden="hidden",
    children='The uploaded files and their filtered versions have been succesfully cleared!'
)

delete_file_label = html.Label(
    id='delete-file-label',
    hidden="hidden",
    children='The selected file has been succesfully deleted!'
)


# Filter on Event Attributes
event_attribute_label = html.Label(
    id='event-attribute-label',
    hidden="hidden",
    children='Filtering on Event Attributes has been successfully applied!'
)

event_attribute_dropdown = dcc.Dropdown(
    id='event-attribute-dropdown',
    options=[{'label': attr, 'value': attr} for attr in log_management.get_ocel().events.columns.tolist()],
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
    value=False,  # default value
    labelStyle={'display': 'inline-block'}
)

# Filter on Object Attributes
object_attribute_label = html.Label(
    id='object-attribute-label',
    hidden="hidden",
    children='Filtering on Object Attributes has been successfully applied!'
)


object_attribute_dropdown = dcc.Dropdown(
    id='object-attribute-dropdown',
    options=[{'label': attr, 'value': attr} for attr in log_management.get_ocel().objects.columns.tolist()],
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
    value=False,  # default value
    labelStyle={'display': 'inline-block'}
)

dcc.DatePickerSingle(
    id='start-date',
    date=str(pd.to_datetime('today').date())
),
dcc.DatePickerSingle(
    id='end-date',
    date=str(pd.to_datetime('today').date()),
    min_date_allowed=str(pd.to_datetime('today').date()),
    max_date_allowed=str(pd.to_datetime('today').date()),
),


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
                    options=[{'label': element, 'value': element} for element in sorted(set(log_management.get_ocel().events[key]))],
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
        key = child['props']['children'][0]['props']['id'].rsplit('-', 1)[0]
        value = child['props']['children'][0]['props']['value']
        selected_values[key] = value

    checkboxes = []
    for key in keys:
        s = set(log_management.get_ocel().objects[key])
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


# define callback for rollback
@app.callback(
    Output('uploaded-files-checklist', 'value'),
    Input('rollback-button', 'n_clicks'),
)
def rollback(button_clicks):
    singleton_instance = dms.dms.SingletonClass()
    selected = singleton_instance.selected

    if button_clicks is None or button_clicks == 0:
        return selected

    log_management.rollback()
    return selected

# define callback for rollback_all
@app.callback(
    Output('uploaded-files-checklist', 'value'),
    Input('rollback-all-button', 'n_clicks'),
)
def rollback_all(button_clicks):
    singleton_instance = dms.dms.SingletonClass()
    selected = singleton_instance.selected

    if button_clicks is None or button_clicks == 0:
        return selected

    log_management.rollback_all()
    return selected


@app.callback(
    Output('filter-trigger-1', 'n-clicks'),
    Input('filter-button', 'n_clicks'),
)
def apply_filtering(button_clicks):
    return button_clicks

@app.callback(
    Output('save-changes-label', 'hidden'),
    Output('output-jsonocel-upload', 'children'),
    Output('uploaded-files-checklist', 'value'),
    Input('save-changes-button', 'n_clicks'),
    State('output-jsonocel-upload', 'children'),
    State('uploaded-files-checklist', 'value'),
)
def save_changes(button_clicks, upload_children, filename):
    if button_clicks is None or button_clicks == 0:
        return 'hidden', upload_children, filename

    new_filename = filename.rpartition('.jsonocel')[0] + '_filtered.jsonocel'
    path = os.path.join(UPLOAD_DIRECTORY, new_filename)
    pm4py.write_ocel(log_management.get_ocel(), path)
    log_management.register(new_filename, path)

    log_management.reset_to_original(filename)

    return None, upload_children, new_filename

@app.callback(
    Output("url", "pathname"),
    Input('go-to-analysis-button', 'n_clicks'),
    State("url", "pathname")
)
def go_to_analysis(button_clicks, pathname):
    if button_clicks is None or button_clicks == 0:
        return pathname
    else:
        return analyse_page_location

@app.callback(
    Output("url", "pathname"),
    Input('go-to-dms-button', 'n_clicks'),
    State("url", "pathname")
)
def go_to_dms(button_clicks, pathname):
    if button_clicks is None or button_clicks == 0:
        return pathname
    else:
        return dms_page_location

@app.callback(
    Output('container-feedback-text', 'children'),
    Output('uploaded-files-checklist', 'value'),
    Output('clear-label', 'hidden'),
    Input('clear-button', 'n_clicks'),
    State('container-feedback-text', 'children'),
)
def clear(button_clicks, children):
    if button_clicks is None or button_clicks == 0:
        selected = dms.dms.SingletonClass().selected
        return children, selected, 'hidden'
    else:
        log_management.clear()
        selected = dms.dms.SingletonClass().selected
        return children, selected, None

@app.callback(
    Output('container-feedback-text', 'children'),
    Output('uploaded-files-checklist', 'value'),
    Output('save-changes-label', 'hidden'),
    Output('save-changes-label', 'children'),
    Input('delete-file-button', 'n_clicks'),
    State('container-feedback-text', 'children'),
)
def delete(button_clicks, children):
    if button_clicks is None or button_clicks == 0:
        selected = dms.dms.SingletonClass().selected
        return children, selected, 'hidden', 'The selected file has been succesfully deleted!'
    else:
        message = 'The selected file has been succesfully deleted!'
        try:
            log_management.delete_selected()
        except Exception:
            message = "Cannot delete the only file left!"
            pass
        selected = dms.dms.SingletonClass().selected
        return children, selected, None, message


@app.callback(
    Output('event-attribute-dropdown', 'value'),
    Output('event-attribute-checkboxes', 'children'),
    Output('event-attribute-positive-radio', 'value'),
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
        return keys, children, positive, 'hidden', 0

    # load the most recent version of the file
    ocel = log_management.load_version_control(filename)

    # load the selected values per each key
    selected_values = {}
    for child in children:
        key = child['props']['children'][0]['props']['id'].rsplit('-', 1)[0]
        value = child['props']['children'][0]['props']['value']
        selected_values[key] = value

    if not keys:
        return [], [], False, 'hidden', button_clicks

    # apply filtering per key
    for key in keys:
        if key not in selected_values:
            selected_values[key] = []
        ocel = pm4py.filter_ocel_event_attribute(ocel, key, selected_values[key], positive)

    log_management.store_version_control(filename, ocel)
    return [], [], False, None, button_clicks


@app.callback(
    Output('object-attribute-dropdown', 'value'),
    Output('object-attribute-checkboxes', 'children'),
    Output('object-attribute-positive-radio', 'value'),
    Output('object-attribute-label', 'hidden'),
    Output('filter-trigger-3', 'n-clicks'),
    Input('filter-trigger-2', 'n-clicks'),
    State('uploaded-files-checklist', 'value'),
    State('object-attribute-dropdown', 'value'),
    State('object-attribute-checkboxes', 'children'),
    State('object-attribute-positive-radio', 'value')
)
def filter_on_object_attributes(button_clicks, filename, keys, children, positive):
    if button_clicks is None or button_clicks == 0:
        return keys, children, positive, 'hidden', 0

    # load the most recent version of the file
    ocel = log_management.load_version_control(filename)

    # load the selected values per each key
    selected_values = {}
    for child in children:
        key = child['props']['children'][0]['props']['id'].rsplit('-', 1)[0]
        value = child['props']['children'][0]['props']['value']
        selected_values[key] = value

    if not keys:
        return [], [], False, 'hidden', button_clicks

    # apply filtering per key
    for key in keys:
        if key not in selected_values:
            selected_values[key] = []
        ocel = pm4py.filter_ocel_object_attribute(ocel, key, selected_values[key], positive)

    log_management.store_version_control(filename, ocel)
    return [], [], False, None, button_clicks


# create layout
filtering_panel = [
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
        html.Button(
            id='filter-trigger-3',
            n_clicks=0,
            hidden=True
        ),
        event_attribute_label,
        event_attribute_dropdown,
        event_attribute_checkboxes,
        event_attribute_positive_radio,
        object_attribute_label,
        object_attribute_dropdown,
        object_attribute_checkboxes,
        object_attribute_positive_radio,
        html.Button(
            'Filter',
            id='filter-button',
            n_clicks=0,
        ),
        html.Button(
            'Rollback',
            id='rollback-button',
            n_clicks=0,
        ),
        html.Button(
            'Rollback all',
            id='rollback-all-button',
            n_clicks=0,
        ),
        html.Button(
            'Save changes',
            id='save-changes-button',
            n_clicks=0,
        ),
        html.Button(
            'Go to analysis',
            id='go-to-analysis-button',
            style={'color': 'white', 'background-color': '#0d6efd'},
            n_clicks=0,
        ),
        filtering_label,
        save_changes_label,
        clear_label,
        delete_file_label,
]
