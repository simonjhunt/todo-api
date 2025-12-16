from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///:memory"
    DEBUG: bool = False

settings = Settings()
