from datetime import datetime

from src.frequency.connector import create_new_frequency_period
from src.sensor.models import DBSensor
from src.database.core import get_db_session

def create_gateway_sensor():
    with get_db_session() as db:
        gateway = DBSensor(sensor_id=0,
                           sensor_faculty="Gateway",
                           sensor_latitude=0.0,
                           sensor_longitude=0.0,
                           sensor_status=1)
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