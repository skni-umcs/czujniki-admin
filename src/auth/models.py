from pydantic import BaseModel


class TokenData(BaseModel):
    username: str = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str
