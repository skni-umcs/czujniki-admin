import typing

import requests
from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jose import jwt, JWTError

from src.auth.exceptions import CredentialsException
from src.database.core import get_db
from src.user.connector import get_or_create_user
from sqlalchemy.orm import Session
from config import Settings

settings = Settings()

class Oauth2ClientCredentials(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> typing.Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

oauth2_scheme = Oauth2ClientCredentials(tokenUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token")

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