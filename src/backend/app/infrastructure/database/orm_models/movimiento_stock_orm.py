from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base

class MovimientoStockORM(Base):  # O heredar de Base según tu estructura
    """
    Registra cada vez que el stock cambia (venta, devolución, cambio, ajuste)
    para garantizar la trazabilidad y auditoría del inventario (HU-08).
    """

    __tablename__ = "movimientos_stock"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    producto_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("productos.id"), nullable=False, index=True
    )

    # Positivo para ingreso (DEVOLUCION, AJUSTE+), negativo para egreso (VENTA, CAMBIO, AJUSTE-)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    tipo_movimiento: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 'VENTA', 'DEVOLUCION', 'CAMBIO', 'AJUSTE'

    referencia_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True, index=True
    )  # ID de la Venta, Cambio o nota de ajuste asociada

    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    usuario_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True, index=True
    )  # Quién realizó el movimiento (Trazabilidad de auditoría)

    producto: Mapped["ProductoORM"] = relationship("ProductoORM")  # type: ignore
