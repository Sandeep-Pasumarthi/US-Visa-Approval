from from_root import from_root
from datetime import datetime

import logging
import os


LOG_FILE = f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log"
LOG_DIR = "logs"
LOGS_PATH = os.path.join(from_root(), LOG_DIR, LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOGS_PATH,
    level=logging.INFO,
    format="[%(asctime)s]:%(levelname)s:%(name)s:%(message)s"
)
