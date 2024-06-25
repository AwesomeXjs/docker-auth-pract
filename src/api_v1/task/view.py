from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from . import crud
from db.db_helper import session_dep
from .dependencies import get_task_by_title
from .schemas import TaskSchema, TaskSchemaCreate, UpdateSchemaTask

router = APIRouter(prefix="/tasks")


@router.post("/")
async def create_task(
    task: TaskSchemaCreate,
    session: Annotated[AsyncSession, Depends(session_dep)],
):
    # try:
    await crud.create_task(task=task, session=session)
    return (
        {
            "status": "ok",
            "detail": f"Таска с названием '{task.title}' создана",
        },
    )


# except:
#     raise HTTPException(
#         status_code=status.HTTP_406_NOT_ACCEPTABLE,
#         detail={
#             "status": "error",
#             "detail": f"Такое имя уже есть",
#         },
#     )


@router.get("/{title}")
async def get_task_by_title(
    task: Annotated[TaskSchema, Depends(get_task_by_title)]
) -> TaskSchema:
    return task


@router.delete("/")
async def delete_task(
    task: Annotated[TaskSchema, Depends(get_task_by_title)],
    session: Annotated[AsyncSession, Depends(session_dep)],
):
    return await crud.delete_task(session=session, task=task)


@router.patch("/")
async def update_task(
    new_task: UpdateSchemaTask,
    task: Annotated[TaskSchema, Depends(get_task_by_title)],
    session: Annotated[AsyncSession, Depends(session_dep)],
):
    return await crud.update_task(
        new_task=new_task,
        task=task,
        session=session,
    )
