"""Create an object-centric event log from SAP data tables.
    """

import pandas as pd

from sap_con import SapConnector
import constants

if __name__ == "__main__":
    
    # Get SAP connection
    con_params = constants.sap_conn_params
    sap_con = SapConnector.getInstance(constants.sap_conn_params)
    con_details = sap_con.get_con_details()
    print(con_details)

    # Get SAP data
    now_string = pd.Timestamp.now().strftime("%Y_%m_%d-%H_%M_%S")

    dfs = {}
    for table, fields in constants.tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=constants.ROWS_AT_A_TIME)

        print(table, end=": \n")
        print(fields)
        print(headers)

        df = pd.DataFrame(results, columns=headers)
        df.to_pickle(f"{table}.pkl")
    sap_con.close_instance()
    
    # Create event log

        

