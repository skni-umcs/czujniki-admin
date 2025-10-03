from sqlalchemy import Float, Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base

class DBSensor(Base):
    __tablename__ = 'sensors'
    sensor_id = Column(Integer, unique=True, primary_key=True)
    sensor_faculty = Column(String(100))
    sensor_latitude = Column(Float)
    sensor_longitude = Column(Float)
    sensor_status = Column(Integer) # always active, for now
    current_frequency_period_id = Column(Integer, ForeignKey('frequency_period.frequency_period_id'), nullable=True)
    current_frequency_period = relationship('DBFrequencyPeriod',foreign_keys=[current_frequency_period_id])
    last_sensor_data_id = Column(Integer, ForeignKey('sensor_data.sensor_data_id'),nullable=True)