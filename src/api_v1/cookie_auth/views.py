import time
import uuid
from typing import Any

from fastapi import APIRouter, Response, Depends, Cookie, HTTPException, status

from api_v1.basic_auth.views import get_auth_user_username

router = APIRouter(
    prefix="/cookie_auth",
    tags=["cookie_auth"],
)

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_key = "web-app-cookie-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


# DEPENDENCY для проверки логина по куки.
def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_key)) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"not auth"
        )
    return COOKIES[session_id]


@router.post("/login-cookie/")
def demo_auth_login_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_username),
):
    # создаем id сессии (случайное число)
    session_id = generate_session_id()

    # заносим в хранилище кук данные
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time.time()),
    }

    # помещаем в куки данные "web-app-cookie-session-id", id_key
    response.set_cookie(COOKIE_SESSION_ID_key, session_id)
    return {"result": "OK"}


@router.get("/check-cookie/")
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data["username"]
    return {
        "status": f"OK, {username}",
        **user_session_data,
    }


# LOGOUT
@router.get("/logout-cookie/")
def logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_key),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_key)
    username = user_session_data["username"]
    return {
        "status": f"Bye, {username}",
        **user_session_data,
    }
