import pandas as pd

from sklearn import datasets

from app import cache
from utils.constants import TIMEOUT


@cache.memoize(timeout=TIMEOUT)
def query_data():
    # This could be an expensive data querying step
    analyse_raw = datasets.load_iris()
    analyse = pd.DataFrame(analyse_raw["data"], columns=analyse_raw["feature_names"])
    return analyse.to_json(date_format='iso', orient='split')


def dataframe():
    return pd.read_json(query_data(), orient='split')
