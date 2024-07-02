import jwt
import bcrypt
from datetime import datetime, timedelta

from db.models import User
from db.config import settings


# кодирование пароля с помощью приватного ключа
def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_time_delta: timedelta | None = None,
):
    to_encode = payload.copy()

    # устанавливаем срок экспирации токена
    # now - текущее время
    now = datetime.utcnow()
    if expire_time_delta:
        expire = now + expire_time_delta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


# декодируем пароль с помощью приватного ключа
def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


# хешируем пароль
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt).decode()


# хешируемвведенный пароль и сверяеми с хешем в базе данных
def validate_pass(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password.encode(),
    )


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


async def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type,
    }
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_time_delta=expire_timedelta,
        expire_minutes=expire_minutes,
    )


# функция для выпуска jwt токена
async def create_access_token(user: User) -> str:
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
        # "logged_in_at"
    }
    return await create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


async def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    return await create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
