from pathlib import Path
import time, os, sys

from manager.data_manager import JSONStorage
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

def app(condition, data_manager):
    pass