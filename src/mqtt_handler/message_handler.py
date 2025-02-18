import json
import logging
from datetime import datetime

from src.dependecies import get_db
from src.module.connector import unwrap_rssi
from src.module.exceptions import ModuleNotFoundException


def unwrap_message(payload:str):
    message = json.loads(payload)
    module_codes = message['module_codes'].split(',')
    rssis = message['hop_rssis'].split(',')
    time = str(datetime.now())
    db = get_db()
    for module_code in module_codes:
        try:
            unwrap_rssi(db, module_code, float(rssis.pop()), time)
        except ModuleNotFoundException as e:
            logging.info("No module with said name, skipping...")