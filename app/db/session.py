from typing import Generator
from sqlmodel import Session
from .engine import engine

def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a fresh SQLModel Session.
    The session has the .exec() method we rely on.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()