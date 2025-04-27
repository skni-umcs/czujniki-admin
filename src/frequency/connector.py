from datetime import datetime
from sqlalchemy.orm import Session
from src.frequency.models import DBFrequencyPeriod

def create_new_frequency_period(db: Session,
                              sensor_id: int,
                              frequency: int,
                              start: datetime) -> DBFrequencyPeriod:

    frequency_period = DBFrequencyPeriod(sensor_id=sensor_id,
                                         frequency=frequency,
                                         start=start)

    db.add(frequency_period)
    db.commit()

    return frequency_period

def get_current_frequency_period_by_sensor_id(db: Session, sensor_id: int) -> DBFrequencyPeriod:
    frequency_period = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.sensor_id == sensor_id, DBFrequencyPeriod.end == None).first()
    return frequency_period

def get_frequency_periods_by_sensor_id(db: Session, sensor_id: int) -> list[DBFrequencyPeriod]:
    frequency_periods = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.sensor_id == sensor_id).all()
    return frequency_periods

def get_frequency_periods_all(db: Session) -> list[DBFrequencyPeriod]:
    frequency_periods = db.query(DBFrequencyPeriod).all()
    return frequency_periods

def get_current_frequencies(db: Session) -> list[DBFrequencyPeriod]:
    frequencies = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.end == None).all()
    return frequencies