from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from .models import TokenData
import jwt
from jwt import PyJWKClient
from .. import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
)


def decode_token(token: str) -> dict:
    url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    jwks_client = PyJWKClient(url)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    try:
        payload = jwt.decode(token, signing_key.key, algorithms=[settings.KEYCLOAK_ALGO])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Decoding error")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    username = payload.get("preferred_username")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TokenData(username=username)
