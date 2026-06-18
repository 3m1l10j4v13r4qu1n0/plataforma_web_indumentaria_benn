# app/infrastructure/database/orm_models/producto_orm.py
from typing import Optional

from sqlalchemy import CheckConstraint, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.infrastructure.database.session import Base


class ProductoORM(Base):
    __tablename__ = "productos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    codigo: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVO")

    __table_args__ = (
        CheckConstraint("stock_actual >= 0", name="check_stock_no_negativo"),
        Index("ix_producto_codigo", "codigo"),
    )
