import uuid, logging
from manager.task_manager import TaskManager

logger = logging.getLogger(__name__)

class ListManager:
    def __init__(self):
        self.lists = {}

    def new_list(self, list_name):
        if list_name not in self.lists.values():
            tasklist = TaskManager(list_name=list_name, list_id=uuid.uuid4())
            self.lists.update({tasklist.list_id : tasklist.list_name})
            logger.info("CREATE LIST: New list created with title: <{list_name}>", list_name)
            return {"message": f"Created list with title <{list_name}>",
                    "status": True}
        
        logger.warning("CREATE LIST: List with title <{list_name}> exists.", list_name)
        return {"message": f"List with title <{list_name}> already exists!",
                "status": False}


    def rename_list(self, old_list_name, new_list_name):
        if not old_list_name in self.lists.values():
            logger.warning(f"REMANE LIST: List with title <{old_list_name}> does not exist.")
            return {"message": f"You do not have list with title <{old_list_name}>!",
                    "status": False}
        
        if new_list_name in self.lists.values():
            logger.warning(f"RENAME LIST: List with the title <{new_list_name}> already exists.")
            return {"message": f'List with the title <{new_list_name}> already exists.',
                    "status": False}
        
        for k in self.lists.keys():
            if self.lists[k] == old_list_name:
                self.lists[k] == new_list_name
                logger.info(f"RENAME LIST: List <{old_list_name}> renamed to <{new_list_name}>")
                return {"message": f"List <{old_list_name}> renamed to <{new_list_name}>",
                        "status": True}
            

    def delete_list(self, list_name):
        if not list_name in self.lists.values():
            logger.warning(f"DELETE LIST: List with title <{list_name}> does not exist.")
            return {"message":f"You do not have a list named <{list_name}>!",
                    "status": False}
        
        for k in self.lists.items():
            if self.lists[k] == list_name:
                self.lists.pop(k)
                logger.info(f"DELETE LIST: Successfully deleted list with title <{list_name}>.")
                return {"message": f"List <{list_name}> removed.",
                        "status": True}


    def export_data(self):
        try:
            data = {}
            for id in self.lists.keys():
                data.update({id: {"list_id": id, "list_name": self.lists[id]}})
            logger.info(f"DATA EXPORT: Data exported successfully")
            return {"message": None,
                    "status": True,
                    "data": data}
        
        except Exception as e:
            logger.error(f"DATA EXPORT: Failed to export data: {e}")
            return {"message": "something went wrong.",
                    "status": False,
                    "data": {}}


    def import_data(self, data_dir):
        try:
            for id in data_dir.keys():
                self.lists.update({id: data_dir[id]["list_name"]})
            logger.info(f"LIST DATA IMPORT: Data imported successfully.")
            return {"message": None,
                    "status": True}
        
        except Exception as e:
            logger.error(f"DATA IMPORT: Failed to import data: {e}")
            return {"message": "something went wrong.",
                    "status": False}


    def return_lists(self):
        lists = []
        for list in self.lists.values():
            lists.append(list)
            return lists 