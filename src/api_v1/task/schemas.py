from pydantic import BaseModel, Field


class TaskSchemaCreate(BaseModel):
    title: str = Field(max_length=15)
    description: str


class UpdateSchemaTask(BaseModel):
    title: str | None = None
    description: str | None = None


class TaskSchema(TaskSchemaCreate):
    id: int
