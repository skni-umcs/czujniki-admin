from datetime import datetime, date
from pydantic import BaseModel


class LogBase(BaseModel):
    message: str
    timestamp: datetime

class LogDate(BaseModel):
    log_date: date

class Log(LogBase):

    class Config:
        from_attributes = True