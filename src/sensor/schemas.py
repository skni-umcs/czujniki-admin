from datetime import datetime
from pydantic import BaseModel


class SensorBase(BaseModel):
    sensor_id: str

class SensorCreate(SensorBase):
    sensor_name: str
    sensor_location: str
    sensor_frequency: int

class SensorFrequencyOnly(SensorBase):
    sensor_frequency: int

class SensorInfoUpdate(SensorBase):
    sensor_name: str | None = None
    sensor_location: str | None = None
    sensor_frequency: int | None = None

class SensorInfoOnly(SensorCreate):
    pass

class SensorDataOnly(SensorBase):
    sensor_status: int
    last_rssi: float | None
    last_cpu_temp: int | None
    last_sensor_noise: int | None
    last_info_timestamp: datetime | None

class Sensor(SensorInfoOnly, SensorDataOnly):

    class Config:
        from_attributes = True