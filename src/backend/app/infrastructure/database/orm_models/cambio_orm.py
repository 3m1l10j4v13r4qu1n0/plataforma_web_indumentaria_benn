from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from app.infrastructure.database.session import Base


class CambioORM(Base):
    __tablename__ = "cambios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    venta_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventas.id"), nullable=False)
    producto_id: Mapped[str] = mapped_column(String(36), ForeignKey("productos.id"), nullable=False)
    
    fecha_solicitud: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Estados posibles del cambio
    estado: Mapped[str] = mapped_column(
        String(20), 
        nullable=False, 
        default="PENDIENTE" # 'PENDIENTE', 'APROBADO', 'RECHAZADO'
    )
    
    motivo_rechazo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relaciones
    venta: Mapped["VentaORM"] = relationship("VentaORM",back_populates="cambios")
    
    producto: Mapped["ProductoORM"] = relationship("ProductoORM")