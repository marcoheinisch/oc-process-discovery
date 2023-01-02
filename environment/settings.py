# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), os.getenv("ENVIRONMENT_FILE"))
load_dotenv(dotenv_path=dotenv_path, override=True)

APP_HOST = os.environ.get("HOST")
APP_PORT = int(os.environ.get("PORT"))
APP_DEBUG = bool(os.environ.get("DEBUG"))
DEV_TOOLS_PROPS_CHECK = bool(os.environ.get("DEV_TOOLS_PROPS_CHECK"))

SAP_USER = os.environ.get("SAP_USER")
SAP_PASSWD = os.environ.get("SAP_PASSWD")
SAP_ASHOST = os.environ.get("SAP_ASHOST")
SAP_SAPROUTER = os.environ.get("SAP_SAPROUTER")
SAP_MSSERV = os.environ.get("SAP_MSSERV")
SAP_SYSID = os.environ.get("SAP_SYSID")
SAP_GROUP = os.environ.get("SAP_GROUP")
SAP_CLIENT = os.environ.get("SAP_CLIENT")
SAP_LANG = os.environ.get("SAP_LANG")
SAP_TRACE = os.environ.get("SAP_TRACE")
SAP_CON_PARAMS = {
    'user': SAP_USER,
    'passwd': SAP_PASSWD,
    'ashost': SAP_ASHOST,
    'saprouter': SAP_SAPROUTER,
    'msserv': SAP_MSSERV,
    'sysid': SAP_SYSID,
    'group': SAP_GROUP,
    'client': SAP_CLIENT,
    'lang': SAP_LANG,
    'trace': SAP_TRACE
}
