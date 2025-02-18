from sqlalchemy import Float, Integer, Column, String, DateTime
from src.database.core import Base


class DBSensor(Base):
    __tablename__ = 'sensors'
    sensor_code = Column(String(100), unique=True, primary_key=True)
    sensor_name = Column(String(100), unique=True)  # human-readable
    sensor_location = Column(String(1000), unique=True)  # TODO: better way to store location (for graphing)
    sensor_status = Column(Integer)
    last_received_signal_date = Column(DateTime)
    signal_power = Column(Float)
