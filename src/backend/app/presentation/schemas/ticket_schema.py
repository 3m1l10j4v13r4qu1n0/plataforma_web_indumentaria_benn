from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ItemTicketResponse(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int


class TicketDetalleResponse(BaseModel):
    numero_ticket: str
    fecha_hora: datetime
    vendedor_id: str
    estado: str
    items: List[ItemTicketResponse]

    model_config = ConfigDict(from_attributes=True)
