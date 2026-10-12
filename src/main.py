import logging

from interface.ul_interface import User_Manager, userdata_storage, U_main
from interface.tdl_interface import List_Manager, app, init
from logging_config import setup_log

logger = logging.getLogger(__name__)

def user_auth_init():
    try:
        userdata_import = User_Manager.importData(userdata_storage.load_data()["data"])
        auth_data = User_Manager.authdata()
        if userdata_import["status"] and auth_data["status"]:
            logger.info("INITIALIZE: User Authentication initialised successfully.")

            Authenticated_User = U_main()
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


def list_manager_init(user_id):
    try:
        storage = init(user_id)
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
    if auth.get("status"):
        # Load the user's lists only after authentication succeeds.
        list_init = list_manager_init(auth["data"])
        if list_init.get("status"):
            print(auth.get("data"))
        else:
            print(list_init.get("message"))
    else:
        print(auth.get("message"))
app(app_run)
logger.info("MAIN: application closed.")