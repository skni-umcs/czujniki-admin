from pydantic import BaseModel


class ModuleBase(BaseModel):
    module_name: str
    module_code: str
    location: str
    is_active: int
    is_deleted: int
    signal_power: int
    url: str


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    module_name: str | None
    module_code: str | None
    location: str | None
    is_active: int | None
    is_deleted: int | None
    signal_power: int | None
    url: str | None


class Module(ModuleBase):
    module_id: int

    class Config:
        orm_mode = True
