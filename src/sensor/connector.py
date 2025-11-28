from datetime import datetime

from .models import DBSensor
from .exceptions import (SensorNotFoundException, SensorNameTakenException,
                         SensorIdTakenException,
                         SensorFrequencyNotWithinLimit, SensorLatitudeLongitudeTakenException)
from sqlalchemy.orm import Session

from ..frequency.connector import create_new_frequency_period


def get_all_sensors(db: Session) -> list[DBSensor]:
    sensors = db.query(DBSensor).all()
    return sensors

def create_new_sensor(db: Session,
                      sensor_id: int,
                      sensor_name: str,
                      sensor_latitude: float,
                      sensor_longitude: float,
                      sensor_frequency: int) ->DBSensor:

    sensor_with_code = db.query(DBSensor).filter(DBSensor.sensor_id == sensor_id).first()

    if sensor_with_code:
        raise SensorIdTakenException

    sensor_with_name = db.query(DBSensor).filter(DBSensor.sensor_name == sensor_name).first()

    if sensor_with_name:
        raise SensorNameTakenException

    sensor_with_location = db.query(DBSensor).filter(DBSensor.sensor_latitude == sensor_latitude,
                                                    DBSensor.sensor_longitude == sensor_longitude).first()

    if sensor_with_location:
        raise SensorLatitudeLongitudeTakenException

    if sensor_frequency > 3600 or sensor_frequency < 5:
        raise SensorFrequencyNotWithinLimit


    sensor = DBSensor(sensor_id=sensor_id,
                      sensor_name=sensor_name,
                      sensor_latitude=sensor_latitude,
                      sensor_longitude=sensor_longitude,
                      sensor_status=1)

    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    frequency = create_new_frequency_period(db,sensor.sensor_id,sensor_frequency, datetime.now())

    sensor.current_frequency_period_id = frequency.frequency_period_id

    sensor.current_frequency_period = frequency

    db.commit()

    return sensor

def get_sensor_by_code(db: Session, sensor_id: int) -> DBSensor:
    sensor = db.query(DBSensor).filter(DBSensor.sensor_id == sensor_id).first()

    if sensor is None:
        raise SensorNotFoundException

    return sensor

# should only be called upon sensor data creation
def update_sensor_last_sensor_data_id(db: Session,
                                      sensor_id: int,
                                      last_sensor_data_id: int):

    sensor = get_sensor_by_code(db,sensor_id)

    if sensor is None:
        raise SensorNotFoundException

    sensor.last_sensor_data_id = last_sensor_data_id

    db.commit()

def update_sensor_info(db: Session,
                       sensor_id: int,
                       sensor_name: str | None,
                       sensor_latitude: float | None,
                       sensor_longitude: float | None,
                       sensor_frequency: int | None) ->DBSensor:
    try:
        sensor = get_sensor_by_code(db,sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    if sensor_name:
        sensor_with_name = db.query(DBSensor).filter(DBSensor.sensor_name == sensor_name).first()

        if sensor_with_name:
            raise SensorNameTakenException
        sensor.sensor_name = sensor_name

    if sensor_frequency is not None:
        if sensor_frequency > 3600 or sensor_frequency < 5:
            raise SensorFrequencyNotWithinLimit
        dt = datetime.now()
        sensor.current_frequency_period.end = dt
        new_period = create_new_frequency_period(db,sensor.sensor_id,sensor_frequency, dt)
        sensor.current_frequency_period_id = new_period.frequency_period_id
        sensor.current_frequency_period = new_period

    # not that clever, maybe to rewrite later
    if sensor_latitude is not None and sensor_longitude is not None:
        sensor_with_location = db.query(DBSensor).filter(
            DBSensor.sensor_latitude == sensor_latitude,
            DBSensor.sensor_longitude == sensor_longitude,
            DBSensor.sensor_id != sensor_id  # Exclude the current sensor
        ).first()
        if sensor_with_location:
            raise SensorLatitudeLongitudeTakenException
        sensor.sensor_latitude = sensor_latitude
        sensor.sensor_longitude = sensor_longitude

    db.commit()
    return sensor

def delete_sensor_by_code(db: Session,
                          sensor_id: int):
    sensor = get_sensor_by_code(db,sensor_id)

    if sensor is None:
        raise SensorNotFoundException

    db.delete(sensor)
    db.commit()


