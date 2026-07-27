from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base


class ProductoORM(Base):
    __tablename__ = "productos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    codigo: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    precio: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id"),
        nullable=False,
    )
    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVO",
    )

    categoria: Mapped["CategoriaORM"] = relationship() # type: ignore

    __table_args__ = (
        CheckConstraint("stock_actual >= 0", name="check_stock_no_negativo"),
        CheckConstraint(
            "estado IN ('ACTIVO', 'INACTIVO')", name="check_estado_valido"
        ),
        Index("ix_producto_codigo", "codigo"),
    )