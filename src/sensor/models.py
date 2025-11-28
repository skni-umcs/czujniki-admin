from sqlalchemy import Float, Integer, Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from src.database.core import Base

class DBClimateFrame(Base):
    __tablename__ = 'climate_frames'
    climate_frame_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensors.sensor_id'))
    timestamp = Column(Integer)

class DBSensor(Base):
    __tablename__ = 'sensors'
    sensor_id = Column(Integer, unique=True, primary_key=True)
    sensor_faculty = Column(String(100))
    sensor_latitude = Column(Float)
    sensor_longitude = Column(Float)
    sensor_status = Column(Integer)
    last_message_timestamp = Column(Integer, nullable=True)
    last_message_type = Column(String(50))
    last_sensor_data_id = Column(Integer, ForeignKey('sensor_data.sensor_data_id'), nullable=True)
    last_climate_frame_id = Column(Integer, ForeignKey('climate_frames.climate_frame_id'), nullable=True)
    current_frequency_period_id = Column(Integer, ForeignKey('frequency_period.frequency_period_id'), nullable=True)
    current_frequency_period = relationship('DBFrequencyPeriod',foreign_keys=[current_frequency_period_id])