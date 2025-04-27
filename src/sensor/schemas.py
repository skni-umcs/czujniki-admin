from datetime import datetime
from pydantic import BaseModel

from src.frequency.schemas import FrequencyPeriod

class SensorBase(BaseModel):
    sensor_id: int

class SensorCreate(SensorBase):
    sensor_name: str
    sensor_longitude: float
    sensor_latitude: float
    sensor_frequency: int

class SensorFrequencyOnly(SensorBase):
    sensor_frequency: int

class SensorInfoUpdate(SensorBase):
    sensor_name: str | None = None
    sensor_frequency: int | None = None
    sensor_longitude: float | None = None
    sensor_latitude: float | None = None

class SensorResponse(SensorBase):
    sensor_name: str
    sensor_longitude: float
    sensor_latitude: float
    current_frequency_period: FrequencyPeriod

class Sensor(SensorResponse):

    class Config:
        from_attributes = True