from sqlalchemy import Float, Integer, Column, String
from src.database.core import Base

# TODO: sync this data with climate data db
class DBSensor(Base):
    __tablename__ = 'sensors'
    sensor_id = Column(Integer, unique=True, primary_key=True)
    sensor_name = Column(String(100), unique=True)  # human-readable (e.g. hint of location)
    sensor_latitude = Column(Float)
    sensor_longitude = Column(Float)
    sensor_status = Column(Integer) # always active, for now
    sensor_frequency = Column(Integer) # time between sending packets in seconds

