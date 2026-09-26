from pathlib import Path
import json, logging

logger = logging.getLogger(__name__)

class JSONStorage():
    def __init__(self, Base_Directory):
        self.dataPath = Base_Directory
        self.dataPath.parent.mkdir(parents=True, exist_ok=True)

    # Loads and sets the data for the user manager class
    def load_data(self):
        try:
            if not self.dataPath.exists():
                self.dataPath.touch()
                self.dataPath.write_text("{}")
                logger.info("Data loading: Data file created successfully")
                return {"message": None,
                        "status": True,
                        "data": {}}
            
            with open(self.dataPath, "r") as dataFile:
                data = json.load(dataFile)
                logger.info("Data loading: Data loaded successfully")
                return {"message": None,
                        "status": True,
                        "data": data}
        except Exception as e:
            logger.error("Data loading: Data loading failed: %s", e)
            return {"message": e,
                    "status": False,
                    "data": None}

    # Saves the data passed by the user manager class
    def save_data(self, rawData):
        try:
            if self.dataPath.exists():
                with open(self.dataPath, "w") as dataFile:
                    json.dump(rawData["data"], dataFile, indent=4)
                logger.info("Data saving: Data saved successfully")
                return {"message": None,
                        "status": True}
            logger.error("Data saving: Data could not be saved because the data file does not exist")
            return {"message": "Data file does not exist",
                    "status": False}
        except Exception as e:
            logger.error("Data saving: Data saving failed: %s", e)
            return {"message": e,
                    "status": False}