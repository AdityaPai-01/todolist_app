import logging
from pathlib import Path

logfile = Path(__file__).resolve().parent.parent/"data"/"log_data.log"

# setting up log
def setup_log():
    try:
        logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        handlers=[logging.FileHandler(logfile, encoding='utf-8')])
    except Exception as e:
        return f"Error: {e}"
    