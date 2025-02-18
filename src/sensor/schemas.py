from datetime import datetime
from pydantic import BaseModel


class SensorBase(BaseModel):
    sensor_code: str
    sensor_name: str
    sensor_location: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    sensor_name: str | None
    sensor_location: str | None
    sensor_status: int | None


class Sensor(SensorBase):
    sensor_status: int
    signal_power: float | None
    last_received_signal_date: datetime | None

    class Config:
        orm_mode = True


class RSSIDataBase(BaseModel):
    sensor_code: str
    rssi: float
    timestamp: str


class RSSIData(RSSIDataBase):
    pass

    class Config:
        orm_mode = True
