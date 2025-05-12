# fastapi_plus/config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Plus"
    version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
