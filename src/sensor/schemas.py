from datetime import datetime
from pydantic import BaseModel


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


class Sensor(SensorCreate):

    class Config:
        from_attributes = True