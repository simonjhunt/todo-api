# app/services/todo_service.py
from datetime import datetime, timezone
from typing import List, Sequence

from sqlmodel import Session, select

from app.models.todo import ToDoDB
from app.schemas.todo_base import ToDoPatch, ToDoPost
from app.schemas.todo_get import ToDoGet


# ---------- LIST ----------
def list_todos(session: Session, offset: int = 0, limit: int = 100) -> List[ToDoGet]:
    stmt = select(ToDoDB).offset(offset).limit(limit)
    todos: Sequence[ToDoDB] = session.exec(stmt).all()
    return [ToDoGet.model_validate(t) for t in todos]


# ---------- GET ----------
def get_todo(session: Session, todo_id: int) -> ToDoGet:
    todo = session.get(ToDoDB, todo_id)
    if not todo:
        raise ValueError("Not found")
    return ToDoGet.model_validate(todo)


# ---------- CREATE ----------
def create_todo(session: Session, payload: ToDoPost) -> ToDoGet:
    db_obj = ToDoDB(**payload.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return ToDoGet.model_validate(db_obj)


# ---------- UPDATE ----------
def update_todo(session: Session, todo_id: int, payload: ToDoPatch) -> ToDoGet:
    stored = session.get(ToDoDB, todo_id)
    if not stored:
        raise ValueError("Not found")

    # done/completed_at handling
    if payload.done is True and not stored.done:
        stored.completed_at = datetime.now(timezone.utc)
    elif payload.done is False and stored.done:
        stored.completed_at = None

    # apply any other supplied fields
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(stored, field, value)

    session.add(stored)
    session.commit()
    session.refresh(stored)
    return ToDoGet.model_validate(stored)


# ---------- DELETE ----------
def delete_todo(session: Session, todo_id: int) -> None:
    obj = session.get(ToDoDB, todo_id)
    if not obj:
        raise ValueError("Not found")
    session.delete(obj)
    session.commit()
