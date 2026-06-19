from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

from app.infrastructure.core.config import settings
from app.infrastructure.database.session import Base  # ajustá el import a tu estructura real

# Importá todos tus modelos acá para que autogenerate los detecte
# from app.infrastructure.database.models import ModeloA, ModeloB  # ← descomentá y ajustá

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Convertimos la URL async (asyncpg) a sync (psycopg2) para que Alembic pueda usarla
def get_sync_url() -> str:
    url = settings.DATABASE_URL
    # postgresql+asyncpg://... → postgresql+psycopg2://...
    return url.replace("postgresql+asyncpg", "postgresql+psycopg2").replace(
        "postgresql+asyncpg", "postgresql"
    )


def run_migrations_offline() -> None:
    """Modo offline: genera el SQL sin conectarse a la DB."""
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Modo online: se conecta a la DB y aplica las migraciones."""
    connectable = create_engine(
        get_sync_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()