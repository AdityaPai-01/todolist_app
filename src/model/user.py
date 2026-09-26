import uuid, logging

logger = logging.getLogger(__name__)

class User:
    def __init__(self, username, password, metadata=None, userID=None):
        self.userID = userID or str(uuid.uuid4())
        self.username = username
        self.password = password
        self.metadata = metadata

    def userdict(self):
        user_data = {self.userID: {"UserID": self.userID, "Username": self.username, "Password": self.password, "Metadata": self.metadata}}
        return {"message": None,
                "status": True,
                "data": user_data}

    def __repr__(self):
        return f"<UserID: {self.userID}, Username: {self.username}, Password: {self.password}, Metadata: {self.metadata}>"