from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # Base de datos
    DATABASE_URL: str

    # Aplicación
    APP_NAME: str = "Plataforma Web Idumentaria BENN"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True  # Cambiar a False en producción

    
    class Config:
        env_file = ".env"           # ← lee del archivo .env
        env_file_encoding = "utf-8"


@lru_cache()             # ← crea la configuración una sola vez
def get_settings() -> Settings:
    return Settings()


settings = get_settings()