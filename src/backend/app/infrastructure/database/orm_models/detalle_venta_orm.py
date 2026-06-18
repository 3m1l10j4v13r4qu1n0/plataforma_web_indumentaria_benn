from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from app.infrastructure.database.session import Base
from app.infrastructure.database.orm_models.venta_orm import VentaORM

class DetalleVentaORM(Base):
    __tablename__ = "detalles_venta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venta_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("ventas.id"), nullable=False
    )
    producto_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("productos.id"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    venta: Mapped["VentaORM"] = relationship(back_populates="detalles")
