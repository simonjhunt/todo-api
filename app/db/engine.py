from sqlmodel import create_engine, SQLModel
from app.core.config import settings

def get_engine():
    """
    Build a SQLModel engine based on the *current* SETTINGS.
    This function can be called any number of times – it always reads the
    latest value of `settings.DATABASE_URL`.
    """
    return create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
    )

# Export the metadata for table creation (unchanged)
metadata = SQLModel.metadata