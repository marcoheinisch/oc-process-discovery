import pandas as pd

from webapp.app import cache
from webapp.utils.constants import TIMEOUT


@cache.memoize(timeout=TIMEOUT)
def query_data():
    # This could be an expensive data querying step
    dms_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
    return dms_data.to_json(date_format='iso', orient='split')

def dataframe():
    return pd.read_json(query_data(), orient='split')