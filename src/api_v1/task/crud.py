from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update

from db.models import Task
from .dependencies import get_task_by_title
from .schemas import TaskSchemaCreate, TaskSchema, UpdateSchemaTask


async def create_task(task: TaskSchemaCreate, session: AsyncSession) -> None:
    new_task = task.model_dump()
    stmt = insert(Task).values(**new_task)
    await session.execute(stmt)
    await session.commit()


async def delete_task(task: TaskSchema, session: AsyncSession) -> None:
    stmt = delete(Task).where(Task.title == task.title)
    await session.execute(stmt)
    await session.commit()


async def update_task(
    task: TaskSchema,
    new_task: UpdateSchemaTask,
    session: AsyncSession,
) -> TaskSchema:
    for name, value in new_task.model_dump(exclude_unset=True).items():
        setattr(task, name, value)
    await session.commit()
    return task
