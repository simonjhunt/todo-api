from typing import Generator

from sqlmodel import Session  # sync Session (will work with the sync engine)

from .engine import get_engine, metadata


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a Session bound to the engine
    returned by `get_engine()`. Because `get_engine()` reads the *current*
    settings, the session automatically points at the correct DB
    (production or the temporary test DB).
    """
    engine = get_engine()
    metadata.create_all(engine)
    with Session(engine) as sess:
        yield sess
