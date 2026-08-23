from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class CambioORM(Base):
    __tablename__ = "cambios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    venta_original_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("ventas.id"), nullable=False
    )
    fecha_cambio: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    cajero_id: Mapped[str] = mapped_column(String(36), nullable=False)
    producto_a_cambiar_id: Mapped[str] = mapped_column(String(36), nullable=False)
    nuevo_producto_id: Mapped[str] = mapped_column(String(36), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fecha_compra_original: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
