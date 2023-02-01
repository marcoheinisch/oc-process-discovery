import pandas as pd
import sqlite3

from sap_con import SapConnector
from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError


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

tables = {
    'BSAD': [11, 'MANDT', 'BUKRS', "KUNNR", "UMSKS", "UMSKZ", 'AUGDT', 'AUGBL', "ZUONR", 'GJAHR', 'BELNR', 'BLART',
             'VBELN'],
    'VBFA': [0, "ERDAT", "ERZET", "VBELN", "VBELV", "VBTYP_N", "VBTYP_V", "RFMNG", "MEINS", "RFWRT", "WAERS", "MATNR",
             "BWART", "VRKME", "FKTYP", "POSNN", "POSNV"],
    'VBAK': [0, "VBELN", "ERDAT", "ERZET", "KUNNR"],
    'CDHDR': [4, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'USERNAME', 'UDATE', 'UTIME', 'TCODE', 'CHANGE_IND'],
    'CDPOS': [8, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'TABNAME', 'TABKEY', 'FNAME', 'CHNGIND'],
}


def save_tables():
    """Function to save SAP data tables in sql. For debugging purposes.
    """
    sap_con = SapConnector(SAP_CON_PARAMS)
    tmp = {}
    for table, fields in constants.tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=3000)
        df = pd.DataFrame(results, columns=headers)
        tmp[table] = df
    del sap_con

    sql_con = sqlite3.connect(SQLITE_PATH)
    for table, df in tmp.items():
        table_name = str(table).upper()
        df.to_sql(table_name, sql_con, if_exists='replace')
    sql_con.close()


if __name__ == "__main__":
    save_tables()
