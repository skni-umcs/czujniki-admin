from pydantic import BaseModel

class UserBase(BaseModel):
    login: str
    keycloak_id: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True