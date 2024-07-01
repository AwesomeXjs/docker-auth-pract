from sqlalchemy import insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from api_v1.jwt_auth import utils_jwt
from .schemas import UserRegisterSchema


async def create_user(
    session: AsyncSession, user: UserRegisterSchema
) -> UserRegisterSchema:
    hashed_password = utils_jwt.hash_password(password=user.password)
    stmt = insert(User).values(username=user.username, hashed_password=hashed_password)
    await session.execute(stmt)
    await session.commit()
    return User(username=user.username, hashed_password=hashed_password)


async def update_username(
    new_username: str,
    user: UserRegisterSchema,
    session: AsyncSession,
):
    setattr(user, "username", new_username)
    await session.commit()
    return user
