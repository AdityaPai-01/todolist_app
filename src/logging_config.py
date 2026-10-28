import logging
from pathlib import Path

logfile = Path(__file__).resolve().parent.parent/"data"/"log_data.log"

# setting up log
def setup_log(log_file=logfile):
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        handlers=[logging.FileHandler(log_file, encoding='utf-8')])