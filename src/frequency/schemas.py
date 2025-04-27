from datetime import datetime

from pydantic import BaseModel


class FrequencyPeriodBase(BaseModel):
    frequency: int
    start: datetime

class FrequencyPeriodCreate(FrequencyPeriodBase):
    sensor_id: int

class FrequencyPeriod(FrequencyPeriodBase):
    end: datetime | None = None

    class Config:
        from_attributes = True
        orm_mode = True