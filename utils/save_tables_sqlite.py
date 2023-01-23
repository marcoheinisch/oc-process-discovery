import pandas as pd
import sqlite3

from utils.sap_con import SapConnector
from utils import constants
from environment.settings import SAP_CON_PARAMS

SQLITE_PATH = "sap_tables.sqlite"

SAP_CON_PARAMS = {
    'user': "SAP_USER",
    'passwd': "SAP_PASSWD",
    'ashost': "SAP_ASHOST",
    'saprouter': "SAP_SAPROUTER",
    'msserv': "SAP_MSSERV",
    'sysid': "SAP_SYSID",
    'group': "SAP_GROUP",
    'client': "SAP_CLIENT",
    'lang': "SAP_LANG",
    'trace': "SAP_TRACE"
}


def save_tables():
    """Function to save SAP data tables in sql. For debugging purposes.
    """
    sap_con = SapConnector(SAP_CON_PARAMS)
    tables = {}
    for table, fields in constants.tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=constants.ROWS_AT_A_TIME)
        df = pd.DataFrame(results, columns=headers)
        tables[table] = df
    del sap_con
    
    sql_con = sqlite3.connect(SQLITE_PATH)  
    for table, df in tables.items():
        table_name = str(table).upper()
        df.to_sql(table_name, sql_con, if_exists='replace')
    sql_con.close()
    sql_con.push_tables(tables)
    
