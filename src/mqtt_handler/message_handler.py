import json
import logging
from src.database.core import get_db_session
from src.sensor.connector import update_sensor_data


def unwrap_message(payload:str):
    try:
        logging.info(f'Unwrapping message: {payload}')
        message = json.loads(payload)
    except Exception as e:
        logging.info(e)
        return

    # keys might finally be different, keep in mind
    sensor_code = message.get('sensor_code')
    new_rssi = message.get('rssi')
    new_cpu_temp = message.get('cpu_temp')
    new_sensor_noise = message.get('sensor_noise')

    with get_db_session() as db:
        update_sensor_data(db,sensor_code,new_rssi,new_cpu_temp,new_sensor_noise)