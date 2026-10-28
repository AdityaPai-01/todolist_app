from pathlib import Path
import time, os

# For theme and UI styling
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from manager.list_manager import ListManager
from manager.task_manager import TaskManager

List_Manager = ListManager()
console_theme = Theme({"title-card": "#9966CC", "desc-card":"#C8A2C8"})
console = Console(theme=console_theme)

def save_ldata(data_manager):
    listdata_export = List_Manager.export_data()
    if listdata_export["status"]:
        data_manager.save_data(listdata_export.get("data"))

def import_ldata(data_manager):
    data_load = data_manager.load_data()
    if data_load["status"]:
        List_Manager.import_data(data_load["data"])

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def create_newlist(listname):
    return List_Manager.new_list(listname)

def delete_existinglist(listname):
    return List_Manager.delete_list(listname)

def update_list(params):
    return List_Manager.rename_list(*params)

def add_task(list_object: TaskManager, params):
    return list_object.add_task(*params)

def remove_task(list_object: TaskManager, task_title):
    return list_object.delete_task(task_title)

def update_task_details(list_object: TaskManager, params):
    return None

def show_tasks(list_object: TaskManager):
    return list_object.show_tasks()

def mark_done(list_object: TaskManager, task_title):
    return list_object.mark_done(task_title)

def mark_pending(list_object: TaskManager, task_title):
    return list_object.mark_undone(task_title)

def change_working_list(listname):
    new_list = List_Manager.load_lists(listname)
    return new_list

def show_lists():
    all_lists = List_Manager.return_lists()
    for tlist in all_lists:
        print(tlist.list_name)

def help():
    functions = {
        "!hp":"help- displays all the functions of the program",
        "!ex":"exit- exits the application",
        "!at":"add task- adds new task in the todolist",
        "!st":"show tasks- shows tasks in the todolist, based on the requirements",
        "!dt":"delete task- deletes existing tasks",
        "!ut":"update task- updates the task details based on the requirements",
        "!md":"mark done- marks a task as completed",
        "!mp":"mark pending- marks a task as pending",
        "!nl":"new list- creates new todolist",
        "!dl":"delete list- deletes an existing list",
        "!ul":"update list- updates the list details based on parameters",
        "!cl":"change working list- changes the working todolist",
        "!sl":"show list- shows all the lists the user has created",
        "!us":"user settings- opens user settings interface" 
    }
    for k, v in functions.items():
        name, desc = v.split("-",1)
        line = Text()
        line.append(f"{k}: ")
        line.append(f"<{name}>".ljust(15), style="title-card")
        line.append(desc)
        console.print(line)

def greet(uname):
    text = Text("Hello, ")
    text.append(f"[{uname}]", style="title-card")
    text.append("!")
    return text

def app(condition, data_manager, username):
    import_ldata(data_manager)
    console.print(greet(username))
    time.sleep(2)
    clear()
    working_list = List_Manager.load_lists()
    while condition:
        option = console.input("Enter your option [desc-card](type '!hp' for help)[/] >>>: ").lower().strip()
        clear()
        if option == "!ex":
            break

        elif option == "!at":
            taskname = input("enter task title: ").strip()
            if not taskname:
                print("PLEASE ENTER VALID TITLE!")
                time.sleep(2)
                clear()
                continue
            task_filter = input("enter task filter: ").strip()
            task_description = input("enter task description: ").strip()
            at = add_task(working_list["data"], (taskname, task_filter if task_filter else None, task_description if task_description else None))
            print(at["message"])
            save_ldata(data_manager)
            time.sleep(2)

        elif option == "!st":
            tasks = show_tasks(working_list["data"])
            for task in tasks:
                print(task)
            input("enter anything to continue: ")

        elif option == "!hp":
            help()
            input("enter anything to continue: ")

        elif option == '!dt':
            print(remove_task(working_list["data"], task_title=console.input("Enter [desc-card]taskname[/] to [red]delete[/]: ").strip())["message"])
            time.sleep(2)
        elif option == '!md':
            print(mark_done(working_list["data"], task_title=console.input("Enter [desc-card]taskname[/] to [green]mark done[/]: ").strip())["message"])
            time.sleep(2)
        elif option == '!mp':
            print(mark_pending(working_list["data"], task_title=console.input("Enter [desc-card]taskname[/] to [#FF7F50] mark pending [/]: ").strip())["message"])
            time.sleep(2)
        elif option == "!nl":
            print(create_newlist(console.input("Enter [desc-card]list-name[/]: "))["message"])
            time.sleep(2)
        elif option == "!dl":
            print(delete_existinglist(console.input("Enter [desc-card]list-name[/] to [red]delete[/]: "))["message"])
            time.sleep(2)
        elif option == "!cl":
            console.print("[bold]All available lists: [/]")
            show_lists()
            working_list = change_working_list(console.input("Enter [desc-card]listname[/] to select list: "))
            print(working_list["message"])
            time.sleep(2)
        elif option == '!sl':
            console.print("[bold]All available lists: [/]")
            show_lists()
            input("enter anything to exit: ")
        elif option == "!wl":
            console.print(f"Current working list: [title-card]{working_list["data"].list_name}[/]")
            time.sleep(3)
        print()
        save_ldata(data_manager)    
        clear()