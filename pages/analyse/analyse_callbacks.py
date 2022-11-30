
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.express as px

from sklearn.cluster import KMeans

from app import app
from pages.analyse.analyse_data import dataframe

from pages.analyse.process_discovery import ocpa_discover
from pages.analyse.process_discovery import pm4py_discover

@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
def make_graph(x, y, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    km = KMeans(n_clusters=max(n_clusters, 1))
    analyse = dataframe()
    df = analyse.loc[:, [x, y]]
    km.fit(df.values)
    df["cluster"] = km.labels_

    centers = km.cluster_centers_

    data = [
        go.Scatter(
            x=df.loc[df.cluster == c, x],
            y=df.loc[df.cluster == c, y],
            mode="markers",
            marker={"size": 8},
            name="Cluster {}".format(c),
        )
        for c in range(n_clusters)
    ]

    data.append(
        go.Scatter(
            x=centers[:, 0],
            y=centers[:, 1],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="Cluster centers",
        )
    )

    layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

    return go.Figure(data=data, layout=layout)

# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    analyse = dataframe()

    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in analyse.columns
    ]

# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
    filter_options
)
app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
    filter_options
)

@app.callback(
    Output("process-model", "dot_source"),
    [
        Input("apda-option", "value"),
    ],
)

def discover_process_model(apda):
    if apda == "ocpa":
        return ocpa_discover()
    elif apda == "pm4py":
        return pm4py_discover()
