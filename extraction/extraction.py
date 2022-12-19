"""Provide Funktion for extraction of an jsonocel data from SAP tables dataframes."""
import pandas as pd
import json
import os
from datetime import datetime

from utils import constants
from utils.constants import VBTYP_DESCRIPTIONS, UPLOAD_DIRECTORY
from utils.sap_con import SapConnector
from environment.settings import SAP_CON_PARAMS
from app import log_management


def columns_astype_str(df, columns, regex: str = False):
    """Convert columns of a dataframe to string."""
    _df = df.copy()
    for column in columns:
        _df[column] = _df[column].astype(str)
        if regex:
            _df[column] = _df[column].str.replace(regex, '')
    return _df


def get_obj_and_types(df, obj_col, type_col) -> pd.DataFrame:
    """Returns pd.DataFrame with object_id and object_type columns."""
    objects = df[[obj_col, type_col]].copy()
    objects.rename(columns={obj_col: "object_id", type_col: "object_type"}, inplace=True)
    objects.astype({"object_id": str, "object_type": str})
    objects.drop_duplicates(subset=['object_id'], inplace=True)
    return objects


def add_object_ids_column(df, object_id_columns="object_id") -> pd.DataFrame:
    """Function to add a "object_id" column."""
    _df = df.copy()
    _df['object_ids'] = _df[object_id_columns].astype(str).values.map(VBTYP_DESCRIPTIONS).tolist()
    return _df


def add_event_timestamp_column(df, date_column="ERDAT", time_column="ERZET", replace_columns=True) -> pd.DataFrame:
    """Function to add a "event_timestamp" column from the SAP date and time fields."""
    _df = df.copy()
    # todo: check if the date and time fields are in the dataframe
    _df["event_timestamp"] = _df[date_column].astype(str) + _df[time_column].astype(str)
    _df["event_timestamp"] = pd.to_datetime(_df["event_timestamp"], format="%Y%m%d%H%M%S")
    if replace_columns:
        _df.drop(["ERDAT", "ERZET"], axis=1, inplace=True)
    return _df


def add_event_activity_column(df, activity_column="VBTYP_N", activity_value_prefix="Create ",
                              replace_columns=True) -> pd.DataFrame:
    """Function to add a "event_activity" column."""
    _df = df.copy()
    # _df[activity_column] = _df[activity_column].str.replace('[^a-zA-Z0-9]', '')  moved to columns_astype_str
    _df["event_activity"] = activity_value_prefix + _df[activity_column].map(VBTYP_DESCRIPTIONS).astype(str)
    if replace_columns:
        _df.drop([activity_column], axis=1, inplace=True)
    return _df


def add_event_id_column(df, event_id_column="event_id") -> pd.DataFrame:
    """Function to add a "event_id" column."""
    _df = df.copy()
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
    # att_names = sorted(list(set(att_types.keys())))
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
        # log["ocel:events"][index]["ocel:omap"] =
    for index, row in df_objects.iterrows():
        log["ocel:objects"][row["object_id"]] = {
            "ocel:type": row["object_type"],
            "ocel:ovmap": {}
        }
    return log


def extract_jsonocel_data(tables):
    """Return jsonocel data from SAP tables dataframes."""

    # 1.1 Get all events creating a new document in VBFA
    vbfa = tables["VBFA"]
    vbfa = vbfa[['ERDAT', 'ERZET', 'VBELN', 'VBELV', 'VBTYP_N', 'VBTYP_V']]  # todo: remove/move to constants
    vbfa = columns_astype_str(vbfa, columns=['VBELN', 'VBELV', 'VBTYP_N', 'VBTYP_V'], regex='[^a-zA-Z0-9]')

    vbfa = add_event_timestamp_column(vbfa)
    vbfa = add_event_activity_column(vbfa, activity_column="VBTYP_N", activity_value_prefix="Create ",
                                     replace_columns=False)
    vbfa['object_ids'] = vbfa[["VBELV", "VBELN"]].values.tolist()

    events_vbfa = vbfa

    # 1.2 Get all objects and their object type from the events in VBFa:
    objects_vbfa_n = get_obj_and_types(vbfa, obj_col="VBELN", type_col="VBTYP_N")
    objects_vbfa_v = get_obj_and_types(vbfa, obj_col="VBELV", type_col="VBTYP_V")
    objects_vbfa = pd.concat([objects_vbfa_n, objects_vbfa_v])
    objects_vbfa.drop_duplicates(inplace=True)

    # 2.1
    # vbak = tables["VBAK"]
    # vbak = vbak[['VBELN', 'ERDAT', 'ERZET']]  # todo: remove/move to constants
    #
    # events_vbak = pd.DataFrame()
    # objects_vbak = pd.DataFrame()

    # Generate jsonocel
    events = events_vbfa  # pd.concat([events_vbfa, events_vbak])
    events = events.sort_values("event_timestamp")
    events = add_event_id_column(events)
    events = columns_astype_str(events, list(events.columns.drop(["event_timestamp", "object_ids"])))
    events = events[events["event_timestamp"] > pd.to_datetime("20190101123000", format="%Y%m%d%H%M%S")]
    events.type = "succint"

    objects = objects_vbfa  # pd.concat([objects_vbfa, objects_vbak])

    log_dict = construct_ocel_dict(events, objects)
    return log_dict


def export_jsonocel(log: dict, file_path: str = "log.jsonocel"):
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
    con_details = sap_con.get_con_details()
    print(con_details)

    tables = {}
    for table, fields in constants.tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=constants.ROWS_AT_A_TIME)
        df = pd.DataFrame(results, columns=headers)
        tables[table] = df
    sap_con.close_instance()
    return tables


def extract_ocel() -> str:
    """Method used by 'extract' button at dms page (gui).
    Returns: extraction status or error message."""
    try:
        from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
    except ImportError:
        return "Application Error: PyRFC not installed"
    try:
        sap_con = SapConnector.getInstance(SAP_CON_PARAMS)
    except CommunicationError:
        return "Could not connect to server."
    except LogonError:
        return "Could not log in. Wrong credentials?"
    except (ABAPApplicationError, ABAPRuntimeError):
        return "An error occurred."
    tables = get_tables_from_sap(sap_con)
    log = extract_jsonocel_data(tables)
    
    log_name = "extracted_at_{}.jsonocel".format(datetime.now().strftime("%y%m%d_%H%M%S"))
    log_path = os.path.join(UPLOAD_DIRECTORY, log_name)
    export_jsonocel(log, file_path=log_path)
    log_management.register(log_name, log_path)
    return "Extraction successful."


if __name__ == "__main__":
    extract_ocel()
