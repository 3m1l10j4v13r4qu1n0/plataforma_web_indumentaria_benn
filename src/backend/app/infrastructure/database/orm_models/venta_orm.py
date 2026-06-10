# Implementacion de Adaptadores Concretos HU-05

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class VentaORM(Base):
    __tablename__ = "ventas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    vendedor_id: Mapped[str] = mapped_column(String(36), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDIENTE")

    # Nuevos campos para HU-05 (Control de Descuentos)
    porcentaje_descuento: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    gerente_autorizacion_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True
    )

    detalles: Mapped[List["DetalleVentaORM"]] = relationship(
        back_populates="venta", cascade="all, delete-orphan"
    )
