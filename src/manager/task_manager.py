import uuid, logging
from model.task import Task

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, list_id, list_name="My List 1"):
        self.list_name = list_name
        self.list_id = list_id
        self.tasklist = []

    # Adds a task to the todolist  
    def add_task(self, title, task_filter, task_desc):
        task = Task(taskname=title, task_id=uuid.uuid4(), task_description= task_desc, task_filter=task_filter)
        self.tasklist.append(task)
        logger.info(f"TASK CREATE: Created new task with title <{title}> in list <{self.list_name}>")
        return {"message":'Task added to your todolist!',
                "status": True}

    # Deletes the task from the todolist
    def delete_task(self, title: str):
        for task in self.tasklist:
            if title == task.to_dict()['taskname']:
                self.tasklist.remove(task)
                logger.info(f"TASK DELETE: Deleted task with title <{title}> in list <{self.list_name}>.")
                return {"message":'Task removed from your todolist!',
                        "status": True}
        logger.warning(f"TASK DELETE: failed to delete: Task <{title}> not in list <{self.list_name}>")
        return {"message":f'Task <{title}> not found in your todolist!',
                "status": False}

    # Updates the task's title
    def update_taskname(self, oldtitle: str, newtitle: str):
        for task in self.tasklist:
            if task.taskname == oldtitle:
                task.taskname = newtitle  # Directly updates the object's attribute
                logger.info(f"TASK RENAME: Renamed task <{oldtitle}> to <{newtitle}> in list <{self.list_name}>")
                return {"message":f'Task name changed from <{oldtitle}> to <{newtitle}>!',
                        "status": True}
        logger.warning(f"TASK RENAME: failed to rename: Task <{oldtitle}> not in list <{self.list_name}>")
        return {"message": f'Task <{oldtitle}> not found in your todolist!',
                "status": False}
    
    def show_tasks(self, filter=None):
        if filter == None:
            return [str(t) for t in self.tasklist] if self.tasklist else ['Your task list is empty!']

    # Returns relevant data about the task objects to be stored in local storage
    def export_data(self):
        try:
            data = {}
            for task in self.tasklist:
                task_dict = task.to_dict()
                data[str(task_dict['task_id'])] = {
                    "task_id": task_dict['task_id'],
                    "task_name": task_dict['task_name'],
                    "task_status": task_dict['task_status'],
                    "task_filter": task_dict["task_filter"],
                    "task_description": task_dict["task_description"]
                }
            logger.info(f"TASK DATA EXPORT: Data exported successfully")
            return {"message": None,
                    "status": True,
                    "data": data}

        except Exception as e:
            logger.error(f"TASK DATA EXPORT: Failed to export data: {e}")
            return {"message": "something went wrong.",
                    "status": False,
                    "data": {}}


    # Creates task objects from the extracted data from local storage, adds it to the list
    def import_data(self, data_dir):
        try:
            for t_id, task_details in data_dir.items():
                status = False if task_details["task_status"] == '⭕' else True
                task_obj = Task(task_id=t_id, taskname=task_details["task_name"], is_completed=status, task_filter=task_details["task_filter"], task_description=task_details["task_description"])
                self.tasklist.append(task_obj)
            logger.info(f"TASK DATA IMPORT: Data imported successfully.")
            return {"message": None,
                    "status": True}

        except Exception as e:
            logger.error(f"TASK DATA IMPORT: Failed to import data: {e}")
            return {"message": "something went wrong.",
                    "status": False}

    # Marks the given task as complete, identified using its title
    def mark_done(self, title: str):
        for task in self.tasklist:
            if task.taskname == title:
                task.mark_complete()
                logger.info(f"TASK MARKED DONE: Marked task <{title}> completed in list <{self.list_name}>")
                return {"message":f"Task <{title}> marked as completed!",
                        "status": True}
        logger.warning(f"TASK MARKED DONE: failed to mark task: Task <{title}> not in list <{self.list_name}>")
        return {"message":f"Task <{title}> not found in your todolist!",
                "status": False}