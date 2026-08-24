from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class CambioORM(Base):
    __tablename__ = "cambios"
    __table_args__ = (
        CheckConstraint(
            "estado_producto IN ('NUEVO_ETIQUETADO', 'USADO', 'DANADO')",
            name="ck_cambios_estado_producto",
        ),
    )

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
    estado: Mapped[str] = mapped_column(String(30), nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fecha_compra_original: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    estado_producto: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tiene_etiqueta: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    observaciones: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fecha_validacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
