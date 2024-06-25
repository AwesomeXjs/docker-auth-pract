from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from db.models import Task
from .schemas import TaskSchema
from db.db_helper import session_dep


async def get_task_by_title(
    title: str, session: Annotated[AsyncSession, Depends(session_dep)]
) -> TaskSchema:
    query = select(Task).where(Task.title == title)
    result = await session.execute(query)
    task = result.scalar()
    if task is not None:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Таска с названием '{title}' не существует",
    )
