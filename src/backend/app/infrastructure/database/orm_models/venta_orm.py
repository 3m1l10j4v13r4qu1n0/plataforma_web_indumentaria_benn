from datetime import datetime


from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base



class VentaORM(Base):
    __tablename__ = "ventas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    vendedor_id: Mapped[str] = mapped_column(String(36), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDIENTE")

    detalles: Mapped[list["DetalleVentaORM"]] = relationship(
        back_populates="venta", cascade="all, delete-orphan"
    )
