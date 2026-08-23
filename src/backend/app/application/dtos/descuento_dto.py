from dataclasses import dataclass
from decimal import Decimal


@dataclass
class AplicarDescuentoCommand:
    """Comando para aplicar un descuento a una venta."""

    venta_id: str
    porcentaje: Decimal
    motivo: str
    autorizado_por: str | None = None
