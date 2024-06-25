from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool) -> None:
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )


db_helper = DatabaseHelper(url=settings.get_db_url, echo=True)


async def session_dep():
    async with db_helper.session_factory() as session:
        yield session
        await session.close()
