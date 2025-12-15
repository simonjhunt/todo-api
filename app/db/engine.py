from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Sync engine – perfect for a simple SQLite‑based API
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite
    echo=settings.DEBUG,
)

# Session factory that FastAPI will use
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)