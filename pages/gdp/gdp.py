from dash import dcc
from dash import html

from pages.gdp.gdp_data import dataframe


layout = html.Div([
    html.H1("GDP viewer"),
    html.Hr(),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=dataframe()['year'].min(),
        max=dataframe()['year'].max(),
        value=dataframe()['year'].min(),
        marks={str(year): str(year) for year in dataframe()['year'].unique()},
        step=None
    )
])