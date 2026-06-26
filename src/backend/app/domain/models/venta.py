from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
 
from app.domain.models.detalle_venta import DetalleVenta

from app.domain.exceptions import DomainException

class EstadoVenta(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

@dataclass
class Venta:
    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: EstadoVenta
    items: list[DetalleVenta] = field(
        default_factory=list
        )

    def __post_init__(self):
        
        if not self.items:
            raise DomainException(
                "Una venta debe tener al menos un item."
                )
