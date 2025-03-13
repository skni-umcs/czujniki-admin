import requests
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError

from src.auth.exceptions import CredentialsException
from src.database.core import get_db
from src.user.connector import get_or_create_user
from sqlalchemy.orm import Session
from config import Settings

settings = Settings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
    refreshUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
)

KEYCLOAK_PUBLIC_KEY = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
certs = requests.get(KEYCLOAK_PUBLIC_KEY).json()
rsa_key = certs["keys"][1]

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token,
                             rsa_key,
                             algorithms=[f"{settings.KEYCLOAK_ALGO}"],
                             audience="account",
                             issuer=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}")
        return payload
    except JWTError as e:
        raise e

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user = get_or_create_user(db, payload.get("sub"), payload.get("preferred_username"))
    except JWTError:
        raise CredentialsException
    return user