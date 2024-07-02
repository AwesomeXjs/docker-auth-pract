from typing import Annotated, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, status, Form

from . import utils_jwt
from db.models import User
from db.db_helper import session_dep
from api_v1.user.dependencies import get_payload_jwt_cookie


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(utils_jwt.TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type '{current_token_type}' expected '{token_type}'",
    )


async def actions_with_valid_token(
    session: AsyncSession = Depends(session_dep),
    payload: dict = Depends(get_payload_jwt_cookie),
) -> User:
    username: str | None = payload.get("username")
    query = select(User).filter_by(username=username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Нужно зарегестрироваться!",
    )


class UserGetterFromToken:
    def __init__(self, token_type: str) -> None:
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_payload_jwt_cookie),
        session: AsyncSession = Depends(session_dep),
    ) -> Any:
        validate_token_type(payload=payload, token_type=self.token_type)
        return await actions_with_valid_token(payload=payload, session=session)


private_route = UserGetterFromToken(token_type=utils_jwt.ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(
    token_type=utils_jwt.REFRESH_TOKEN_TYPE
)


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
