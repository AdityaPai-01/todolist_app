import logging

from helpers import *
from interface import app
from logging_config import setup_log

logger = logging.getLogger(__name__)

def initialize():
    userdata_import = User_Manager.importData(userdata_storage.load_data()["data"])
    listdata_import = List_Manager.import_data(listdata_storage.load_data()["data"])
    auth_data = User_Manager.authdata()

    if userdata_import["status"] and listdata_import["status"] and auth_data["status"]:
        logger.info("INITIALIZE: Application initialised successfully.")
        return True
    else:
        if not userdata_import["status"]:
            logger.error(f"INITIALIZE: Failed to initialize: {userdata_import["message"]}")
        if not listdata_import["status"]:
            logger.error(f"INITIALIZE: Failed to initialize: {listdata_import["message"]}")
        if not auth_data["status"]:
            logger.error(f"INITIALIZE: Failed to initialize: {auth_data["message"]}")
        return False

app_run = False
if __name__ == '__main__':
    setup_log()
    if initialize():
        app_run = True
    else:
        print("Something went wrong.")
app(app_run)
logger.info("MAIN: application closed.")