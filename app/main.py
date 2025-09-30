from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, AsyncGenerator, Generator, Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import Column, DateTime


class ToDoBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=20, max_length=1000)


class ToDoPost(ToDoBase):
    pass


class ToDoPatch(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, min_length=20, max_length=1000)
    done: Optional[bool]


class ToDoDB(ToDoBase, table=True):
    id: Optional[int] = Field(primary_key=True, index=True, default=None)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=20, max_length=1000)
    done: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )


class ToDoGet(ToDoDB):
    pass


sqlite_file_name = "app/database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/todos", response_model=list[ToDoGet])
async def get_todos(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[ToDoGet]:
    """Return a paginated list of To‑Do items.

    Args:
        session: DB session injected by ``get_session``.
        offset: Number of rows to skip (default 0).
        limit: Max rows to return, capped at 100 (default 100).

    Returns:
        List of ``ToDoDB`` objects for the requested slice.
    """
    todos = session.exec(select(ToDoDB).offset(offset).limit(limit)).all()

    return [ToDoGet.model_validate(todo) for todo in todos]


@app.get("/todos/{id}", response_model=ToDoGet)
async def get_todo(id: int, session: Session = Depends(get_session)) -> ToDoGet:
    """Return a single To‑Do item for the given id.

    Args:
        session: DB session injected by ``get_session``.
        id: The id off the To-Do to fetch.

    Returns:
        List of ``ToDoDB`` objects for the requested slice.

    Raises:
        HTTPException: raises a ``404 Not Found``
        error if the id does not exist.
    """
    todo = session.get(ToDoDB, id)
    if not todo:
        raise HTTPException(status_code=404, detail="To do list was not found")
    return ToDoGet.model_validate(todo)


@app.patch("/todos/{id}", response_model=ToDoGet)
async def update_todo(
    id: int, updated: ToDoPatch, session: Session = Depends(get_session)
) -> ToDoGet:
    """Updates the To-Do for the given id.

    If the `done` field is changed to True then then completed_at field is set to
    the current date and time.
    If the `done` field is change to False then the completed_at date is cleared.

    Args:
        session: DB session injected by ``get_session``.
        id: The id off the To-Do to fetch.
        updated: The modified properties of the To-Do item.

    Returns:
        List of ``ToDoDB`` objects for the requested slice.

    Raises:
        HTTPException: raises a ``404 Not Found``
        error if the id does not exist.
    """
    stored_todo = session.get(ToDoDB, id)

    if not stored_todo:
        raise HTTPException(status_code=404, detail="To do list was not found")

    if updated.done is True and not stored_todo.done:
        stored_todo.completed_at = datetime.now(timezone.utc)
    elif updated.done is False and stored_todo.done:
        stored_todo.completed_at = None

    for field, value in updated.model_dump(exclude_unset=True).items():
        setattr(stored_todo, field, value)

    session.add(stored_todo)
    session.commit()
    session.refresh(stored_todo)

    return ToDoGet.model_validate(stored_todo)


@app.delete("/todos/{id}", status_code=204)
async def delete_todo(id: int, session: Session = Depends(get_session)) -> None:
    """Deletes the To‑Do item with the given id.

    Args:
        session: DB session injected by ``get_session``.
        id: The id off the To-Do to fetch.

    Returns:
        No Content

    Raises:
        HTTPException: raises a ``404 Not Found``
        error if the id does not exist.
    """
    todo = session.get(ToDoDB, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return None


@app.post("/todos", response_model=ToDoGet)
async def add_todo(todo: ToDoPost, session: Session = Depends(get_session)) -> ToDoGet:
    todo_db = ToDoDB(**todo.model_dump())
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return ToDoGet.model_validate(todo_db)


def main() -> None:
    print("Hello from todo-api!")


if __name__ == "__main__":
    main()
