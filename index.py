from app import app, server

from routes import render_page_content

from layout.sidebar.sidebar_callbacks import toggle_collapse, toggle_classname

from pages.dms.dms_callbacks import update_figure
from pages.analyse.analyse_callbacks import discover_process_model

from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK


if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )