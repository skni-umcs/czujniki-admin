from datetime import datetime

from .models import DBSensor
from .exceptions import (SensorNotFoundException, SensorNameTakenException,
                         SensorCodeTakenException,
                         SensorLocationTakenException)
from sqlalchemy.orm import Session

def get_all_sensors(db: Session) -> list[DBSensor]:
    sensors = db.query(DBSensor).all()
    return sensors

def create_new_sensor(db: Session,
                      sensor_code: str,
                      sensor_name: str,
                      sensor_location: str,
                      sensor_frequency: int) ->DBSensor:

    sensor_with_code = db.query(DBSensor).filter(DBSensor.sensor_code == sensor_code).first()

    if sensor_with_code:
        raise SensorCodeTakenException

    sensor_with_name = db.query(DBSensor).filter(DBSensor.sensor_name == sensor_name).first()

    if sensor_with_name:
        raise SensorNameTakenException

    sensor_with_location = db.query(DBSensor).filter(sensor_location == sensor_location).first()

    if sensor_with_location:
        raise SensorLocationTakenException

    sensor = DBSensor(sensor_code=sensor_code,
                      sensor_name=sensor_name,
                      sensor_location=sensor_location,
                      sensor_status=1,
                      sensor_frequency=sensor_frequency)

    db.add(sensor)
    db.commit()

    return sensor

def get_sensor_by_code(db: Session, sensor_code: str) -> DBSensor:
    sensor = db.query(DBSensor).filter(DBSensor.sensor_code == sensor_code).first()

    if sensor is None:
        raise SensorNotFoundException

    return sensor

def update_sensor_info(db: Session,
                       sensor_code: str,
                       sensor_name: str | None,
                       sensor_location: str | None,
                       sensor_frequency: int | None) ->DBSensor:
    try:
        sensor = get_sensor_by_code(db,sensor_code)
    except SensorNotFoundException:
        raise SensorNotFoundException

    if sensor_name:
        sensor_with_name = db.query(DBSensor).filter(DBSensor.sensor_name == sensor_name).first()

        if sensor_with_name:
            raise SensorNameTakenException
        sensor.sensor_name = sensor_name
    if sensor_location:
        sensor_with_location = db.query(DBSensor).filter(sensor_location == sensor_location).first()

        if sensor_with_location:
            raise SensorLocationTakenException
        sensor.sensor_location = sensor_location

    if sensor_frequency:
        sensor.sensor_frequency = sensor_frequency

    db.commit()
    return sensor

def delete_sensor_by_code(db: Session,
                          sensor_code: str):
    sensor = get_sensor_by_code(db,sensor_code)

    if sensor is None:
        raise SensorNotFoundException

    db.delete(sensor)
    db.commit()

# this method should only be called by mqtt message handler!
def update_sensor_data(db: Session,
                       sensor_code: str,
                       new_rssi: float,
                       new_cpu_temp: int,
                       new_noise: int):
    sensor = get_sensor_by_code(db,sensor_code)
    sensor.last_rssi = new_rssi
    sensor.last_cpu_temp = new_cpu_temp
    sensor.last_sensor_noise = new_noise
    sensor.last_info_timestamp = datetime.now()

    db.commit()

