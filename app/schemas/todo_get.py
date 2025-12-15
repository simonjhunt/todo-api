from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

class ToDoGet(SQLModel):
    """Response model – mirrors the DB model but is kept separate for flexibility."""
    id: int
    title: str
    description: str
    done: bool
    created_at: datetime
    completed_at: Optional[datetime] = None