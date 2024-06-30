import jwt
import bcrypt
from datetime import datetime, timedelta

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
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_pass(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password,
    )
