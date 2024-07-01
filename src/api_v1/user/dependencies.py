from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie, Depends, Form, HTTPException, status

from db.models import User
from db.db_helper import session_dep
from api_v1.jwt_auth import utils_jwt
from jwt.exceptions import DecodeError


async def get_auth_user(
    session: Annotated[AsyncSession, Depends(session_dep)],
    username: str = Form(),
    password: str = Form(),
) -> User:
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid username or password",
    )

    # Проверяем есть ли такой юзернейм в нашей бд, и возвращаем либо None либо user
    query = select(User).filter_by(username=username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    # возвращаем ошибку если не найден в бд
    if user is None:
        raise unauth_exc

    # Сравниваем пароль который пришел с правильным паролем из бд
    if not utils_jwt.validate_pass(
        hashed_password=user.hashed_password,
        password=password,
    ):
        raise unauth_exc
    return user


# DEPENDENCY для проверки токена в куках и возвращаем payload.
async def get_payload_jwt_cookie(
    token: str = Cookie(alias="JWT-TOKEN-AUTH"),
):
    try:
        if utils_jwt.decode_jwt(token).get("username") is not None:
            return utils_jwt.decode_jwt(token)
    except DecodeError:
        return {"error": "invalid jwt token"}
