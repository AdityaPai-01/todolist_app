from model.user import User
import logging

logger = logging.getLogger(__name__)

#This class manages the user objects and performs certain operations to manage the database
class UserManager():
    def __init__(self):
        self.users = {} #Stores userdata()during the runtime of application
        self.authenticatedUser = []
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
        self.authenticatedUser.append(username)
        logger.info("USER LOGIN: User logged in successfully")
        return {"message": "Login successful!",
                "status": True}

    # Register function, enables the user to register themselves (create an account) in the application's database
    def register(self, Username, Password):
        if Username in self.userauthdata.keys():
            logger.warning("USER REGISTERATION: User '%s' already exists", Username)
            return {"message": f"User [{Username}] already exists!",
                    "status": False}
        else:
            newUser = User(Username, Password)
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
            logger.error("USER DATA IMPORT: User data import failed: %s", e)
            return {"message":e,
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
            logger.error("USER DATA EXPORT: Could not export user data: %s", e)
            return {"message": f"Could not export data.\n{e}",
                    "status": False}
    
    #Seperates and collects only the data required for login/registeration functions
    def authdata(self):
        try:
            for k, v in self.users.items():
                for key, value in v.userdict()["data"].items():
                    self.userauthdata.update({value["Username"] : value["Password"]})
            logger.info("USER DATA AUTHENTICATION: Authentication data loaded successfully")
            return {"message": None,
                    "status": True}
        except Exception as e:
            logger.error("USER DATA AUTHENTICATION: Authentication data loading failed: %s", e)
            return {"message": e,
                    "status": False}