from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, from sqlalchemy import String, DateTime, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class VentaORM(Base):
    """
    Agregamos la columna numero_ticket a la tabla
    de ventas. Dado que este campo se utilizará
    para buscar la venta original durante un cambio
    (HU-02 y HU-04), es crucial que sea único y esté
    indexado para un rendimiento óptimo.

    """

    __tablename__ = "ventas"

    id: Mapped[str] = mapped_column(
            String(36), 
            primary_key=True
    )
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    vendedor_id: Mapped[str] = mapped_column(
            String(36), 
            nullable=False
    )

    # Nuevo campo para HU-02, HU-04 y HU-07
    numero_ticket: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False, 
        index=True
    )

    estado: Mapped[str] = mapped_column(
            String(20), 
            nullable=False, 
            default="PENDIENTE"
    )

    # Campos para HU-05 (Descuentos)
    porcentaje_descuento: Mapped[float] = mapped_column(
        Float, 
        nullable=False, 
        default=0.0
    )
    gerente_autorizacion_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        nullable=True
    )

    # -------------------------------------------------------------------
    # CAMBIOS PARA HU-02, HU-03 y HU-04:
    # -------------------------------------------------------------------

    # 1. Número de ticket único e indexado para búsquedas rápidas
    numero_ticket: Mapped[str] = mapped_column(
        String(50),
        unique=True,  # <--- NUEVO: Garantiza unicidad
        nullable=False,
        index=True,  # <--- NUEVO: Acelera la búsqueda por ticket
    )

    # 2. Relación con los detalles de la venta (ya existía, se mantiene)
    detalles: Mapped[List["DetalleVentaORM"]] = relationship(
        back_populates="venta", 
        cascade="all, delete-orphan"
    )

    # 3. Relación con los cambios asociados a esta venta
    cambios: Mapped[List["CambioORM"]] = relationship(
        back_populates="venta", 
        cascade="all, delete-orphan"
    )  # <--- NUEVO: Permite hacer venta_orm.cambios para ver el historial

    # 4. Definición del índice para el ticket (buena práctica en SQLAlchemy)
    __table_args__ = (
        Index("ix_venta_numero_ticket", "numero_ticket", unique=True),  # <--- NUEVO
    )
