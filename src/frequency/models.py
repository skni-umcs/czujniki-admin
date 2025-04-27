from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP

from src.database.core import Base

class DBFrequencyPeriod(Base):
    __tablename__ = "frequency_period"
    frequency_period_id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensors.sensor_id"))
    frequency = Column(Integer) # if 0 then sensor is offline
    start = Column(TIMESTAMP)
    end = Column(TIMESTAMP, nullable=True) # upon creation will be null, set with freq update