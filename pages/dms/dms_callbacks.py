import base64
import io
import datetime
import pandas as pd

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

from pm4py.objects.ocel.validation import jsonocel
from pages.dms.dms_data import dataframe

from app import app
from pages.dms.dms_data import dataframe


def ocel_is_valid(filename):
  if __name__ == "__main__":
    return jsonocel.apply("tests/input_data/ocel/filename",
                          "tests/input_data/ocel/schema.json")
  return False


def parse_contents(contents, filename, date):
  content_type, content_string = contents.split(',')

  decoded = base64.b64decode(content_string)
  try:
    if ocel_is_valid(filename):
      df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
  except Exception as e:
    print(e)
    return html.Div(['There was an error processing this file.'])

  return html.Div([
    html.H5(filename),
    html.H6(datetime.datetime.fromtimestamp(date)),
    dash_table.DataTable(df.to_dict('records'), [{
      'name': i,
      'id': i
    } for i in df.columns]),
    html.Hr(),
    html.Div('Raw Content'),
    html.Pre(contents[0:200] + '...',
             style={
               'whiteSpace': 'pre-wrap',
               'wordBreak': 'break-all'
             })
  ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)



"""
import plotly.express as px

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    dms_data = dataframe()
    filtered_df = dms_data[dms_data.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
"""