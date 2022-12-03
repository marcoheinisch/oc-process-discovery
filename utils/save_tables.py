"""Create an object-centric event log from SAP data tables.
    """

import pandas as pd

from utils.sap_con import SapConnector
from utils import constants
from environment.settings import SAP_CON_PARAMS


def save_tables():
    
    # Get SAP connection
    con_params = SAP_CON_PARAMS
    sap_con = SapConnector.getInstance(con_params)
    con_details = sap_con.get_con_details()
    print(con_details)

    # Get SAP data
    now_string = pd.Timestamp.now().strftime("%Y_%m_%d-%H_%M_%S")

    dfs = {}
    for table, fields in constants.tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=constants.ROWS_AT_A_TIME)
        df = pd.DataFrame(results, columns=headers)
        df.to_pickle(f"{table}.pkl")
    sap_con.close_instance()
    
    # Create event log

        

