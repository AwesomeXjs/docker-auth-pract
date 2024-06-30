import secrets
from typing import Annotated

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix="/demo_auth",
    tags=["demo_auth"],
)


security = HTTPBasic()


# Просто вход по username : password без проверки:
@router.get("/basic_auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "data": "OK",
        "credent": credentials.username,
    }


usernames_to_password = {
    "admin": "admin",
    "john": "password",
}


# DEPENDENCY для аутентификации
# проверка пользователя и пароля на его наличие в бд
def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    # Проверяем есть ли такой юзернейм в нашей бд, и возвращаем либо юзернейм
    correct_password = usernames_to_password.get(credentials.username)

    # возвращаем ошибку если не найден в бд
    if correct_password is None:
        raise unauth_exc

    # проверка пароля с помощью модуля secrets.
    # Сравниваем пароль который пришел с правильным паролем из бд
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauth_exc
    return credentials.username


@router.get("/basic_auth-username/")
def demo_basic_auth_username(
    auth_username: Annotated[str, Depends(get_auth_user_username)]
):
    return {
        "data": "OK",
        "credent": f"Hi!, {auth_username}",
    }
