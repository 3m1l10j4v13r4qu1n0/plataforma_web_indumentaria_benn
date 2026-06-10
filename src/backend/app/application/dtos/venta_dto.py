from dataclasses import dataclass
from typing import List


@dataclass
class ItemVentaDTO:
    producto_id: str
    cantidad: int


@dataclass
class CrearVentaCommand:
    vendedor_id: str
    items: List[ItemVentaDTO]
