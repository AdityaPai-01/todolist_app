import uuid, logging
from manager.task_manager import TaskManager

logger = logging.getLogger(__name__)

class ListManager:
    def __init__(self):
        self.lists = {}

    def new_list(self, list_name="My List 1"):
        try:
            if self.lists:
                for values in self.lists.values():
                    if list_name != values.list_name:
                        tasklist = TaskManager(list_name=list_name, list_id=("TASKLIST-"+str(uuid.uuid4())))
                        self.lists.update({tasklist.list_id : tasklist})
                        logger.info(f"CREATE LIST: New list created with title: <{list_name}>")
                        return {"message": f"Created list with title <{list_name}>",
                                "data": tasklist,
                                "status": True}
            
                logger.warning(f"CREATE LIST: List with title <{list_name}> exists.")
                return {"message": f"List with title <{list_name}> already exists!",
                        "data": None,
                        "status": False}
            else:
                tasklist = TaskManager(list_name=list_name, list_id=("TASKLIST-"+str(uuid.uuid4())))
                self.lists.update({tasklist.list_id : tasklist})
                logger.info(f"CREATE LIST: New list created with title: <{list_name}>")
                return {"message": f"Created list with title <{list_name}>",
                        "data": tasklist,
                        "status": True}
        except Exception as e:
            logger.error(f"ERROR: NEW-LIST: List could not be created: {type(e).__name__}: {e}")
            return {"message": f"List could not be created: {type(e).__name__}: {e}",
                    "status": False,
                    "data": None}


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
            for k,v in self.lists.items():
                taskdata = v.export_data()
                data.update({str(k):{"list_id": str(v.list_id), "list_name": v.list_name, "tasks":taskdata["data"]}})
            logger.info(f"DATA EXPORT: Data exported successfully")
            return {"message": None,
                    "status": True,
                    "data": data}
        
        except Exception as e:
            logger.error(f"DATA EXPORT: Failed to export data: {type(e).__name__}:{e}")
            return {"message": "something went wrong.",
                    "status": False,
                    "data": {}}


    def import_data(self, data_dir):
        try:
            for id in data_dir.keys():
                tasklist_object = TaskManager(id, data_dir[id]["list_name"])
                for task in data_dir[id]["tasks"].values():
                    tasklist_object.add_task(
                    title=task["task_name"],
                    task_id=task["task_id"],
                    task_status=task["task_status"],
                    task_desc=task["task_description"],
                    task_filter=task["task_filter"]
                )      
                self.lists.update({id: tasklist_object})
            logger.info(f"LIST DATA IMPORT: Data imported successfully.")
            return {"message": None,
                    "status": True}
        
        except Exception as e:
            logger.error(f"DATA IMPORT: Failed to import data: {type(e).__name__}:{e}")
            return {"message": "something went wrong.",
                    "status": False}


    def return_lists(self):
        lists = []
        for list in self.lists.values():
            lists.append(list)
            return lists 

    def load_lists(self, listname="My List 1"):
        if self.lists:
            for tlist in self.lists.values():
                if not listname == tlist.list_name:
                    continue
                logger.info(f"LOAD TASK-LIST: Task list with name <{listname}> was loaded.")
                return {"message": None,
                        "status": True,
                        "data": tlist}
        else:
            return self.new_list(listname)
        logger.error(f"LOAD LIST ERROR: Tasklist with name <{listname}> not found in the database")
        return {"message": f"Tasklist <{listname}> not found",
                "status": False,
                "data": None}
