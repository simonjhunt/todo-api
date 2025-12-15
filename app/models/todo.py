# app/models/todo.py
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class ToDoBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=20, max_length=100)

class ToDoDB(ToDoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    done: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )