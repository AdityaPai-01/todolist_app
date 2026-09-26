import logging
logger = logging.getLogger(__name__)

class Task:
    def __init__(self, taskname, task_id, task_filter, task_description, is_completed=False):
        self.taskname: str = taskname
        self.task_id: str = task_id
        self.is_completed: bool = is_completed
        self.task_filter = task_filter
        self.task_description = task_description

    # Used to display only the necessary information about the task
    def __str__(self):
        if self.is_completed:
            return f'✅: {self.taskname} ({self.task_filter})'
        return f'⭕: {self.taskname} ({self.task_filter})'

    # Useful to return data in the form of dictionary, to be stored in JSON format
    def to_dict(self):
        return {"task_id": self.task_id, 
                "task_name":self.taskname, 
                "task_status":'✅' if self.is_completed else '⭕',
                'task_filter': self.task_filter,
                'task_description':self.task_description}

    # Marks the task as complete
    def mark_complete(self):
        self.is_completed = True