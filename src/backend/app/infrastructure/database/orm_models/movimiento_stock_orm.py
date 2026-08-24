"""Modelo ORM de la tabla movimientos_stock (auditoría de cambios de stock)."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class MovimientoStockORM(Base):
    """Registro de auditoría de cada modificación de stock de un producto."""

    __tablename__ = "movimientos_stock"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    producto_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("productos.id"), nullable=False
    )
    tipo_movimiento: Mapped[str] = mapped_column(String(20), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    documento_referencia_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "tipo_movimiento IN ('VENTA', 'DEVOLUCION', 'AJUSTE')",
            name="check_tipo_movimiento_valido",
        ),
        CheckConstraint(
            "(tipo_movimiento = 'VENTA' AND cantidad < 0) "
            "OR (tipo_movimiento <> 'VENTA' AND cantidad > 0)",
            name="check_signo_cantidad_consistente",
        ),
        Index("ix_movimiento_stock_producto", "producto_id"),
        Index("ix_movimiento_stock_documento_ref", "documento_referencia_id"),
    )
