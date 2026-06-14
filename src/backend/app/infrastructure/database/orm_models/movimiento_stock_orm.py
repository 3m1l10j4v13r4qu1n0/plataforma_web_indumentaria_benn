from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class MovimientoStockORM(Base):
    """
    Prepara la trazabilidad del inventario (HU-08), registrando cada vez que
    el stock cambia (venta, devolución, cambio, ajuste).

    """

    __tablename__ = "movimientos_stock"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    producto_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("productos.id"), nullable=False
    )

    cantidad: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # Positivo para ingreso, negativo para egreso

    tipo_movimiento: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 'VENTA', 'DEVOLUCION', 'CAMBIO', 'AJUSTE'

    referencia_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True
    )  # ID de la Venta o Cambio asociado
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    usuario_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True
    )  # Quién realizó el movimiento

    producto: Mapped["ProductoORM"] = relationship()
