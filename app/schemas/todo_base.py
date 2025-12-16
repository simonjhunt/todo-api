from typing import Optional

from sqlmodel import Field, SQLModel


class ToDoBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=20, max_length=100)


class ToDoPost(ToDoBase):
    """Payload for creating a new todo."""

    pass


class ToDoPatch(SQLModel):
    """Partial update payload."""

    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, min_length=20, max_length=100)
    done: Optional[bool] = None
