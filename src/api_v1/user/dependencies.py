from fastapi import Cookie

from api_v1.jwt_auth import utils_jwt
from jwt.exceptions import InvalidTokenError


# DEPENDENCY для проверки токена в куках и возвращаем payload.
async def get_payload_jwt_cookie(
    token: str = Cookie(alias="JWT-TOKEN-AUTH"),
):
    try:
        payload = utils_jwt.decode_jwt(token)
    except InvalidTokenError as e:
        return {"error": f"invalid token error: {e}"}

    return payload
