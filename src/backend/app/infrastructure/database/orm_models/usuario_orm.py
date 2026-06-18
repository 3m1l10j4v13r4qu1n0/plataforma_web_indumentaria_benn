# HU-05
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.infrastructure.database.session import Base


class UsuarioORM(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    rol: Mapped[str] = mapped_column(
        String(50), nullable=False, default="VENDEDOR"
    )  # 'VENDEDOR', 'GERENTE', 'CAJERO'
