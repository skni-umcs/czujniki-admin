import logging
from .exceptions import SensorIdTakenException
from ..database.core import get_db_session
from ..logs.logger import Logger
from .connector import create_new_sensor
import requests

def request_sensors_json_from_backend():
    response = requests.get("https://czujniki.skni.umcs.pl/api/sensors?size=80")
    return response.json()

def parse_backend_data(data):
    try:
        sensors = []
        for sensor in data['content']:
            sensors.append({
                'sensor_id': sensor['id'],
                'sensor_name': sensor['location']['facultyName'],
                'sensor_latitude': sensor['location']['latitude'],
                'sensor_longitude': sensor['location']['longitude']
            })
        return sensors

    except KeyError as e:
        print(f"Error retrieving key: {e}")
        return []

def sync_sensors_data():
    logging.info("Starting sensors data sync from backend.")
    sensors = parse_backend_data(request_sensors_json_from_backend())

    if sensors is None:
        Logger.write("Sync failed: No sensors data retrieved from backend.")
        return
    with  get_db_session() as db:
        for sensor in sensors:
            try:
                create_new_sensor(db, sensor['sensor_id'], sensor['sensor_name'], sensor['sensor_latitude'], sensor['sensor_longitude'], 1200)
                logging.info(f"Sensor with id {sensor['sensor_id']} added successfully.")
                Logger.write(f"Sensor with id {sensor['sensor_id']} added by synchronizing with climate backend data.")
            except SensorIdTakenException:
                logging.info(f"Sensor with id {sensor['sensor_id']} already exists. Skipping.")
            continue

    logging.info("Sensors data sync from backend completed.")