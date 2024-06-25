from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Task(Base):
    title: Mapped[str] = mapped_column(String(15), unique=True)
    description: Mapped[str]

    def __repr__(self) -> str:
        return f"Task id: {self.id}, Title: {self.title}, Descr: {self.description}"
