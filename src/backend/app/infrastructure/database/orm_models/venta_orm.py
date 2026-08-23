from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base

if TYPE_CHECKING:
    from app.infrastructure.database.orm_models.detalle_venta_orm import DetalleVentaORM


class VentaORM(Base):
    __tablename__ = "ventas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    vendedor_id: Mapped[str] = mapped_column(String(36), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDIENTE")
    numero_ticket: Mapped[str | None] = mapped_column(
        String(30), unique=True, nullable=True
    )
    total: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    detalles: Mapped[list["DetalleVentaORM"]] = relationship(
        back_populates="venta", cascade="all, delete-orphan"
    )
