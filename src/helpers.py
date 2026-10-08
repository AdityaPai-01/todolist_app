from pathlib import Path
import time, os, sys

from manager.user_manager import UserManager
from manager.data_manager import JSONStorage
from manager.list_manager import ListManager

if getattr(sys, 'frozen', False): #Running script as .exe
    BaseDirectory = Path(sys.executable).resolve().parent.parent
else: #Running script as a script
    BaseDirectory = Path(__file__).resolve().parent.parent

DataDir = BaseDirectory / "data"
DataDir.mkdir(parents=True, exist_ok=True)
List_Manager = ListManager()
User_Manager = UserManager()
print(DataDir)

userdata_storage = JSONStorage(DataDir/"user_data.json")
listdata_storage = JSONStorage(DataDir / "list_data.json")
taskdata_storage = JSONStorage(DataDir / "task_data.json")

# Clearing the terminal for cleaner UI.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return "1: clear terminal executed"

def check_username_validity(username):
    specials = "!@#$%^&*()_+=-<>,?/'\'"
    if not username:
        return {"message": "Please enter valid username!",
                "status": False}
    elif len(username) < 8 or len(username) > 20:
        return {"message": "Your username must contain minimum 8 characters and maximum 20 characters!",
                "status": False}
    for sp in specials:
        if sp in username:
            return {"message": "Special characters except '.' and '_' aren't allowed in usernames!",
                    "status": False}
    else:
        return {"message": None,
                "status": True}
    
def login():
    while True:
        Username = input("Enter your username: ").strip()
        if Username == '!Q':
            clear()
            return False
        Password = input("Enter your password: ").strip()
        LoginMethod = User_Manager.login(Username, Password)
        print(LoginMethod["message"])
        time.sleep(1)
        clear()
        if LoginMethod["status"]:
            return True
        
def register():
    while True:
        Username = input("Enter username: ").strip()
        if Username == '!Q':
            clear()
            return True        
        u_validity = check_username_validity(Username)
        print(u_validity["message"] if not u_validity["message"] == None else f"-"*15)
        if u_validity["status"]:
            Password = input("Enter password: ").strip()
            RegisterMethod = User_Manager.register(Username, Password)
            print(RegisterMethod["message"]), time.sleep(2), print("Please login again."), time.sleep(2)
            clear()
            if RegisterMethod["status"]:
                User_Manager.authdata()
                return True
            
def save_udata():
    userdata_export = User_Manager.exportData()
    if userdata_export["status"]:
        userdata_storage.save_data(userdata_export["data"])

def save_ldata():
    listdata_export = List_Manager.export_data()
    if listdata_export["status"]:
        listdata_storage.save_data({listdata_export["data"]})

def save_tdata(tlist_obj):
    taskdata_export = tlist_obj.export_data()

def initial_interface():
    if not List_Manager.lists:
        List_Manager.new_list("My List 1")
        save_ldata()
    current_list = List_Manager.return_lists()[0]
    