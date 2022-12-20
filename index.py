from app import app, server

from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK

# import callback functions
from routes import render_page_content

from pages.dms.dms_callbacks import *
from pages.analyse.analyse_callbacks import *
from layout.sidebar.sidebar_callbacks import *


if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )