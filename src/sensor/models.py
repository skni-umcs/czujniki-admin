from sqlalchemy import Float, Integer, Column, String, DateTime
from src.database.core import Base


class DBSensor(Base):
    __tablename__ = 'sensors'
    sensor_id = Column(String(100), unique=True, primary_key=True)
    sensor_name = Column(String(100), unique=True)  # human-readable (maybe not needed?)
    sensor_location = Column(String(1000), unique=True)
    sensor_status = Column(Integer)
    sensor_frequency = Column(Integer) # time between sending packets in seconds
    last_rssi = Column(Float, nullable=True)
    last_cpu_temp = Column(Integer, nullable=True)
    last_sensor_noise = Column(Integer, nullable=True)
    last_info_timestamp = Column(DateTime, nullable=True)

