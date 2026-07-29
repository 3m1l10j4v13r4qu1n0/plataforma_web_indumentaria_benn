from datetime import datetime


from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base



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

    detalles: Mapped[list["DetalleVentaORM"]] = relationship(
        back_populates="venta", cascade="all, delete-orphan"
    )
