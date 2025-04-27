from sqlalchemy import Float, Integer, Column, String, DateTime, ForeignKey, ARRAY, TIMESTAMP
from sqlalchemy.orm import relationship

from src.database.core import Base

class DBEdge(Base):
    __tablename__ = 'edges'
    edge_id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id = Column(Integer, ForeignKey('sensor_data.sensor_data_id'))
    source = Column(Integer, ForeignKey('sensors.sensor_id'))
    target = Column(Integer, ForeignKey('sensors.sensor_id'))
    rssi = Column(Integer)

class DBSensorData(Base):
    __tablename__ = 'sensor_data'
    sensor_data_id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensors.sensor_id'))
    raw_packet = Column(String(200)) # raw message from gate
    timestamp = Column(TIMESTAMP)
    noise = Column(Integer)
    cpu_temp = Column(Integer)
    free_heap = Column(Integer)
    queue_fill = Column(Integer)
    hop_ids = Column(ARRAY(Integer))
    edges = relationship('DBEdge')