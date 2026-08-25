from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # Base de datos
    DATABASE_URL: str

    # Aplicación
    APP_NAME: str = "Plataforma Web Idumentaria BENN"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True  # Cambiar a False en producción

    # JWT / Autenticación
    JWT_SECRET_KEY: str = "CHANGE_ME_TO_A_RANDOM_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"  # ← lee del archivo .env
        env_file_encoding = "utf-8"


@lru_cache()  # ← crea la configuración una sola vez
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
