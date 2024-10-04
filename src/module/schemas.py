from datetime import datetime
from pydantic import BaseModel


class ModuleBase(BaseModel):
    module_code: str
    module_name: str
    module_location: str


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    module_name: str | None
    module_location: str | None
    module_status: int | None


class Module(ModuleBase):
    module_status: int
    signal_power: float | None
    last_received_signal_date: datetime | None

    class Config:
        orm_mode = True


class RSSIDataBase(BaseModel):
    module_code: str
    rssi: float
    timestamp: str


class RSSIData(RSSIDataBase):
    pass

    class Config:
        orm_mode = True
