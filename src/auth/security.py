import typing

import requests
from fastapi import Depends, Request, HTTPException
from fastapi.security.oauth2 import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jose import jwt, JWTError

from src.auth.exceptions import CredentialsException
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

token_url = f"{settings.AUTHENTIK_SERVER_URL}/application/o/token/"
oauth2_scheme = Oauth2ClientCredentials(tokenUrl=token_url)

jwks_url = f"{settings.AUTHENTIK_SERVER_URL}/application/o/{settings.AUTHENTIK_APP_NAME}/jwks/"
jwk = requests.get(jwks_url).json()
rsa_key = jwk["keys"][0]

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token,
                             rsa_key,
                             algorithms=[f"{settings.AUTHENTIK_ALGORITHM}"],
                             audience=f"{settings.AUTHENTIK_CLIENT_ID}",
                             issuer=f"{settings.AUTHENTIK_SERVER_URL}/application/o/{settings.AUTHENTIK_APP_NAME}/")
        return payload
    except JWTError as e:
        raise e

async def get_current_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_token(token)
        return payload
    except JWTError:
        raise CredentialsException()