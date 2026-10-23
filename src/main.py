import logging, sys, os
from pathlib import Path

from interface.ul_interface import User_Manager, U_main
from interface.tdl_interface import List_Manager, app
from logging_config import setup_log
from manager.data_manager import JSONStorage

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False): #Running script as .exe
    BaseDirectory = Path(sys.executable).resolve().parent.parent
else: #Running script as a script
    BaseDirectory = Path(__file__).resolve().parent.parent

def init(token, user_id):
    if token == "U":
        DataDir = BaseDirectory / "data"
        DataDir.mkdir(parents=True, exist_ok=True)
        return JSONStorage(DataDir/"user_data.json")
    elif token == "L":
        DataDir = BaseDirectory / "data" / user_id
        DataDir.mkdir(parents=True, exist_ok=True)
        return JSONStorage(DataDir / "list_data.json")


# Initializes the user-management class
"""
    - userdata_storage (data manager object) loads data from the userdata file
    - the data is then transfered to the user_manager object, which will then be used for authentication
    - When the user is authenticated, the function returns the authenticated user's ID
"""

def user_auth_init():
    storage = init("U",None)
    try:
        userdata_import = User_Manager.importData(storage.load_data()["data"]) 
        auth_data = User_Manager.authdata()
        if userdata_import["status"] and auth_data["status"]:
            logger.info("INITIALIZE: User Authentication initialised successfully.")

            Authenticated_User = U_main(storage)
            if Authenticated_User["status"]:
                logger.info("INITIALIZE: User Authentication executed successfully.")
                return {"status": True,
                        "data": Authenticated_User["data"],
                        "message": Authenticated_User["message"]}
            logger.error("INITIALIZE: User Authentication execution failed.")
            return {"status": False,
                    "data": None,
                    "message": Authenticated_User.get("message", "User authentication failed.")}

        return {"status": False,
                "data": None,
                "message": [userdata_import.get("message"), auth_data.get("message")]}
    except Exception as e:
        logger.error(f"INITIALIZE: User Authentication initialisation failed. ERROR: {type(e).__name__}:{e}")
        return {"status": False,
                "data": None,
                "message": f"{type(e).__name__}:{e}"}

"""
    - Initialises the authenticated user's list data management object
    - Data is loaded, and passed to list manager for further use
"""
def list_manager_init(user_id):
    try:
        storage = init("L", user_id)
        listdata_load = storage.load_data()
        if not listdata_load["status"]:
            logger.error(f"INITIALIZE: List data loading failed: {listdata_load['message']}")
            return {"status": False,
                    "data": None,
                    "message": listdata_load.get("message", "List data loading failed.")}

        listdata_import = List_Manager.import_data(listdata_load["data"])
        if listdata_import["status"]:
            logger.info("INITIALIZE: Application initialised successfully")
            return {"status": True,
                    "data": storage,
                    "message": "Application initialized successfully."}

        logger.error(f"INITIALIZE: Application intialisation failed: {listdata_import['message']}")
        return {"status": False,
                "data": None,
                "message": listdata_import.get("message", "Application initialisation failed.")}
    except Exception as e:
        logger.error(f"INITIALIZE: Application intialisation failed: ERROR: {type(e).__name__}:{e}")
        return {"status": False,
                "data": None,
                "message": f"{type(e).__name__}:{e}"}

app_run = False
if __name__ == '__main__':
    setup_log()
    auth = user_auth_init()
    if  not auth.get("status"):
        print(auth.get("message"))
        
    # Load the user's lists only after authentication succeeds.
    list_init = list_manager_init(auth["data"])
    if not list_init.get("status"):
        print(list_init.get("message"))

    # Status true, app ready to work    
    app_run = True
    app(app_run,list_init.get("data"))
logger.info("MAIN: application closed.")