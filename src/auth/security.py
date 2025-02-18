import requests
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from src.dependecies import get_db
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
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, rsa_key, algorithms=["RS256"], audience="account", issuer=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}")
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Decoding error")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, rsa_key, algorithms=["RS256"], audience="account", issuer=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}")
        user = get_or_create_user(db ,payload.get("sub"), payload.get("preferred_username"))
    except JWTError:
        raise credentials_exception
    return user