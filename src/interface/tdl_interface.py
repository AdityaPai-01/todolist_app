from pathlib import Path
import time, os, sys

from manager.data_manager import JSONStorage
from manager.list_manager import ListManager
from manager.task_manager import TaskManager

if getattr(sys, 'frozen', False): #Running script as .exe
    BaseDirectory = Path(sys.executable).resolve().parent.parent
else: #Running script as a script
    BaseDirectory = Path(__file__).resolve().parent.parent

DataDir = BaseDirectory / "data"
DataDir.mkdir(parents=True, exist_ok=True)

List_Manager = ListManager()
listdata_storage = JSONStorage(DataDir / "list_data.json")

def save_ldata():
    listdata_export = List_Manager.export_data()
    if listdata_export["status"]:
        listdata_storage.save_data({listdata_export["data"]})