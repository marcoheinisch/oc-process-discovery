"""Provide Funktion for extraction of an jsonocel data from SAP tables dataframes."""
import pandas as pd
import json
import os
from datetime import datetime

from utils import constants
from utils.constants import VBTYP_DESCRIPTIONS, UPLOAD_DIRECTORY, OBJECTCLAS_DESCRIPTIONS, REGEX_ALPHANUMERIC
from utils.sap_con import SapConnector
from utils.sql_con import SqlLiteConnection
from app import log_management


def columns_astype_str(df, columns, regex: str = ""):
    """Convert columns of a dataframe to string."""
    _df = df.copy()
    for column in columns:
        _df[column] = _df[column].astype(str)
        if regex != "":
            _df[column] = _df[column].str.replace(regex, '')
    return _df


def get_obj_and_types(df, obj_col, type_col) -> pd.DataFrame:
    """Returns pd.DataFrame with object_id and object_type columns."""
    objects = df[[obj_col, type_col]].copy()
    objects[type_col] = objects[type_col].apply(lambda x: VBTYP_DESCRIPTIONS[x] if x in VBTYP_DESCRIPTIONS else x)
    objects.rename(columns={obj_col: "object_id", type_col: "object_type"}, inplace=True)
    objects.astype({"object_id": str, "object_type": str})
    objects.drop_duplicates(subset=['object_id'], inplace=True)
    return objects


def add_object_ids_column(df, from_columns: list = ["VBELV", "VBELN"]) -> pd.DataFrame:
    """Function to add a "object_id" column."""
    _df = df.copy()
    _df['object_ids'] = _df[from_columns].values.tolist()   
    return _df


def add_event_timestamp_column(df, date_column="ERDAT", time_column="ERZET", replace_columns=True) -> pd.DataFrame:
    """Function to add a "event_timestamp" column from the SAP date and time fields."""
    _df = df.copy()
    _df["event_timestamp"] = _df[date_column].astype(str) + _df[time_column].astype(str)
    _df["event_timestamp"] = pd.to_datetime(_df["event_timestamp"], format="%Y%m%d%H%M%S")
    if replace_columns:
        _df.drop([date_column, time_column], axis=1, inplace=True)
    
    _df = _df[_df["event_timestamp"] > pd.to_datetime("20220101123000", format="%Y%m%d%H%M%S")]
    return _df


def add_event_activity_column(df, activity_column="VBTYP_N", activity_value_prefix="Create ",
                              replace_columns=True) -> pd.DataFrame:
    """Function to add a "event_activity" column."""
    _df = df.copy()
    _df["event_activity"] = activity_value_prefix + _df[activity_column].apply(lambda x: VBTYP_DESCRIPTIONS[x] if x in VBTYP_DESCRIPTIONS else x).astype(str)
    if replace_columns:
        _df.drop([activity_column], axis=1, inplace=True)
    return _df


def add_event_id_column(df, event_id_column="event_id") -> pd.DataFrame:
    """Function to add a "event_id" column."""
    _df = df.copy()
    _df = _df.reset_index()
    _df[event_id_column] = _df.index.astype(str)
    return _df


def construct_ocel_dict(df_events: pd.DataFrame, df_objects: pd.DataFrame) -> dict:
    """Construct the ocel dictionary from the events and objects dataframes.
    Example:
    log = get_ocel_dict(
        df_events=pd.DataFrame({
            "event_activity": ["e_0", "e_1", "e_2"],
            "event_timestamp": ["2021-03-16T09:00:00+01:00","2021-03-17T09:00:00+01:00", "2021-03-18T09:00:00+01:00"],
            "object_ids": [["1", "2"], ["3", "4"], ["2", "4"]]}),
        df_objects=pd.DataFrame({
            "object_id": ["1", "2", "3","4"], 
            "object_type": ["a", "a", "a", "b"]}),
        obj_types=["a", "b", "c"],
        att_names=[]
    )
    """

    log = {}
    object_types = df_objects["object_type"].unique()
    object_types = sorted(list(object_types))

    log["ocel:global-event"] = {"ocel:activity": "__INVALID__"}
    log["ocel:global-object"] = {"ocel:type": "__INVALID__"}
    log["ocel:global-log"] = {
        "ocel:attribute-names": [],
        "ocel:object-types": sorted(list(object_types)),
        "ocel:version": ["1.0"],
        "ocel:ordering": ["timestamp"]
    }
    log["ocel:events"] = {}
    log["ocel:objects"] = {}

    for index, row in df_events.iterrows():
        log["ocel:events"][index] = {
            "ocel:activity": row["event_activity"],
            "ocel:timestamp": row["event_timestamp"],
            "ocel:omap": list(row["object_ids"]),
            "ocel:vmap": {}
        }
    
    for index, row in df_objects.iterrows():
        log["ocel:objects"][row["object_id"]] = {
            "ocel:type": row["object_type"],
            "ocel:ovmap": {}
        }
    return log


def extract_jsonocel(tables) -> dict:
    """Return jsonocel data from SAP tables dataframes."""

    # 1.1 Get all events creating a new document in VBFA
    vbfa = tables["VBFA"]
    vbfa = vbfa[['ERDAT', 'ERZET', 'VBELN', 'VBELV', 'VBTYP_N', 'VBTYP_V', "POSNN", "POSNV"]]  # todo: remove/move to constants
    vbfa = columns_astype_str(vbfa, columns=['VBELN', 'VBELV', 'VBTYP_N', 'VBTYP_V', "POSNN", "POSNV"], regex=REGEX_ALPHANUMERIC)

    vbfa = add_event_timestamp_column(vbfa)
    vbfa = vbfa.groupby(['event_timestamp', 'VBELV', 'VBELN']).first().reset_index()
    
    objects_vbfa_n = get_obj_and_types(vbfa, obj_col="VBELN", type_col="VBTYP_N")
    objects_vbfa_v = get_obj_and_types(vbfa, obj_col="VBELV", type_col="VBTYP_V")
    objects_vbfa = pd.concat([objects_vbfa_n, objects_vbfa_v], ignore_index=True)
    objects_vbfa.drop_duplicates(inplace=True)
    
    df = vbfa.groupby(['event_timestamp', 'VBELN', 'VBTYP_N'])['VBELV'].apply(set).apply(list).reset_index()
    df['object_ids'] = df['VBELV'] + df['VBELN'].apply(lambda x: [x])
    df = add_event_activity_column(df, activity_column="VBTYP_N", activity_value_prefix="Create ",
                                     replace_columns=False)
    events_vbfa = df

    # 2 Get Initial Inquirys
    vbak = tables["VBAK"]
    vbfa_vbeln = vbfa['VBELN'].unique()
    vbfa = vbfa[~vbfa['VBELV'].isin(vbfa_vbeln)] 
    vbfa = vbfa[['VBELV', 'VBTYP_V']].groupby('VBELV').first().reset_index() # all unique VBELV not occuring in VBELN of the whole vbfa table
    events_vbak = pd.merge(left=vbak, right=vbfa, left_on='VBELN', right_on='VBELV', how='right', suffixes=('_vbak', '_vbfa'))
    events_vbak = add_event_timestamp_column(events_vbak)
    events_vbak = add_object_ids_column(events_vbak, from_columns=["VBELN"])
    events_vbak = add_event_activity_column(events_vbak, activity_column="VBTYP_V", activity_value_prefix="Create ",replace_columns=False)
    objects_vbak = get_obj_and_types(events_vbak, obj_col="VBELV", type_col="VBTYP_V")

    # 3 Get Cleared-Invoice events. These lines costed me a weekned of work. Kinda sad;)
    bsad = tables["BSAD"]
    bsad.replace('', pd.NA).dropna(subset=["VBELN"])
    bsad = columns_astype_str(bsad, columns=['VBELN', 'AUGDT'], regex=REGEX_ALPHANUMERIC)
    bsad = bsad[bsad['VBELN'].apply(lambda ids: len(ids) == 10)]
    bsad['ERZET'] = "235959"
    bsad['VBTYP_N'] = "Cleared Invoice"
    bsad = add_event_timestamp_column(bsad, date_column="AUGDT", time_column="ERZET")
    bsad = add_object_ids_column(bsad, from_columns=[ "VBELN"]) #"AUGBL",
    bsad = add_event_activity_column(bsad, activity_column="VBTYP_N", activity_value_prefix="",
                                     replace_columns=False)
    events_bsad = bsad

    # 4 Get all events changing a document loged in CDHDR and CDPOS
    #cdpos = tables["CDPOS"]
    cdhdr = tables["CDHDR"]
    cdhdr = columns_astype_str(cdhdr, columns=['OBJECTCLAS', 'OBJECTID', 'UDATE', 'UTIME'], regex=REGEX_ALPHANUMERIC)
    cdhdr = cdhdr[cdhdr['OBJECTCLAS'].isin(["LIEFERUNG", "VERKBELEG"])]
    cdhdr['OBJECTCLAS'] = cdhdr['OBJECTCLAS'].apply(lambda x: OBJECTCLAS_DESCRIPTIONS[x] if x in OBJECTCLAS_DESCRIPTIONS else x)
    cdhdr = add_event_timestamp_column(cdhdr, date_column="UDATE", time_column="UTIME")
    cdhdr = add_object_ids_column(cdhdr, from_columns=[ "OBJECTID"]) #"AUGBL",
    cdhdr = add_event_activity_column(cdhdr, activity_column="OBJECTCLAS", activity_value_prefix="Update ",
                                        replace_columns=False)
    events_cdhdr = cdhdr
    objects_cdhdr = get_obj_and_types(events_cdhdr, obj_col="OBJECTID", type_col="OBJECTCLAS")

    # Generate jsonocel
    events = pd.concat([events_vbfa, events_vbak, events_bsad, events_cdhdr], ignore_index=True)
    events = events.sort_values("event_timestamp")
    events = add_event_id_column(events)
    events.reset_index(drop=True, inplace=True)
    events = columns_astype_str(events, list(events.columns.drop(["event_timestamp", "object_ids"])))
    events = events[["event_id", "event_timestamp", "event_activity", "object_ids"]]
    events.type = "succint"

    objects = pd.concat([objects_vbfa, objects_vbak, objects_cdhdr], ignore_index=True)
    objects.reset_index(drop=True, inplace=True)

    log_dict = construct_ocel_dict(events, objects)
    return log_dict


def dump_jsonocel(log: dict, file_path: str = "log.jsonocel"):
    """Export jsonocel to .jsonocel file."""

    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if "time" in str(type(obj)):
            return obj.isoformat()
        return str(obj)

    with open(file_path, "w+") as f:
        json.dump(log, f, default=json_serial, indent=4)


def get_tables_from_sap(sap_con) -> dict[str, pd.DataFrame]:
    # Get SAP connection

    tables = {}
    for table, fields in constants.tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=constants.ROWS_AT_A_TIME)
        df = pd.DataFrame(results, columns=headers)
        tables[table] = df
    return tables


def extract_ocel() -> str:
    """Method used by 'extract' button at dms page (gui).
    Returns: extraction status or error message."""
    
    use_sqlite = log_management.use_sqlite
    
    if not use_sqlite:
        try:
            from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
            SAP_CON_PARAMS = log_management.sap_config
            sap_con = SapConnector(SAP_CON_PARAMS)
            tables = get_tables_from_sap(sap_con)
            del sap_con
        except ImportError:
            return "Application Error: PyRFC not installed"
        except CommunicationError:
            return "Could not connect to server."
        except LogonError:
            return "Could not log in. Wrong credentials?"
        except Exception as e:
            return "An error occurred: {}".format(type(e).__name__)
        tables = get_tables_from_sap(sap_con)
        #sql_con = SqlLiteConnection()
        #sql_con.push_tables(tables)
    else:
        sql_con = SqlLiteConnection()
        tables = sql_con.get_tables()
        
    log = extract_jsonocel(tables)
    
    if not use_sqlite:
        log_name = "extracted_at_{}.jsonocel".format(datetime.now().strftime("%y%m%d_%H%M%S"))
    else:
        log_name = "sql_at_{}.jsonocel".format(datetime.now().strftime("%y%m%d_%H%M%S"))

    log_path = os.path.join(UPLOAD_DIRECTORY, log_name)
    
    dump_jsonocel(log, file_path=log_path)
    log_management.register(log_name, log_path)
    
    return "Extraction successful."


if __name__ == "__main__":
    extract_ocel()
