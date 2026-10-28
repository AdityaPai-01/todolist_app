# This module contains functions related to the user-login interface.
# Once the user logs in, the authentication data is passed to the todolist application to load authenticated data.

from pathlib import Path
import time, os

# For theme and UI styling
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from manager.user_manager import UserManager

console_theme = Theme({})
console = Console(theme=console_theme)
User_Manager = UserManager()
default_metadata = {"selected_theme": "raspberry",
                    "default_list": "My List 1"}

# Clearing the terminal for cleaner UI.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return "1: clear terminal executed"

# Checks the validity of the username created by the user
def check_username_validity(username):
    specials = "!@#$%^&*()_+=-<>,?/'\'"
    if not username:
        return {"message": "Please enter valid username!",
                "status": False}
    elif len(username) < 8 or len(username) > 20:
        return {"message": "Your username must contain minimum 8 characters and maximum 20 characters!",
                "status": False}
    for sp in specials:
        if sp in username and sp not in "._":
            return {"message": "Special characters except '.' and '_' aren't allowed in usernames!",
                    "status": False}
    else:
        return {"message": None,
                "status": True}

# Allows the user to login to their account   
def login():
    while True:
        Username = input("Enter your username: ").strip()
        if Username == 'Q':
            clear()
            return {"status": False,
                    "data": None}
        Password = input("Enter your password: ").strip()
        LoginMethod = User_Manager.login(Username, Password)
        print(LoginMethod["message"])
        time.sleep(1)
        clear()
        if LoginMethod["status"]:
            return {"status": True,
                    "data":User_Manager.authenticatedUser}

# Allows the new user to create a new account      
def register():
    while True:
        Username = input("Enter username: ").strip()
        if Username == 'Q':
            clear()
            return False        
        u_validity = check_username_validity(Username)
        print(u_validity["message"] if not u_validity["message"] == None else "",end="")
        if u_validity["status"]:
            Password = input("Enter password: ").strip()
            RegisterMethod = User_Manager.register(
                Username, Password, default_metadata.copy()
            )
            print(RegisterMethod["message"]), time.sleep(2), print("Please login again."), time.sleep(2)
            clear()
            if RegisterMethod["status"]:
                User_Manager.authdata()
                return True

def delete_user(user_data_manager):
    while True:
        username = input("Enter username: ").strip()
        if username == 'Q':
            clear()
            return False
        u_validity = check_username_validity(username)
        print(u_validity["message"] if not u_validity["message"] == None else "",end="")
        if u_validity["status"]:
            password = input("Enter password: ").strip()
            delete = User_Manager.delete_user(
                username, password, user_data_manager.dataPath.parent
            )
            print(delete["message"]), time.sleep(2), clear()
            if delete["status"]: 
                print("You will be logged out of your account, application will close."), time.sleep(2), time.sleep, clear()
                return True
            return False

def change_theme(themes):
    console.print("Available themes:")
    for theme_name, theme_styles in themes.items():
        console.print(theme_name, style=theme_styles["title-card"])

    while True:
        selected_theme = console.input(
            "Enter a theme name to preview ([desc-card]Q[/] to cancel): "
        ).strip().lower()
        clear()
        if selected_theme == "q":
            return None
        if selected_theme not in themes:
            console.print("Please enter a valid theme name.")
            continue

        theme_console = Console(theme=Theme(themes[selected_theme]),
                                color_system="truecolor")
        theme_console.print("[header-card]Your current todolist:[/]")
        theme_console.print("Buy groceries", style="title-card")
        theme_console.print("Task description: Milk, bread, and fruit",
                            style="desc-card")
        theme_console.print("[warning-card]PLEASE ENTER A VALID OPTION[/]")

        answer = console.input(
            f"Select the {selected_theme} theme? (y/n): "
        ).strip().lower()
        clear()
        if answer == "y":
            return selected_theme
        if answer != "n":
            console.print("Please enter y or n.")

def change_username(username, user_data_manager):
    password = console.input("Enter your password to confirm: ").strip()
    if not password or password.upper() == "Q":
        return {"message": "Username change cancelled.",
                "status": False}

    new_username = console.input("Enter your new username: ").strip()
    if not new_username or new_username.upper() == "Q":
        return {"message": "Username change cancelled.",
                "status": False}

    validity = check_username_validity(new_username)
    if not validity["status"]:
        return {"message": validity["message"],
                "status": False}

    rename_result = User_Manager.rename_user(username, new_username, password)
    if not rename_result["status"]:
        return rename_result

    save_result = save_udata(user_data_manager)
    if not save_result["status"]:
        User_Manager.rename_user(new_username, username, password)
        return {"message": f"Username could not be saved: {save_result['message']}",
                "status": False}

    return {"message": "Username changed successfully.",
            "status": True,
            "username": new_username}

def select_default_list(available_lists):
    if not available_lists:
        console.print("No lists are available to select.")
        return None

    console.print("Available lists:")
    for task_list in available_lists:
        console.print(f"- {task_list.list_name}")

    while True:
        selected_list = console.input(
            "Enter the default list name (Q to cancel): "
        ).strip()
        if selected_list.upper() == "Q":
            return None
        for task_list in available_lists:
            if task_list.list_name == selected_list:
                return selected_list
        console.print("Please enter one of the listed names.")

def change_password():
    pass

# Saves the data created during the runtime of the process (if any)            
def save_udata(data_manager):
    userdata_export = User_Manager.exportData()
    if userdata_export["status"]:
        save_result = data_manager.save_data(userdata_export["data"])
        return {"status": save_result["status"],
                "message": save_result["message"]}
    else:
        print(userdata_export)
        return {"status": False,
                "message": userdata_export["message"]}

def user_login(data_manager):
    while True:
        print("-"*15,"WELCOME TO PyLISTS", "-"*15)
        option = console.input("Login or register ([#C51E3A]L[/]/[#90EE90]R[/]/[#6CB4EE]Q[/] for exit) >>>: ").upper().strip()
        clear()
        if option == "L":
            loginmethod = login()
            if loginmethod["status"]:
                return {"status":True, "data":loginmethod["data"], "message": None}
        elif option == "R":
            if register():
                save_udata(data_manager=data_manager)
        elif option == "Q":
            return {"status": False, "data": None, "message": "user terminated login process"}
        else:
            print("INVALID OPTION!")
        print()
        time.sleep(2)
        clear()

def user_settings_interface(username, theme, all_themes, user_metadata,
                            user_data_manager, available_lists):
    usi_console = Console(theme=theme)
    while True:
        usi_console.print(f"Hello, [title-card]{username}[/]!")
        usi_console.print("[header-card]User settings[/]")
        usi_console.print("[desc-card]!cu[/] - Change username")
        usi_console.print("[desc-card]!ct[/] - Change theme")
        usi_console.print("[desc-card]!sl[/] - Set default list")
        usi_console.print("[desc-card]!da[/] - Delete account")
        usi_console.print("[desc-card]!ex[/] - Return to todolist")

        option = usi_console.input("Choose an option: ").lower().strip()
        clear()

        if option == "!ex":
            return {"message": None,
                    "status-code": 0}

        elif option == "!cu":
            rename_result = change_username(username, user_data_manager)
            if rename_result["status"]:
                return {"message": None,
                        "status-code": 4,
                        "username": rename_result["username"]}
            else:
                usi_console.print(
                    f"[warning-card]{rename_result['message']}[/]"
                )

        elif option == "!ct":
            selected_theme = change_theme(all_themes)
            if selected_theme is not None:
                previous_theme = user_metadata["selected_theme"]
                user_metadata["selected_theme"] = selected_theme
                save_result = save_udata(user_data_manager)
                if save_result["status"]:
                    return {"message": None,
                            "status-code": 2}

                user_metadata["selected_theme"] = previous_theme
                usi_console.print(
                    f"[warning-card]Theme could not be saved: "
                    f"{save_result['message']}[/]"
                )

        elif option == "!sl":
            selected_list = select_default_list(available_lists)
            if selected_list is not None:
                previous_list = user_metadata["default_list"]
                user_metadata["default_list"] = selected_list
                save_result = save_udata(user_data_manager)
                if save_result["status"]:
                    return {"message": None,
                            "status-code": 3,
                            "default_list": selected_list}

                user_metadata["default_list"] = previous_list
                usi_console.print(
                    f"[warning-card]Default list could not be saved: "
                    f"{save_result['message']}[/]"
                )

        elif option == "!da":
            delete = delete_user(user_data_manager)
            if delete:
                save_udata(user_data_manager)
                return {"message": None,
                        "status-code":1}

        else:
            usi_console.print("[warning-card]Please enter a valid command.[/]")
        time.sleep(2)
        clear()