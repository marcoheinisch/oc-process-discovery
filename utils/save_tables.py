"""Create an object-centric event log from SAP data tables.
    """

import pandas as pd

from utils.sap_con import SapConnector
from utils import constants
from environment.settings import SAP_CON_PARAMS


def save_tables():
    """Function to save SAP data tables as pickle files. For debugging purposes only.!
    """
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
        df.to_pickle(f"C:\\Users\\Marco\\Projekte\\os-process-testing\\{table}.pkl")
    sap_con.close_instance()

    # Create event log

def load_tables():
    """Function to load SAP data tables from pickle files. For debugging purposes only.!
    example: 
    dfs = load_tables()
    vbfa = dfs["VBFA"].copy()
    """
    import pandas as pd
    import os
    #list all the files in the current folder with the extension .pkl
    files = [f for f in os.listdir('.') if f.endswith('.pkl')]
    tables = []

    # load pickle file to dataframes
    dfs = {}
    for file  in files:
        table = file.split(".")[0]
        tables.append(table)
        
        dfs[table] = pd.read_pickle(file)

    return dfs



if __name__ == "__main__":
    save_tables()

