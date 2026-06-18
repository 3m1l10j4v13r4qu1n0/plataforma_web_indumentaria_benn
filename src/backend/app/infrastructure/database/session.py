from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.infrastructure.core.config import settings  # ← reemplaza os.getenv


# Motor de conexión a PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,  # ← viene de config.py
    echo=settings.DEBUG,    # ← True en desarrollo, False en producción
    future=True
)

# Fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para los modelos ORM
class Base(DeclarativeBase):
    pass

# Dependencia para los endpoints
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
     Dependency que provee una sesión de BD por request.
     Garantiza que la sesión se cierre correctamente al finalizar la petición.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise