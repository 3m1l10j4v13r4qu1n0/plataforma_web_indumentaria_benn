from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List

from app.domain.models.venta import EstadoVenta


@dataclass
class ItemVentaDTO:
    producto_id: str
    cantidad: int


@dataclass
class CrearVentaCommand:
    vendedor_id: str
    items: List[ItemVentaDTO]


@dataclass
class ItemVentaResultado:
    """Ítem del resultado de una venta, con el nombre resuelto para presentación."""

    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: Decimal = Decimal("0")


@dataclass
class ResultadoVenta:
    """DTO de salida del caso de uso de venta, listo para la capa de presentación.

    Encapsula los datos de la venta confirmada junto con los nombres de los
    productos, de modo que el router no necesite acceder a repositorios.
    """

    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: EstadoVenta
    numero_ticket: str | None = None
    total: Decimal | None = None
    items: List[ItemVentaResultado] = field(default_factory=list)
