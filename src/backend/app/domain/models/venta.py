# HU-01 implementacion de ventas y HU-05 implementacion de descuento

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta


@dataclass
class Venta:
    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: str = "PENDIENTE"  # 'PENDIENTE', 'CONFIRMADA', 'CANCELADA'
    items: List[DetalleVenta] = field(default_factory=list)
    descuento: Descuento = field(default_factory=Descuento)

    def __post_init__(self):
        # SRP: Venta solo se preocupa por sus invariantes como Agregado Raíz
        if self.estado not in ("PENDIENTE", "CONFIRMADA", "CANCELADA"):
            raise ValueError("Estado de venta inválido.")
        if not self.items:
            raise ValueError("Una venta debe tener al menos un item.")
        if self.fecha_hora is None:
            raise ValueError("La fecha y hora de la venta son obligatorias.")

    # Comportamientos del Agregado (Encapsulamiento)
    def confirmar(self) -> None:
        if self.estado != "PENDIENTE":
            raise ValueError("Solo se pueden confirmar ventas en estado PENDIENTE.")
        self.estado = "CONFIRMADA"

    def cancelar(self) -> None:
        if self.estado not in ("PENDIENTE", "CONFIRMADA"):
            raise ValueError("Solo se pueden cancelar ventas PENDIENTES o CONFIRMADAS.")
        self.estado = "CANCELADA"
