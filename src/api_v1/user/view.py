from typing import Annotated

from fastapi.security import HTTPBasic
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Response, HTTPException, status

from . import crud
from db.models import User
from db.db_helper import session_dep
from api_v1.jwt_auth import utils_jwt
from .schemas import UserRegisterSchema
from jwt.exceptions import ExpiredSignatureError
from .dependencies import get_auth_user, get_payload_jwt_cookie


security = HTTPBasic()

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post("/")
async def create_user(
    user: UserRegisterSchema,
    session: AsyncSession = Depends(session_dep),
):
    return await crud.create_user(session=session, user=user)


# Аутентифицируемся и ложим токен в куки
@router.post("/auth")
async def auth_test(response: Response, user: User = Depends(get_auth_user)):
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
        # "logged_in_at"
    }
    token = utils_jwt.encode_jwt(jwt_payload)
    response.set_cookie("JWT-TOKEN-AUTH", token)
    return {"status": "OK"}


@router.patch("/update")
async def update_username(
    new_username: str,
    user: UserRegisterSchema = Depends(get_auth_user),
    session: AsyncSession = Depends(session_dep),
):
    return await crud.update_username(
        new_username=new_username,
        user=user,
        session=session,
    )


@router.get("/try")
async def payload_jwt(jwt_payload: str = Depends(get_payload_jwt_cookie)):
    try:
        return jwt_payload["username"]
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"token not found"
        )
