from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.domain.models.detalle_venta import DetalleVenta


@dataclass
class Venta:
    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: str = "PENDIENTE"  # 'PENDIENTE', 'CONFIRMADA', 'CANCELADA'
    items: List[DetalleVenta] = field(default_factory=list)

    def __post_init__(self):
        if self.estado not in ("PENDIENTE", "CONFIRMADA", "CANCELADA"):
            raise ValueError("Estado de venta inválido.")
        if not self.items:
            raise ValueError("Una venta debe tener al menos un item.")
