from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    _BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATABASE_FILE: Path = _BASE_DIR / "data" / "database.db"
    DATABASE_URL: str = f"sqlite:///{DATABASE_FILE}"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
