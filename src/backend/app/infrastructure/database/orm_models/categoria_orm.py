from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class CategoriaORM(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )