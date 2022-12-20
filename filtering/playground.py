from dash.dependencies import Input, Output, State
import copy
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import math
import pm4py
from pm4py.objects.ocel.obj import OCEL

original_path = None
log_paths = []
ocel = None

# should be triggered by sap extraction callback


def prepare_for_filtering():
    global original_path
    original_path = 'test/p2p-normal.jsonocel'  # change later to the path of the extracted jsonocel
    global log_paths
    log_paths.append(copy.deepcopy(original_path))
    global ocel
    ocel = pm4py.read_ocel(get_path())


def get_path():
    return log_paths[len(log_paths) - 1]


def get_ocel() -> OCEL:
    return pm4py.read_ocel(get_path())


def get_new_path_name():
    length = len(log_paths)
    if length == 1:
        return 'test/filtered_ocel.json'
    else:
        return 'test/filtered_ocel{}.json'.format(length - 1)

def save_filtered_ocel(ocel):
    path = get_new_path_name()
    pm4py.write_ocel(ocel, path)
    log_paths.append(path)


prepare_for_filtering()
app = dash.Dash()


# panel components
# Filter on Event Attributes
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
    [Input('event-attribute-dropdown', 'value')]
)
def update_event_attribute_checkboxes(keys):
    checkboxes = []
    for key in keys:
        checkboxes.append(html.Div(
            children=[
                dcc.Checklist(
                    id=f'{key}-checklist',
                    options=[{'label': element, 'value': element} for element in sorted(set(get_ocel().events[key]))],
                    value=[]
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
    [Input('object-attribute-dropdown', 'value')]
)
def update_object_attribute_checkboxes(keys):
    checkboxes = []
    for key in keys:
        s = set(get_ocel().objects[key])
        elements = copy.copy(s)
        for x in s:
            if str(x).replace('-', '', 1).replace('.', '', 1).isdigit():
                elements = sorted(filter(lambda y: not math.isnan(y), s))
                # for x in s:
                #     if math.isnan(x):
                #         elements.append(x)
                #         break
                break

        checkboxes.append(html.Div(
            children=[
                dcc.Checklist(
                    id=f'{key}-checklist',
                    options=[{'label': element, 'value': element} for element in elements],
                    value=[]
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
    [
        Output('event_attribute_dropdown', 'value'),
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
    return [], [], True, [], [], True


# create layout
app.layout = html.Div(
    [
        event_attribute_dropdown,
        event_attribute_checkboxes,
        event_attribute_positive_radio,
        object_attribute_dropdown,
        object_attribute_checkboxes,
        object_attribute_positive_radio,
        html.Button('Rollback', id='rollback-button')
    ],
    id='filtering_panel'
)

if __name__ == '__main__':
    app.run_server()
