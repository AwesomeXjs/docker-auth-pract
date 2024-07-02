from typing import Annotated

from fastapi.security import HTTPBasic
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Response, Form

from . import crud
from db.models import User
from db.db_helper import session_dep
from api_v1.jwt_auth import utils_jwt
from .schemas import UserRegisterSchema, TokenInfo
from api_v1.jwt_auth.validation import (
    get_auth_user,
    private_route,
    actions_with_valid_token,
    get_current_auth_user_for_refresh,
)


security = HTTPBasic()

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post("/")
async def create_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(session_dep),
):
    return await crud.create_user(
        session=session,
        username=username,
        password=password,
    )


# Аутентифицируемся и ложим access токен в куку а refresh token в бд
@router.post("/auth", response_model=TokenInfo)
async def auth_test(
    response: Response,
    user: User = Depends(get_auth_user),
):
    access_token = await utils_jwt.create_access_token(user=user)
    refresh_token = await utils_jwt.create_refresh_token(user=user)
    response.set_cookie("JWT-TOKEN-AUTH", access_token)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.patch("/update")
async def update_username(
    new_username: str,
    user: UserRegisterSchema = Depends(get_auth_user),
    session: AsyncSession = Depends(session_dep),
    jwt_validate: str = Depends(private_route),
):
    user = await crud.update_username(
        new_username=new_username,
        user=user,
        session=session,
    )
    return {"data": user, "username_from_jwt": jwt_validate}


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    user: UserRegisterSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = await utils_jwt.create_access_token(user=user)
    return TokenInfo(access_token=access_token)


@router.get("/verification_auth")
async def verification_page(user: User = Depends(actions_with_valid_token)):
    return user
