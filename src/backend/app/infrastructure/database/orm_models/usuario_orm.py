# HU-05
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Asumimos que Base ya está definida o importada desde un base.py compartido
# from app.infrastructure.database.orm_models.base import Base


class UsuarioORM(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    rol: Mapped[str] = mapped_column(
        String(50), nullable=False, default="VENDEDOR"
    )  # 'VENDEDOR', 'GERENTE', 'CAJERO'
