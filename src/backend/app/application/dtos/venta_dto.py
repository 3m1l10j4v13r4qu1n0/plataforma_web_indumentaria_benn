# Actualizacion de DTOs de la capa de Aplicacion HU-01 y HU-05

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ItemVentaDTO:
    producto_id: str
    cantidad: int


@dataclass
class CrearVentaCommand:
    vendedor_id: str
    items: List[ItemVentaDTO]
    # Nuevos campos para HU-05
    porcentaje_descuento: float = 0.0
    gerente_autorizacion_id: Optional[str] = None
