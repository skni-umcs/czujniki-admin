from datetime import datetime, timedelta
from .models import DBSensor
from .exceptions import (SensorNotFoundException,
                         SensorIdTakenException,
                         SensorFrequencyNotWithinLimit)
from sqlalchemy.orm import Session
from ..frequency.connector import create_new_frequency_period

def get_all_sensors(db: Session) -> list[DBSensor]:

    return db.query(DBSensor).all()

def create_new_sensor(db: Session,
                      sensor_id: int,
                      sensor_faculty: str,
                      sensor_latitude: float,
                      sensor_longitude: float,
                      sensor_frequency: int) -> DBSensor:

    sensor_with_id = db.query(DBSensor).filter(DBSensor.sensor_id == sensor_id).first()

    if sensor_with_id:
        raise SensorIdTakenException

    if sensor_frequency > 3600 or sensor_frequency < 5:
        raise SensorFrequencyNotWithinLimit

    sensor = DBSensor(sensor_id=sensor_id,
                      sensor_faculty=sensor_faculty,
                      sensor_latitude=sensor_latitude,
                      sensor_longitude=sensor_longitude,
                      sensor_status=0, # assume new sensor is offline
                      last_timestamp=datetime.now() - timedelta(days=1),
                      last_message_type="N/A")

    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    frequency = create_new_frequency_period(db,sensor.sensor_id,sensor_frequency, datetime.now())

    sensor.current_frequency_period_id = frequency.frequency_period_id

    sensor.current_frequency_period = frequency

    db.commit()

    return sensor

def get_sensor_by_id(db: Session,
                     sensor_id: int) -> DBSensor:

    sensor = db.query(DBSensor).filter(DBSensor.sensor_id == sensor_id).first()

    if sensor is None:
        raise SensorNotFoundException

    return sensor

def update_sensor_last_sensor_data_id(db: Session,
                                      sensor_id: int,
                                      last_sensor_data_id: int) -> None:

    sensor = get_sensor_by_id(db,sensor_id)

    if sensor is None:
        raise SensorNotFoundException

    sensor.last_sensor_data_id = last_sensor_data_id

    db.commit()

def update_sensor_on_ping(db: Session,
                          sensor_id: int,
                          timestamp: datetime,
                          message_type: str) -> None:

        sensor = get_sensor_by_id(db,sensor_id)

        if sensor is None:
            raise SensorNotFoundException

        sensor.last_timestamp = timestamp
        sensor.last_message_type = message_type

        if sensor.sensor_status == 0:
            sensor.sensor_status = 1

        db.commit()

def update_sensor_frequency(db: Session,
                            sensor_id: int,
                            sensor_frequency: int) -> None:

    try:
        sensor = get_sensor_by_id(db,sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    if sensor_frequency is not None:
        if sensor_frequency > 3600 or sensor_frequency < 5:
            raise SensorFrequencyNotWithinLimit
        dt = datetime.now()
        sensor.current_frequency_period.end = dt
        new_period = create_new_frequency_period(db,sensor.sensor_id,sensor_frequency, dt)
        sensor.current_frequency_period_id = new_period.frequency_period_id
        sensor.current_frequency_period = new_period

    db.commit()

def delete_sensor_by_id(db: Session,
                        sensor_id: int):

    sensor = get_sensor_by_id(db,sensor_id)

    if sensor is None:
        raise SensorNotFoundException

    db.delete(sensor)
    db.commit()


