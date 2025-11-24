import logging
from time import time
from datetime import datetime
from src.frequency.connector import create_new_frequency_period
from src.logs.logger import Logger
from src.sensor.models import DBSensor
from src.database.core import get_db_session
from config import Settings
from src.sensor_data.models import DBSensorData

sett = Settings()

def create_gateway_sensor():
    with get_db_session() as db:
        gateway = DBSensor(sensor_id=0,
                           sensor_faculty="Gateway",
                           sensor_latitude=0.0,
                           sensor_longitude=0.0,
                           sensor_status=1,
                           last_message_timestamp=time(),
                           last_message_type="Gateway Init")

        db.add(gateway)
        db.commit()
        db.refresh(gateway)
        frequency = create_new_frequency_period(db, gateway.sensor_id, 5, datetime.now())

        gateway.current_frequency_period_id = frequency.frequency_period_id

        gateway.current_frequency_period = frequency

        db.commit()

def check_gateway_sensor():
    with get_db_session() as db:
        gateway_sensor = db.query(DBSensor).filter(DBSensor.sensor_id == 0).first()
        return gateway_sensor is not None

def check_sensors_status():
    """
    Checks if the sensors with online status have not sent data for a defined threshold period.
    :return:
    """
    with get_db_session() as db:
        sensors = db.query(DBSensor).filter(DBSensor.sensor_status == 1).all()
        for sensor in sensors:
                timediff = time() - sensor.last_message_timestamp
                if timediff > sett.SENSOR_OFFLINE_THRESHOLD:
                    sensor.sensor_status = 0
                    Logger.write(f"Sensor with ID {sensor.sensor_id} marked as offline due to inactivity.")
                    logging.info(f"Sensor with ID {sensor.sensor_id} marked as offline due to inactivity.")
        db.commit()
