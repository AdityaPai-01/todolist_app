from model.user import User
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

#This class manages the user objects and performs certain operations to manage the database
class UserManager():
    def __init__(self):
        self.users = {} #Stores userdata()during the runtime of application
        self.authenticatedUser = {}
        self.userauthdata = {}

    # Login function, enables the user to access the meta-data of the respective application
    def login(self, username, password):
        if username not in self.userauthdata.keys():
            logger.warning("USER LOGIN: Username '%s' not in database", username)
            return {"message": f"User [{username}] not found!",
                    "status": False}
        if password != self.userauthdata[username]:
            logger.warning("USER LOGIN: Incorrect password used for user '%s'", username)
            return {"message": "Invalid Password",
                    "status": False}
        for user in self.users.values():
            if user.username == username:
                self.authenticatedUser.update({"uid":user.userID, "user_data":{"uname":user.username, "metadata":user.metadata}})
        logger.info("USER LOGIN: User logged in successfully")
        return {"message": "Login successful!",
                "status": True}

    # Register function, enables the user to register themselves (create an account) in the application's database
    def register(self, Username, Password, Meta_Data=None):
        if Username in self.userauthdata.keys():
            logger.warning("USER REGISTERATION: User '%s' already exists", Username)
            return {"message": f"User [{Username}] already exists!",
                    "status": False}
        else:
            newUser = User(Username, Password, metadata=Meta_Data)
            self.users.update({newUser.userID: newUser})
            logger.info("USER REGISTERATION: User '%s' registered successfully", Username)
            return {"message": "User successfully registered!",
                    "status": True}
    
    # Takes raw data as the input, builds user objects so that UserManager class can perform it's business functions
    def importData(self, rawdata):
        try:
            for k, v in rawdata.items():
                newUser = User(userID=k, username=v["Username"], password=v["Password"], metadata=v["Metadata"])
                self.users.update({k:newUser})
            logger.info("USER DATA IMPORT: User data imported successfully")
            return {"message":None,
                    "status": True}
        except Exception as e:
            logger.error("USER DATA IMPORT: User data import failed: %s", f"{type(e).__name__}:{e}")
            return {"message": f"{type(e).__name__}:{e}",
                    "status": False}

    # Takes the data created/modified during the business functions and converts into locally storable data, to pass on to the storage class to store.
    def exportData(self):
        try:
            rawdata = {}
            for userID in self.users.keys():
                for k, v in self.users[userID].userdict()["data"].items():
                    rawdata.update({k:v})
            logger.info("USER DATA EXPORT: User-class data exported successfully")
            return {"message": "User-class data exported successfully",
                    "status": True,
                    "data": rawdata}
        except Exception as e:
            logger.error("USER DATA EXPORT: Could not export user data: %s", f"{type(e).__name__}:{e}")
            return {"message": f"Could not export data.\n{type(e).__name__}:{e}",
                    "status": False,
                    "data": {}}
    
    #Seperates and collects only the data required for login/registeration functions
    def authdata(self):
        try:
            self.userauthdata = {}
            for k, v in self.users.items():
                for key, value in v.userdict()["data"].items():
                    self.userauthdata.update({value["Username"] : value["Password"]})
            logger.info("USER DATA AUTHENTICATION: Authentication data loaded successfully")
            return {"message": None,
                    "status": True}
        except Exception as e:
            logger.error("USER DATA AUTHENTICATION: Authentication data loading failed: %s", f"{type(e).__name__}:{e}")
            return {"message": f"{type(e).__name__}:{e}",
                    "status": False}

    def rename_user(self, current_username, new_username, password):
        user_id = self.authenticatedUser.get("uid")
        user = self.users.get(user_id)
        if user is None or user.username != current_username:
            return {"message": "The signed-in user could not be found.",
                    "status": False}
        if user.password != password:
            return {"message": "Incorrect password.",
                    "status": False}
        if new_username in self.userauthdata and new_username != current_username:
            return {"message": f"Username [{new_username}] is already in use.",
                    "status": False}

        user.username = new_username
        self.userauthdata.pop(current_username, None)
        self.userauthdata[new_username] = password
        self.authenticatedUser["user_data"]["uname"] = new_username
        logger.info("USER RENAME: Username changed successfully")
        return {"message": "Username changed successfully.",
                "status": True}

    def delete_user(self, username, password, data_directory):
        user = next(
            (user for user in self.users.values()
             if user.username == username),
            None,
        )
        if user is None:
            logger.warning("DELETE USER: User with username <%s> not found.", username)
            return {"message": f"User with username <{username}> not found.",
                    "status": False}
        if user.password != password:
            logger.warning("DELETE USER: Incorrect password entered for <%s>.", username)
            return {"message": "Incorrect password entered!",
                    "status": False}

        # WRITTEN BY AI
        try:
            data_root = Path(data_directory).resolve()
            user_directory = (data_root / user.userID).resolve()
            if user_directory.parent != data_root:
                logger.error(
                    "DELETE USER: Invalid data directory for user <%s>.",
                    username,
                )
                return {"message": "User data directory is invalid.",
                        "status": False}
            if user_directory.exists():
                shutil.rmtree(user_directory)
        except (OSError, RuntimeError, ValueError) as e:
            logger.error(
                "DELETE USER: Could not remove data directory for <%s>: %s",
                username,
                f"{type(e).__name__}:{e}",
            )
            return {"message": f"User data could not be deleted: {e}",
                    "status": False}

        self.users.pop(user.userID)
        self.userauthdata.pop(user.username, None)
        logger.info(
            "DELETE USER: User with username <%s> and userID <%s> is deleted.",
            username,
            user.userID,
        )
        return {"message": "Your account has been deleted.",
                "status": True}