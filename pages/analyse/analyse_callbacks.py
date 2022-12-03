
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.express as px

from sklearn.cluster import KMeans

from app import app
#from app import long_callback_manager 
from pages.analyse.analyse_data import dataframe

from pages.analyse.process_discovery import ocpa_discover
from pages.analyse.process_discovery import pm4py_discover
from pages.analyse.process_discovery import dfg_discover


@app.callback(
    Output("process-model", "dot_source"),
    [
        Input("apda-option", "value"),
    ],
    #manager=long_callback_manager,
)

def discover_process_model(apda):
    if apda == "ocpa":
        return ocpa_discover()
    elif apda == "pm4py":
        return pm4py_discover()
    elif apda == "dfg":
        return dfg_discover()
