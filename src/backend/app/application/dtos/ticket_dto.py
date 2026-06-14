from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ItemTicketDTO:
    producto_id: str
    nombre: str
    cantidad: int


@dataclass
class TicketDetalleDTO:
    numero_ticket: str
    fecha_hora: datetime
    vendedor_id: str
    estado: str
    items: List[ItemTicketDTO]
