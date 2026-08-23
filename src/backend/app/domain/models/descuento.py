from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.domain.exceptions import DomainException


class TipoDescuento(str):
    """Tipo de descuento aplicado."""
    PORCENTAJE = "PORCENTAJE"
    MONTO_FIJO = "MONTO_FIJO"


@dataclass
class Descuento:
    """Entidad de dominio que representa un descuento aplicado a una venta."""

    id: str
    venta_id: str
    porcentaje: Decimal
    monto_descuento: Decimal
    motivo: str
    autorizado_por: str | None = None
    fecha_aplicacion: datetime | None = None

    def __post_init__(self):
        if self.porcentaje <= 0 or self.porcentaje > 100:
            raise DomainException(
                f"El porcentaje de descuento {self.porcentaje}% no es válido. "
                "Debe estar entre 0 y 100."
            )

        if self.monto_descuento < 0:
            raise DomainException("El monto de descuento no puede ser negativo.")

    def requiere_autorizacion(self, limite_porcentaje: Decimal = Decimal("20")) -> bool:
        """Verifica si el descuento requiere autorización de gerente.

        Args:
            limite_porcentaje: Porcentaje máximo sin autorización (default 20%).

        Returns:
            True si el descuento supera el límite, False caso contrario.
        """
        return self.porcentaje > limite_porcentaje

    def esta_autorizado(self) -> bool:
        """Verifica si el descuento ya fue autorizado por un gerente.

        Returns:
            True si tiene autorización registrada, False caso contrario.
        """
        return self.autorizado_por is not None
