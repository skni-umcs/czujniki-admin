from datetime import datetime

from .models import DBSensor
from .exceptions import (SensorNotFoundException, SensorNameTakenException, LocationTakenException,
                         ReceivedRSSIFromNotActiveSensorException, SensorCodeTakenException, BadDateTimeFormatException)
from sqlalchemy.orm import Session
from .schemas import SensorCreate, SensorUpdate


def get_all_sensors(db: Session) -> list[DBSensor]:
    sensors = db.query(DBSensor).all()
    return sensors


def create_new_sensor(db: Session, sensor_to_add: SensorCreate) -> DBSensor:

    code_err = db.query(DBSensor).filter(DBSensor.sensor_code == sensor_to_add.sensor_code).first()

    if code_err is not None:
        raise SensorCodeTakenException

    new_sensor = DBSensor(
                        sensor_code=sensor_to_add.sensor_code,
                        sensor_name=sensor_to_add.sensor_name,
                        sensor_location=sensor_to_add.sensor_location,
                        sensor_status=1)

    db.add(new_sensor)
    db.commit()

    return new_sensor


def get_sensor_by_code(db: Session, sensor_code: str) -> DBSensor:
    sensor = db.query(DBSensor).filter(DBSensor.sensor_code == sensor_code).first()

    if sensor is None:
        raise SensorNotFoundException

    return sensor


def update_sensor_by_index(db: Session, sensor_code: str, updated_sensor: SensorUpdate) -> DBSensor:
    sensor_to_update: DBSensor = db.query(DBSensor).filter(DBSensor.sensor_code == sensor_code).first()

    if sensor_to_update is None:
        raise SensorNotFoundException

    if updated_sensor.sensor_name is not None:
        name_err = db.query(DBSensor).filter(DBSensor.sensor_name == updated_sensor.sensor_name).first()
        if name_err is not None:
            raise SensorNameTakenException
        sensor_to_update.sensor_name = updated_sensor.sensor_name

    if updated_sensor.sensor_location is not None:
        location_err = db.query(DBSensor).filter(DBSensor.sensor_location == updated_sensor.sensor_location).first()
        if location_err is not None:
            raise LocationTakenException
        sensor_to_update.sensor_location = updated_sensor.sensor_location
    if updated_sensor.sensor_status is not None:
        sensor_to_update.sensor_status = updated_sensor.sensor_status

    db.commit()

    return sensor_to_update


def unwrap_rssi(db: Session, sensor_code: str, rssi: float, timestamp: str):
    sensor = db.query(DBSensor).filter(DBSensor.sensor_code == sensor_code).first()

    if sensor is None:
        raise SensorNotFoundException

    if sensor.sensor_status == 0:
        raise ReceivedRSSIFromNotActiveSensorException

    sensor.signal_power = rssi

    try:
        sensor.last_received_signal_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise BadDateTimeFormatException

    db.commit()
    return sensor
