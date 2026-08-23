from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class DescuentoORM(Base):
    __tablename__ = "descuentos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    venta_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("ventas.id"), unique=True, nullable=False
    )
    porcentaje: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    monto_descuento: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    motivo: Mapped[str] = mapped_column(String(255), nullable=False)
    autorizado_por: Mapped[str | None] = mapped_column(String(36), nullable=True)
    fecha_aplicacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
