from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum

from app.domain.models.detalle_venta import DetalleVenta

from app.domain.exceptions import DomainException


class EstadoVenta(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


@dataclass
class Venta:
    """Agregado raíz de una venta con su comprobante asociado."""

    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: EstadoVenta
    numero_ticket: str | None = None
    total: Decimal | None = None
    items: list[DetalleVenta] = field(default_factory=list)

    def __post_init__(self):

        if not self.items:
            raise DomainException("Una venta debe tener al menos un item.")

        if self.total is not None and self.total < 0:
            raise DomainException("El total de la venta no puede ser negativo.")

    def calcular_total(self) -> Decimal:
        """Calcula el total de la venta sumando los subtotales de sus ítems.

        Returns:
            El total como Decimal.
        """
        return sum((item.subtotal() for item in self.items), Decimal("0"))
