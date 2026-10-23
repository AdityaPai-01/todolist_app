from pathlib import Path
import time, os, sys

from manager.list_manager import ListManager
from manager.task_manager import TaskManager

if getattr(sys, 'frozen', False): #Running script as .exe
    BaseDirectory = Path(sys.executable).resolve().parent.parent.parent
else: #Running script as a script
    BaseDirectory = Path(__file__).resolve().parent.parent.parent

List_Manager = ListManager()

def save_ldata(data_manager):
    listdata_export = List_Manager.export_data()
    if listdata_export["status"]:
        data_manager.save_data({listdata_export["data"]})
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def create_newlist(listname):
    return List_Manager.new_list(listname)

def delete_existinglist(listname):
    return List_Manager.delete_list(listname)

def rename_existinglist(old_listname, new_listname):
    return List_Manager.rename_list(old_listname, new_listname)

def add_task(list_object, params):
    return list_object.add_task(*params)

def remove_task(list_object):
    pass

def update_task_details(list_object):
    pass

def show_tasks(list_object):
    return list_object.show_tasks()

def mark_done(list_object):
    pass

def app(condition, data_manager):
    while condition:
        working_list = List_Manager.new_list()["data"]
        option = input("Enter an option: ").lower().strip()
        if option == "!q":
            break

        elif option == "!nt":
            taskname = input("enter task title: ").strip()
            task_filter = input("enter task filter: ").strip()
            task_description = input("enter task description")
            at = add_task(working_list, (taskname, task_filter if task_filter else None, task_description if task_description else None))
            print(at["message"])
            save_ldata(data_manager)

        elif option == "!st":
            tasks = show_tasks(working_list)
            for task in tasks:
                print(task)
            input("enter anything: ")
        print()    
        clear()