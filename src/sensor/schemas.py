from datetime import datetime
from pydantic import BaseModel
from src.frequency.schemas import FrequencyPeriod

class SensorBase(BaseModel):
    sensor_id: int

class SensorResponse(SensorBase):
    sensor_faculty: str
    sensor_longitude: float
    sensor_latitude: float
    sensor_status: int
    last_timestamp: datetime
    last_message_type: str
    current_frequency_period: FrequencyPeriod

class Sensor(SensorResponse):
    class Config:
        from_attributes = True