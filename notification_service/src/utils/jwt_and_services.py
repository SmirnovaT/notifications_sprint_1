from enum import Enum
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyCookie
from pydantic import BaseModel, ValidationError

from src.core.config import settings
from src.core.logger import notification_logger
from src.utils.services_constant import ServiceEnum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    iss: str
    type: TokenType
    iat: int
    exp: int


class AccessTokenPayload(TokenPayload):
    service_name: str


cookie_scheme = APIKeyCookie(name="access_token")


async def verify_access_token_dep(
    jwt_token: Annotated[str, Depends(cookie_scheme)],
) -> AccessTokenPayload:
    if not jwt_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is missing",
        )
    decoded_token = await validate_token(jwt_token)
    try:
        access_token = AccessTokenPayload(**decoded_token)
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is invalid",
        )
    return access_token


async def validate_token(token: str) -> dict:
    """Validates token"""
    leeway = 30
    try:
        decoded_token: dict[str, str] = jwt.decode(
            jwt=token, key=settings.public_key, algorithms=["RS256"], leeway=leeway
        )
    except jwt.exceptions.DecodeError as decode_error:
        notification_logger.error(f"Error while JWT decoding: {decode_error}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is invalid",
        )
    except jwt.ExpiredSignatureError:
        notification_logger.error("Token expires")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is expired",
        )
    except ValueError as err:
        notification_logger.error(f"Error while JWT decoding: {err}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token is invalid",
        )

    return decoded_token


class CheckService:
    def __init__(self, services: list[ServiceEnum]) -> None:
        self.services = services

    async def __call__(
        self,
        access_token: AccessTokenPayload = Depends(verify_access_token_dep),
    ) -> None:
        if access_token.service_name not in self.services:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Service doesn't have required permissions",
            )
