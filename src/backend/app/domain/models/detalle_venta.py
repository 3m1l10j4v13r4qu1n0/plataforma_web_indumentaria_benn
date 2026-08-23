from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import DomainException


@dataclass
class DetalleVenta:
    """Ítem de una venta, con el precio unitario congelado al momento de venderse."""

    producto_id: str
    cantidad: int
    precio_unitario: Decimal = Decimal("0")

    def __post_init__(self):
        if self.cantidad <= 0:
            raise DomainException("La cantidad a vender debe ser mayor a cero.")

        if self.precio_unitario < 0:
            raise DomainException("El precio unitario no puede ser negativo.")

    def subtotal(self) -> Decimal:
        """Calcula el subtotal del ítem (cantidad x precio unitario).

        Returns:
            El subtotal como Decimal.
        """
        return Decimal(self.cantidad) * self.precio_unitario
