# This module contains functions related to the user-login interface.
# Once the user logs in, the authentication data is passed to the todolist application to load authenticated data.

from pathlib import Path
import time, os, sys

from manager.user_manager import UserManager

User_Manager = UserManager()

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
        if Username == '!Q':
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
        if Username == '!Q':
            clear()
            return False        
        u_validity = check_username_validity(Username)
        print(u_validity["message"] if not u_validity["message"] == None else "",end="")
        if u_validity["status"]:
            Password = input("Enter password: ").strip()
            RegisterMethod = User_Manager.register(Username, Password)
            print(RegisterMethod["message"]), time.sleep(2), print("Please login again."), time.sleep(2)
            clear()
            if RegisterMethod["status"]:
                User_Manager.authdata()
                return True

# Saves the data created during the runtime of the process (if any)            
def save_udata(data_manager):
    userdata_export = User_Manager.exportData()
    if userdata_export["status"]:
        data_manager.save_data(userdata_export["data"])
        return {"status": True,
                "message":None}
    else:
        print(userdata_export)
        return {"status": False,
                "maessage": userdata_export["message"]}

def U_main(data_manager):
    while True:
        print("-"*15,"WELCOME TO PyLISTS", "-"*15)
        option = input("Login or register(L/R/Q for exit) >>>: ").upper().strip()
        if option == "L":
            clear()
            loginmethod = login()
            if loginmethod["status"]:
                return {"status":True,
                        "data":loginmethod["data"],
                        "message": None}
        elif option == "R":
            clear()
            if register():
                save_udata(data_manager=data_manager)
        elif option == "Q":
            return {"status": False,
                    "data": None,
                    "message": "user terminated login process"}
        else:
            print("INVALID OPTION!")
        print()
        time.sleep(2)
        clear()