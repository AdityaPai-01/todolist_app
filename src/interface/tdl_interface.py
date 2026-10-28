from pathlib import Path
import time, os

# For theme and UI styling
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from manager.list_manager import ListManager
from manager.task_manager import TaskManager
from interface.ul_interface import user_settings_interface

List_Manager = ListManager()
themes = {"raspberry": 
          {"title-card": "#9966CC",
            "desc-card": "#B284BE",
            "header-card": "bold",
            "warning-card": "bold italic #8B004B"},

            "tangerine":
            {"title-card":"#FF4F00",
             "desc-card": "#FF7F50",
             "header-card":"bold #FBCEB1",
             "warning-card":"bold italic #BF5700"},

             "apple":
             {"title-card":"#FE6F5E",
              "desc-card":"#AB274F",
              "header-card":"bold #FDBCB4",
              "warning-card": "bold italic #800020"},

              "fresh":
              {"title-card": "#76FF7A",
               "desc-card": "#29AB87",
               "header-card": "bold #E3F988",
               "warning-card": "bold italic #00693E"}
             }


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

def show_tasks(list_object: TaskManager, con):
    tasks = list_object.show_tasks()
    if tasks:
        con.print("[header-card]Your current todolist: [/]")
        for task in tasks:
            con.print(task)
    else:
        con.print(tasks)

def mark_done(list_object: TaskManager, task_title):
    return list_object.mark_done(task_title)

def mark_pending(list_object: TaskManager, task_title):
    return list_object.mark_undone(task_title)

def change_working_list(listname):
    new_list = List_Manager.load_lists(listname)
    return new_list

def show_lists(con):
    all_lists = List_Manager.return_lists()
    for tlist in all_lists:
        con.print(f"[title-card]{tlist.list_name}[/]")


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


def greet(uname):
    text = Text("Hello, ")
    text.append(f"[{uname}]", style="title-card")
    text.append("!")
    return text

def app(condition, data_manager, username, user_metadata, user_data_manager):
    import_ldata(data_manager)
    con_theme = Theme(themes[user_metadata["selected_theme"]])
    console = Console(theme=con_theme,color_system="truecolor")
    working_list = List_Manager.load_lists(user_metadata["default_list"])
    while condition:
        console.print(greet(username))
        show_tasks(working_list["data"],console)
        option = console.input("Enter your option [desc-card](type '!hp' for help)[/] >>>: ").lower().strip()
        clear()
        if option == "!ex":
            return {"message": None,
                    "status-code":0}
        
        elif option == "!at":
            taskname = console.input("Enter task title: ").strip()
            if not taskname:
                console.print("[warning-card]Please enter a task title.[/]")
                time.sleep(2)
                clear()
                continue
            task_filter = console.input("Enter task filter: ").strip()
            task_description = console.input("Enter task description: ").strip()
            at = add_task(working_list["data"], (taskname, task_filter if task_filter else None, task_description if task_description else None))
            console.print(at["message"])
            save_ldata(data_manager)
            time.sleep(2)

        elif option == "!st":
            show_tasks(working_list["data"], console)
            console.input("Press Enter to continue: ")

        elif option == "!hp":
            for k, v in functions.items():
                name, desc = v.split("-",1)
                line = Text()
                line.append(f"{k}: ")
                line.append(f"<{name}>".ljust(15), style="title-card")
                line.append(desc)
                console.print(line)
            console.input("Press Enter to continue: ")

        elif option == '!dt':
            console.print(remove_task(working_list["data"], task_title=console.input("Enter task name to delete: ").strip())["message"])
            time.sleep(2)

        elif option == '!md':
            console.print(mark_done(working_list["data"], task_title=console.input("Enter task name to mark done: ").strip())["message"])
            time.sleep(2)

        elif option == '!mp':
            console.print(mark_pending(working_list["data"], task_title=console.input("Enter task name to mark pending: ").strip())["message"])
            time.sleep(2)

        elif option == "!nl":
            console.print(create_newlist(console.input("Enter list name: "))["message"])
            time.sleep(2)

        elif option == "!dl":
            listname = console.input("Enter list name to delete: ").strip()
            if not working_list["data"].list_name == listname:
                console.print(delete_existinglist(listname)["message"])
                time.sleep(2)
            else:
                console.print(f"The list [red]<{listname}>[/] is currently being used, hence it can't be deleted!")
                time.sleep(2)

        elif option == "!cl":
            console.print("[header-card]All available lists: [/]")
            show_lists(console)
            working_list = change_working_list(console.input("Enter list name to select: "))
            console.print(working_list["message"])
            time.sleep(2)

        elif option == '!sl':
            console.print("[header-card]All available lists: [/]")
            show_lists(console)
            console.input("Press Enter to return: ")
            
        elif option == "!wl":
            console.print(f"Current working list: [title-card]{working_list["data"].list_name}[/]")
            time.sleep(3)

        elif option == "!us":
            user_settings = user_settings_interface(
                username,
                theme=con_theme,
                all_themes=themes,
                user_metadata=user_metadata,
                user_data_manager=user_data_manager,
                available_lists=List_Manager.return_lists(),
            )
            if user_settings["status-code"] == 1:
                return {"message": None,
                        "status-code":1}
            elif user_settings["status-code"] == 2:
                con_theme = Theme(themes[user_metadata["selected_theme"]])
                console = Console(theme=con_theme, color_system="truecolor")
            elif user_settings["status-code"] == 3:
                working_list = List_Manager.load_lists(
                    user_settings["default_list"]
                )
            elif user_settings["status-code"] == 4:
                username = user_settings["username"]
        else:
            console.print("[warning-card]PLEASE ENTER A VALID OPTION[/]")
            time.sleep(2)
        print()
        save_ldata(data_manager)    
        clear()