from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Nota: En un proyecto real, settings.DATABASE_URL vendría de app.core.config
# Por ahora, usamos SQLite asíncrono para desarrollo/pruebas locales como indica la guía.
DATABASE_URL = "sqlite+aiosqlite:///./sgvir_test.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para debug de SQL
    future=True,
)

# expire_on_commit=False es crucial en Async SQLAlchemy para evitar errores de "detached instance"
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncSession:
    """
    Dependency que provee una sesión de BD por request.
    Garantiza que la sesión se cierre correctamente al finalizar la petición.
    """
    async with async_session_maker() as session:
        yield session
