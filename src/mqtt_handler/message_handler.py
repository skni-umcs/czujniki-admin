import json
import logging
from datetime import datetime
from src.database.core import get_db_session
from src.sensor.connector import unwrap_rssi, update_sensor_by_index
from src.sensor.exceptions import SensorNotFoundException
from src.sensor.schemas import SensorUpdate


def unwrap_message(payload:str):
    try:
        message = json.loads(payload)
    except Exception as e:
        logging.info("Error: failed to convert string message to json!")
        return


    with get_db_session() as db:
        pass #TODO: After sensor model and connector refactor